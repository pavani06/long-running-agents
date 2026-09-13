---
title: "Runbook — execução de uma etapa do EPIC analyze-and-improve v4"
type: plan
date: 2026-09-13
tags:
  - harness-engineering
  - agentes-orquestracao
  - governanca
  - agentic-coding
aliases:
  - runbook analyze-and-improve v4
  - execução etapa analyze-and-improve
  - v4 execution runbook
relates-to:
  - "[[docs/plans/2026-09-13-analyze-and-improve-v4|Analyze-and-Improve v4 — design]]"
  - "[[docs/system-of-record|System of Record]]"
  - "[[AGENTS|AGENTS]]"
---

# Runbook — execução de uma etapa do EPIC analyze-and-improve v4

Runbook **reutilizável** para executar **uma etapa** do EPIC #257 (analyze-and-improve v4)
de ponta a ponta, **incluindo o ritual de fim-de-fase** (atualizar o épico + revisitar as
etapas restantes). Uma etapa por sessão, em contexto limpo.

**Fonte de verdade do desenho:** [`docs/plans/2026-09-13-analyze-and-improve-v4.md`](2026-09-13-analyze-and-improve-v4.md).
**Épico + sub-issues:** #257 (Etapas 0–8 = #258–#266).

> Comece pela **#258** (Etapa 0). Ordem por dependência: 0→1→2→3→**4 (gate A/B)**→5→{6,7}→8.
> A Etapa 4 (#262) é o **gate de progressão**: só siga pro Tier B (5–8) se os 2 critérios pass/fail passarem.

---

## Como usar
Cole o bloco abaixo numa sessão nova (contexto limpo), trocando `ISSUE_ALVO` pela etapa da vez.
Modo autônomo equivalente: `executar issue completa #<N>` (o `issue-executor-master` roda o ciclo —
**o ritual de fim-de-fase da Seção 5 continua obrigatório**; inclua-o no pedido).

```markdown
# Executar uma etapa do EPIC #257 (analyze-and-improve v4)

ISSUE_ALVO: #258        # ← troque para a etapa da vez (respeite as dependências)
EPIC: #257
REPO: pavani06/long-running-agents

## 0. Fonte de verdade (leia antes de tudo)
- Design doc: docs/plans/2026-09-13-analyze-and-improve-v4.md
- Épico: `gh issue view 257`
- A sub-issue alvo: `gh issue view <ISSUE_ALVO>` (Contexto/DoD/Escopo/Deps/Fluxo/Housekeeping)
- Memória do projeto (carrega sozinha): analyze-and-improve-v4, youtube-extracts-layer, youtube-themes-layer

## 1. Pré-voo (gates de entrada — pare se falhar)
- Confirme que TODAS as dependências da sub-issue estão CLOSED (`gh issue view <dep>`).
  Se alguma dep está aberta, NÃO comece — reporte e pare.
- Confirme que a sub-issue não está com label `agent:working` de outra sessão (não roube trabalho).
- Este repo tem OUTRA sessão ativa (X-bookmarks). Trabalhe SEMPRE em git worktree isolado
  a partir de origin/main; nunca no working tree compartilhado.

## 2. Restrições travadas (arquitetura v4 — não reabrir)
- Topologia só-LRA; runtime HTTP portátil (gerador GLM `ZAI_API_KEY`, evaluator OpenAI `OPENAI_API_KEY`).
- Machine-gated (determinístico + evaluator adversarial + quarentena); nada de auto-editar via agente.
- Padrão stateless (diff derivado do disco), reusar técnica de embeddings/pipelines de YouTube.
- SEM over-engineering: entregue só o DoD da sub-issue; nada de circuit-breaker/rotação/etapas extras
  que foram explicitamente descartados no épico.

## 3. Loop de execução
a) issue-start: `/issue-start <ISSUE_ALVO>` (claim + label agent:working + worktree isolado
   a partir de origin/main + brief de execução).
b) build: implemente SÓ o escopo atômico da sub-issue.
   - TDD nas funções puras; código em scripts/analyze-and-improve/ (greenfield).
   - Verificações externas incertas (endpoints/formatos) → PROVAR antes de codar
     (script de verificação rodando com a chave via secret/Action descartável, nunca colando chave no chat).
c) gates locais: rode os testes do pacote + `npm run validate:obsidian` (se tocar .md);
   compile o que precisa. Verde obrigatório.
d) issue-review: `/issue-review <ISSUE_ALVO>` — validação + review de 2º agente ADVERSARIAL
   (não rubber-stamp). Findings BLOCKING → corrija no worktree e repita. Só siga com review limpo.
e) issue-finish: `/issue-finish <ISSUE_ALVO>` — merge (squash, auto-merge, --delete-branch; NUNCA --admin)
   + fechar a issue. Confirme MERGED antes de seguir.

## 4. Housekeeping (obrigatório, no fim)
- Remover worktree isolado; `git remote prune origin`; branch local removida.
- `git pull --ff-only origin main` na cópia principal — SÓ se nenhuma sessão concorrente estiver
  usando o working tree principal (o `--ff-only` aborta em vez de sobrescrever; na dúvida, pule).
- Atualizar a memória do projeto com o que a etapa entregou/aprendeu.
- Confirmar: sem resíduo (worktrees/branches/arquivos temporários).

## 5. Ritual de fim-de-fase (OBRIGATÓRIO — não pular)
1) Atualizar o ÉPICO #257:
   - Marcar o checkbox da etapa concluída (`- [x]`).
   - Adicionar 1–3 linhas de "Aprendizados" abaixo da etapa (o que a execução revelou:
     surpresas, decisões, custos reais, calibrações — ex. o floor real, a nota do evaluator).
   - `gh issue edit 257 --body <novo corpo>` (releia o corpo atual antes de editar).
2) REVISITAR as etapas restantes (#259–#266):
   - Para cada uma ainda aberta, cheque se o que ESTA etapa revelou muda escopo/DoD/deps/premissas.
   - Se mudar, edite a sub-issue (`gh issue edit <N> --body ...`) com o ajuste + 1 linha do porquê.
   - Se algo novo emergiu (gap/risco), crie sub-issue nova e vincule ao épico
     (`gh api -X POST repos/pavani06/long-running-agents/issues/257/sub_issues -F sub_issue_id=<id>`
     — `<id>` é o id NUMÉRICO do banco, obtido com `gh issue view <N> --json id`, NÃO o número `#<N>`).
   - Se nada muda, registre explicitamente "revisão pós-Etapa X: nenhuma alteração nas restantes".

## 6. Parar e escalar (não force)
- Dep aberta, review com BLOCKING irrecuperável, ambiguidade de escopo, ou verificação externa
  que falha → PARE, reporte com evidência, e peça decisão. Não invente premissa nem amplie escopo.

## 7. Saída (report final)
- Etapa concluída + PR mergeado (link) + gates/review verdes.
- Épico atualizado (checkbox + aprendizados) e etapas restantes revisitadas (o que mudou, se mudou).
- Housekeeping confirmado. Próxima etapa executável = <a de menor número com deps fechadas>.
```

---

## Notas
- **Uma etapa por sessão**, em contexto limpo — o plano está externalizado (design doc + sub-issues
  auto-contidas), então cada sessão de execução não depende do histórico de planejamento.
- **Skills usadas:** `issue-start`, `issue-review`, `issue-finish` (ou `issue-executor-master` no modo autônomo).
- **Segurança:** worktree isolado sempre (há sessão concorrente no repo); nunca `--admin` no merge;
  nunca colar segredo no chat (verificação de endpoint via Action/secret descartável).
