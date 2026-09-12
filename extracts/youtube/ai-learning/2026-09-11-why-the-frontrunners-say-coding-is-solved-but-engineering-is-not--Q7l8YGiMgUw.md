---
title: "Why the Frontrunners Say Coding Is Solved BUT Engineering is Not"
type: "extract"
source: "youtube"
video_id: "Q7l8YGiMgUw"
url: "https://www.youtube.com/watch?v=Q7l8YGiMgUw"
channel: "Beyond Coding"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-the-frontrunners-say-coding-is-solved-but-engineering-is-not--Q7l8YGiMgUw.txt]]"
tags: ["agentic-coding", "spec-driven-development", "harness", "model-selection", "code-review", "agent-loop", "verification", "process", "agents", "production"]
thesis: "Dois engenheiros praticantes sustentam que escrever código foi 'resolvido' pelos modelos de fronteira desde o Opus 4.5 e que o papel humano migra para especificar, orquestrar e verificar: engenhar o processo (spec-driven development, loops de revisão automatizados e provas de funcionamento) rumo a uma 'dark factory' de software."
concepts: ["Dark Factory (fábrica de software sem humanos, 'luzes apagadas')", "Software development (escrita de código) vs. software engineering (arquitetura, cloud, integrações)", "Especificação dirigida por desenvolvimento (spec-driven development)", "Gords de revisão: humanos como gargalo de pull requests", "Revisão baseada em risco (só humanos revisam PRs de alto risco)", "Anatomia do harness: system prompt, agents.md, skills, conjunto de ferramentas (edit/read/write/bash no pi)", "Modelo importa mais que harness (~90% do trabalho vem do modelo)", "Proxy man-in-the-middle para inspecionar tráfego modelo-harness ('é só texto indo e voltando')", "Specs estilo Gherkin como corpus de comportamentos arquivados/mergiados ao longo do tempo", "Loop de revisão cruzada entre modelos (implementa → revisa com Opus → revisa com GPT → até não achar issues)", "'Prova' de funcionamento como artefato de verificação (screenshots para frontend, request/response JSON para backend)", "Ralph loop (loop autônomo de tarefas sequenciais)", "'Engineering ao quadrado': engenhar o processo que habilita engenhar o produto", "Tokens de orçamento de inovação e o risco de 'plateauing' (estagnar em um setup confortável)", "Equipes menores amplificadas por agentes; 'agent company'", "Eliminação de toil em empresas médias baseadas em Excel", "Vantagem de aprender com modelos de fronteira em vez de modelos velhos/baratos/locais durante a curva de aprendizado"]
tools: ["Claude Opus 4.5", "Codex", "Claude Code", "GitHub Copilot", "OpenSpec", "spec-kit (GitHub)", "opencode", "pi (harness)", "Amp (Sourcegraph)", "Cody (Sourcegraph)", "DeepSeek", "Gemini 3.5 Flash", "Agents.md", "Gherkin", "Visual Studio Code", "IntelliJ", "Azure", "Amazon/AWS Cloud", "Go", "MITM proxy"]
people: ["Jeroen Gordijn", "Jeroen Dee", "Geoffrey Huntley", "Jack Dorsey", "Block", "Meta", "Sourcegraph", "Anthropic", "OpenAI", "Google", "Nvidia", "GitHub", "Microsoft"]
claims: ["Pare de digitar código: a escrita de código foi resolvida pelos modelos desde o Opus 4.5 (24 de novembro do ano passado) e é mais barata que o tempo de um desenvolvedor", "Trate a revisão de PRs como gargalo: aplique revisão humana apenas a mudanças de alto risco e invista em agentes revisores automatizados", "Adote OpenSpec em vez de spec-kit: gera proposta + design document (estilo ADR) + specs legíveis estilo Gherkin, e arquiva/mescla os specs num corpus cumulativo de comportamentos exigidos do software", "Não faça engenharia reversa das specs antes de adotar: comece com OpenSpec imediatamente na base existente e reveja specs depois, se necessário", "Priorize comparar modelos (ex.: Opus melhor em frontend, DeepSeek melhor em backend) em vez de gastar tempo trocando de harness, pois mais de 90% do resultado vem do modelo", "Use um proxy man-in-the-middle para inspecionar o que o harness envia (system prompt, agents.md, skills, definição de tools) e desmistificar o marketing", "Construa um pipeline hands-off: implementar → revisar cruzadamente com múltiplos modelos até não haver issues → PR → deploy em ambiente de teste → gerar prova (screenshots do fluxo ou request/response JSON)", "Redimensione o papel do engenheiro para: escrever specs, checar as provas e engenhar o próprio workflow ('engineering ao quadrado')", "Não aprenda com modelos antigos/baratos/locais: isso sabota a curva de aprendizado; use modelos locais apenas para entender o contraste e a lacuna de qualidade/velocidade", "Antecipe a reestruturação para equipes menores (tendência já vista em Block e Meta) e o reposicionamento da empresa como 'agent company'", "Combata o plateauing reservando 'tokens de inovação' para experimentar novos harnesses, modelos e execução remota/em nuvem em vez de só local", "Mire empresas médias 'Excel-based' (grandes demais para Excel, pequenas para times de dev) como oportunidade de eliminação de toil com agentes"]
deep_dive: "medium"
deep_dive_reason: "Há boa densidade acionável em spec-driven development (OpenSpec), loops de revisão/verificação com provas e anatomia de harness, mas é uma conversa de podcast com redundância e sem novidade arquitetural profunda."
---

