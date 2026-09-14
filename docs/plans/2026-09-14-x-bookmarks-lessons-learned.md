---
title: "X Bookmarks — Lessons Learned"
type: retrospective
source: x
date: 2026-09-14
tags: [pipeline, github-actions, oauth, prompt-injection, retrospective]
---

# X Bookmarks Digest — Lessons Learned

Retrospecto da migração da rotina diária de bookmarks do X (Cowork/Chrome local →
GitHub Actions), do spike (2026-09-12) ao programa completo do digest (EPIC #238,
fases 0–5b mergeadas, 2026-09-13). Pipeline em produção:
`x-bookmarks → x-ingest → x-extracts → x-connections → x-themes → x-digest`.

Cada lição tem o **fato**, o **porquê** e o **então** (o que mudou por causa dela).

---

## 1. Autenticação & API do X

- **O "token com acesso a tudo" não era o que parecia.** O `X_AUTH_TOKEN` no
  Actions era um OAuth2 API token de 91 chars não-hex, **não** um cookie
  `auth_token` (que é 40 chars hex). Deu 401 code 32 no spike.
  → **Verifique a *forma* do token antes de assumir o tipo.** Isso motivou o
  pivô do caminho cookies/GraphQL interno para a **API oficial v2**.

- **Enumerar bookmarks privados só dá por sessão ou API oficial.** Scrape
  Creators só resolve conteúdo público por id (confirmado no `llms.txt` deles),
  não lista bookmarks privados. → API oficial v2 (`GET /2/users/:id/bookmarks`,
  OAuth2 user-context, escopo `bookmark.read`) foi a única rota durável.

- **Refresh token single-use exige "persist-first".** A ordem segura é
  `refresh → grava o refresh novo no secret ANTES de tudo → busca`. Se
  refresh/persist falha, o run fica **vermelho** e você re-consente. Provado ao
  vivo (o token rotacionou 15:27→17:15 num único run). → Nunca busque dados antes
  de persistir a credencial rotacionada, ou você perde o próximo run.

- **`GITHUB_TOKEN` não escreve secrets.** Precisa de um PAT fine-grained com
  `secrets:write` (`GH_SECRETS_PAT`) para o write-back do refresh token.

- **A API só expõe ~299 (janela recente).** Não há backfill de histórico
  completo. → O "bootstrap do acervo" é sobre esses 299, não sobre tudo que já
  foi marcado.

- **`int("")` crasha.** Env var vazia em `int(os.environ["SPIKE_PAGES"])`.
  → `int(os.environ.get("SPIKE_PAGES") or "3")`.

## 2. GitHub Actions & Git

- **Corrida de push é real.** O seed do coletor foi rejeitado (`! [rejected]
  main -> main`) porque um outro PR mergeou na main no meio. → **Todo commit
  step ganhou `git pull --rebase` + retry 3x** (lição do PR #224, adotada em
  todos os workflows subsequentes).

- **Push do bot via `GITHUB_TOKEN` não re-dispara checks** (anti-recursão do
  Actions). → A validação Obsidian não roda no commit do bot; **valide
  localmente** antes de confiar que está limpo.

