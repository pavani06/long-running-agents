---
title: "ant apply: agentes como código"
type: "extract"
source: "x"
status_id: "2095651107645145538"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2095651107645145538"
created_at: "2026-09-03T23:12:14.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-we-ve-added-ant-apply-to-the-ant-cli-now-you-can-declare-cla--2095651107645145538.json]]"
tags: ["agent-tooling", "agents", "production", "process", "stack-tooling", "state"]
topic: "ant apply: agentes como código"
summary: "Anthropic adicionou `ant apply` ao CLI ant, permitindo declarar agents, environments, skills, memory stores e deployments como arquivos no repositório e sincronizá-los com a API do Claude via um plano aprovável e um lockfile (claude-lock.json). É essencialmente infrastructure-as-code para o ecossistema de agentes gerenciados da Anthropic, cobrindo fluxo local e CI."
key_points: ["Recursos são declarados como arquivos Markdown/YAML/JSON em diretórios convencionais (agents/, environments/, memory_stores/, deployments/, skills/); o frontmatter carrega a configuração (modelo, tools, schedule) e o corpo do texto vira o system prompt, descrição ou primeira mensagem.", "claude-lock.json registra os IDs dos recursos, a organização e o workspace; commitá-lo garante que execuções seguintes (locais ou em CI) atualizem os mesmos recursos em vez de criar duplicatas, e seus hashes detectam edições no arquivo ou mudanças fora dele.", "Recursos se referenciam por caminho relativo em vez de ID: ant apply cria tudo em ordem de dependência e preenche os IDs reais; skills também podem ser referenciadas por URL do GitHub, pinadas ao commit resolvido até rodar com --upgrade.", "Semântica de reconciliação: deletar um campo limpa o recurso (se a API permitir), deletar um arquivo mantém o recurso até --prune, mudanças feitas fora dos arquivos (ex.: no Console) bloqueiam o plano até --force, e recursos criados no Console/beta não são adotados automaticamente.", "Em CI: rodar `ant apply --yes .` no branch default pós-merge, `--dry-run` em PRs para revisores, commitar o lockfile mesmo após apply parcial, executar um apply por vez (não há lock) e autenticar via Workload Identity Federation — o comando recusa credenciais de outra org/workspace."]
entities: ["Anthropic", "ant CLI", "Claude", "claude-lock.json", "Claude Console", "GitHub Actions", "Workload Identity Federation"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://platform.claude.com/docs/en/cli-sdks-libraries/cli/apply"]
media: ["https://pbs.twimg.com/amplify_video_thumb/2095650094054068224/img/hvX6SIXBRvLUPici.jpg"]
relates-to: ["[[extracts/x/bookmarks/2026-09-12-claudedevs-also-see-our-open-source-reference-implementation-this-inclu--2095233747562180849|implementação de referência de agentes de comércio]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-read-the-full-announcement-https-t-co-cdudn3gvhd--2095233748719817153|Blueprint de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-two-fresh-updates-to-claude-managed-agents-first-we-ve-added--2098120133549895978|Session viewer no ant CLI]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-stanford-researchers-did-it-again-they-just-built-the-agent--2086079311279493389|versionamento agent-native de estado]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-our-ci-team-s-on-call-first-responder-is-claude-tag-it-reads--2097437571634639035|Agente Claude on-call para incidentes]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-re-open-sourcing-claude-commerce-agents-this-is-a-bluepri--2095233745167282602|agentes de comércio open-source]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-claude-code-can-design-now-the-new-design-skill-research-pre--2089471692762673408|Claude Code /design skill]]"]
---

# ant apply: agentes como código

**@ClaudeDevs** · [2095651107645145538](https://x.com/ClaudeDevs/status/2095651107645145538) · `announcement`

## Resumo
Anthropic adicionou `ant apply` ao CLI ant, permitindo declarar agents, environments, skills, memory stores e deployments como arquivos no repositório e sincronizá-los com a API do Claude via um plano aprovável e um lockfile (claude-lock.json). É essencialmente infrastructure-as-code para o ecossistema de agentes gerenciados da Anthropic, cobrindo fluxo local e CI.

## Pontos-chave
- Recursos são declarados como arquivos Markdown/YAML/JSON em diretórios convencionais (agents/, environments/, memory_stores/, deployments/, skills/); o frontmatter carrega a configuração (modelo, tools, schedule) e o corpo do texto vira o system prompt, descrição ou primeira mensagem.
- claude-lock.json registra os IDs dos recursos, a organização e o workspace; commitá-lo garante que execuções seguintes (locais ou em CI) atualizem os mesmos recursos em vez de criar duplicatas, e seus hashes detectam edições no arquivo ou mudanças fora dele.
- Recursos se referenciam por caminho relativo em vez de ID: ant apply cria tudo em ordem de dependência e preenche os IDs reais; skills também podem ser referenciadas por URL do GitHub, pinadas ao commit resolvido até rodar com --upgrade.
- Semântica de reconciliação: deletar um campo limpa o recurso (se a API permitir), deletar um arquivo mantém o recurso até --prune, mudanças feitas fora dos arquivos (ex.: no Console) bloqueiam o plano até --force, e recursos criados no Console/beta não são adotados automaticamente.
- Em CI: rodar `ant apply --yes .` no branch default pós-merge, `--dry-run` em PRs para revisores, commitar o lockfile mesmo após apply parcial, executar um apply por vez (não há lock) e autenticar via Workload Identity Federation — o comando recusa credenciais de outra org/workspace.

## Links
- https://platform.claude.com/docs/en/cli-sdks-libraries/cli/apply

## Entidades
Anthropic, ant CLI, Claude, claude-lock.json, Claude Console, GitHub Actions, Workload Identity Federation

> **Revisit:** `high` · **fonte:** `article`
