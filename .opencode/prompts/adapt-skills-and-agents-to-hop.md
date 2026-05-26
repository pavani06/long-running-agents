# Prompt: Adaptar skills + AGENTS.md do projeto neonet para o HoP

**TASK**: Ler os documentos canonicos do projeto HoP, entender a estrutura real do projeto, e fazer dois ajustes:

1. Reescrever as 4 skills em `.opencode/skills/` removendo referencias ao projeto neonet (NestJS compliance agent).
2. Reescrever o `AGENTS.md` do HoP incorporando as regras uteis do neonet, adaptadas ao contexto HoP.

**EXPECTED OUTCOME**:

- 4 skills reescritas e funcionais para HoP:
  - `.opencode/skills/issue-start/SKILL.md`
  - `.opencode/skills/issue-finish/SKILL.md`
  - `.opencode/skills/issue-review/SKILL.md`
  - `.opencode/skills/orchestrator/SKILL.md`
- `/HoP/AGENTS.md` atualizado: mantem as 4 regras de engenharia existentes e adiciona regras de workflow adaptadas.
- Nenhuma referencia restante a NestJS, Prisma, `just`, `Compliance Docs/`, `develop`, `DESIGN-PHASE*.md`, modulos neonet, ou tracks A-F.

**REQUIRED TOOLS**: Read, Edit, Write, Bash. Use Bash somente para comandos leves de descoberta, como `git log --oneline -15`, `git branch -a`, `ls`, e leitura de scripts do `package.json`.

---

## MUST DO — Leitura obrigatoria antes de editar

Leia em paralelo:

- `/HoP/AGENTS.md` — as 4 regras atuais, que sao a base a preservar.
- `/HoP/agents/manifest.yaml` — sistema de agentes e orquestrador Rezek.
- `/HoP/docs/system-of-record.md` — precedencia documental.
- `/HoP/.github/PULL_REQUEST_TEMPLATE.md` — formato real do PR, em PT-BR.
- `/HoP/package.json` scripts section — comandos npm disponiveis.
- `/HoP/README.md` — estrutura da repo e fronteira tecnica.
- `git log --oneline -15` — padrao real de commits.
- `git branch -a` — padrao real de branches.
- `/HoP/DESIGN.md` — design system vigente.

---

## PARTE 1 — Adaptar as 4 skills

### Substituicoes obrigatorias em todas as skills

| Nas skills neonet | Substituir por HoP |
|---|---|
| Branch base `develop` | `main` |
| Branch naming `feat/scanner-desc` | `issue/<N>-<slug>` |
| `git worktree add ... origin/develop` | `git worktree add ... origin/main` |
| `just validate` / `justfile` | `npm run test:regression:mock` e outros scripts npm reais |
| `Compliance Docs/agents/start-here.md` | `AGENTS.md`, `agents/manifest.yaml`, `docs/system-of-record.md` |
| `Compliance Docs/agents/repo-map.md` | `README.md`, secao de estrutura da repo |
| `Compliance Docs/agents/execution-brief-template.md` | Template simples inline na skill |
| `docs/briefs/` | `docs/analysis/` ou criar `docs/briefs/` somente se decidido explicitamente |
| `DESIGN-PHASE1.md` / `DESIGN-PHASE2.md` | `DESIGN.md` |
| Skills `nestjs-review`, `test-coverage` | Remover — nao existem no HoP |
| Review criteria NestJS, Zod, thin controllers, Finding | Criterios HoP: Node.js scripts, Next.js 15 dashboard, multi-tenant paths |
| Tracks A-F / Rule 13 neonet | Remover completamente |
| Modulos `scanner/`, `evaluator/`, `policy/`, `checks/` | Areas HoP: `src/lib/`, `src/runner/`, `src/evaluator/`, `src/persistence/`, `scripts/`, `packages/dashboard/`, `tests/` |
| `AGENTS.md Rule N` neonet | Regras reais do AGENTS.md HoP adaptado |
| `prisma/schema.prisma` | Remover — nao existe no HoP |
| `src/config/env.schema.ts` | `.env.example` + README, conforme padrao HoP |
| PR template neonet | PR template HoP: Resumo, Mudancas, Testes, Crossroad-file impact |

### `issue-review` — Step 2: validacao

Substituir `just validate` por comandos HoP reais:

