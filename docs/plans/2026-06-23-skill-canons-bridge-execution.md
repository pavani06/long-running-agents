# Skill-Canons Bridge — Plano de Execução

**Goal:** Conectar a skill `system-design` aos 14 padrões canônicos do vault `long-running-agents`, com injeção inline por fase, harness de alinhamento e compliance gate pós-design.

**Architecture:** Duas ondas. Onda 1 estabelece a bridge de grounding — cada fase do `system-design` carrega 2-3 canons específicos antes de executar. Onda 2 adiciona compliance gate pós-design + detecção de staleness. A bridge usa `canonical-context` como runtime de injeção e `obsidian-eval` para resolução de vaults.

**Tech Stack:** Python 3.9+ (harness), Bash (obsidian-eval CLI), Markdown (SKILL.md)

**Source plan:** `.omo/plans/2026-06-23-skill-canons-bridge.md` (REV 3.2, aprovado)

---

## File Map

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `~/.config/opencode/skills/system-design/SKILL.md` | Modify | +Canonical References table, +micro-passes, +compliance gate, +fallback |
| `~/.config/opencode/skills/system-design/harness/schemas.py` | Modify | +CANONICAL_REFS constante |
| `~/.config/opencode/skills/system-design/harness/tests/test_canonical_alignment.py` | Create | Testa que SKILL.md referencia canons e que resolvem |
| `~/.config/opencode/skills/system-design/harness/tests/test_staleness.py` | Create | Testa staleness dos canons referenciados (snapshot diff, 90d) |
| `/mnt/c/Users/pavan/long-running-agents/docs/canonical/sed7k5DT1` | Delete | Artefato de temp file (duplicata de stable-harness-prompt.md) |
| `/mnt/c/Users/pavan/long-running-agents/docs/canonical/sedTtma3E` | Delete | Artefato de temp file (duplicata de shared-design-concept-handoff.md) |

---

## Onda 1: Bridge de Grounding

### Tarefa 0: Cleanup de artefatos

**Files:** Delete 2 files

- [ ] **Step 1: Remover sed7k5DT1**
```bash
rm /mnt/c/Users/pavan/long-running-agents/docs/canonical/sed7k5DT1
```

- [ ] **Step 2: Remover sedTtma3E**
```bash
rm /mnt/c/Users/pavan/long-running-agents/docs/canonical/sedTtma3E
```

- [ ] **Step 3: Verificar que foram removidos**
```bash
test -f /mnt/c/Users/pavan/long-running-agents/docs/canonical/sed7k5DT1 && echo "STILL EXISTS" || echo "REMOVED"
test -f /mnt/c/Users/pavan/long-running-agents/docs/canonical/sedTtma3E && echo "STILL EXISTS" || echo "REMOVED"
```
Expected: `REMOVED` / `REMOVED`

---

### Tarefa 1: Adicionar CANONICAL_REFS ao schemas.py

**Files:** Modify `~/.config/opencode/skills/system-design/harness/schemas.py`

- [ ] **Step 1: Adicionar CANONICAL_REFS após DESIGN_PHASES**

