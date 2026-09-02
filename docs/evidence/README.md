---
title: "docs/evidence/ — casos de regressão e evidências validadas"
type: index
tags: ["index", "testes-qa", "evals", "production"]
aliases: ["evidence readme", "casos de regressao", "schema de caso de evidencia"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/system-of-record|System of Record]]", "[[docs/evidence/2026-09-01-qi-loop-telemetry-correlation-break|Caso: telemetria do qi-loop]]"]
sources: ["https://github.com/pavani06/long-running-agents/issues/211"]
---

# docs/evidence/

Evidências validadas do repositório: benchmarks, resultados de teste, métricas e casos de regressão de produção. Nível 3 da precedência (`docs/system-of-record.md:14-21`): ADRs aceitos e canonical docs mandam sobre qualquer caso desta pasta (AGENTS.md Rule 8). Nenhum caso pode contradizer ADR; conflito deve ser escalado, não absorvido.

O consumidor principal da pasta é o [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]: toda falha de produção com gap comportamental vira caso durável, salvo rejeição explícita como duplicado, inacionável ou fora de escopo.

## Schema do caso

Arquivos nomeados `YYYY-MM-DD-<slug>.md` (slug lowercase-hyphens, Rule 16.5; a data é a do incidente de origem). Frontmatter obrigatório: `title`, `type: evidence`, `date`, `tags`, `aliases` (não vazio), `relates-to`, `sources`. Este tipo `evidence` é extensão local desta pasta, não existe na tabela Rule 16.2 (ver não-aplicabilidade do validador abaixo).

Corpo do caso, campos mínimos (todos com evidência real, nenhum inventado):

| Campo | Conteúdo |
|---|---|
| ID do caso | O slug do arquivo |
| Origem/intake | Incidente, queixa ou gap que gerou o caso, com data |
| Captura | Referência resolvível à interação/trace (arquivo do repo, ou vault externo via sintaxe `vault:`) |
| Versões | Versões de skill, stack, repo/commit conhecidas no incidente; "não localizado" é resposta válida |
| Esperado vs observado | Comportamento esperado (com referência ao contrato) e observado (com referência à evidência) |
| Classe de falha | Uma classe da taxonomia do flywheel (`:42-53`); se nenhuma encaixar, a mais próxima + nota de divergência no corpo do caso |
| Privacidade/retenção | O que foi filtrado ou não copiado (nenhuma fixture bruta sem filtro, nenhum secret) |
| Dedupe/cobertura | Verificação contra casos existentes + recorrências da mesma classe anexadas ao mesmo caso |
| Recorrências | Nova ocorrência da mesma classe: data, evento, bypass, registro |
| Baseline/candidate | Status do backfill: FAIL documentado antes do fix; reverificação depois |
| Tier | Atribuição contra eval tier stratification quando houver suite |
| Links | Incidente, PR, analysis, issue de origem |

## Recorrências e dedupe

Falha da mesma classe e mecanismo é recorrência dentro do caso existente (passo 5 do flywheel), nunca caso novo. Caso novo só para classe nova ou mecanismo distinto. Duplicados e casos de baixo valor são pruneados ou mergeados periodicamente preservando cobertura única (passo 9).

## Promoção e retenção

- **Entrada:** caso entra como registro do incidente com baseline FAIL (ou evidência do estado quebrado) e correção pendente.
- **Promoção:** com a correção aterrissada, o backfill candidate reexecuta o cenário e o caso passa a evidência validada referenciável (passo 7). Referências do SOR e de canonical docs para casos desta pasta contam como reconhecimento, não como promoção de precedência.
- **Retenção:** casos mantidos enquanto a cobertura de falha for única; prune/merge pelo passo 9. Fixture de produção só permanece após filtros de privacidade (passo 3); `telemetry.db` e artefatos com paths de sessão não são copiados para o repo.

## Não-aplicabilidade do validador

`scripts/validate-obsidian.ts` monitora apenas `docs/canonical/`, `docs/analysis/` e `curriculum/` (`MONITORED_DIRS`, `scripts/validate-obsidian.ts:261`; critérios de aplicabilidade por check em `:334-359`). `docs/evidence/` **não é monitorado**: `npm run validate:obsidian` e `npm run lint` passam independentemente do conteúdo desta pasta, e o check de broken wikilinks só valida arestas originadas em `docs/canonical/`.

Convenções voluntárias desta pasta (aderência à Rule 16 sem enforcement):

1. Frontmatter completo conforme o schema acima.
2. Wikilinks somente para arquivos que existem neste repo. Referência a arquivo de vault externo usa a sintaxe sancionada pelo ADR Vault Federation (`docs/decisions/2026-09-01-vault-federation-consultable-registry.md`), `vault:<nome>/<path>`, em `sources` ou inline code, nunca wikilink (o alvo não existe neste repo e quebraria o grafo se o monitoramento for estendido).
3. Tags ancoradas em domínios/tópicos do system-of-record (Rule 16.4) e com interseção com os docs linkados (Rule 16.7).
