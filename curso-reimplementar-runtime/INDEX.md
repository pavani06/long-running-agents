---
title: "🗂️ INDEX — Mapa completo e dependências"
type: curriculum-index
aliases: ["índice", "index", "mapa", "dependências"]
tags: [curriculo-conteudo, sisyphus-runtime, index]
relates-to: ["[[README|Overview]]", "[[QUICK_START|Quick Start]]", "[[GLOSSARY|Glossário]]"]
last_updated: 2026-08-13
---

# 🗂️ INDEX — Mapa completo e dependências

Cada lição declara seu **pré-requisito** no frontmatter. Esta é a ordem canônica.

## Nível 0 — Orientação
- `00-nivel-0-orientacao/01-o-que-e-o-runtime.md`
- `00-nivel-0-orientacao/02-o-loop-em-uma-tela.md` ← contém o gabarito do "teste dos 5 minutos"

## Nível 1 — O substrato (pré-req: Nível 0)
- `01-nivel-1-substrato/01-layout-do-vault.md`
- `01-nivel-1-substrato/02-fatos-duraveis.md`
- `01-nivel-1-substrato/03-estado-e-handoffs.md`
- `01-nivel-1-substrato/04-obsidian-eval.md`
- `exercises/exercise-01-skeleton.md` · `exercise-02-primeiro-fato.md` (+ solutions/)

## Nível 2 — A máquina (pré-req: Nível 1)
- `02-nivel-2-a-maquina/01-topologia-de-papeis.md`
- `02-nivel-2-a-maquina/02-o-loop-dispatch-gate.md`
- `02-nivel-2-a-maquina/03-o-intent-primitivo.md`
- `exercises/exercise-01-ciclo-a-mao.md` (+ solutions/)

## Nível 3 — Governança e cicatrizes (pré-req: Nível 2) ← o coração
- `03-.../01-a-familia-de-regras.md`
- `03-.../02-disciplina-de-gate.md`
- `03-.../03-a-regra-do-rele.md`
- `03-.../04-o-achado-central.md`
- `case-studies/caso-momus-skip.md` ← incident-2026-07-09 (lição-amostra)
- `case-studies/caso-gate-traversal.md` ← incident-2026-07-05
- `case-studies/caso-api-key-leak.md` ← incident-2026-07-23
- `exercises/exercise-01-derivar-a-regra.md` (+ solutions/)

## Nível 4 — Reimplementar e evoluir (pré-req: Níveis 1–3) ← o objetivo
- `04-.../01-nucleo-reproduzivel-minimo.md`
- `04-.../02-bootstrap-nova-maquina.md`
- `04-.../03-evoluir-o-schema-global.md`
- `case-studies/caso-schema-v6-a-v20.md` ← forensics-schema-version-20
- `real-world-exercises/exercise-01-dry-run.md` (+ solutions/)

## Ferramentas (referência transversal)
- `08-tools-templates/templates/` — frontmatter de durable-fact, dispatch, incident, charter
- `08-tools-templates/skeleton/` — árvore mínima do vault

---

## 🔗 Fios que atravessam o curso

Três ideias reaparecem em todos os níveis — se o leitor pegar só estas, pegou o sistema:

1. **O disco vence** (Nível 1 → 3) — autoridade está nos arquivos, não nos resumos.
2. **Gates medem o disco, não leem promessas** (Nível 2 → 3) — texto-base.
3. **Afirmação sobre estado não vira durável sem medição de terceiro** (Nível 3 → 4) — o
   achado central, que vira exigência de design nos gates e nos próprios exercícios.
