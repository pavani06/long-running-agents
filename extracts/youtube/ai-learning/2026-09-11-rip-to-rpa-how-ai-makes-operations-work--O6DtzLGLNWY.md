---
title: "RIP to RPA: How AI Makes Operations Work"
type: "extract"
source: "youtube"
video_id: "O6DtzLGLNWY"
url: "https://www.youtube.com/watch?v=O6DtzLGLNWY"
channel: "a16z"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-rip-to-rpa-how-ai-makes-operations-work--O6DtzLGLNWY.txt]]"
tags: ["agents", "analise", "process", "investimentos", "roadmap", "model-selection", "monitoramento"]
thesis: "RPA determinístico falha na cauda longa de processos bagunçados, e agentes de IA verticais baseados em LLMs — capazes de processar dados não estruturados e coletar contexto dinamicamente — podem automatizar trabalho de back-office que o software nunca alcançou, tornando o orçamento de mão de obra (não o de software) o verdadeiro mercado."
concepts: ["RPA (robotic process automation) determinístico por mimetização de cliques", "falha de RPA em casos de borda e longa cauda (~80/20)", "automação inteligente com LLMs ('LLMs in action')", "agente vertical vs. enabler horizontal de IA", "extração de dados não estruturados para estruturados", "browser/computer-use agents como infraestrutura habilitadora", "gestão de referências médicas por fax como caso de uso", "comparação orçamento de mão de obra vs. orçamento de software", "estratégia de wedge: um fluxo vertical nítido antes de expandir", "fluxos geradores de receita previamente limitados por capacidade", "UI self-serve drag-and-drop substituindo consultores de implementação", "direito de vencer (right to win) via integrações com sistemas core"]
tools: ["RPA", "Anthropic Computer Use", "OpenAI Operator", "fax (legado)"]
people: ["Tenor", "Anthropic", "OpenAI", "Bureau of Labor Statistics"]
claims: ["RPA quebra em qualquer desvio do processo padronizado (nome mal escrito, mudança de posição de um box de login), deixando ~20% do trabalho ainda manual e exigindo reter equipe de back-office", "Agentes inteligentes com LLMs conseguem processar dados não estruturados e coletar contexto para decidir a próxima ação, viabilizando automação ponta a ponta que o RPA não cobria", "Comece com um único fluxo vertical de alto volume e altamente manual, domine-o com integrações profundas nos sistemas-core do setor, e só depois expanda para fluxos adjacentes", "Existe oportunidade horizontal em componentes como extração de dados não estruturados que quase todo pipeline de automação inteligente precisa", "Priorize fluxos geradores de receita em que o cliente era limitado por capacidade de processamento (ex.: pedidos por voz, gestão de referências) — o ROI é venda óbvia", "Uma UI self-serve de arrastar-e-soltar que esconde complexidade elimina o custo e o gargalo dos consultores de implementação exigidos pelo RPA", "Dimensione o mercado contra dados de mão de obra (ex.: BLS) e não contra a receita dos incumbentes de software, que historicamente subestimam o TAM por não alcançarem a longa cauda", "Startups de automação inteligente devem alavancar a pesquisa dos grandes labs (computer use, Operator) em vez de fazer pesquisa fundamental própria, focando nos nichos que os labs não atacarão", "Entrar agora com um agente vertical de ROI óbvio garante o 'direito de vencer' para assumir tarefas de mão de obra cada vez mais core ao longo de 5–10 anos", "Construtores devem mirar tarefas e indústrias que o RPA nunca pôde atacar, com paradigmas limpos de UI/UX específicos para cada fluxo"]
deep_dive: "medium"
deep_dive_reason: "Tese de mercado e investimento com direcionamento tático claro (vertical-first, fluxos geradores de receita, sizing por orçamento de mão de obra), mas sem densidade técnica ou novidade arquitetural em harness, context-engineering, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-agentic-ai-how-bots-came-for-our-workflows-and-drudgery-ft-working-it--e85AxYW0Qyk|Agentic AI - how bots came for our workflows and drudgery | FT Working It]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-tools-for-forward-deployed-engineering-vasuman-moza-varick-agents--l0FLhNqBOic|AI tools for Forward Deployed Engineering — Vasuman Moza, Varick Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-26-key-takeaways-from-building-150-agents-in-9-months--jmeGqDu4tPU|26 Key Takeaways from Building 150+ Agents in 9 months]]", "[[extracts/youtube/ai-learning/2026-09-11-o-treinamento-secreto-da-ia-que-vai-mudar-tudo-vetto-ai--Z4BXg02i8sI|O treinamento secreto da IA que vai mudar tudo | Vetto AI]]", "[[extracts/youtube/ai-learning/2026-09-11-startup-ideas-you-can-now-build-with-ai--K4s6Cgicw_A|Startup Ideas You Can Now Build With AI]]", "[[extracts/youtube/ai-learning/2026-09-11-why-enterprise-ai-adoption-is-slower-than-you-think-aaron-levie-box-harrison-cha--agSRMrhNTf4|Why Enterprise AI Adoption Is Slower Than You Think — Aaron Levie (Box) + Harrison Chase]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-harvard-professor-reveals-the-hidden-ai-formula-for-explosive-startup-growth--wNUIhCI_jsw|Ex-Harvard Professor Reveals the Hidden AI Formula for Explosive Startup Growth]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt4v-puppeteer-ai-agent-browse-web-like-human--IXRkmqEYGZA|GPT4V + Puppeteer = AI agent browse web like human? 🤖]]", "[[extracts/youtube/ai-learning/2026-09-11-how-ai-is-disrupting-a-1-8-trillion-market--iBBOLjt8haY|How AI Is Disrupting a $1.8 Trillion Market]]"]
---

