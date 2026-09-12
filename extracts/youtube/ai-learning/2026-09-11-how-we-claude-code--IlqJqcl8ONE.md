---
title: "How we Claude Code"
type: "extract"
source: "youtube"
video_id: "IlqJqcl8ONE"
url: "https://www.youtube.com/watch?v=IlqJqcl8ONE"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-we-claude-code--IlqJqcl8ONE.txt]]"
tags: ["agentic-coding", "evals", "verification", "spec-driven-development", "context-engineering", "harness", "agent-tooling", "testes-qa", "stack-tooling", "production"]
thesis: "À medida que modelos mais capazes permitem agentes de execução longa, é preciso mudar os hábitos de trabalho com Claude Code: deixar o agente entrevistar o usuário para extrair requisitos, substituir specs em markdown por HTML mais denso e ergonômico, e embutir verificação nativa no próprio artefato (contratos de dados no DOM, invariantes, sondas) para que humanos, agentes e CI possam executá-la e registrá-la como evidência."
concepts: ["Bitter Lesson de Richard Sutton aplicada a agentes: resistir a restringir modelos mais capazes", "Requisitos latentes: o modelo extrai requisitos melhor do que o usuário os articula", "Entrevista iterativa de requisitos via ferramenta ask user question", "HTML como formato de spec substituindo markdown ('lingua franca do SDLC nativo de IA')", "Densidade de informação e ergonomia da spec (~200 linhas de markdown como limite de legibilidade)", "Verificação nativa ao artefato (agent-native verification), distinta de testes", "Contratos de dados publicados no DOM via data attributes/data-verify", "Esquemas, fixtures, estados conhecidos, invariantes e sondas (probes) por componente", "Três superfícies de verificação: dashboard humano, execução agêntica no navegador, headless em CI", "Gravação de execuções de verificação como clipes de vídeo compartilháveis (evidência)", "Verificação gerada por Claude para Claude (escalabilidade do loop)", "Separação entre quebrar o app e quebrar o contrato de verificação", "Eficiência de tokens de longo prazo: specs HTML reduzem iterações totais"]
tools: ["Claude Code", "Claude Opus 4.7", "Claude Sonnet", "Playwright MCP", "Storybook", "React", "Bun (bun verify)", "Amazon S3", "Ferramenta ask user question do Claude Code", "Fast mode", "Auto mode (shift+tab)", "Parâmetro /effort"]
people: ["Ara (arquiteto, Applied AI, Anthropic)", "Tar (equipe Claude Code, autor do talk e do post 'The Unreasonable Effectiveness of HTML Files')", "Richard Sutton (autor do Bitter Lesson)", "Anthropic", "CWC Workshops (repositório how-we-claude-code)"]
claims: ["Use auto mode (shift+tab) no Claude Code em vez de modo manual de aprovação", "Configure o parâmetro de effort para x-high ou max", "Use fast mode para iterar rapidamente em specs, mesmo custando mais tokens", "Instrua explicitamente o Claude a usar a ferramenta 'ask user question' para disparar o fluxo de entrevista de requisitos", "Evite prompts vagos como 'make it better'; especifique domínios, audiência e áreas de interesse, não o resultado final", "Migre specs de markdown para HTML quando ultrapassarem ~200 linhas", "Peça múltiplas direções de design geradas em HTML para comparar e dar feedback", "Tire screenshots e alimente de volta ao Claude para feedback de frontend, aproveitando o melhor modelo de visão do Opus 4.7", "Prefira Opus 4.7 a Sonnet para este fluxo por causa da visão superior", "Publique o estado do app no DOM via data attributes para o agente ler contratos de dados sem raspar a interface", "Defina esquemas, fixtures, estados conhecidos e invariantes por componente como base da verificação", "Inclua sondas (probes) para empurrar a execução para fora do caminho feliz", "Opere três superfícies de verificação: dashboard legível por humanos, execução agêntica no navegador via Playwright MCP e 'bun verify' headless em CI", "Grave as execuções de verificação como clipes de vídeo e compartilhe (ex.: S3) como bundle de evidência, como faz a equipe do Claude Code", "Quebrar o contrato de dados (remover data attributes) faz a verificação falhar sem quebrar o app, isolando contrato de implementação", "Deixe o Claude diagnosticar falhas de verificação headless conectado ao Playwright MCP", "A longo prazo, uma spec HTML rica reduz iterações e tokens totais mesmo custando mais em gerações pontuais", "Modularize os componentes para facilitar a extração de contratos pelo agente"]
deep_dive: "high"
deep_dive_reason: "Apresenta arquitetura acionável e nova de verificação agent-native (contratos de dados no DOM, invariantes, sondas, três superfícies, evidências gravadas) combinada a práticas de context-engineering (HTML vs markdown) e harness usadas em produção pela equipe do Claude Code."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-code-best-practices-code-w-claude--gv0WHhKelSE|Claude Code best practices | Code w/ Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-mastering-claude-code-in-30-minutes--6eBSHbLKuN0|Mastering Claude Code in 30 minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-codes-new-intent-md-what-is-it--LoMOPj-lO8U|Claude Codes New INTENT.MD, What is It?]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-thariq-claude-code-anthropic--IHbsfvbfAto|Thariq (Claude Code) @ Anthropic]]"]
---

