---
title: "Skill-Canons Bridge — Decisões de Implementação (Ondas 0-2)"
type: adr
status: accepted
date: 2026-06-24
deciders: ["pavan"]
tags: ["governanca", "decision-discipline", "skill-canons-bridge", "arquitetura", "harness-engineering"]
aliases: ["bridge implementation ADR", "skill canons bridge decisions", "bridge decisions"]
last_updated: 2026-06-24
relates-to:
  - "[[../canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[../canonical/ice-craft-separation|ICE Craft Separation]]"
  - "[[../canonical/deliberate-forgetting|Deliberate Forgetting]]"
  - "[[../canonical/constraint-budget-gate|Constraint Budget Gate]]"
  - "[[../canonical/intent-five-part-primitive|Intent Five-Part Primitive]]"
  - "[[../../.omo/plans/2026-06-23-skill-canons-bridge-framework|Skill-Canons Bridge Framework]]"
sources:
  - "[[../../.omo/plans/2026-06-24-review-work-bridge-plan|Review-Work Bridge Plan]]"
  - "[[../../.omo/plans/2026-06-24-architecture-bridge-plan|Architecture Bridge Plan]]"
  - "[[../../.omo/plans/2026-06-24-writing-plans-bridge-plan|Writing-Plans Bridge Plan]]"
---

# ADR: Skill-Canons Bridge — Decisões de Implementação (Ondas 0-2)

## Contexto

O framework `skill-canons-bridge` define 3 níveis de bridging para conectar skills do ecossistema
aos padrões canônicos do vault `long-running-agents`. A skill pioneira `system-design` já possui
Level 3 completo. As Ondas 0-2 do rollout (3 skills: `review-work`, `architecture`, `writing-plans`)
foram implementadas em 2026-06-24. Durante a implementação, 5 decisões arquiteturais cross-cutting
foram tomadas. Este ADR as documenta formalmente.

## Decisão

As 3 skills receberam Level 3 Full Bridge seguindo o padrão estabelecido pelo `system-design`,
com as seguintes decisões cross-cutting:

1. **Grounding strategy: Opção B (inline injection)** como padrão
2. **Promotion rule: D8 (≥2 invocadores → +1 nível)** aplicada a `architecture` e `writing-plans`
3. **Baseline policy: snapshot aceito** como evidência quando runs manuais são inviáveis
4. **Budget gate: 4 fases** (Green/Yellow/Orange/Red) como evolução do system-design (3 fases)
5. **DRY strategy: cópia local** por enquanto, extrair para shared module quando >5 skills

## Opções Consideradas

| Opção | Complexidade | Custo | Escalabilidade | Familiaridade | Pros | Contras |
|-------|-------------|-------|---------------|--------------|------|---------|
| **D1-A: Opção B (inline)** | Baixa | Médio (staleness) | Média | Alta (system-design) | Simples, zero load_skills overhead, sem dependência de canonical-context no runtime | Texto inline fica stale se canon muda; staleness test mitiga |
| D1-B: Opção C (load_skills) | Média | Alto (5× canonical-context queries) | Alta | Média | Resolve dinamicamente, sempre atualizado | 5× mais tokens, falha se obsidian-eval offline |
| **D2-A: Aplicar regra D8** | Baixa | Zero | Alta | Alta (framework) | Consistente com árvore de decisão | — |
| D2-B: Manter Level 2 | Zero | Zero | — | — | Menos trabalho | Inconsistente com framework; architecture/writing-plans invocadas por 3-4 skills |
| **D3-A: Snapshot como baseline** | Muito baixa | Zero | Alta | Alta (framework permite skip) | Evita 11 runs manuais (~45min) | Não captura menções canônicas espontâneas do modelo |
| D3-B: Runs manuais | Média | 45min | Baixa | Alta | Evidência completa de output real | Custo de tempo alto; budget da sessão consome |
| **D4-A: 4 fases** | Baixa | Zero | Alta | Alta (canon phase-gated) | Alinha com canonical phase-gated-token-health-monitor | system-design tem 3 fases (inconsistência) |
| D4-B: 3 fases (igual system-design) | Zero | Zero | — | Alta | Consistente com pioneiro | Perde granularidade Orange (20-30%) |
| **D5-A: Cópia local** | Baixa | Zero (hoje) | Baixa (N skills = N cópias) | Alta | Cada skill autocontida | DRY violation; 4 cópias para manter |
| D5-B: Shared module | Média | 2h de refactor | Alta | Média | Single source of truth | Quebra isolamento das skills; risco de breaking change |

## Análise de Trade-offs

- **Dimensão decisiva:** Familiaridade — o system-design como pioneiro estabeleceu o padrão. Divergir sem razão forte criaria inconsistência no ecossistema.
- **Risco aceito (D1):** Staleness do texto inline. Se um canon for reescrito, o texto nos 3 SKILL.md fica desatualizado até o staleness test (90 dias) alertar. Mitigação: `canonical-snapshot.json` + `test_staleness.py`.
- **Risco aceito (D3):** Baseline via snapshot não captura menções canônicas espontâneas do modelo (ex: se o modelo já conhece `intent-five-part-primitive` do treinamento). Risco baixo — o modelo não foi treinado nos padrões canônicos do ecossistema Pavan.
- **Por que não D1-B (load_skills)?** O review-work lança 5 agentes paralelos. Cada um carregando `canonical-context` via `load_skills` consumiria ~5× mais tokens e criaria dependência de `obsidian-eval` disponível no runtime de cada sub-agente.
- **Custo de reverter (D4):** Se as 4 fases se mostrarem complexas demais, voltar para 3 fases é trivial — remover a linha Orange da tabela de budget gate em cada SKILL.md. Sem migração de dados, sem breaking change.

## Consequências

**Fica mais fácil:**
- Aplicar bridge a novas skills — o padrão está estabelecido e documentado
- Auditar alinhamento canônico — `test_canonical_alignment.py` verifica consistência dual-source
- Detectar defasagem — `test_staleness.py` alerta após 90 dias

**Fica mais difícil:**
- Atualizar texto inline de um canon — é preciso editar N SKILL.md (3 hoje, mais no futuro)
- Manter `resolve_utils.py` sincronizado — 4 cópias (system-design + 3 novas)

**Revisitar quando:**
- **D1 (inline vs load_skills):** Quando o ecossistema tiver >10 skills com bridge, reavaliar custo de manutenção do texto inline vs custo de runtime do load_skills
- **D3 (baseline via snapshot):** Quando houver budget para capturar runs manuais, substituir snapshots por evidência real
- **D4 (4 fases):** Se o system-design for atualizado para 4 fases, a consistência cross-skill é restaurada
- **D5 (shared module):** Quando >5 skills tiverem bridge, extrair `resolve_utils.py` e `test_staleness.py` para `~/.config/opencode/tests/skills/shared_contract_helpers.py`

## Ações

- [x] Implementar Level 3 bridge em review-work (946 linhas, 26/26 testes)
- [x] Implementar Level 3 bridge em architecture (280 linhas, 20/20 testes)
- [x] Implementar Level 3 bridge em writing-plans (231 linhas, 26/26 testes)
- [x] Capturar baselines via snapshot (3 skills)
- [x] Corrigir 12 findings do review-work pós-implementação
- [ ] Atualizar system-design para budget gate 4 fases (alinhar pioneiro)
- [ ] Extrair shared module quando >5 skills tiverem bridge (GC Day 2026-08-22)
- [ ] Capturar runs manuais de baseline quando houver budget de sessão
