---
title: "From coding to Knowledge work agents — Karan Vaidya, Composio"
type: "extract"
source: "youtube"
video_id: "xxfMT-bPEmU"
url: "https://www.youtube.com/watch?v=xxfMT-bPEmU"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU.txt]]"
tags: ["harness", "context-engineering", "memory-architecture", "governanca", "permissions", "verification", "evals", "gate-design", "error-handling", "observability", "agent-tooling", "agents", "arquitetura", "knowledge-management", "production"]
thesis: "Agentes de coding são autônomos não por causa dos modelos, mas porque a infraestrutura ao redor do código já fornecia seis primitivas — centralização, história/registro, contexto, verificação, governança e reversibilidade — que não existem no knowledge work, e construir essa infraestrutura é o novo gargalo a ser resolvido."
concepts: ["seis primitivas para agentes (centralização, registro, contexto, verificação, governança, reversibilidade)", "fonte única de verdade equivalente ao repo para knowledge work", "record of work: log de toda ação do agente como memória e auditoria", "destilação de skills a partir de padrões de logs em três níveis (ferramenta, empresa, pessoal)", "dois tipos de contexto: shape (arquitetura/mapa) e style (o que é 'bom' na empresa)", "verificação pré-ação via sandboxes que mockam ferramentas reais", "governança determinística fora do prompt vs. instrução frágil (compaction, loopholes)", "políticas em linguagem natural restringindo comportamento dentro do acesso concedido", "gate múltiplo dimensionado ao blast radius", "reversibilidade: undo pós-fato (código) vs. captura pré-fato (knowledge work)", "confiança after-the-fact vs. before-the-fact e irreversibilidade de falhas"]
tools: ["Composio", "Claude Code", "Codex", "Cursor", "Git", "Salesforce", "Notion", "Gmail", "Slack", "Zendesk", "PostHog", "OpenClaw", "TypeScript", "CI/CD", "preview deployments", "bugbot / review skills"]
people: ["Karan Vya (cofundador e CTO da Composio)", "Composio", "Meta Super Intelligence Lab (diretora de alignment, incidente dos 200 e-mails)"]
claims: ["O gargalo dos agentes migrou dos modelos para a infraestrutura: o mesmo modelo que codifica pode fazer vendas/support/finanças, mas opera 'cego' sem história, contexto, verificação, guardrails ou undo.", "Centralize apps, conexões e logins num único lugar para o agente começar com a baseline que o coding agent tem (o repo) em vez de estichar dados espalhados por cinco plataformas.", "Logue toda ação do agente em todas as apps: isso dá memória ao agente (replicar tarefas bem-sucedidas) e confiança ao humano (auditar em vez de acreditar no relato do agente).", "Padrões extraídos do registro formam 'skills' — um playbook real de como a organização opera — consultável pelo agente em três níveis: como a ferramenta funciona, como a empresa trabalha e preferências pessoais.", "Governança via prompt falha porque vive na memória do agente e pode ser esquecida/compactada; o controle deve viver fora do agente, determinístico e inegociável.", "Implemente duas camadas de governança: controle determinístico de acesso (o que o agente alcança) + políticas em linguagem natural (o que ele pode fazer com esse alcance, ex.: 'nunca deletar mais de 10 e-mails sem permissão').", "Para ações destrutivas, ofereça sandboxes que mockam as ferramentas reais: o blast radius atinge o sandbox, o humano revisa e só então a ação vai ao mundo real.", "Verificação de style em knowledge work: antes de enviar, o agente compara o draft contra e-mails/histórico do usuário para checar aderência ao estilo.", "Dimensione múltiplos gates ao blast radius (branch livre, revisor humano no merge, code owners em arquivos críticos, preview vs. produção) sem desacelerar o agente em zonas seguras.", "Classifique ações em reversíveis (botão de undo, ex.: adicionar label) e irreversíveis (hard delete, envio, wire) — para as irreversíveis, capturar o erro antes do fato: 'timing diferente, mesmo resultado'.", "Aprenda com bilhões de ações quais podem ser revertidas e prepare sandboxes de acordo.", "Composio processa 1B+ tool calls no total e ~300M por mês."]
deep_dive: "high"
deep_dive_reason: "Apresenta um framework arquitetural denso e acionável (seis primitivas com mecanismos concretos: muros determinísticos fora do prompt, sandboxes pré-ação, camada de registro que vira skills) diretamente relevante a harness, context-engineering, governança e evals, com novidade real apesar do viés promocional."
---