Open `~/.config/opencode/skills/system-design/harness/schemas.py`, find lines 7-10:
```python
DESIGN_PHASES = [
    "requirements", "high-level-design", "deep-dive",
    "scale-reliability", "trade-offs",
]
```
After line 10, add:
```python

# ── Canonical references (hardcoded mapping, single source of truth) ──

# Each entry: (vault_name, relative_path, phase_number_or_label)
# Phase labels: 1=Requirements, 2=High-Level, 3=Deep Dive,
#               4=Scale/Reliability, 5=Trade-offs, C=Compliance
CANONICAL_REFS = [
    # Fase 1: Requirements
    ("long-running-agents", "docs/canonical/constraint-budget-gate.md", 1),
    ("long-running-agents", "docs/canonical/intent-five-part-primitive.md", 1),
    # Fase 2: High-Level Design
    ("long-running-agents", "docs/canonical/owned-agent-control-loop.md", 2),
    ("long-running-agents", "docs/canonical/generator-evaluator.md", 2),
    # Fase 3: Deep Dive
    ("long-running-agents", "docs/canonical/invariant-compensation-split.md", 3),
    ("long-running-agents", "docs/canonical/failure-pattern-classification-loop.md", 3),
    ("long-running-agents", "docs/canonical/asymmetric-failure-correction-router.md", 3),
    # Fase 4: Scale/Reliability
    ("long-running-agents", "docs/canonical/tested-degradation-ladder.md", 4),
    ("long-running-agents", "docs/canonical/production-failure-regression-flywheel.md", 4),
    # Fase 5: Trade-offs
    ("long-running-agents", "docs/canonical/constraint-failure-decision-rule.md", 5),
    ("long-running-agents", "docs/canonical/manual-brake-question-gate.md", 5),
    # Supporting (rationale/governance)
    ("long-running-agents", "docs/canonical/ice-craft-separation.md", 0),
    ("long-running-agents", "docs/canonical/measured-harness-evolution-lifecycle.md", 0),
    ("long-running-agents", "docs/canonical/deliberate-forgetting.md", 0),
]
```

- [ ] **Step 2: Verificar sintaxe Python**
```bash
python3 -c "import sys; sys.path.insert(0, '$HOME/.config/opencode/skills/system-design/harness'); from schemas import CANONICAL_REFS; print(f'{len(CANONICAL_REFS)} canonical refs loaded')"
```
Expected: `14 canonical refs loaded`

---

### Tarefa 2: Criar test_canonical_alignment.py

**Files:** Create `~/.config/opencode/skills/system-design/harness/tests/test_canonical_alignment.py`

- [ ] **Step 1: Criar o arquivo de teste**

Create `~/.config/opencode/skills/system-design/harness/tests/test_canonical_alignment.py`:
```python
"""Testa alinhamento da skill system-design com os padroes canonicos."""
import subprocess
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent.parent
SKILL_NAME = "system-design"
SKILL_MD = SKILLS_DIR / SKILL_NAME / "SKILL.md"

sys.path.insert(0, str(Path(__file__).parent.parent))
from schemas import CANONICAL_REFS


def resolve_vault(vault_name):
    """Resolve vault name to absolute path via obsidian-eval CLI."""
    result = subprocess.run(
        ["obsidian-eval", "resolve-vault", vault_name],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def test_skill_references_canonical_docs():
    """SKILL.md contem secao 'Canonical References'."""
    content = SKILL_MD.read_text(encoding="utf-8")
    assert "Canonical References" in content, (
        "SKILL.md nao contem secao 'Canonical References'"
    )


def test_all_vault_references_resolve():
    """Cada entrada em CANONICAL_REFS resolve para um arquivo existente."""
    failures = []
    for vault_name, rel_path, phase in CANONICAL_REFS:
        vault_path = resolve_vault(vault_name)
        if vault_path is None:
            failures.append(
                f"SKIP: vault '{vault_name}' nao resolveu "
                f"(obsidian-eval resolve-vault falhou)"
            )
            continue
        full_path = Path(vault_path) / rel_path
        if not full_path.exists():
            failures.append(
                f"FAIL: {vault_name}/{rel_path} nao encontrado "
                f"(resolved: {full_path})"
            )
    if failures:
        skips = [f for f in failures if f.startswith("SKIP")]
        fails = [f for f in failures if f.startswith("FAIL")]
        if fails:
            assert False, "\n".join(fails)
        if skips:
            print(f"WARNING: {len(skips)} vault(s) skipped:\n" + "\n".join(skips))


def test_canonical_refs_count_matches_expected():
    """CANONICAL_REFS contem o numero esperado de entradas."""
    assert len(CANONICAL_REFS) == 14, (
        f"CANONICAL_REFS tem {len(CANONICAL_REFS)} entradas, esperado 14"
    )
```

- [ ] **Step 2: Executar o teste**
```bash
python3 ~/.config/opencode/skills/system-design/harness/run_tests.py
```
Expected: `test_canonical_alignment.py` aparece na listagem, todos os 3 novos testes passam.

