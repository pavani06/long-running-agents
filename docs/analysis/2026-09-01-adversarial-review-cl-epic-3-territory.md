---
title: "Adversarial review CL-EPIC 3: lifecycle unificado vs territorio"
type: analysis
date: 2026-09-01
tags: ["agentes-orquestracao", "governanca", "harness-engineering", "evals"]
aliases: ["plan territory check epic 208", "review adversarial epic 208", "territorio CL-EPIC 3"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[docs/decisions/2026-09-01-vault-federation-consultable-registry|ADR Vault Federation]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/alarm-clock-agent-lifecycle|Alarm Clock Agent Lifecycle]]"]
sources: ["pavani06/long-running-agents issues #208, #209, #210, #211", "Exploração do território em /home/pavanpavan/long-running-agents (2026-09-01)"]
---

# Adversarial review CL-EPIC 3: lifecycle unificado vs territorio

Diagnóstico `plan-territory-check` do epic #208 (CL-EPIC 3: lifecycle de issues unificado + `agent-lifecycle.md` + estreia de `docs/evidence/`) contra o estado real do repositório em 2026-09-01. Método: leitura direta de cada arquivo citado nos corpos de #208/#209/#210/#211, varredura exaustiva de labels e convenções de worktree em todo o repo, e inspeção do estado GitHub (labels, issues abertas, worktrees). Não modifica código; as emendas sugeridas são para os corpos das issues.

## Veredito

O epic está bem alicerçado: todas as citações verificáveis dos corpos das issues batem com o disco. Foi encontrado 1 gap P1 que bloqueia execução limpa de #211 (arquivo-fonte do incidente não está no repo) e 4 achados menores. A decisão de unificar em `agent:working` é validada pelo território.

## Claims do epic confirmados contra o território

| Claim | Evidência verificada |
|---|---|
| `issue-start` usa `agent:working` + worktree `.worktrees/<N>-<slug>` | `.opencode/skills/issue-start/SKILL.md:44,49-50,72,188` |
| `issue-workflow` usa `in-progress` | `.opencode/skills/issue-workflow/SKILL.md:15,29,102-103,198,210,226,237` (7 ocorrências, todas neste arquivo) |
| [[docs/system-of-record\|System of Record]] marca `agent-lifecycle.md` pendente | `docs/system-of-record.md:71` e `:354` |
| `docs/evidence/` vazio | `ls docs/evidence/`: apenas `.gitkeep` |
| Precedência (evidence = nível 3) e flywheel no SOR | `docs/system-of-record.md:14-21` e `:207` |
| Peça faltante nº 1 do canonical | `docs/canonical/closed-loop-agent-operating-system.md:65` ("A single canonical closed-loop OS model") e `:61` (Partial Coverage) |
| Flywheel: 9 passos e taxonomia de falhas | `docs/canonical/production-failure-regression-flywheel.md:30-40` e `:42-53` |
| Gates existem | `package.json:9` (`lint`), `:11` (`test:unit`); `scripts/validate-obsidian.ts` existe e passa limpo |
| Sub-issues consistentes | #209/#210/#211 existem; dependência 209→210 declarada nos dois lados; ondas corretas; labels `epic`+`qi-loop` presentes |

## Validação da decisão REC-105 (unificar em `agent:working`)

O label `agent:working` é consumido por `.opencode/skills/orchestrator/SKILL.md:49,57,134-197` (detecção de issues ativas no dashboard e cleanup) e liberado por `.opencode/skills/issue-finish/SKILL.md:14,150,153,166,190`. Já é norma do repositório em `AGENTS.md:57` (Rule 5). `in-progress` tem zero consumidores fora de `issue-workflow`; o label não existe no GitHub (`gh label list` retorna só `agent:working`) e nenhuma issue aberta o usa. Superfície real da migração: 1 arquivo, 7 linhas. `.worktrees/**` já está excluído do lint (`eslint.config.js:24`).

## Findings

### F-A1 (P1, bloqueia #211): arquivo-fonte do incidente não está no repo