# Why the Frontrunners Say Coding Is Solved BUT Engineering is Not

## Tese
Dois engenheiros praticantes sustentam que escrever código foi 'resolvido' pelos modelos de fronteira desde o Opus 4.5 e que o papel humano migra para especificar, orquestrar e verificar: engenhar o processo (spec-driven development, loops de revisão automatizados e provas de funcionamento) rumo a uma 'dark factory' de software.

## Conceitos-chave
- Dark Factory (fábrica de software sem humanos, 'luzes apagadas')
- Software development (escrita de código) vs. software engineering (arquitetura, cloud, integrações)
- Especificação dirigida por desenvolvimento (spec-driven development)
- Gords de revisão: humanos como gargalo de pull requests
- Revisão baseada em risco (só humanos revisam PRs de alto risco)
- Anatomia do harness: system prompt, agents.md, skills, conjunto de ferramentas (edit/read/write/bash no pi)
- Modelo importa mais que harness (~90% do trabalho vem do modelo)
- Proxy man-in-the-middle para inspecionar tráfego modelo-harness ('é só texto indo e voltando')
- Specs estilo Gherkin como corpus de comportamentos arquivados/mergiados ao longo do tempo
- Loop de revisão cruzada entre modelos (implementa → revisa com Opus → revisa com GPT → até não achar issues)
- 'Prova' de funcionamento como artefato de verificação (screenshots para frontend, request/response JSON para backend)
- Ralph loop (loop autônomo de tarefas sequenciais)
- 'Engineering ao quadrado': engenhar o processo que habilita engenhar o produto
- Tokens de orçamento de inovação e o risco de 'plateauing' (estagnar em um setup confortável)
- Equipes menores amplificadas por agentes; 'agent company'
- Eliminação de toil em empresas médias baseadas em Excel
- Vantagem de aprender com modelos de fronteira em vez de modelos velhos/baratos/locais durante a curva de aprendizado

## Ferramentas & pessoas
**Ferramentas:** Claude Opus 4.5, Codex, Claude Code, GitHub Copilot, OpenSpec, spec-kit (GitHub), opencode, pi (harness), Amp (Sourcegraph), Cody (Sourcegraph), DeepSeek, Gemini 3.5 Flash, Agents.md, Gherkin, Visual Studio Code, IntelliJ, Azure, Amazon/AWS Cloud, Go, MITM proxy

**Pessoas/orgs:** Jeroen Gordijn, Jeroen Dee, Geoffrey Huntley, Jack Dorsey, Block, Meta, Sourcegraph, Anthropic, OpenAI, Google, Nvidia, GitHub, Microsoft

## Claims acionáveis
- Pare de digitar código: a escrita de código foi resolvida pelos modelos desde o Opus 4.5 (24 de novembro do ano passado) e é mais barata que o tempo de um desenvolvedor
- Trate a revisão de PRs como gargalo: aplique revisão humana apenas a mudanças de alto risco e invista em agentes revisores automatizados
- Adote OpenSpec em vez de spec-kit: gera proposta + design document (estilo ADR) + specs legíveis estilo Gherkin, e arquiva/mescla os specs num corpus cumulativo de comportamentos exigidos do software
- Não faça engenharia reversa das specs antes de adotar: comece com OpenSpec imediatamente na base existente e reveja specs depois, se necessário
- Priorize comparar modelos (ex.: Opus melhor em frontend, DeepSeek melhor em backend) em vez de gastar tempo trocando de harness, pois mais de 90% do resultado vem do modelo
- Use um proxy man-in-the-middle para inspecionar o que o harness envia (system prompt, agents.md, skills, definição de tools) e desmistificar o marketing
- Construa um pipeline hands-off: implementar → revisar cruzadamente com múltiplos modelos até não haver issues → PR → deploy em ambiente de teste → gerar prova (screenshots do fluxo ou request/response JSON)
- Redimensione o papel do engenheiro para: escrever specs, checar as provas e engenhar o próprio workflow ('engineering ao quadrado')
- Não aprenda com modelos antigos/baratos/locais: isso sabota a curva de aprendizado; use modelos locais apenas para entender o contraste e a lacuna de qualidade/velocidade
- Antecipe a reestruturação para equipes menores (tendência já vista em Block e Meta) e o reposicionamento da empresa como 'agent company'
- Combata o plateauing reservando 'tokens de inovação' para experimentar novos harnesses, modelos e execução remota/em nuvem em vez de só local
- Mire empresas médias 'Excel-based' (grandes demais para Excel, pequenas para times de dev) como oportunidade de eliminação de toil com agentes

> **Deep dive:** `medium` — Há boa densidade acionável em spec-driven development (OpenSpec), loops de revisão/verificação com provas e anatomia de harness, mas é uma conversa de podcast com redundância e sem novidade arquitetural profunda.
