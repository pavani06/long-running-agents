---
title: "What's Next After RLHF? — Diogo Almeida, TypeSafe AI"
type: "extract"
source: "youtube"
video_id: "cJ0EOzey--o"
url: "https://www.youtube.com/watch?v=cJ0EOzey--o"
channel: "AI Engineer"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-18-what-s-next-after-rlhf-diogo-almeida-typesafe-ai--cJ0EOzey--o.txt]]"
tags: ["agents", "agent-loop", "analise", "arquitetura", "decision-discipline", "production", "roadmap"]
thesis: "A era atual da IA (ChatGPT e até Claude Code) é nativamente de assistência porque o RLHF otimiza para preferência humana — colocando o humano no loop por construção — e a próxima era exigirá uma nova stack de pós-treinamento focada em decisão calibrada para automação real e software mais inteligente."
concepts: ["RLHF (otimização de preferência humana)", "RLVR (recompensa verificável / correção pura)", "assistência vs. automação como divisão fundamental", "human-in-the-loop intrínseco ao objetivo da tarefa", "assimetria do reward model (analogia com mode collapse de GANs)", "alucinação como subproduto da otimização de preferência", "overpromising by design (otimização para engajamento)", "pós-treinamento como disciplina inventada no OpenAI", "just-in-time software vs. software mais inteligente/expressivo", "decisão calibrada como nova função objetivo", "hierarquia tarefa > dados > compute (releitura do bitter lesson)", "scaling laws originais questionadas"]
tools: ["GPT-4", "ChatGPT", "InstructGPT", "Claude Code", "Typesafe"]
people: ["Diego Almeida", "OpenAI", "Gary Tan", "Yoshua Bengio", "Richard Sutton", "Typesafe"]
claims: ["Trate LLMs atuais como assistentes, não como automatizadores: ~100% dos LLMs em uso são treinados com RLHF e carregam o humano no loop por construção do próprio objetivo de treinamento.", "Não use IA atual para decisões com stakes para o negócio; o padrão de mercado vigente é empurrar custos ao usuário (ex.: docs infinitos em customer service) e não à empresa.", "Espere que modelos RLHF pareçam corretos mesmo quando erram — overpromising é feature do design, então automação exige verificação e calibração externas.", "Alucinação é intrínseca à otimização de preferência humana (assimetria do reward model análoga a GANs) e não se resolve só com mais dados; exige paradigma de objetivo diferente.", "Claude Code ainda pertence à era da assistência (RLHF): força em tarefas agênticas trade-offa com seguir o que o usuário realmente quer.", "Pré-treinamento não é o gargalo — modelos pré-treinados são altamente inteligentes; o problema é como desenterrar essa inteligência para uso útil.", "Priorize escolher a tarefa certa acima de dados e compute: o bitter lesson (algoritmos > compute) vale em jogos, mas não na realidade.", "Automatizar a escrita de software (just-in-time software) não torna o software mais expressivo; a oportunidade de produto é 'smarter software', não chatbots anexados a SaaS existentes.", "Trabalho realmente automatizado hoje é um erro de arredondamento apesar da inteligência dos LLMs — o próximo salto é uma terceira via de pós-treinamento otimizada para decisão calibrada, distinta de RLHF e RLVR, até no formato da API."]
deep_dive: "medium"
deep_dive_reason: "O framing assistência-vs-automação e a explicação estrutural da alucinação são insights originais e acionáveis, mas a palestra é conceitual, sem detalhes arquiteturais de harness/evals e com forte viés promocional do pitch da Typesafe."
theme: "Futuro Estratégico dos Agentes"
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-ilya-sutskever-we-re-moving-from-the-age-of-scaling-to-the-age-of-research--aR20FWCCjAs|Ilya Sutskever – We're moving from the age of scaling to the age of research]]", "[[extracts/youtube/ai-learning/2026-09-11-creating-agents-that-co-create-karina-nguyen-openai--1XvN5EBDnDw|Creating Agents that Co-Create — Karina Nguyen, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-fabio-akita-minha-experiencia-com-agile-vibe-coding--U3bZavG8qQY|Fabio Akita: Minha Experiência com Agile Vibe Coding]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-s-1b-bet-against-llms-part-1--kYkIdXwW2AE|Yann LeCun's $1B Bet Against LLMs [Part 1]]]", "[[extracts/youtube/ai-learning/2026-09-19-we-need-to-talk-about-jev--2z-7pIj57f8|We need to talk about Jev...]]", "[[extracts/youtube/ai-learning/2026-09-11-did-openai-just-solve-hallucinations--xGO5Q94XXf0|Did OpenAI just solve hallucinations?]]"]
---

