# raw/x/bookmarks

Camada **raw** dos bookmarks do X (owner: @fepavani). Coleta diária, versionada,
sem depender de máquina local — alimenta o modelo raw → (futuro) extrato → digest.

## Conteúdo
- `items/<YYYY-MM-DD>-<handle>-<slug>--<status_id>.json` — 1 arquivo por bookmark,
  com o tweet como a API devolve (`text`, `handle`, `created_at`, `url`). A data é a
  **data de coleta** (America/Sao_Paulo); o `<status_id>` numérico é a chave estável do diff.
- `index.json` — regenerado do disco a cada run: `status_id`, `handle`, `url`, `file`.

## Como é atualizado
Rotina diária em **GitHub Actions** (`.github/workflows/x-bookmarks.yml`):

- **Coleta:** API oficial do X v2, `GET /2/users/:id/bookmarks` (OAuth2 user-context,
  escopo `bookmark.read`), paginada por `next_token`.
- **Auth:** o access token dura ~2h, então cada run troca o **refresh token** por um
  access novo. O refresh do X é **single-use e rotativo**: o run **grava o refresh novo
  de volta** no secret `X_REFRESH_TOKEN` (via `gh`, com o PAT `GH_SECRETS_PAT`) **antes**
  de qualquer outra coisa.
- **Diff stateless:** o repositório é a fonte de verdade — novos = bookmarks da API
  menos o que já está em `items/`.
- **Commit:** só esta pasta, como `github-actions[bot]`.

### Agendamento
- Diário `45 8 * * *` UTC (05:45 SP), depois do `youtube-transcripts`.
- `workflow_dispatch` → modos `daily` / `dry-run` (dry-run: coleta e faz o diff, não grava).

### Comportamento
- **Vermelho** (email nativo do GitHub): refresh falhou (re-consentir), refresh rotacionado
  mas não persistido (token stale → re-consentir), ou falha de auth na busca (401/403).
- 429: interrompe mas fica **verde**, o resto fica pro próximo run.

> **Limite conhecido:** a API oficial expõe só uma **janela recente** de bookmarks
> (~centenas), não o histórico completo. Suficiente para a coleta diária adiante;
> backfill do histórico antigo não é possível por esta via.

## Secrets (repo → Settings → Secrets → Actions)
- `X_CLIENT_ID`, `X_CLIENT_KEY` — client id / secret do app OAuth2 (confidential).
- `X_REFRESH_TOKEN` — refresh token (rotacionado em cada run).
- `GH_SECRETS_PAT` — PAT fine-grained (este repo, Secrets: read/write) para o write-back.

## Código
`scripts/x-bookmarks/` (`pipeline.py` + `oauth.py` / `bookmarks.py` / `store.py` / `naming.py`).
Testes de funções puras (sem rede) em `tests/unit/x_bookmarks_test.py`:

```bash
python3 tests/unit/x_bookmarks_test.py
```