```bash
npm run test:regression:mock
npm run ops:preflight
```

Documentar que `npm run smoke:live` requer runtime live e nao deve ser tratado como gate local obrigatorio para qualquer PR.

### `issue-review` — Step 5: review subagent

O subagente deve avaliar codigo HoP, nao codigo NestJS. O prompt de review deve cobrir:

- Node.js scripts em `scripts/`.
- Bibliotecas em `src/lib/`, `src/clients/`, `src/config/`, `src/persistence/`.
- Dashboard Next.js 15 em `packages/dashboard/`.
- Testes em `tests/`.
- Multi-tenant isolation: escritas em `.runtime/` e `artifacts/` devem respeitar `HOP_TENANT_ID`.
- Crossroad files:
  - `src/lib/safe-console.js`
  - `src/lib/logger.js`
  - `src/lib/redaction.js`
  - `src/persistence/supabase-client.js`
  - `tests/helpers/supabase-mock.js`

Mudancas em crossroad files exigem nota de migracao, listagem de importers afetados, e aprovacao de code-owner conforme `.github/CODEOWNERS` e `.github/PULL_REQUEST_TEMPLATE.md`.

### `orchestrator` — Phase 2

Remover o sistema de tracks A-F e referencias a `AGENTS.md Rule 13`. Substituir por:

- Sugerir proxima issue sem `agent:working` e sem `blocked`.
- Priorizar por label se labels de prioridade existirem no repo.
- Se nao houver labels de prioridade claras, priorizar issue aberta de menor numero.
- Verificar com `gh label list` antes de citar labels como `phase-1` ou `phase-2`.

### Manter nas skills

Preservar o que ja e util:

- Claim de issue via GitHub.
- Label `agent:working`.
- Uso de worktree.
- Criação de PR draft.
- Review antes de merge.
- Confirmacao explicita do usuario antes de merge.
- Squash merge.
- Cleanup de worktree, branch e label.
- Gates de `/compact`.

---

## PARTE 2 — Adaptar o AGENTS.md

O `AGENTS.md` atual do HoP tem 4 regras de engenharia. O AGENTS.md do neonet tem 19 regras detalhadas de workflow. A tarefa e incorporar as regras uteis do neonet adaptadas ao HoP, sem perder as 4 regras atuais.

### Mapeamento de regras neonet

| Regra neonet | Acao | Como adaptar |
|---|---|---|
| Rule 0: Single-task per session | Manter | Universal. Uma sessao, uma tarefa. |
| Rule 1: Branches | Adaptar | Usar `main`, nao `develop`; branch `issue/<N>-<slug>`. |
| Rule 2: Track em issues | Manter | Todo trabalho deve estar ligado a uma GitHub issue. Ajustar labels ao repo. |
| Rule 3: Testes + docs + review | Adaptar | Exigir testes/doc quando aplicavel; sem JSDoc obrigatorio universal. |
| Rule 4: Commit format | Adaptar | `type(scope): desc (#PR)` e `[FUP-N] type(scope): desc (#PR)` para follow-ups. |
| Rule 5: Module ownership | Adaptar | Substituir modulos NestJS por fronteiras HoP e crossroad files. |
| Rule 6: PR gates | Adaptar | Usar npm scripts reais; remover `just`, Prisma e coverage por modulos neonet. |
| Rule 7: Prisma | Descartar | Nao existe no HoP. |
| Rule 8: Dependency management | Manter | Dependencias novas devem ter justificativa e PR separado quando possivel. |
| Rule 9: Error escalation | Manter | Depois de 3 tentativas, consultar Oracle; se nao resolver, bloquear e documentar. |
| Rule 10: Security | Adaptar | Sem segredos, sem force push, sem type suppressions; adicionar tenant isolation. |
| Rule 11: Code standards | Adaptar | Remover NestJS/Zod/DI; usar padroes HoP: Node >= 20, ESLint, pino, config central. |
| Rule 12: Documentation | Adaptar | Usar `docs/system-of-record.md`, `docs/canonical/`, `docs/decisions/`, `docs/evidence/`, `DESIGN.md`. |
| Rule 13: Tracks A-F | Descartar | Nao existe no HoP. |
| Rule 14: Search before code | Adaptar | Sem Obsidian; ler docs HoP e buscar padroes no repo. |
| Rule 15: Agent review protocol | Adaptar | Sem `nestjs-review`; usar review subagent com criterios HoP. |
| Rules 16-19 | Preservar | Sao equivalentes as 4 regras atuais do HoP. Nao duplicar sem necessidade. |