# What's Next After RLHF? — Diogo Almeida, TypeSafe AI

## Tese
A era atual da IA (ChatGPT e até Claude Code) é nativamente de assistência porque o RLHF otimiza para preferência humana — colocando o humano no loop por construção — e a próxima era exigirá uma nova stack de pós-treinamento focada em decisão calibrada para automação real e software mais inteligente.

## Conceitos-chave
- RLHF (otimização de preferência humana)
- RLVR (recompensa verificável / correção pura)
- assistência vs. automação como divisão fundamental
- human-in-the-loop intrínseco ao objetivo da tarefa
- assimetria do reward model (analogia com mode collapse de GANs)
- alucinação como subproduto da otimização de preferência
- overpromising by design (otimização para engajamento)
- pós-treinamento como disciplina inventada no OpenAI
- just-in-time software vs. software mais inteligente/expressivo
- decisão calibrada como nova função objetivo
- hierarquia tarefa > dados > compute (releitura do bitter lesson)
- scaling laws originais questionadas

## Ferramentas & pessoas
**Ferramentas:** GPT-4, ChatGPT, InstructGPT, Claude Code, Typesafe

**Pessoas/orgs:** Diego Almeida, OpenAI, Gary Tan, Yoshua Bengio, Richard Sutton, Typesafe

## Claims acionáveis
- Trate LLMs atuais como assistentes, não como automatizadores: ~100% dos LLMs em uso são treinados com RLHF e carregam o humano no loop por construção do próprio objetivo de treinamento.
- Não use IA atual para decisões com stakes para o negócio; o padrão de mercado vigente é empurrar custos ao usuário (ex.: docs infinitos em customer service) e não à empresa.
- Espere que modelos RLHF pareçam corretos mesmo quando erram — overpromising é feature do design, então automação exige verificação e calibração externas.
- Alucinação é intrínseca à otimização de preferência humana (assimetria do reward model análoga a GANs) e não se resolve só com mais dados; exige paradigma de objetivo diferente.
- Claude Code ainda pertence à era da assistência (RLHF): força em tarefas agênticas trade-offa com seguir o que o usuário realmente quer.
- Pré-treinamento não é o gargalo — modelos pré-treinados são altamente inteligentes; o problema é como desenterrar essa inteligência para uso útil.
- Priorize escolher a tarefa certa acima de dados e compute: o bitter lesson (algoritmos > compute) vale em jogos, mas não na realidade.
- Automatizar a escrita de software (just-in-time software) não torna o software mais expressivo; a oportunidade de produto é 'smarter software', não chatbots anexados a SaaS existentes.
- Trabalho realmente automatizado hoje é um erro de arredondamento apesar da inteligência dos LLMs — o próximo salto é uma terceira via de pós-treinamento otimizada para decisão calibrada, distinta de RLHF e RLVR, até no formato da API.

> **Deep dive:** `medium` — O framing assistência-vs-automação e a explicação estrutural da alucinação são insights originais e acionáveis, mas a palestra é conceitual, sem detalhes arquiteturais de harness/evals e com forte viés promocional do pitch da Typesafe.
