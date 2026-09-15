---
title: "Building ambitious software — Jonathan Kelley, Dioxus Labs & Cognition"
type: "extract"
source: "youtube"
video_id: "H7vFrcNWXzs"
url: "https://www.youtube.com/watch?v=H7vFrcNWXzs"
channel: "AI Engineer"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-15-building-ambitious-software-jonathan-kelley-dioxus-labs-cognition--H7vFrcNWXzs.txt]]"
tags: ["agentic-coding", "agents", "code-review", "harness", "testes-qa", "arquitetura", "frameworks", "production", "stack-tooling", "verification", "process", "decision-discipline"]
thesis: "Com coding agents, o código tornou-se barato mas a qualidade não, de modo que o trabalho do engenheiro em software ambicioso se desloca para arquitetura, revisão rigorosa e comunicação clara de intenção, usando agentes como assistentes pacientes para problemas difíceis e tarefas mundanas."
concepts: ["slop cannon (código gerado por IA que não passa na qualidade bar)", "revisão linha a linha de todo PR", "qualidade do código como substrato da velocidade", "arquitetura de software como arte que agentes não dominam", "agentes como resolvedores de problemas de conhecimento (docs, APIs, quirks de plataformas)", "aprendizado de Rust como feature na era dos agentes", "comunicação de intenção e prompt engineering como fator de qualidade", "ler código importa mais que escrever código", "harnesses de fuzzing construídos por agentes", "testes certos vs testes superficiais gerados por IA", "automação de checklists de release e backporting", "manutenção de documentação sincronizada com o código", "tensão entre velocidade de features e estabilidade de API"]
tools: ["Dioxus", "Blitz", "Subsecond", "Rust", "Claude Code", "Zed", "Firefox", "Kotlin", "Swift", "WebAssembly", "React Native", "Flutter", "Electron", "WebKit", "Google Chrome", "Safari"]
people: ["Jonathan Kelly", "Cognition", "Google", "Apple"]
claims: ["Dioxus alcançou ~37.000 stars no GitHub e apps construídos com ele somam mais de 200 milhões de usuários finais estimados", "Apps com o engine Blitz ficam abaixo de 5MB de bundle e consomem menos de 50MB de RAM, contra Electron que consome muito mais", "Subsecond é apresentado como o único hot reload engine para código nativo compilado (Rust, C, C++) com ampla cobertura de linguagens, patcheando apps em ~100ms", "Plugins Kotlin e Swift profundamente integrados ao build system foram entregues em 2-3 semanas com agentes, sendo a implementação feita no primeiro dia e o resto em testes", "Muito do código gerado por agentes inicialmente não passou na qualidade bar de merge, acumulando-se em drafts", "Agentes são excelentes em revolver problemas de conhecimento como ler specs CSS e recall de como Chrome e Safari resolvem layout", "Agentes escrevem testes superficiais (ex.: testar o construtor) e falham em escrever os testes certos, exigindo enumeração manual de condições", "Agentes são muito bons em construir harnesses de fuzzing com inputs adversariais", "A equipe ainda revisa todo PR linha por linha apesar do uso de AI review", "A qualidade da implementação depende fortemente do prompt dado ao modelo", "A maior parte do tempo de desenvolvimento agora é gasta pensando em arquitetura, não escrevendo código", "Com agentes, a cadência de releases passou a ser semanal ou multi-semanal, algo antes temido pela equipe", "Com ferramentas de nível 'fable', a qualidade do código gerado é alta desde que a intenção seja comunicada adequadamente", "Cognition adquiriu o projeto/equipe do Dioxus"]
deep_dive: "medium"
deep_dive_reason: "Relato de experiência com lições práticas acionáveis sobre adoção de agentes em um projeto Rust de produção (incluindo fuzzing harnesses e práticas de code-review), mas sem densidade arquitetural ou novidade em context-engineering, evals ou orquestração de agentes."
---

# Building ambitious software — Jonathan Kelley, Dioxus Labs & Cognition

## Tese
Com coding agents, o código tornou-se barato mas a qualidade não, de modo que o trabalho do engenheiro em software ambicioso se desloca para arquitetura, revisão rigorosa e comunicação clara de intenção, usando agentes como assistentes pacientes para problemas difíceis e tarefas mundanas.

## Conceitos-chave
- slop cannon (código gerado por IA que não passa na qualidade bar)
- revisão linha a linha de todo PR
- qualidade do código como substrato da velocidade
- arquitetura de software como arte que agentes não dominam
- agentes como resolvedores de problemas de conhecimento (docs, APIs, quirks de plataformas)
- aprendizado de Rust como feature na era dos agentes
- comunicação de intenção e prompt engineering como fator de qualidade
- ler código importa mais que escrever código
- harnesses de fuzzing construídos por agentes
- testes certos vs testes superficiais gerados por IA
- automação de checklists de release e backporting
- manutenção de documentação sincronizada com o código
- tensão entre velocidade de features e estabilidade de API

## Ferramentas & pessoas
**Ferramentas:** Dioxus, Blitz, Subsecond, Rust, Claude Code, Zed, Firefox, Kotlin, Swift, WebAssembly, React Native, Flutter, Electron, WebKit, Google Chrome, Safari

**Pessoas/orgs:** Jonathan Kelly, Cognition, Google, Apple

## Claims acionáveis
- Dioxus alcançou ~37.000 stars no GitHub e apps construídos com ele somam mais de 200 milhões de usuários finais estimados
- Apps com o engine Blitz ficam abaixo de 5MB de bundle e consomem menos de 50MB de RAM, contra Electron que consome muito mais
- Subsecond é apresentado como o único hot reload engine para código nativo compilado (Rust, C, C++) com ampla cobertura de linguagens, patcheando apps em ~100ms
- Plugins Kotlin e Swift profundamente integrados ao build system foram entregues em 2-3 semanas com agentes, sendo a implementação feita no primeiro dia e o resto em testes
- Muito do código gerado por agentes inicialmente não passou na qualidade bar de merge, acumulando-se em drafts
- Agentes são excelentes em revolver problemas de conhecimento como ler specs CSS e recall de como Chrome e Safari resolvem layout
- Agentes escrevem testes superficiais (ex.: testar o construtor) e falham em escrever os testes certos, exigindo enumeração manual de condições
- Agentes são muito bons em construir harnesses de fuzzing com inputs adversariais
- A equipe ainda revisa todo PR linha por linha apesar do uso de AI review
- A qualidade da implementação depende fortemente do prompt dado ao modelo
- A maior parte do tempo de desenvolvimento agora é gasta pensando em arquitetura, não escrevendo código
- Com agentes, a cadência de releases passou a ser semanal ou multi-semanal, algo antes temido pela equipe
- Com ferramentas de nível 'fable', a qualidade do código gerado é alta desde que a intenção seja comunicada adequadamente
- Cognition adquiriu o projeto/equipe do Dioxus

> **Deep dive:** `medium` — Relato de experiência com lições práticas acionáveis sobre adoção de agentes em um projeto Rust de produção (incluindo fuzzing harnesses e práticas de code-review), mas sem densidade arquitetural ou novidade em context-engineering, evals ou orquestração de agentes.