# From coding to Knowledge work agents — Karan Vaidya, Composio

## Tese
Agentes de coding são autônomos não por causa dos modelos, mas porque a infraestrutura ao redor do código já fornecia seis primitivas — centralização, história/registro, contexto, verificação, governança e reversibilidade — que não existem no knowledge work, e construir essa infraestrutura é o novo gargalo a ser resolvido.

## Conceitos-chave
- seis primitivas para agentes (centralização, registro, contexto, verificação, governança, reversibilidade)
- fonte única de verdade equivalente ao repo para knowledge work
- record of work: log de toda ação do agente como memória e auditoria
- destilação de skills a partir de padrões de logs em três níveis (ferramenta, empresa, pessoal)
- dois tipos de contexto: shape (arquitetura/mapa) e style (o que é 'bom' na empresa)
- verificação pré-ação via sandboxes que mockam ferramentas reais
- governança determinística fora do prompt vs. instrução frágil (compaction, loopholes)
- políticas em linguagem natural restringindo comportamento dentro do acesso concedido
- gate múltiplo dimensionado ao blast radius
- reversibilidade: undo pós-fato (código) vs. captura pré-fato (knowledge work)
- confiança after-the-fact vs. before-the-fact e irreversibilidade de falhas

## Ferramentas & pessoas
**Ferramentas:** Composio, Claude Code, Codex, Cursor, Git, Salesforce, Notion, Gmail, Slack, Zendesk, PostHog, OpenClaw, TypeScript, CI/CD, preview deployments, bugbot / review skills

**Pessoas/orgs:** Karan Vya (cofundador e CTO da Composio), Composio, Meta Super Intelligence Lab (diretora de alignment, incidente dos 200 e-mails)

## Claims acionáveis
- O gargalo dos agentes migrou dos modelos para a infraestrutura: o mesmo modelo que codifica pode fazer vendas/support/finanças, mas opera 'cego' sem história, contexto, verificação, guardrails ou undo.
- Centralize apps, conexões e logins num único lugar para o agente começar com a baseline que o coding agent tem (o repo) em vez de estichar dados espalhados por cinco plataformas.
- Logue toda ação do agente em todas as apps: isso dá memória ao agente (replicar tarefas bem-sucedidas) e confiança ao humano (auditar em vez de acreditar no relato do agente).
- Padrões extraídos do registro formam 'skills' — um playbook real de como a organização opera — consultável pelo agente em três níveis: como a ferramenta funciona, como a empresa trabalha e preferências pessoais.
- Governança via prompt falha porque vive na memória do agente e pode ser esquecida/compactada; o controle deve viver fora do agente, determinístico e inegociável.
- Implemente duas camadas de governança: controle determinístico de acesso (o que o agente alcança) + políticas em linguagem natural (o que ele pode fazer com esse alcance, ex.: 'nunca deletar mais de 10 e-mails sem permissão').
- Para ações destrutivas, ofereça sandboxes que mockam as ferramentas reais: o blast radius atinge o sandbox, o humano revisa e só então a ação vai ao mundo real.
- Verificação de style em knowledge work: antes de enviar, o agente compara o draft contra e-mails/histórico do usuário para checar aderência ao estilo.
- Dimensione múltiplos gates ao blast radius (branch livre, revisor humano no merge, code owners em arquivos críticos, preview vs. produção) sem desacelerar o agente em zonas seguras.
- Classifique ações em reversíveis (botão de undo, ex.: adicionar label) e irreversíveis (hard delete, envio, wire) — para as irreversíveis, capturar o erro antes do fato: 'timing diferente, mesmo resultado'.
- Aprenda com bilhões de ações quais podem ser revertidas e prepare sandboxes de acordo.
- Composio processa 1B+ tool calls no total e ~300M por mês.

> **Deep dive:** `high` — Apresenta um framework arquitetural denso e acionável (seis primitivas com mecanismos concretos: muros determinísticos fora do prompt, sandboxes pré-ação, camada de registro que vira skills) diretamente relevante a harness, context-engineering, governança e evals, com novidade real apesar do viés promocional.