A citação `docs/analysis/2026-09-01-adversarial-review-issue-195-execution.md:25` no corpo de #211 aponta para arquivo inexistente no repositório. Verificado: ausente em `docs/analysis/` na main, ausente no worktree `195-hygiene-validator`, `git log --all --diff-filter=A` vazio para o padrão. O arquivo existe fora do repo, no vault de runtime: `~/sisyphus-runtime/docs/analysis/2026-09-01-adversarial-review-issue-195-execution.md` (a linha ~25 contém exatamente a alegação de telemetria cega: `0 task_calls`, `agent/repo NULL`, sem correlação pai-filho — incidente real e evidenciado).

Consequência: o executor de #211 bate em file-not-found e o aceite "sem campo inventado" fica em risco de violação. A issue também não define o que fazer quando a analysis vive fora do repo: o caso de evidence precisa de referência resolvível, e wikilink para arquivo inexistente quebra o grafo.

Emenda sugerida à task 1 de #211: substituir o path pela localização real e definir o destino da analysis — (a) importá-la para `docs/analysis/` com frontmatter conforme Rule 16, ou (b) referenciar o vault externo em `sources` do caso.

### F-A2 (P2, #211): classe de falha não encaixa na taxonomia do flywheel

A classe escolhida, "Latency or cost regression", é definida em `docs/canonical/production-failure-regression-flywheel.md:51` como "Correct behavior became too slow or expensive". Telemetria quebrada não é comportamento lento nem caro: é gap de medição. Nenhuma das 8 classes da taxonomia (`:42-53`) cobre observabilidade.

Emenda sugerida à task 2 de #211: instruir uso da classe mais próxima com a divergência documentada no próprio caso (o handoff de #211 já pede registrar "a primeira divergência entre flywheel teórico e prática" — este é exatamente o caso), ou registrar a classe faltante como observação para o canonical sem editá-lo neste ciclo.

### F-A3 (P3, narrativa do epic): "duas mecânicas" subestima a superfície

O lifecycle tem 5 componentes operacionais: `issue-start`, `issue-workflow`, `issue-review`, `issue-finish` e `orchestrator`. A task 1 de #210 já lista os cinco como leitura obrigatória, mas a narrativa do epic pode induzir o executor a migrar só os 2 arquivos de claim e deixar o canonical curto.

### F-A4 (P3, #210): tabela de pendências do SOR está stale em outras linhas

`docs/system-of-record.md:352-358` lista `obsidian-document-conventions.md` como pendente, mas o arquivo já existe e está ativo em `:216`. Ao atualizar, restringir a edição à linha de `agent-lifecycle.md` (`:354`) ou declarar a limpeza das demais linhas como subtarefa explícita.

### F-A5 (P3, #210): desambiguação com alarm-clock-agent-lifecycle

[[docs/canonical/alarm-clock-agent-lifecycle|Alarm Clock Agent Lifecycle]] (Kavak: ciclo wake→work→sleep de frota) já ocupa o tema "agent lifecycle" com outro significado. O novo canonical deve usar aliases que não colidam e incluir `relates-to` apontando para ele.

### F-A6 (P3, positivo, #209): task 4 é no-op pré-verificado

Estado do GitHub em 2026-09-01: o label `in-progress` não existe no repo e zero issues abertas o usam. A task 4 de #209 pode ser resolvida no claim com "zero existentes, documentado". A migração real se limita a `.opencode/skills/issue-workflow/SKILL.md`.

## Recomendações

1. Emendar #211: corrigir o path do incidente (F-A1) e instruir classe taxonômica com divergência documentada (F-A2).
2. Emendar #210: explicitar cobertura dos 5 componentes (F-A3); escopo restrito na linha `:354` do SOR (F-A4); desambiguação com alarm-clock (F-A5).
3. Emendar #209: pré-documentar "zero issues com `in-progress`" no claim (F-A6).

## Re-verificação 2026-09-02 (pós-mudanças no território)