---

### Tarefa 3: Adicionar tabela Canonical References ao SKILL.md

**Files:** Modify `~/.config/opencode/skills/system-design/SKILL.md`

- [ ] **Step 1: Inserir seção Canonical References após a seção "Quando NÃO usar"**

Localize a linha `---` após "Quando NÃO usar" com grep dinâmico (evita cascade de line numbers):
```bash
grep -n '^---$' ~/.config/opencode/skills/system-design/SKILL.md | head -1
```
Após essa linha, insira:

```markdown

## Canonical References

Esta skill depende dos seguintes padrões canônicos do vault `long-running-agents`.
O agente DEVE carregá-los via `canonical-context` no início de cada fase.
O mapeamento é hardcoded — a tabela abaixo é a fonte da verdade.

### Vault: long-running-agents

| Padrão | Path | Fase |
|---|---|---|
| Constraint Budget Gate | docs/canonical/constraint-budget-gate.md | 1 |
| Intent Five-Part Primitive | docs/canonical/intent-five-part-primitive.md | 1 |
| Owned Agent Control Loop | docs/canonical/owned-agent-control-loop.md | 2 |
| Generator-Evaluator | docs/canonical/generator-evaluator.md | 2 |
| Invariant-Compensation Split | docs/canonical/invariant-compensation-split.md | 3 |
| Failure Pattern Classification Loop | docs/canonical/failure-pattern-classification-loop.md | 3 |
| Asymmetric Failure Correction Router | docs/canonical/asymmetric-failure-correction-router.md | 3 |
| Tested Degradation Ladder | docs/canonical/tested-degradation-ladder.md | 4 |
| Production Failure Regression Flywheel | docs/canonical/production-failure-regression-flywheel.md | 4 |
| Constraint-Failure Decision Rule | docs/canonical/constraint-failure-decision-rule.md | 5 |
| Manual Brake Question Gate | docs/canonical/manual-brake-question-gate.md | 5 |

### Supporting (governança e rationale)

| Padrão | Path | Uso |
|---|---|---|
| ICE Craft Separation | docs/canonical/ice-craft-separation.md | Progressive disclosure — justifica injeção inline, não upfront |
| Measured Harness Evolution Lifecycle | docs/canonical/measured-harness-evolution-lifecycle.md | Lifecycle tracking da própria bridge |
| Deliberate Forgetting | docs/canonical/deliberate-forgetting.md | Budget gate — não injetar todos os 80+ canons |

**Resolução:** `obsidian-eval resolve-vault long-running-agents` → path absoluto.
Em caso de falha, prosseguir sem canons (ver Fallback abaixo).
```

- [ ] **Step 2: Verificar que a seção foi inserida**
```bash
grep -c "Canonical References" ~/.config/opencode/skills/system-design/SKILL.md
```
Expected: `2` (uma no heading, uma no texto da nota de resolução)

---

### Tarefa 4: Adicionar micro-passos de grounding em cada fase

**Files:** Modify `~/.config/opencode/skills/system-design/SKILL.md`

- [ ] **Step 1: Fase 1 — inserir micro-passo após o heading**

Localize o heading da Fase 1 dinamicamente:
```bash
grep -n '^### Fase 1: Requirements Gathering$' ~/.config/opencode/skills/system-design/SKILL.md
```
Após a linha do heading, insira antes de `**Objetivo:**`:

```markdown

**Canonical Grounding:** Antes de levantar requisitos, carregue os padrões
de constraints e intents via `canonical-context`:
- `constraint-budget-gate` — manter constraints em 5-7, separar de specs
- `intent-five-part-primitive` — garantir que o intent tem descrição, constraints,
  cenários de falha, cenários de sucesso e conexões

Se `canonical-context` falhar ou budget ≤30%: reduzir para apenas `constraint-budget-gate`.
Se budget ≤20% (red phase): pular injeção, prosseguir sem canons.
```

- [ ] **Step 2: Fase 2 — inserir micro-passo após o heading**