# How we Claude Code

## Tese
À medida que modelos mais capazes permitem agentes de execução longa, é preciso mudar os hábitos de trabalho com Claude Code: deixar o agente entrevistar o usuário para extrair requisitos, substituir specs em markdown por HTML mais denso e ergonômico, e embutir verificação nativa no próprio artefato (contratos de dados no DOM, invariantes, sondas) para que humanos, agentes e CI possam executá-la e registrá-la como evidência.

## Conceitos-chave
- Bitter Lesson de Richard Sutton aplicada a agentes: resistir a restringir modelos mais capazes
- Requisitos latentes: o modelo extrai requisitos melhor do que o usuário os articula
- Entrevista iterativa de requisitos via ferramenta ask user question
- HTML como formato de spec substituindo markdown ('lingua franca do SDLC nativo de IA')
- Densidade de informação e ergonomia da spec (~200 linhas de markdown como limite de legibilidade)
- Verificação nativa ao artefato (agent-native verification), distinta de testes
- Contratos de dados publicados no DOM via data attributes/data-verify
- Esquemas, fixtures, estados conhecidos, invariantes e sondas (probes) por componente
- Três superfícies de verificação: dashboard humano, execução agêntica no navegador, headless em CI
- Gravação de execuções de verificação como clipes de vídeo compartilháveis (evidência)
- Verificação gerada por Claude para Claude (escalabilidade do loop)
- Separação entre quebrar o app e quebrar o contrato de verificação
- Eficiência de tokens de longo prazo: specs HTML reduzem iterações totais

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Claude Opus 4.7, Claude Sonnet, Playwright MCP, Storybook, React, Bun (bun verify), Amazon S3, Ferramenta ask user question do Claude Code, Fast mode, Auto mode (shift+tab), Parâmetro /effort

**Pessoas/orgs:** Ara (arquiteto, Applied AI, Anthropic), Tar (equipe Claude Code, autor do talk e do post 'The Unreasonable Effectiveness of HTML Files'), Richard Sutton (autor do Bitter Lesson), Anthropic, CWC Workshops (repositório how-we-claude-code)

## Claims acionáveis
- Use auto mode (shift+tab) no Claude Code em vez de modo manual de aprovação
- Configure o parâmetro de effort para x-high ou max
- Use fast mode para iterar rapidamente em specs, mesmo custando mais tokens
- Instrua explicitamente o Claude a usar a ferramenta 'ask user question' para disparar o fluxo de entrevista de requisitos
- Evite prompts vagos como 'make it better'; especifique domínios, audiência e áreas de interesse, não o resultado final
- Migre specs de markdown para HTML quando ultrapassarem ~200 linhas
- Peça múltiplas direções de design geradas em HTML para comparar e dar feedback
- Tire screenshots e alimente de volta ao Claude para feedback de frontend, aproveitando o melhor modelo de visão do Opus 4.7
- Prefira Opus 4.7 a Sonnet para este fluxo por causa da visão superior
- Publique o estado do app no DOM via data attributes para o agente ler contratos de dados sem raspar a interface
- Defina esquemas, fixtures, estados conhecidos e invariantes por componente como base da verificação
- Inclua sondas (probes) para empurrar a execução para fora do caminho feliz
- Opere três superfícies de verificação: dashboard legível por humanos, execução agêntica no navegador via Playwright MCP e 'bun verify' headless em CI
- Grave as execuções de verificação como clipes de vídeo e compartilhe (ex.: S3) como bundle de evidência, como faz a equipe do Claude Code
- Quebrar o contrato de dados (remover data attributes) faz a verificação falhar sem quebrar o app, isolando contrato de implementação
- Deixe o Claude diagnosticar falhas de verificação headless conectado ao Playwright MCP
- A longo prazo, uma spec HTML rica reduz iterações e tokens totais mesmo custando mais em gerações pontuais
- Modularize os componentes para facilitar a extração de contratos pelo agente

> **Deep dive:** `high` — Apresenta arquitetura acionável e nova de verificação agent-native (contratos de dados no DOM, invariantes, sondas, três superfícies, evidências gravadas) combinada a práticas de context-engineering (HTML vs markdown) e harness usadas em produção pela equipe do Claude Code.
