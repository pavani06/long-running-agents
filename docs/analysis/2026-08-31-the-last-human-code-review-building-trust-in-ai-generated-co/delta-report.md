---
title: "Delta Report — The Last Human Code Review (Phase 0 incremental)"
type: analysis
date: 2026-08-31
aliases: ["delta report last human code review", "phase 0 delta 2026-08-31"]
tags: ["governanca", "harness-engineering"]
relates-to: ["[[docs/plans/2026-08-31-skill-hardening-adversarial-findings|Skill Hardening Plan]]"]
---

# Delta Report — Phase 0 Incremental

Produzido pelo orquestrador no Passo 0a de `analyze-and-improve` Phase 0.
Insumo para o Passo 0b (atualização incremental delegada).

## Base model

- **Arquivo:** `mapa-mental-repo/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-mental-model.yaml`
- **`meta.date`:** 2026-08-30
- **mtime:** 2026-08-30 21:14:47 -0300
- **Dias desde o modelo:** 1

### Nota de seleção da base (desvio da prescrição)

O Passo 0a prescreve `ls -1 mapa-mental-repo/*.yaml | sort | tail -1`. Esse
comando desempata **alfabeticamente** quando dois modelos compartilham a data no
nome, e devolve `2026-08-30-kavak-s-playbook-...` em vez de
`2026-08-30-gtm-ai-agents-...`. A base correta é o modelo **gtm**:

1. mtime posterior (21:14 vs 19:20 do kavak);
2. o próprio conteúdo do modelo gtm declara ter absorvido o cluster kavak
   ("142 arquivos em `docs/canonical/` (inclui cluster Kavak absorvido
   2026-08-30)").

Usar o kavak como base contaria todo o run GTM (12 canonical + 9 curriculum +
2 skills + 2 exercises = 25+ deltas) como delta, forçando full rebuild
indevidamente. A base usada aqui é a **gtm**.

## Deltas

Scan por `find <dir> -name '*.md' -newer <base>.yaml`, cobrindo
`docs/canonical/`, `docs/decisions/`, `curriculum/`, `.opencode/skills/`,
`.opencode/agents/`, `docs/plans/`, `docs/evidence/`.

| # | Path | Classificação | mtime | Descrição |
|---|---|---|---|---|
| 1 | `.opencode/skills/analyze-and-improve/SKILL.md` | `atualizacao` | 2026-08-31 09:08 | Semantic evaluation gate adicionado ao Step 6 (citation sampling, executable content, source fidelity) e regra no-fabricated-premises. Commit `f19cb1d`, +11 linhas. |
| 2 | `.opencode/skills/harness-analyze-and-improve/SKILL.md` | `atualizacao` | 2026-08-31 09:08 | Mesmo commit `f19cb1d`: verificação semântica proporcional ao risco do artefato, campo `verification_depth` em `test-results.json`, regra de restauração do placeholder do STEER.md. +12/-10 linhas. |
| 3 | `docs/plans/2026-08-31-skill-hardening-adversarial-findings.md` | `novo-plano` | 2026-08-31 09:08 | Plano de execução das 8 correções da análise adversarial de 2026-08-30 (premissa falsa em delegação, ambiente errado, commit fora de escopo, PASS estrutural, gate morto, estado residual, conflito wrapper/spec, gap-repair improvisado). Novo arquivo, 169 linhas. |

**Total de deltas: 3**

### Excluídos da contagem (não são estrutura de repositório)

- `PROGRESS.md` — estado de runtime do harness, resetado a cada pipeline.
- `docs/analysis/**` — artefatos dos runs anteriores, já refletidos na base.
- `.opencode/skills/analyze-and-improve/harness/templates/test-results.json` — template de contrato (não `.md`); alterado no mesmo commit `f19cb1d`, coberto pelo delta #1/#2.
- 19 arquivos em `.obsidian/plugins/` e 5 em `.understand-anything/` — estado de plugin do vault e workspace de ferramenta, sem relação com a estrutura do repositório.

## Decisão de modo

| Critério | Limite | Medido | Resultado |
|---|---|---|---|
| Dias desde o modelo anterior | > 30 → full rebuild | 1 | OK |
| Total de deltas | > 10 → full rebuild | 3 | OK |
| `mapa-mental-repo/` vazio | → full rebuild | 5 modelos ativos | OK |

**Modo: incremental.** Fallback para full rebuild foi considerado e rejeitado —
nenhum dos três gatilhos disparou. Prossegue para o Passo 0b.

## Cobertura esperada no Passo 0b

Os 3 deltas concentram-se em dois pontos do modelo:

- **`architecture.abstractions` → "Camada de skills" e "Pipeline de análise
  (analyze-and-improve)" / "Runtime do harness":** os gates de verificação
  mudaram de estruturais para estruturais + semânticos. A descrição do pipeline
  na base não menciona verificação semântica.
- **`gaps`:** o plano de skill hardening documenta 8 falhas operacionais
  observadas; as que foram fechadas por `f19cb1d` devem sair da lista de gaps,
  as remanescentes devem entrar.

Todo o restante do modelo base permanece válido e não deve ser reescrito.