```bash
grep -n '^### Fase 2: High-Level Design$' ~/.config/opencode/skills/system-design/SKILL.md
```
Após a linha do heading, insira antes de `**Objetivo:**`:

```markdown

**Canonical Grounding:** Antes de desenhar a arquitetura de alto nível, carregue:
- `owned-agent-control-loop` — decompor o sistema em Prompt, Context Builder,
  Switch Statement e Loop com pontos de intervenção explícitos
- `generator-evaluator` — separar geração de avaliação em componentes distintos

Fallback orçamentário: yellow→top-1 (`generator-evaluator`), red→skip.
```

- [ ] **Step 3: Fase 3 — inserir micro-passo após o heading**

```bash
grep -n '^### Fase 3: Deep Dive$' ~/.config/opencode/skills/system-design/SKILL.md
```
Após a linha do heading, insira antes de `**Objetivo:**`:

```markdown

**Canonical Grounding:** Antes do detalhamento, carregue padrões de handling de falhas:
- `invariant-compensation-split` — classificar cada controle como domain invariant
  (permanente) ou model-specific compensation (removível)
- `failure-pattern-classification-loop` — classificar falhas por root cause
  (model ignorance, missing harness, local coherence, prompt ambiguity,
  context loss, model regression) antes de desenhar handling
- `asymmetric-failure-correction-router` — separar fluxo de correção (root cause,
  repair, regression) do fluxo de reforço (exemplars, confidence calibration)

Fallback: yellow→top-1 (`invariant-compensation-split`), red→skip.
```

- [ ] **Step 4: Fase 4 — inserir micro-passo após o heading**

```bash
grep -n '^### Fase 4: Scale and Reliability$' ~/.config/opencode/skills/system-design/SKILL.md
```
Após a linha do heading, insira antes de `**Objetivo:**`:

```markdown

**Canonical Grounding:** Antes de planejar escala e confiabilidade, carregue:
- `tested-degradation-ladder` — classificar falhas por severidade em retryable,
  unsafe, hold rungs com retry, fallback, escalation e logging
- `production-failure-regression-flywheel` — converter falhas de produção em
  casos de teste que impedem regressão

Fallback: yellow→top-1 (`tested-degradation-ladder`), red→skip.
```

- [ ] **Step 5: Fase 5 — inserir micro-passo após o heading**

```bash
grep -n '^### Fase 5: Trade-off Analysis$' ~/.config/opencode/skills/system-design/SKILL.md
```
Após a linha do heading, insira antes de `**Objetivo:**`:

```markdown

**Canonical Grounding:** Antes da análise de trade-offs, carregue:
- `constraint-failure-decision-rule` — classificar requisitos como constraints
  (builder surface) ou failure conditions (validator surface)
- `manual-brake-question-gate` — aplicar as 3 perguntas de valor antes de
  autorizar decisões de design: vale a pena? quem precisa? qual o custo?

Fallback: yellow→top-1 (`constraint-failure-decision-rule`), red→skip.
```

- [ ] **Step 6: Verificar que todos os micro-passos foram inseridos**
```bash
grep -c "Canonical Grounding" ~/.config/opencode/skills/system-design/SKILL.md
```
Expected: `5`

---

### Tarefa 5: Adicionar fallback global e budget gate

**Files:** Modify `~/.config/opencode/skills/system-design/SKILL.md`

- [ ] **Step 1: Adicionar seção de Fallback após Output final**

Localize `## Integracoes` dinamicamente:
```bash
grep -n '^## Integracoes$' ~/.config/opencode/skills/system-design/SKILL.md
```
Antes dessa linha, insira:

```markdown

## Fallback e Budget Gate

Se o `canonical-context` skill falhar (obsidian-eval não instalado, vault não resolve):
- Prosseguir com o design sem canons injetados
- Emitir nota no design doc: "Canonical grounding skipped — canonical-context unavailable"
- NÃO bloquear o design

**Budget-aware injection:** A injeção de canons consome tokens. O `canonical-context`
skill aplica seleção budget-aware automaticamente. Por fase:
- **Green (>50%):** 2-3 canons (default)
- **Yellow (≤30%):** 1 canon (top-1 da lista da fase)
- **Red (≤20%):** 0 canons (pular injeção)

O agente deve verificar o budget antes de cada micro-passo de grounding.
```

