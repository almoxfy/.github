# Contributing Guide

First of all, thank you for your interest in contributing to a **almoxfy** project.

This document describes how to set up your development environment, run tests, and submit improvements. Common workflows are exposed through the project `Makefile`, so you can rely on the same targets from repo to repo; the Makefile (or the repository README) is the source of truth for what each target runs.

---

## Initial Setup

### 1. Fork and Clone

1. **Fork** this repository to your own GitHub account.
2. Clone your fork locally:

   ```bash
   git clone https://github.com/YOUR_USERNAME/<PROJECT_NAME>.git
   cd <PROJECT_NAME>
   ```

3. **Stay up to date with upstream** (replace `almoxfy` and `<PROJECT_NAME>` with the canonical owner and repo name):

   ```bash
   git remote add upstream https://github.com/almoxfy/<PROJECT_NAME>.git
   git fetch upstream
   git merge upstream/main
   ```

   Use `upstream/<default-branch>` if the default branch is not `main`.

### 2. Development Environment

- **Install everything (environment + dependencies):**

  ```bash
  make install
  ```

- **Configure Git hooks (linter / commits):**  
  This helps keep changes aligned with our standards before every commit.

  ```bash
  make pre-commit-install
  ```

  Many repositories delegate installation to [uv](https://github.com/astral-sh/uv) or similar; if anything fails, inspect the `Makefile` or README for that project.

---

## Development Cycle

To maintain code quality, use the `Makefile` targets. Run `make` with no arguments to list available commands.

### Code Quality

- **Format and auto-fix issues:** `make format`
- **Validate linting rules:** `make lint`

### Testing and Coverage

- **Run tests locally:** `make test`
- **Run tests via Docker:** `make docker-test`
- **Validate minimum coverage (same check as CI):**

  ```bash
  make test-coverage-ci
  ```

**Coverage threshold:** CI fails when coverage is below the value set in this repository’s `Makefile` (often **90%** by default). PRs are expected to meet that threshold unless maintainers agree otherwise.

---

## Submission Process

1. **Discuss large changes first:** For substantial features or refactors, open an issue on **this repository** before investing heavy work, so direction and scope can align early.
2. **Create a branch:** Use semantic prefixes (e.g. `feat/`, `fix/`, `docs/`).

   ```bash
   git checkout -b feat/your-feature-name
   ```

3. **Develop:** Implement your changes and add or update tests where relevant. Documentation-only contributions should still follow formatting and lint rules when the project defines them.
4. **Validate:** Run `make format` and `make test` (and other targets your change needs) before opening a PR.
5. **Commits:** Follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g. `feat: add open-search validation`).
6. **Pull request:** Open a PR against the default branch (usually `main`). Describe the change clearly and link related issues. Use our [pull request template](https://github.com/almoxfy/.github/blob/main/.github/pull_request_template.md).

**Merge requirements:** PRs are not merged while tests fail or coverage is below the threshold described under [Testing and Coverage](#testing-and-coverage).

**Good first contributions:** When available, look for issues labeled `good first issue` or `help wanted`.

---

## Community Standards

By participating in this project, you agree to abide by our [Code of Conduct](https://github.com/almoxfy/.github/blob/main/CODE_OF_CONDUCT.md).

---

## Contact

If you need help or have questions:

1. **Technical issues and questions:** Use the **Issues** tab on **this repository**. If GitHub offers templates, pick the one that fits (bug report, feature request, etc.).
2. **Sensitive matters:** Report Code of Conduct concerns using the contact details in the [Code of Conduct](https://github.com/almoxfy/.github/blob/main/CODE_OF_CONDUCT.md).
3. **Security vulnerabilities:** Do not disclose them in public issues. Use the security reporting process described in this repository’s `SECURITY.md` if it exists; otherwise use the private contact channel indicated in the Code of Conduct.