Re-execução da verificação após 7 commits novos na main (`12dbc37..48c5d45`) e após as sessões de execução de epics de 2026-09-01/02. Corpo original acima preservado como registro datado; esta seção é a emenda.

### Premissa corrigida: CL-EPIC 3 NÃO foi executado

As duas sessões apontadas como execução de epic (`ses_fa17ac78fffebetCGAqh9a3A1d`, `ses_fa0b158aeffePJlo4B4nsc1tuJ`) executaram outros trabalhos: a primeira migrancou `@pavani/obsidian-eval` → `@pavani_org/obsidian-eval ^0.3.0` em 6 repos (commit `48c5d45` neste repo); a segunda executou o epic #53 do vault `sisyphus-runtime`. As issues #209, #210 e #211 permanecem **abertas** e o território das três frentes está intacto:

- CL3-1: `grep -rn "in-progress" .opencode/skills/` retorna as mesmas 8 linhas de `.opencode/skills/issue-workflow/SKILL.md`.
- CL3-2: `docs/canonical/agent-lifecycle.md` continua NOT_FOUND.
- CL3-3: `docs/evidence/` continua só com `.gitkeep`.

Todos os findings F-A1 a F-A6 foram re-verificados e **permanecem válidos** (F-A6 re-confirmado: label `in-progress` não existe no GitHub; zero issues com ele em qualquer estado).

### Delta de território que afeta este diagnóstico

1. **Novo ADR aceito (nível 1 da precedência):** [[docs/decisions/2026-09-01-vault-federation-consultable-registry|ADR Vault Federation]] estabelece registro consultável de vaults federados e sintaxe sancionada de referência cross-vault com prefixo `vault:<nome>/<path>` (usada no próprio `relates-to` do ADR, que valida limpo). Isso **fortalece a opção (b) do F-A1**: referenciar a analysis do runtime como `vault:sisyphus-runtime/docs/analysis/2026-09-01-adversarial-review-issue-195-execution.md` passou a ser mecanismo formal do repo, não improviso. O fato durável "fonte de verdade = home Linux" do ADR também legitima o arquivo em `/home/pavanpavan/sisyphus-runtime/` como cópia autoritativa.
2. **Validador migrado de pacote:** `scripts/validate-obsidian.ts` mudou apenas o import (`@pavani` → `@pavani_org`, commit `48c5d45`); comportamento idêntico. O repo ganhou o gate canônico `npm run validate:obsidian` (`package.json:13`). As citações `npx tsx scripts/validate-obsidian.ts` em #210/#211 continuam funcionando, mas a forma npm script é a alinhada com a Rule 7 (gates reais do `package.json`).
3. **Nova ocorrência da classe de falha do incidente de #211:** a sessão de 2026-09-02 do vault runtime registrou segunda falha de telemetria da mesma classe (collector estoura `NOT NULL constraint failed: sessions.started_at` no merge com transcript de export SQL; bypass `--no-collect` aplicado; registro no handoff `~/sisyphus-runtime/sessions/runtime/2026-09-02-121647-sisyphus-handoff.md`). Para o executor de #211: o passo 5 do flywheel (dedupe/cobertura) recomenda registrar isso como recorrência no mesmo caso, não como caso novo.
4. **Validador re-executado:** limpo, 445 notas (440 na revisão original; delta = ADR, este documento e análises novas).

### Emendas recomendadas aos corpos das issues

- #211/F-A1: opção (b) agora tem sintaxe sancionada pelo ADR (`vault:` prefixo); opção (a) permanece válida se o objetivo for trazer a analysis para dentro do vault versionado.
- #210 e #211: substituir `npx tsx scripts/validate-obsidian.ts` por `npm run validate:obsidian` (Rule 7).

## Ressalva de rastreabilidade

A "revisão adversarial closed-loop-agent-operating-system (2026-09-01)" citada como origem do epic, e os IDs REC-105/106/107 e F7/F8/F9, não correspondem a nenhum artefato dentro do repo. Não bloqueia (o epic é auto-contido), mas os IDs de findings são inrastreáveis internamente.