- [ ] **Step 2: Verificar que a seção foi inserida**
```bash
grep -c "Fallback e Budget Gate" ~/.config/opencode/skills/system-design/SKILL.md
```
Expected: `1`

---

### Tarefa 6: Executar harness completo e verificar Onda 1

- [ ] **Step 1: Executar todos os testes do harness**
```bash
python3 ~/.config/opencode/skills/system-design/harness/run_tests.py
```
Expected: Todos os testes passam. Novos testes (`test_canonical_alignment.py`) aparecem no report.

- [ ] **Step 2: Verificar que test_canonical_alignment passa**
```bash
python3 -m pytest ~/.config/opencode/skills/system-design/harness/tests/test_canonical_alignment.py -v
```
Expected: 3 passed (test_skill_references_canonical_docs, test_all_vault_references_resolve, test_canonical_refs_count_matches_expected)

- [ ] **Step 2.5: Integration smoke test — verificar injeção real de canons**
Carregue a skill `system-design` com um prompt dummy e verifique que os canons são mencionados:
```bash
grep -c "docs/canonical/" ~/.config/opencode/skills/system-design/SKILL.md
```
Expected: `>= 14` (todos os canons estão referenciados no SKILL.md).
Para o teste de integração real, execute `system-design` com prompt "design a simple blog system" e confirme visualmente que `constraint-budget-gate` e `intent-five-part-primitive` aparecem no contexto da Fase 1.

- [ ] **Step 3: Commit Onda 1**
```bash
cd ~/.config/opencode
git add skills/system-design/SKILL.md
git add skills/system-design/harness/schemas.py
git add skills/system-design/harness/tests/test_canonical_alignment.py
git commit -m "feat(system-design): add canonical grounding bridge (Onda 1)

Add Canonical References table with 14 canons mapped to design phases.
Add inline micro-passes per phase (2-3 canons each) with fallback + budget gate.
Add CANONICAL_REFS to harness schemas.
Add test_canonical_alignment.py — validates all vault references resolve."
```

---

## Onda 2: Compliance Gate + Staleness

### Tarefa 7: Adicionar Compliance Gate ao SKILL.md

**Files:** Modify `~/.config/opencode/skills/system-design/SKILL.md`

- [ ] **Step 1: Inserir Compliance Gate antes de Output final**

```bash
grep -n '^## Output final$' ~/.config/opencode/skills/system-design/SKILL.md
```
Antes dessa linha, insira:

```markdown

## Compliance Gate (pós-design)

Após gerar o design doc completo (Fases 1-5), execute um evaluator que verifica
alinhamento com os padrões canônicos injetados. **Não é uma fase numerada do
framework** — é um gate pós-design, executado após a Fase 5.

**Procedimento:**
1. Reler o design doc gerado
2. Para cada padrão canônico injetado nas fases 1-5, verificar:
   - (a) A decisão de design correspondente é rastreável ao padrão, OU
   - (b) O design doc justifica explicitamente o desvio do padrão
3. Verificar que a taxonomia dos canons é usada corretamente:
   - "invariant" vs "compensation" (do invariant-compensation-split)
   - "prevention" vs "correction" (do asymmetric-failure-correction-router)
   - Classes de root cause (do failure-pattern-classification-loop)

**Output do gate:** Lista de padrões aplicados + justificativas de desvio.
Designs simples (ex: blog pessoal, CRUD básico) podem pular o gate com nota
explícita: "Compliance gate skipped — low complexity design."
```

- [ ] **Step 2: Verificar que a seção foi inserida**
```bash
grep -c "Compliance Gate" ~/.config/opencode/skills/system-design/SKILL.md
```
Expected: `2` (heading + menção no texto)

---

