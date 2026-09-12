---
title: "The Pipeline Is Dead - Iris ten Teije, Sky Valley Ambient Computing"
type: "extract"
source: "youtube"
video_id: "bRnoEpoK5m4"
url: "https://www.youtube.com/watch?v=bRnoEpoK5m4"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-pipeline-is-dead-iris-ten-teije-sky-valley-ambient-computing--bRnoEpoK5m4.txt]]"
tags: ["arquitetura", "agents", "agentic-coding", "runtime", "evals", "verification", "observability", "tracing", "governanca", "permissions", "production"]
thesis: "Com agentes de IA levando o custo de produzir mudanças corretas e escopadas a quase zero, a distribuição de software migra do modelo de um artefato congelado para todos (CI, registros, imagens) para um stem canônico único do qual cada usuário executa sua própria divergência viva, isolada e reversível."
concepts: ["software adaptativo", "artefato congelado (frozen artifact)", "uma versão para todos como consequência de custo, não lei do software", "desenvolvimento e distribuição como fases que se fundem quando o runtime (agente) pode modificar o software", "stem canônico + divergências por usuário", "divergências limitadas, isoladas, imutáveis e individualmente reversíveis", "blast radius de uma mudança = um contexto, não o sistema", "rollback ao vivo sem deploy", "limites de adaptação definidos pelo desenvolvedor (ex.: campos obrigatórios, auth e payments fora do alcance)", "mudanças solicitadas pelo usuário dentro do espírito original do software sem voltar ao desenvolvedor", "fonte da verdade = stem + divergências imutáveis", "o que o usuário executa vira uma consulta em grafo, não um número de versão", "bug report como descrição de um programa único daquele usuário", "tracing de proveniência: sinal → recomendação → adaptação exata", "correção (testar stem + toda divergência possível) vs desejabilidade (a mudança gerou uplift?)", "métricas de desejabilidade: retenção, churn, tickets de suporte", "autonomia vs controle: ganhar confiança suficiente para humanos saírem do loop", "coordenação: fundir intenção e desejável, não código — convergir no mesmo objetivo por caminhos próprios", "geração de código como os fáceis 80%; observabilidade, validação, proveniência e coordenação como o negócio real", "demanda comprovada por personalização: forward-deployed engineers/serviços profissionais, dotfiles, Excel como programação de usuário final", "predecessores: feature flags, segmentação, A/B testing"]
tools: ["Differ", "CI pipelines", "registros de pacotes (package registries)", "imagens de contêiner", "revisões de app store", "feature flags", "A/B testing", "Salesforce", "Slack", "Excel", "dotfiles / configuração de editor", "CRM (exemplo)", "LLMs / agentes de codificação"]
people: ["Iris (cofundadora da Differ)", "Noam (cofundador da Differ, primeiro engenheiro da JFrog)", "Differ", "JFrog", "Salesforce"]
claims: ["Toda a pilha de distribuição (CI, registros, imagens) codifica a suposição de que software é produzido em um lugar, roda em outro e congela num artefato — consequência direta de produção cara e rara, não uma lei do software", "Quando fazer uma mudança corretamente escopada custa quase zero, o congelamento em build time vira decisão em tempo real e as peças podem ser produzidas onde rodam, inclusive na sessão viva do usuário", "A arquitetura proposta: um stem canônico único e divergências por usuário limitadas, isoladas, imutáveis e individualmente reversíveis, com blast radius de um único contexto e rollback ao vivo sem deploy", "A fragilidade temida em código gerado por IA vem da ausência de estrutura/bordas dentro de um artefato emaranhado, não da geração por IA — e é exatamente o que stem + divergências isoladas previne", "Desenvolvedores devem declarar limites de adaptação: campos que nunca podem ser removidos e módulos como auth e payments sempre fora do alcance da adaptação autônoma", "Usuários podem solicitar mudanças implementadas sem passar pelo desenvolvedor, contanto que estejam dentro dos limites e do propósito original do software", "Sem artefato único, a pergunta 'o que este usuário executa e por quê' passa de número de versão a consulta em grafo; toda divergência precisa ser imutável, inspecionável, atribuível e rastreável do sinal à adaptação exata", "Testar adaptativamente exige raciocinar sobre o stem e toda divergência possível, e corretude não basta: é preciso medir desejabilidade como uplift contra metas de negócio (retenção, churn, tickets)", "A resposta de coordenação para milhões de versões não é merge de código, mas de intenção/desejável: todos convergem no mesmo objetivo por caminhos próprios", "Chamar um LLM para escrever código é o fácil; o valor está no substrato: observabilidade, validação, proveniência e coordenação", "A demanda por software personalizado é antiga e comprovada (forward-deployed engineers, dotfiles, Excel), e agentes de codificação finalmente a tornam viável na camada de software para personas mais amplas sem aumentar o gasto de P&D"]
deep_dive: "medium"
deep_dive_reason: "A tese arquitetural (stem + divergências isoladas, proveniência por grafo, fusão de intenção) é nova e relevante para harness, evals e governança de agentes, mas o conteúdo permanece em nível de visão/pitch de startup sem detalhes de implementação, métricas ou resultados."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-ci-cd-is-dead-agents-need-continuous-compute-and-computers-hugo-santos-and-madis--VktrqzQgytY|CI/CD Is Dead, Agents Need Continuous Compute and Computers — Hugo Santos and Madison Faulkner]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-frontrunners-say-coding-is-solved-but-engineering-is-not--Q7l8YGiMgUw|Why the Frontrunners Say Coding Is Solved BUT Engineering is Not]]", "[[extracts/youtube/ai-learning/2026-09-11-everything-we-knew-about-software-has-changed-theo-browne-t3dotgg--xUnRQ9vLXxo|Everything we knew about software has changed — Theo Browne, @t3dotgg ​]]", "[[extracts/youtube/ai-learning/2026-09-11-the-engineer-of-the-future-is-the-person-who-is-able-to-choose-what-is-worth-doi--n97BCfyFIvw|\"The engineer of the future is the person who is able to choose what is worth doing.\" — Addy Osmani]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-the-end-of-the-static-screen-architecting-intent-driven-ux-gus-iwanaga-commercet--QrMcNe2jjt8|The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools]]"]
---

# The Pipeline Is Dead - Iris ten Teije, Sky Valley Ambient Computing

## Tese
Com agentes de IA levando o custo de produzir mudanças corretas e escopadas a quase zero, a distribuição de software migra do modelo de um artefato congelado para todos (CI, registros, imagens) para um stem canônico único do qual cada usuário executa sua própria divergência viva, isolada e reversível.

## Conceitos-chave
- software adaptativo
- artefato congelado (frozen artifact)
- uma versão para todos como consequência de custo, não lei do software
- desenvolvimento e distribuição como fases que se fundem quando o runtime (agente) pode modificar o software
- stem canônico + divergências por usuário
- divergências limitadas, isoladas, imutáveis e individualmente reversíveis
- blast radius de uma mudança = um contexto, não o sistema
- rollback ao vivo sem deploy
- limites de adaptação definidos pelo desenvolvedor (ex.: campos obrigatórios, auth e payments fora do alcance)
- mudanças solicitadas pelo usuário dentro do espírito original do software sem voltar ao desenvolvedor
- fonte da verdade = stem + divergências imutáveis
- o que o usuário executa vira uma consulta em grafo, não um número de versão
- bug report como descrição de um programa único daquele usuário
- tracing de proveniência: sinal → recomendação → adaptação exata
- correção (testar stem + toda divergência possível) vs desejabilidade (a mudança gerou uplift?)
- métricas de desejabilidade: retenção, churn, tickets de suporte
- autonomia vs controle: ganhar confiança suficiente para humanos saírem do loop
- coordenação: fundir intenção e desejável, não código — convergir no mesmo objetivo por caminhos próprios
- geração de código como os fáceis 80%; observabilidade, validação, proveniência e coordenação como o negócio real
- demanda comprovada por personalização: forward-deployed engineers/serviços profissionais, dotfiles, Excel como programação de usuário final
- predecessores: feature flags, segmentação, A/B testing

## Ferramentas & pessoas
**Ferramentas:** Differ, CI pipelines, registros de pacotes (package registries), imagens de contêiner, revisões de app store, feature flags, A/B testing, Salesforce, Slack, Excel, dotfiles / configuração de editor, CRM (exemplo), LLMs / agentes de codificação

**Pessoas/orgs:** Iris (cofundadora da Differ), Noam (cofundador da Differ, primeiro engenheiro da JFrog), Differ, JFrog, Salesforce

## Claims acionáveis
- Toda a pilha de distribuição (CI, registros, imagens) codifica a suposição de que software é produzido em um lugar, roda em outro e congela num artefato — consequência direta de produção cara e rara, não uma lei do software
- Quando fazer uma mudança corretamente escopada custa quase zero, o congelamento em build time vira decisão em tempo real e as peças podem ser produzidas onde rodam, inclusive na sessão viva do usuário
- A arquitetura proposta: um stem canônico único e divergências por usuário limitadas, isoladas, imutáveis e individualmente reversíveis, com blast radius de um único contexto e rollback ao vivo sem deploy
- A fragilidade temida em código gerado por IA vem da ausência de estrutura/bordas dentro de um artefato emaranhado, não da geração por IA — e é exatamente o que stem + divergências isoladas previne
- Desenvolvedores devem declarar limites de adaptação: campos que nunca podem ser removidos e módulos como auth e payments sempre fora do alcance da adaptação autônoma
- Usuários podem solicitar mudanças implementadas sem passar pelo desenvolvedor, contanto que estejam dentro dos limites e do propósito original do software
- Sem artefato único, a pergunta 'o que este usuário executa e por quê' passa de número de versão a consulta em grafo; toda divergência precisa ser imutável, inspecionável, atribuível e rastreável do sinal à adaptação exata
- Testar adaptativamente exige raciocinar sobre o stem e toda divergência possível, e corretude não basta: é preciso medir desejabilidade como uplift contra metas de negócio (retenção, churn, tickets)
- A resposta de coordenação para milhões de versões não é merge de código, mas de intenção/desejável: todos convergem no mesmo objetivo por caminhos próprios
- Chamar um LLM para escrever código é o fácil; o valor está no substrato: observabilidade, validação, proveniência e coordenação
- A demanda por software personalizado é antiga e comprovada (forward-deployed engineers, dotfiles, Excel), e agentes de codificação finalmente a tornam viável na camada de software para personas mais amplas sem aumentar o gasto de P&D

> **Deep dive:** `medium` — A tese arquitetural (stem + divergências isoladas, proveniência por grafo, fusão de intenção) é nova e relevante para harness, evals e governança de agentes, mas o conteúdo permanece em nível de visão/pitch de startup sem detalhes de implementação, métricas ou resultados.