# RIP to RPA: How AI Makes Operations Work

## Tese
RPA determinístico falha na cauda longa de processos bagunçados, e agentes de IA verticais baseados em LLMs — capazes de processar dados não estruturados e coletar contexto dinamicamente — podem automatizar trabalho de back-office que o software nunca alcançou, tornando o orçamento de mão de obra (não o de software) o verdadeiro mercado.

## Conceitos-chave
- RPA (robotic process automation) determinístico por mimetização de cliques
- falha de RPA em casos de borda e longa cauda (~80/20)
- automação inteligente com LLMs ('LLMs in action')
- agente vertical vs. enabler horizontal de IA
- extração de dados não estruturados para estruturados
- browser/computer-use agents como infraestrutura habilitadora
- gestão de referências médicas por fax como caso de uso
- comparação orçamento de mão de obra vs. orçamento de software
- estratégia de wedge: um fluxo vertical nítido antes de expandir
- fluxos geradores de receita previamente limitados por capacidade
- UI self-serve drag-and-drop substituindo consultores de implementação
- direito de vencer (right to win) via integrações com sistemas core

## Ferramentas & pessoas
**Ferramentas:** RPA, Anthropic Computer Use, OpenAI Operator, fax (legado)

**Pessoas/orgs:** Tenor, Anthropic, OpenAI, Bureau of Labor Statistics

## Claims acionáveis
- RPA quebra em qualquer desvio do processo padronizado (nome mal escrito, mudança de posição de um box de login), deixando ~20% do trabalho ainda manual e exigindo reter equipe de back-office
- Agentes inteligentes com LLMs conseguem processar dados não estruturados e coletar contexto para decidir a próxima ação, viabilizando automação ponta a ponta que o RPA não cobria
- Comece com um único fluxo vertical de alto volume e altamente manual, domine-o com integrações profundas nos sistemas-core do setor, e só depois expanda para fluxos adjacentes
- Existe oportunidade horizontal em componentes como extração de dados não estruturados que quase todo pipeline de automação inteligente precisa
- Priorize fluxos geradores de receita em que o cliente era limitado por capacidade de processamento (ex.: pedidos por voz, gestão de referências) — o ROI é venda óbvia
- Uma UI self-serve de arrastar-e-soltar que esconde complexidade elimina o custo e o gargalo dos consultores de implementação exigidos pelo RPA
- Dimensione o mercado contra dados de mão de obra (ex.: BLS) e não contra a receita dos incumbentes de software, que historicamente subestimam o TAM por não alcançarem a longa cauda
- Startups de automação inteligente devem alavancar a pesquisa dos grandes labs (computer use, Operator) em vez de fazer pesquisa fundamental própria, focando nos nichos que os labs não atacarão
- Entrar agora com um agente vertical de ROI óbvio garante o 'direito de vencer' para assumir tarefas de mão de obra cada vez mais core ao longo de 5–10 anos
- Construtores devem mirar tarefas e indústrias que o RPA nunca pôde atacar, com paradigmas limpos de UI/UX específicos para cada fluxo

> **Deep dive:** `medium` — Tese de mercado e investimento com direcionamento tático claro (vertical-first, fluxos geradores de receita, sizing por orçamento de mão de obra), mas sem densidade técnica ou novidade arquitetural em harness, context-engineering, evals ou governança.