### Tarefa 8: Criar test_staleness.py

**Files:** Create `~/.config/opencode/skills/system-design/harness/tests/test_staleness.py`

- [ ] **Step 1: Criar o arquivo de teste**

Create `~/.config/opencode/skills/system-design/harness/tests/test_staleness.py`:
```python
"""Testa staleness dos canons referenciados — snapshot diff, threshold 90d."""
import json
import subprocess
import sys
import time
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent.parent
HARNESS_DIR = Path(__file__).parent.parent
SNAPSHOT_FILE = HARNESS_DIR / "canonical-snapshot.json"

sys.path.insert(0, str(HARNESS_DIR))
from schemas import CANONICAL_REFS

STALENESS_THRESHOLD_SECONDS = 90 * 86400  # 90 dias


def resolve_vault(vault_name):
    result = subprocess.run(
        ["obsidian-eval", "resolve-vault", vault_name],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def collect_current_snapshot():
    """Coleta last_updated de todos os canons referenciados."""
    snapshot = {}
    for vault_name, rel_path, phase in CANONICAL_REFS:
        vault_path = resolve_vault(vault_name)
        if vault_path is None:
            continue
        full_path = Path(vault_path) / rel_path
        if not full_path.exists():
            continue
        mtime = full_path.stat().st_mtime
        snapshot[f"{vault_name}/{rel_path}"] = mtime
    return snapshot


def test_staleness_snapshot_bootstrap():
    """Primeira execucao: gera baseline sem falhar."""
    if not SNAPSHOT_FILE.exists():
        snapshot = collect_current_snapshot()
        SNAPSHOT_FILE.write_text(json.dumps(snapshot, indent=2))
        print(f"Bootstrap: snapshot criado com {len(snapshot)} entradas")
        return  # nao falha na primeira execucao


def test_canonical_docs_not_staler_than_skill():
    """Nenhum canon referenciado mudou sem atualizacao correspondente na skill."""
    if not SNAPSHOT_FILE.exists():
        # Bootstrap ainda nao rodou — roda agora e passa
        snapshot = collect_current_snapshot()
        SNAPSHOT_FILE.write_text(json.dumps(snapshot, indent=2))
        return

    previous = json.loads(SNAPSHOT_FILE.read_text())
    current = collect_current_snapshot()
    skill_mtime = (SKILLS_DIR / "system-design" / "SKILL.md").stat().st_mtime

    staleness_warnings = []
    for path_key, current_mtime in current.items():
        if path_key not in previous:
            continue  # novo canon adicionado, nao e staleness
        prev_mtime = previous[path_key]
        if current_mtime > prev_mtime:
            # Canon foi atualizado
            delta_days = (skill_mtime - current_mtime) / 86400
            if delta_days < -STALENESS_THRESHOLD_SECONDS / 86400:
                staleness_warnings.append(
                    f"STALE: {path_key} atualizado ha {-delta_days:.0f}d "
                    f"(skill nao foi atualizada ha mais de 90d apos mudanca)"
                )

    # Atualiza snapshot para proxima execucao
    SNAPSHOT_FILE.write_text(json.dumps(current, indent=2))

    if staleness_warnings:
        print("WARNING: Canonical staleness detected (not blocking):")
        for w in staleness_warnings:
            print(f"  {w}")


def test_staleness_only_on_actual_updates():
    """Snapshot diff: so alerta se canon mudou, nao por decurso de tempo."""
    if not SNAPSHOT_FILE.exists():
        return  # bootstrap ainda nao rodou

    previous = json.loads(SNAPSHOT_FILE.read_text())
    current = collect_current_snapshot()

    changed = []
    for path_key, current_mtime in current.items():
        prev_mtime = previous.get(path_key)
        if prev_mtime is None:
            continue
        if current_mtime != prev_mtime:
            changed.append(
                f"{path_key}: {prev_mtime} -> {current_mtime}"
            )

    if changed:
        print(f"INFO: {len(changed)} canon(s) mudaram desde o ultimo snapshot:")
        for c in changed:
            print(f"  {c}")
    # Nao falha — mudancas em canons sao esperadas.
    # O alerta de staleness so dispara se a skill nao acompanhou (teste acima).
```