### Regras HoP-specific que devem entrar

Adicionar regras que refletem o que e unico no HoP:

1. **Multi-tenant isolation**: qualquer operacao que escreve em `.runtime/` ou `artifacts/` deve respeitar `HOP_TENANT_ID`. Nunca usar paths bare sem considerar isolamento de tenant.
2. **Crossroad files**: arquivos compartilhados de alto impacto exigem nota de migracao, impacto em consumidores e aprovacao de code-owner.
3. **Document precedence**: em conflito documental, seguir `docs/system-of-record.md`: ADR aceito > docs canonical > evidence > analysis > archive > README.
4. **ADR discipline**: nao contradizer ADRs aceitos em `docs/decisions/` sem levantar explicitamente o conflito.
5. **Design discipline**: mudancas visuais no dashboard devem seguir `DESIGN.md`.

### Formato desejado do AGENTS.md final

O novo `AGENTS.md` deve:

- Ser escrito em ingles.
- Numerar regras claramente: `Rule 0`, `Rule 1`, etc.
- Ser conciso, com exemplos curtos.
- Manter o tom direto do neonet: regras obrigatorias para agentes.
- Ter secao **Project Context** com stack real: Node >= 20, ESLint, Supabase, pino, Next.js 15 dashboard.
- Nao referenciar NestJS, Prisma, `just`, `develop`, `DESIGN-PHASE*.md`, `Compliance Docs/`, Obsidian, ou tracks A-F.

---

## MUST NOT DO

- Nao inventar comandos npm que nao existem no `package.json`.
- Nao criar arquivos fora de `.opencode/skills/` e `AGENTS.md`.
- Nao alterar `agents/manifest.yaml`, docs canonicos, ADRs, ou `docs/system-of-record.md`.
- Nao remover os gates de `/compact` nas skills.
- Nao adicionar referencias a frameworks ausentes, como NestJS, Prisma, Jest, ou `just`.
- Nao duplicar mecanicamente as 4 regras atuais do HoP; incorpora-las de forma coerente.
- Nao forcar JSDoc universal sem verificar o estilo real do projeto.
- Nao alterar paths em `.runtime/` ou `artifacts/` sem considerar tenant isolation.

---

## CONTEXT

- Projeto: HoP — Control Tower do KODA, agente WhatsApp.
- Stack: Node.js >= 20, ESLint, Supabase (`@supabase/supabase-js`), pino logging, Next.js 15 em `packages/dashboard/`.
- Branch padrao: `main`.
- Branch naming observado: `issue/<N>-<slug>`.
- Commit format observado: `type(scope): desc (#PR)`, `[FUP-N] type(scope): desc (#PR)`, `docs(planning): post-merge integrity update for #N`.
- CI: GitHub Actions em `.github/workflows/`, incluindo `lint.yml`, `pr-regression.yml`, `crossroad-file-gate.yml`, `design-gate.yml`.
- Testes: `npm run test:regression:mock`, `npm run smoke:live`, `npm run ops:preflight`.
- PR template: `.github/PULL_REQUEST_TEMPLATE.md` com seções Resumo, Mudancas, Testes, Crossroad-file impact.
- Docs canonicos: `docs/canonical/`.
- ADRs: `docs/decisions/`.
- Design system: `DESIGN.md`.
- Agente orquestrador: Rezek via `agents/manifest.yaml`.
- Skills: `.opencode/skills/<nome>/SKILL.md`.
- Crossroad files: `src/lib/safe-console.js`, `src/lib/logger.js`, `src/lib/redaction.js`, `src/persistence/supabase-client.js`, `tests/helpers/supabase-mock.js`.
- Multi-tenant: `.runtime/` e `artifacts/` sao namespaced por `HOP_TENANT_ID`.
- Modulos em `src/`: `assertions`, `classification`, `clients`, `config`, `evaluator`, `extraction`, `generator`, `lib`, `loop`, `observability`, `orchestration`, `persistence`, `promotion`, `reporter`, `runner`.
- Fonte original das skills e do AGENTS.md: projeto `neonet.ai-agents.compliance` com NestJS, Prisma, `just`, `Compliance Docs/`.
