## Descrição

Resuma o que foi alterado e o motivo de forma clara e concisa.

**Issue:** Resolve # (número da issue, ou escreva **N/A** — ex: `Resolve #123`)

## Tipo de mudança

- [ ] Correção de falha (Bug fix)
- [ ] Nova funcionalidade (New feature)
- [ ] Mudança estrutural (Breaking change - altera integrações, APIs ou contratos)
- [ ] Atualização de documentação
- [ ] Manutenção (CI, refatoração, tooling, infraestrutura)

## Mudanças Estruturais e Foco da Revisão

- **Breaking changes:** Descreva qualquer mudança que afete a compatibilidade para integrações ou para os demais repositórios do ecossistema Almoxfy. Caso não haja, escreva **Nenhum**.
- **Onde focar:** Indique arquivos, APIs, manifestos ou comportamentos específicos que exigem atenção detalhada dos revisores. Caso não haja, escreva **N/A**.
- **Impacto no fluxo:** Esta alteração interfere na usabilidade, no fluxo de governança ou na capacidade de auditoria do sistema? (Justifique brevemente em caso afirmativo).

## Checklist do Desenvolvedor

**Qualidade de Código e Testes**
- [ ] Realizei uma autorrevisão minuciosa do meu código.
- [ ] O código submetido segue os padrões e guias de estilo estabelecidos pelo projeto (`make lint`).
- [ ] Escrevi testes automatizados para as alterações realizadas (ou apresentei justificativa técnica na descrição caso não sejam aplicáveis).
- [ ] Executei a suíte de testes e todas as validações passaram localmente (`make test`; utilize `make test-coverage-ci` quando aplicável para paridade com CI).
- [ ] A métrica de cobertura de testes atende ao limite mínimo definido no `Makefile` deste repositório (`MIN_COVERAGE`).

**Impacto no Ecossistema (Cross-Repository)**
- [ ] A alteração proposta exige atualizações técnicas ou conceituais na documentação? (Em caso positivo, referencie o respectivo PR no repositório `almoxfy-docs`).
- [ ] Houve modificação de infraestrutura ou variáveis de ambiente que exija atualização dos manifestos no repositório `almoxfy-k8s`?
- [ ] Houve modificação de contrato na API (`almoxfy-back`) que demande alinhamento imediato com o repositório de interface (`almoxfy-front`)?
