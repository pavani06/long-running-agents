# Análise Agregada: Integration Roadmap → Manifesto Permanente

**Data**: 2026-06-14
**Sessão**: Continuação das correções pós-review do analyze-and-improve
**Agentes**: Oracle (deep analysis), Plan (correction plan), Oracle (permanent solution design)

---

## Contexto

Após commit `7fe895b` com as correções pós-review, o review de 5 agentes identificou 4 blocking issues:

1. Phase 4 gate ainda exige "Integration roadmap" (SKILL.md:755)
2. Phase 5 prompt não instrui agente a criar "Artifacts Created" (SKILL.md:788-803)
3. Partial Coverage Medium inconsistente (SKILL.md:839 + :889)
4. "Agent 4" residual fora do OBSOLETO (SKILL.md:777)

---

## Convergência (todos os agentes concordam)

1. **Integration roadmap tinha valor real, mas o formato estava errado.**
   - Necessidade de rastreabilidade: classificação → artefatos → integração é legítima
   - Arquivo separado `integration-roadmap.md` + Agent 4 dedicado = overhead desnecessário

2. **Nenhum Agent 4 novo.**
   - O trabalho deve ser absorvido pela Phase 4 (verificação) ou Phase 5 (sumarização)

3. **Phase 4 gate atual está quebrado.**
   - "Integration roadmap conecta todos os artefatos" é contraditório após remover Agent 4

4. **GUIDE-analyze-and-improve.md precisa ser atualizado.**
   - Documenta estado antigo: Phase 4 gera `integration-roadmap.md`, Phase 6 é "opcional"

5. **Phase 5 prompt não instrui o agente.**
   - "Artifacts Created Summary" está fora do bloco `task()` delegado

---

## Divergência: Dois Designs

### Design A (Agent 1 — Opção B simplificada)
- **Onde**: Seção "Artifacts Created" em `docs/system-of-record.md`
- **Quem gera**: Phase 5 agente `quick`
- **PC Medium**: Integrar por default na Phase 6 (pode pular)

### Design B (Agent 3 — Manifesto separado) ← RECOMENDADO
- **Onde**: Arquivo `docs/analysis/<session>/<date>-artifacts.{md,yaml}`
- **Quem gera**: Orquestrador (pós-Phase 4, pré-Phase 5)
- **PC Medium**: NÃO integrar por default. Documentar apenas. Opt-in para Phase 6.

### Trade-off

| Critério | Design A | Design B |
|---|---|---|
| Simplicidade imediata | Maior (menos arquivos) | Menor (novo par de arquivos) |
| Separação de responsabilidades | Fraca (log de sessão no índice canônico) | Forte (manifesto session-local) |
| Machine-readable | Não (só markdown) | Sim (YAML estruturado) |
| Contrato Phase 4→Phase 5 | Ambíguo (infere do git diff) | Explícito (manifesto como contrato) |
| Poluição do system-of-record | Sim (log por sessão) | Não (índice permanece limpo) |
| Consistência PC Medium | Força integração mesmo com baixo valor | Documenta gap sem forçar churn |

---

## Recomendação: Design B (Agent 3)

Seguir o manifesto separado porque:
- `system-of-record.md` é índice canônico, não log de execução
- Contrato explícito entre fases elimina ambiguidade para o orquestrador
- PC Medium como "documenta, não integra" é mais consistente com a realidade do repositório

### Formato do Manifesto

```yaml
meta:
  type: artifact-manifest
  date: <date>
  source_slug: <source-slug>
  classification_file: docs/analysis/<date-slug>/<date-slug>-classification.yaml

artifacts:
  canonical_docs: []
  skills: []
  exercises: []
  examples: []

skipped:
  already_exists: []
  better_implementation: []
  partial_coverage_medium_no_phase6: []

gate:
  phase4_complete: true
  notes: []
```

---

## Plano de Correção (Agent 2 — 7 tarefas, adaptável ao Design B)

O Agent 2 produziu um plano com 7 tarefas (T0-T7) baseado no Design A. Para o Design B, as tarefas T1, T2, T4 e T6 precisam ser ajustadas:

| Task | Design A (atual) | Design B (ajuste necessário) |
|---|---|---|
| T0 | Baseline red checks | Igual |
| T1 | Substituir roadmap por "Artifacts Created" no system-of-record | Substituir roadmap por manifesto `-artifacts.yaml` |
| T2 | Mover instrução para dentro do prompt Phase 5 | Orquestrador gera manifesto; Phase 5 lê manifesto |
| T3 | Alinhar canonical docs para incluir P2 | Igual (P2 ganha canonical doc) |
| T4 | PC Medium integrado por default | PC Medium documentado, NÃO integrado por default |
| T5 | Marcar roadmaps históricos como legacy | Igual |
| T6 | Sync harness guide | Ajustar para refletir manifesto, não system-of-record |
| T7 | Final QA | Igual |

---

## Decisão Pendente

Escolher entre Design A e Design B para continuar a execução na próxima sessão.