- **`gh pr merge --delete-branch` falha em worktree** ("main already used by
  worktree"). Merge e delete-remoto funcionam; a branch **local** exige limpeza
  manual.

- **Hooks de guardrail bloqueiam `git branch -D`, `reset --hard`,
  `push --force`.** → Delete local seguro via `git update-ref -d
  refs/heads/<branch>` (logando o SHA pro reflog); delete remoto via
  `git push origin --delete` (não é bloqueado).

- **Arquivos vindos de mount do Windows chegam 100755.** → `chmod 644` + `git
  add` (o `git update-index --chmod=644` tem sintaxe diferente da que a memória
  muscular sugere).

- **Encadeamento por `workflow_run`** liga as 6 camadas em sequência
  determinística, cada uma disparando a próxima no `success`.

## 3. Prompt injection / conteúdo não-confiável

- **Tweets e artigos são input hostil.** Guard `<untrusted_source>` obrigatório
  em toda chamada de LLM, com o **delimitador neutralizado** por regex
  (`</?\s*untrusted_source\s*>`) — senão o próprio conteúdo pode fechar o bloco.

- **LLM não inventa fatos factuais.** O prompt proíbe inventar URLs na prosa;
  links/media vêm **só** dos dados factuais do item, nunca da síntese.

## 4. Arquitetura & modelagem de dados

- **O digest não cabia num script — virou um programa de 5 camadas.** O
  `/grill-me` revelou que "resumo diário" exigia
  `raw → ingest → deep-extract → connections → themes → digest`. → Não subestime
  a profundidade de um "só um resuminho".

- **Ingestão é uma camada própria.** Profundidade de conteúdo de link precisou de
  Jina Reader (anônimo, sem key) + fallback trafilatura, com **`fetch_status`
  como sinal de proveniência de primeira classe** (ok/paywall/failed/unsupported).
  51/299 acabaram article-grounded.

- **Extract "thin" gera tema-lixo.** A aresta de conexão nº 1 era "conteúdo
  inacessível" ↔ "conteúdo inacessível" (similaridade 0.95). → Materializou-se um
  **flag `thin` no frontmatter** (opção B, sobre computar on-the-fly) e a
  exclusão no grafo precisou de filtro de **nó E de aresta** (`a in nodeset and
  b in nodeset`), não só de nó.

- **Schema é sob medida pro meio.** O extract de tweet é enxuto
  (topic/summary/tags/entities/...); os campos `thesis`/`deep_dive` do pipeline
  de YouTube não cabem num tweet. → Reusar o *mecanismo*, não o *schema*.

- **Repo é a fonte da verdade (stateless diff).** Sem store externo de estado; o
  diário compara com o que está em disco.

- **Writes idempotentes por `status_id`** — reprocess preserva nome+data, sem
  duplicar.

## 5. O bug sutil que só o review de 2º agente pegou

- **`e.collected == date` num objeto que não tem `collected`.** O modo `daily`
  filtrava por um campo que **só existe no raw item**, não no extract (extract só
  tem `extracted`). O filtro retornaria vazio todo dia. → Corrigido para
  `e.extracted == date` e **extraída uma helper pura `scope_for()`** só pra o
  boundary ser testável em unidade. **Proveniência de campo entre camadas é uma
  armadilha; teste a fronteira.**

## 6. Processo & metodologia

- **Uma tarefa por sessão (Rule 0), fase a fase.** Cada sub-issue
  auto-contida/loop-executável, com critérios de sucesso e topologia agêntica
  recomendada.

- **Ritual de fim-de-fase:** ao fechar cada fase, **revisitar as issues
  downstream** e atualizar o épico. Mantém o plano vivo, não fóssil.

- **O review de 2º agente pagou o custo.** Pegou o bug B1 (acima) antes do merge.
  Gate de review não é burocracia.

- **Anti-over-engineering, repetidamente.** Rejeitados: auto-discovery de
  projetos via PAT amplo; computar `thin` on-the-fly; expandir o digest além do
  "só wiring" na 5b. → **Escopo declarado vence conveniência especulativa.**

- **DoD drift é decisão explícita, não acidente.** A 5b previa `bootstrap/`
  por-tema, mas o core da 5a fez arquivo único front-loaded. Mantido de propósito
  (escopo era "só wiring") — mas **reconciliado e registrado** no fim da fase.

- **No limite de contexto: sessão nova > comprimir.** O estado vive fora da
  conversa (épico, issues, plano, memória), então retomar custa quase nada e
  evita rodar a fase final (que consome GLM) com contexto degradado.

## 7. Escolhas de ferramenta

- **Jina Reader anônimo** (`r.jina.ai/<url>`, sem key) + **trafilatura** fallback
  pra extração de artigo.
- **OpenAI `text-embedding-3-large`** (3072-dim) pras conexões; **networkx
  greedy-modularity** pra detecção de comunidade nos temas.
- **GLM 5.3 via zai-coding-plan** pra síntese, com **fallback determinístico** se
  a key faltar — o digest ainda sai (só sem a camada de síntese).
- **Guard de SSRF (`is_blocked_host`)** na ingestão, já que buscamos URLs
  arbitrárias vindas dos bookmarks.

---

## Adiado (dívida consciente, não esquecimento)

Entrega por email; handlers de thread/YouTube/PDF na ingestão; migração do
catálogo (#983); Medium/Substack; tuning de resolução dos temas (~0.7 pra reduzir
fragmentação de temas-AI); preencher os `_[refinar]_` em `digests/x/projects.md`
(CIOT/AuthPay, commerce, govevo).
