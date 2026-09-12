---
title: "Master the Perfect ChatGPT Prompt Formula (in just 8 minutes)!"
type: "extract"
source: "youtube"
video_id: "jC4v5AS4RIM"
url: "https://www.youtube.com/watch?v=jC4v5AS4RIM"
channel: "Jeff Su"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-master-the-perfect-chatgpt-prompt-formula-in-just-8-minutes--jC4v5AS4RIM.txt]]"
tags: ["context-engineering", "process"]
thesis: "Um prompt eficaz se compõe de seis blocos — Task, Context, Exemplars, Persona, Format e Tone — aplicados em hierarquia de importância, sendo a tarefa obrigatória e os demais componentes graduais conforme a necessidade."
concepts: ["engenharia de prompts", "fórmula de 6 blocos (Task, Context, Exemplars, Persona, Format, Tone)", "hierarquia de importância dos componentes do prompt", "verbo de ação no início da tarefa", "exemplars / exemplos no prompt (few-shot)", "framework STAR como estrutura de exemplo", "persona prompting", "especificação de formato (tabela, e-mail, bullets, markdown, headers H2)", "especificação de tom de voz", "checklist mental para escrita de prompts", "princípio de dar 'informação suficiente' para restringir o espaço de saídas", "uso de referências existentes como molde de formatação", "metaprompting: pedir ao modelo palavras-chave de tom"]
tools: ["ChatGPT", "Google Bard", "Google Sheets", "Google Workspace", "LinkedIn"]
people: ["Jeff Su", "Warren Buffett", "Steve Jobs", "Tim Cook", "Batman (personagem)", "Alfred (personagem)", "Apple", "Tesla", "Google"]
claims: ["Todo prompt deve conter obrigatoriamente uma tarefa; sem tarefa não há saída significativa, enquanto contexto sem tarefa não gera nada útil", "Inicie a frase da tarefa com um verbo de ação (gerar, escrever, analisar) e articule claramente o objetivo final, que pode ser simples ou multi-etapas", "Para calibrar o contexto, responda três perguntas: qual o background do usuário, como se parece o sucesso e em que ambiente ele está — inclua apenas o suficiente para restringir as possibilidades", "Incluir exemplos ou frameworks no prompt melhora drasticamente a qualidade da saída segundo pesquisas sobre LLMs", "Use a estrutura 'realizei X, medido por Y, que resultou em Z' em bullets de currículo e o framework STAR em respostas de entrevista como exemplares", "Para persona, imagine um especialista a quem gostaria de acesso imediato; nomes de indivíduos específicos só funcionam quando são famosos, e personagens fictícios também produzem bons resultados", "Visualize o formato final desejado (tabela, bullets, e-mail, markdown) e especifique-o explicitamente para obter saídas prontas para colar em outras ferramentas", "Ao pedir revisão de documentos, exija que as alterações fiquem em negrito para facilitar a inspeção das mudanças", "Se não souber definir o tom, peça ao próprio modelo uma lista de palavras-chave de tom e reutilize-as no prompt final", "Nem todo prompt precisa dos seis componentes; a fórmula funciona como checklist para dosar a informação relevante"]
deep_dive: "low"
deep_dive_reason: "Conteúdo introdutório e genérico de prompting para usuários finais, sem densidade arquitetural, novidade ou relevância para harness, evals, context-engineering avançado ou agentes, com trecho promocional de newsletter."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-best-chatgpt-prompt-i-ve-ever-created-i-spent-2-months-curating-this-prompt--ABCqfaTjNd4|The best ChatGPT Prompt I've ever created - I spent 2 months curating this prompt to write prompts]]", "[[extracts/youtube/ai-learning/2026-09-11-next-level-prompts-10-mins-into-advanced-prompting--69bH4IHZivs|\"Next Level Prompts?\" - 10 mins into advanced prompting]]", "[[extracts/youtube/ai-learning/2026-09-11-google-s-9-hour-ai-prompt-engineering-course-in-20-minutes--p09yRj47kNM|Google's 9 Hour AI Prompt Engineering Course In 20 Minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-the-prompting-playbook--G2B0YWuJUgI|The prompting playbook]]", "[[extracts/youtube/ai-learning/2026-09-11-state-of-the-art-prompting-for-ai-agents--DL82mGde6wo|State-Of-The-Art Prompting For AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-prompt-engineering-a-deep-dive--T9aRN5JkmL8|AI prompt engineering: A deep dive]]"]
theme: "Stack de IA e Prompting"
---

# Master the Perfect ChatGPT Prompt Formula (in just 8 minutes)!

## Tese
Um prompt eficaz se compõe de seis blocos — Task, Context, Exemplars, Persona, Format e Tone — aplicados em hierarquia de importância, sendo a tarefa obrigatória e os demais componentes graduais conforme a necessidade.

## Conceitos-chave
- engenharia de prompts
- fórmula de 6 blocos (Task, Context, Exemplars, Persona, Format, Tone)
- hierarquia de importância dos componentes do prompt
- verbo de ação no início da tarefa
- exemplars / exemplos no prompt (few-shot)
- framework STAR como estrutura de exemplo
- persona prompting
- especificação de formato (tabela, e-mail, bullets, markdown, headers H2)
- especificação de tom de voz
- checklist mental para escrita de prompts
- princípio de dar 'informação suficiente' para restringir o espaço de saídas
- uso de referências existentes como molde de formatação
- metaprompting: pedir ao modelo palavras-chave de tom

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Google Bard, Google Sheets, Google Workspace, LinkedIn

**Pessoas/orgs:** Jeff Su, Warren Buffett, Steve Jobs, Tim Cook, Batman (personagem), Alfred (personagem), Apple, Tesla, Google

## Claims acionáveis
- Todo prompt deve conter obrigatoriamente uma tarefa; sem tarefa não há saída significativa, enquanto contexto sem tarefa não gera nada útil
- Inicie a frase da tarefa com um verbo de ação (gerar, escrever, analisar) e articule claramente o objetivo final, que pode ser simples ou multi-etapas
- Para calibrar o contexto, responda três perguntas: qual o background do usuário, como se parece o sucesso e em que ambiente ele está — inclua apenas o suficiente para restringir as possibilidades
- Incluir exemplos ou frameworks no prompt melhora drasticamente a qualidade da saída segundo pesquisas sobre LLMs
- Use a estrutura 'realizei X, medido por Y, que resultou em Z' em bullets de currículo e o framework STAR em respostas de entrevista como exemplares
- Para persona, imagine um especialista a quem gostaria de acesso imediato; nomes de indivíduos específicos só funcionam quando são famosos, e personagens fictícios também produzem bons resultados
- Visualize o formato final desejado (tabela, bullets, e-mail, markdown) e especifique-o explicitamente para obter saídas prontas para colar em outras ferramentas
- Ao pedir revisão de documentos, exija que as alterações fiquem em negrito para facilitar a inspeção das mudanças
- Se não souber definir o tom, peça ao próprio modelo uma lista de palavras-chave de tom e reutilize-as no prompt final
- Nem todo prompt precisa dos seis componentes; a fórmula funciona como checklist para dosar a informação relevante

> **Deep dive:** `low` — Conteúdo introdutório e genérico de prompting para usuários finais, sem densidade arquitetural, novidade ou relevância para harness, evals, context-engineering avançado ou agentes, com trecho promocional de newsletter.
