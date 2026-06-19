---
title: "Skill Testing Conventions"
type: canonical
tags:
  - stack-tooling
  - evals
  - harness
  - testes
aliases:
  - skill-test-harness
  - test-framework
  - como-testar-skills
last_updated: 2026-06-18
relates-to:
  - "[[curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs|Evaluation Rubrics]]"
sources:
  - "Skill Test Harness Framework (.omo/plans/2026-06-18-skill-test-harness-framework.md)"
  - "Expansion Plan (.omo/plans/2026-06-18-skill-test-harness-expansion.md)"
---

# Skill Testing Conventions

## Visao Geral

Todo skill em `~/.config/opencode/skills/` deve ter um diretorio `harness/`
com testes automatizados. O framework cobre 3 niveis de complexidade:

| Tier | Skills | Cobertura |
|------|--------|-----------|
| **Tier 1** — Pipeline/Workflow | review-work, debugging, system-design, quality-improvement-loop, issue-executor-master | Contrato SKILL.md + schemas customizados + testes de algoritmo |
| **Tier 2** — Structured Process | architecture, incident-response, skillify, doc-coauthoring, writing-plans | Contrato SKILL.md + schemas minimos |
| **Tier 3** — Instructional | start, update, task-management, memory-management, etc. | Contrato SKILL.md (bootstrap) |

## Estrutura de Diretorios

```
~/.config/opencode/
├── templates/skill-harness/          ← Template reutilizavel
│   ├── setup-harness.sh              ← Bootstrap script
│   ├── schemas.py.template
│   └── test-results.json.template
├── tests/skills/
│   ├── run_harness.py                ← Runner centralizado (symlink)
│   ├── shared_contract_helpers.py    ← YAML parser + SkillContract canonico
│   ├── run_all_skill_tests.sh        ← Executa todos os harnesses
│   └── test_core_triad_integration.py
└── skills/<nome>/
    └── harness/
        ├── run_tests.py → symlink    ← Aponta para run_harness.py
        ├── schemas.py                ← Schemas especificos da skill
        ├── test-results.json         ← Contrato de fases
        └── tests/
            ├── test_contract.py      ← 6 testes de estrutura SKILL.md
            └── test_<algoritmo>.py   ← Testes especificos (Tier 1/2)
```

## Como Adicionar Testes a um Novo Skill

### Passo 1: Bootstrap

```bash
SKILL_DIR=~/.config/opencode/skills/<nome> \
  bash ~/.config/opencode/templates/skill-harness/setup-harness.sh <nome>
```

Isso cria `harness/` com symlink para o runner centralizado, `schemas.py`
do template, `test-results.json`, e `tests/test_contract.py` com 6 testes
de contrato.

### Passo 2: Customizar schemas.py (se necessario)

Para skills Tier 1 ou Tier 2, edite `harness/schemas.py` e adicione
dataclasses com metodo `validate()`. Use `ValueError` para validacao:

```python
from dataclasses import dataclass

@dataclass
class MeuSchema:
    campo: str

    def validate(self) -> None:
        if not self.campo:
            raise ValueError("campo e obrigatorio")
```

**NUNCA use `assert` em validadores de dataclass** — `assert` e removido
pelo Python com flag `-O`. Use `raise ValueError(...)`.

### Passo 3: Adicionar testes de algoritmo

Crie `harness/tests/test_<nome>.py` com funcoes `test_*`. O runner
descobre automaticamente.

### Passo 4: Executar

```bash
# Teste individual
python ~/.config/opencode/skills/<nome>/harness/run_tests.py

# Suite completa
bash ~/.config/opencode/tests/skills/run_all_skill_tests.sh
```

## Contrato de Testes (test_contract.py)

Todo skill deve passar 6 testes de contrato:

| Teste | O que verifica |
|-------|---------------|
| `test_skill_md_exists` | SKILL.md existe e tem > 100 caracteres |
| `test_frontmatter_has_required_fields` | Frontmatter tem `name` e `description` com tamanho minimo |
| `test_has_triggers_or_invocation` | Tem secao de triggers ou `## Invocation` |
| `test_has_when_to_use` | Tem secao "Quando usar" |
| `test_has_when_not_to_use` | Tem secao "Quando NAO usar" |
| `test_no_tbd_placeholders` | Zero placeholders `[TBD]`/`[TODO]` |

## Schemas Compartilhados

### SkillContract (canonico)

Definicao unica em `shared_contract_helpers.py`. NAO duplique esta classe
em `schemas.py` individuais. Use `from shared_contract_helpers import SkillContract`
apenas se o schema da skill precisar referenciar SkillContract.

### YAML Parser

`extract_frontmatter()` em `shared_contract_helpers.py` suporta:
- Block scalars (`>`, `|`) para valores multi-linha
- Formato simples `key: value`
- Aspas simples e duplas

NAO duplique parsers YAML inline em `test_contract.py`.

## Runner

O runner `run_harness.py` e centralizado. Cada `harness/run_tests.py` e um
**symlink** para ele. NAO copie o runner.

Caracteristicas:
- Stdlib-only (zero dependencias externas)
- Descobre `test_*.py` automaticamente
- Reporta pass/fail/error counts
- Exit 0 se todos passam, exit 1 se falha

## Convencoes

### Nomenclatura

- Funcoes de teste: `test_<comportamento_esperado>` (snake_case)
- Arquivos de teste: `test_<modulo>.py`
- Schemas: dataclasses com metodo `validate()`

### Validacao

- **Dataclass validators**: `raise ValueError(...)` — seguro contra `-O`
- **Test helpers**: `raise AssertionError(...)` — esperado pelo runner
- **NUNCA**: bare `assert` em validadores expostos

### Idempotencia

`setup-harness.sh` e idempotente. Re-executar preserva `schemas.py`,
`test-results.json`, e `test_contract.py` existentes. Apenas recria
o symlink do runner.

## Execucao

```bash
# Suite completa (todos os 25 skills + integracao)
bash ~/.config/opencode/tests/skills/run_all_skill_tests.sh

# Skill individual
python ~/.config/opencode/skills/<nome>/harness/run_tests.py
```

Resultado esperado: 26/26 suites, 237 testes, exit 0.

## Historico

- **2026-06-18**: Fase 1 (5 skills) + Expansao (20 skills) concluidas.
  GAP 5 resolvido. 25 skills com cobertura de testes automatizados.
- **2026-06-18**: Correcoes pos-review: SeverityGate bug fix,
  SkillContract deduplication, YAML parser unification,
  assert → raise explicito.