- [ ] **Step 2: Executar o teste (bootstrap)**
```bash
python3 -m pytest ~/.config/opencode/skills/system-design/harness/tests/test_staleness.py -v -s
```
Expected: 3 passed. `test_staleness_snapshot_bootstrap` cria `canonical-snapshot.json`.

- [ ] **Step 3: Verificar que o snapshot foi criado**
```bash
python3 -c "import json; d=json.load(open('$HOME/.config/opencode/skills/system-design/harness/canonical-snapshot.json')); print(f'{len(d)} entries in snapshot')"
```
Expected: `14 entries in snapshot`

---

### Tarefa 9: Executar harness completo e verificar Onda 2

- [ ] **Step 1: Executar todos os testes do harness**
```bash
python3 ~/.config/opencode/skills/system-design/harness/run_tests.py
```
Expected: Todos os testes passam. `test_staleness.py` aparece no report.

- [ ] **Step 2: Verificar que test_staleness passa**
```bash
python3 -m pytest ~/.config/opencode/skills/system-design/harness/tests/test_staleness.py -v
```
Expected: 3 passed

- [ ] **Step 3: Commit Onda 2**
```bash
cd ~/.config/opencode
git add skills/system-design/SKILL.md
git add skills/system-design/harness/tests/test_staleness.py
git add skills/system-design/harness/canonical-snapshot.json
git commit -m "feat(system-design): add compliance gate + staleness detection (Onda 2)

Add Compliance Gate (post-design, not a numbered phase) — evaluator verifies
canonical alignment after Fases 1-5.

Add test_staleness.py — snapshot diff of canonical last_updated, 90d threshold.
First run bootstraps baseline without failing."
```

---

## Verificação Final

- [ ] **Step 1: Executar suite completa de harness**
```bash
python3 ~/.config/opencode/skills/system-design/harness/run_tests.py
```
Expected: Exit 0, todos os testes passam (contract + design_phases + canonical_alignment + staleness).

- [ ] **Step 2: Verificar que SKILL.md tem todas as seções novas**
```bash
echo "=== New sections ===" && grep -c "Canonical References\|Canonical Grounding\|Fallback e Budget Gate\|Compliance Gate" ~/.config/opencode/skills/system-design/SKILL.md
```
Expected: `Canonical References: 2, Canonical Grounding: 5, Fallback e Budget Gate: 1, Compliance Gate: 2`

- [ ] **Step 3: Smoke test — carregar a skill e verificar que canons são mencionados**
```bash
grep -c "docs/canonical/" ~/.config/opencode/skills/system-design/SKILL.md
```
Expected: `>= 14`

- [ ] **Step 4: Verificar git log**
```bash
cd ~/.config/opencode && git log --oneline -3
```
Expected: Dois commits visíveis (Onda 1, Onda 2).

---

**Plan complete.** Total: 9 tarefas, ~45 passos, 2 commits, 6 arquivos alterados (4 criados/modificados + 2 deletados).

**Notas de execução:**
- **Line numbers**: Todas as tasks usam `grep -n` para localizar headings dinamicamente (não dependem de números de linha fixos). Isso evita o cascade failure de edições sequenciais.
- **Integration smoke test**: Além dos testes de harness, execute `system-design` com prompt dummy ("design a simple blog system") e verifique que os canons aparecem no contexto do agente em cada fase.
- **Git state**: Verifique `git status --porcelain skills/system-design/` antes de começar. O SKILL.md pode ter modificações pré-existentes — use `git stash` se necessário.
- **pytest**: O harness padrão usa `run_tests.py` (stdlib-only). `python3 -m pytest` é conveniência adicional — certifique-se de que está instalado (`pip install pytest`).
- **Snapshot count**: Task 8 Step 3 espera "14 entries" mas o número real pode ser menor se algum vault não resolver. Ajuste a verificação se necessário.
