#!/usr/bin/env python3
"""Sync GitHub labels from a YAML manifest to one or more repositories.

Fails loudly on missing token, HTTP errors, or empty results — unlike
micnncim/action-label-syncer, which can exit 0 while doing nothing.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

try:
    import yaml
except ImportError:
    import subprocess

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "PyYAML"],
        stdout=subprocess.DEVNULL,
    )
    import yaml


API = "https://api.github.com"
API_VERSION = "2022-11-28"


def die(msg: str, code: int = 1) -> None:
    print(f"::error::{msg}", file=sys.stderr)
    raise SystemExit(code)


def api(
    token: str,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
) -> Any:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "almoxfy-label-sync",
            **({"Content-Type": "application/json"} if body is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        die(f"{method} {path} → HTTP {exc.code}: {detail}")


def list_labels(token: str, owner: str, repo: str) -> list[dict[str, Any]]:
    labels: list[dict[str, Any]] = []
    page = 1
    while True:
        path = (
            f"/repos/{owner}/{repo}/labels"
            f"?per_page=100&page={page}"
        )
        batch = api(token, "GET", path)
        if not isinstance(batch, list):
            die(f"Unexpected labels response for {owner}/{repo}")
        labels.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return labels


def sync_repo(
    token: str,
    full_name: str,
    desired: list[dict[str, Any]],
    prune: bool,
) -> None:
    if "/" not in full_name:
        die(f"Invalid repository name: {full_name!r}")
    owner, repo = full_name.split("/", 1)
    print(f"==> Syncing {full_name}")

    # Probe access early with a clear error.
    api(token, "GET", f"/repos/{owner}/{repo}")

    existing = {lab["name"]: lab for lab in list_labels(token, owner, repo)}
    desired_by_name = {lab["name"]: lab for lab in desired}

    for name, lab in desired_by_name.items():
        color = str(lab["color"]).lstrip("#")
        description = lab.get("description") or ""
        payload = {"new_name": name, "color": color, "description": description}
        if name in existing:
            cur = existing[name]
            if (
                cur.get("color", "").lower() == color.lower()
                and (cur.get("description") or "") == description
            ):
                print(f"  keep   {name}")
                continue
            print(f"  update {name}")
            encoded = urllib.parse.quote(name)
            api(token, "PATCH", f"/repos/{owner}/{repo}/labels/{encoded}", payload)
        else:
            print(f"  create {name}")
            api(
                token,
                "POST",
                f"/repos/{owner}/{repo}/labels",
                {"name": name, "color": color, "description": description},
            )

    if prune:
        for name in sorted(existing.keys() - desired_by_name.keys()):
            print(f"  delete {name}")
            encoded = urllib.parse.quote(name)
            api(token, "DELETE", f"/repos/{owner}/{repo}/labels/{encoded}")

    print(f"  done   {full_name} ({len(desired_by_name)} labels)")


def main() -> None:
    token = os.environ.get("LABEL_SYNC_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not token.strip():
        die(
            "LABEL_SYNC_TOKEN está vazio ou não existe. "
            "Crie um PAT (classic: scope `repo`, ou fine-grained com Issues: Read and write "
            "nos repositórios privados) e configure o secret LABEL_SYNC_TOKEN."
        )

    manifest = os.environ.get("LABEL_MANIFEST", ".github/config/labels.yaml")
    repos_raw = os.environ.get("LABEL_REPOS", "")
    prune = os.environ.get("LABEL_PRUNE", "true").lower() in {"1", "true", "yes"}

    repos = [r.strip() for r in repos_raw.splitlines() if r.strip()]
    if not repos:
        die("LABEL_REPOS está vazio — informe ao menos um owner/repo.")

    with open(manifest, encoding="utf-8") as fh:
        desired = yaml.safe_load(fh)
    if not isinstance(desired, list) or not desired:
        die(f"Manifesto inválido ou vazio: {manifest}")

    for full_name in repos:
        sync_repo(token, full_name, desired, prune)

    print("All repositories synced.")


if __name__ == "__main__":
    main()
