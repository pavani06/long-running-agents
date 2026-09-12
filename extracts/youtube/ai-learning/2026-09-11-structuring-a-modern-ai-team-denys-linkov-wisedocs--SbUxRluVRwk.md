---
title: "Structuring a modern AI team — Denys Linkov, Wisedocs"
type: "extract"
source: "youtube"
video_id: "SbUxRluVRwk"
url: "https://www.youtube.com/watch?v=SbUxRluVRwk"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-structuring-a-modern-ai-team-denys-linkov-wisedocs--SbUxRluVRwk.txt]]"
tags: ["agents", "analise-estrutural", "decision-discipline", "evals", "model-selection", "process", "stack-tooling", "governanca"]
thesis: "Estruture sua equipe de IA a partir dos gargalos reais e do domínio do negócio, priorizando generalistas adaptáveis com trade-offs explícitos de habilidades (treinamento, serving, negócio) em vez de pesquisadores de elite."
concepts: ["Anatomia de uma equipe de IA", "Espectro de empresas: tecnologia, verticalizada/serviços, tech-enabled", "Generalistas vs. especialistas", "Eixos de trade-off de habilidades: treinamento de modelos, serving, acumen de negócio", "Inner loop / outer loop da equipe", "Upskilling e reskilling", "Contratar para reter contexto e agir sobre contexto", "Ampere's wager (trocar a equipe por cinco pesquisadores de labs de ponta)", "Blackwell's wager (GPUs vs. equipe)", "Protótipos funcionais substituindo requisitos estáticos de produto", "Domain experts escrevendo casos de uso e evals", "Engenheiros em calls com clientes para encurtar feedback loops", "Cadência semanal de aprendizado", "Responsabilização humana por sistemas de IA", "'Você entrega seu organograma' (efeito Conway)"]
tools: ["ChatGPT", "Hugging Face", "Kubernetes", "APIs de modelos comerciais", "Plataforma MLOps custom/open source", "Shadow deployments e A/B testing"]
people: ["Dennis Linkov", "Wisdocs", "Shopify", "Duolingo", "Zapier", "OpenAI", "Anthropic", "Google", "Palantir", "Y Combinator (YC)", "IBM"]
claims: ["Não contrate pesquisadores de IA antes de atingir escala ou necessidade de especialidade; trabalho de transformação (dados, integração, ROI) vem antes de treinar/fine-tunar modelos", "Identifique o gargalo real (shipping, aquisição, retenção, monetização, escalabilidade, confiabilidade/observabilidade) e contrate de acordo com ele", "Empresas não são uma equipe só: times isolados fazem você 'entregar o organograma' e gerar comportamentos estranhos de produto", "Defina limiares de habilidade por eixo (ex.: fine-tuning de encoders e data engineering com Hugging Face bastam no treinamento) em vez de nota máxima em tudo", "Com o avanço do open source e de modelos comerciais, não é mais preciso escrever a própria plataforma de ML/serving", "Inner loop técnico fraco compromete a execução; loop de domínio fraco impede product-market fit", "Generalistas vencem nas fases iniciais de transformação; especialistas empurram os últimos ~5% de performance em estágios maduros", "Substitua requisitos estáticos por protótipos funcionais que elicitem edge cases e encurtem o feedback loop entre PMs e engenheiros", "Domain experts devem escrever os casos de uso e as evaluations com alfabetização em LLMs, não apenas dar feedback", "Coloque engenheiros em calls com clientes; recusa em falar com cliente é oportunidade de aprendizado", "Institua cadências semanais de 30 minutos de aprendizado sobre prioridades do time e da empresa", "Contrate pessoas por dois motivos: reter contexto e agir sobre contexto — expertise humana é necessária para verificar a execução de agentes", "Humanos devem permanecer responsáveis pelos sistemas construídos ('não se pode responsabilizar uma máquina')", "Verifique tendências por primeiros princípios: a onda 'não contrate juniores' contrasta com a YC reunindo ~2.000 jovens em escola de IA", "Faça perguntas de entrevista relevantes à vaga; LeetCode perdeu valor como avaliação com LLMs resolvendo", "Já se tem ~90% da tecnologia necessária; fax, cheques e a lentidão da digitalização de prontuários médicos mostram que adoção, não tecnologia, é o limite"]
deep_dive: "medium"
deep_dive_reason: "Oferece frameworks acionáveis de desenho de equipe (eixos de trade-off de habilidades, inner/outer loops, contratação orientada a gargalo), mas permanece no nível organizacional/gerencial sem densidade arquitetural ou novidade em harness, context-engineering ou evals de agentes."
---

# Structuring a modern AI team — Denys Linkov, Wisedocs

## Tese
Estruture sua equipe de IA a partir dos gargalos reais e do domínio do negócio, priorizando generalistas adaptáveis com trade-offs explícitos de habilidades (treinamento, serving, negócio) em vez de pesquisadores de elite.

## Conceitos-chave
- Anatomia de uma equipe de IA
- Espectro de empresas: tecnologia, verticalizada/serviços, tech-enabled
- Generalistas vs. especialistas
- Eixos de trade-off de habilidades: treinamento de modelos, serving, acumen de negócio
- Inner loop / outer loop da equipe
- Upskilling e reskilling
- Contratar para reter contexto e agir sobre contexto
- Ampere's wager (trocar a equipe por cinco pesquisadores de labs de ponta)
- Blackwell's wager (GPUs vs. equipe)
- Protótipos funcionais substituindo requisitos estáticos de produto
- Domain experts escrevendo casos de uso e evals
- Engenheiros em calls com clientes para encurtar feedback loops
- Cadência semanal de aprendizado
- Responsabilização humana por sistemas de IA
- 'Você entrega seu organograma' (efeito Conway)

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Hugging Face, Kubernetes, APIs de modelos comerciais, Plataforma MLOps custom/open source, Shadow deployments e A/B testing

**Pessoas/orgs:** Dennis Linkov, Wisdocs, Shopify, Duolingo, Zapier, OpenAI, Anthropic, Google, Palantir, Y Combinator (YC), IBM

## Claims acionáveis
- Não contrate pesquisadores de IA antes de atingir escala ou necessidade de especialidade; trabalho de transformação (dados, integração, ROI) vem antes de treinar/fine-tunar modelos
- Identifique o gargalo real (shipping, aquisição, retenção, monetização, escalabilidade, confiabilidade/observabilidade) e contrate de acordo com ele
- Empresas não são uma equipe só: times isolados fazem você 'entregar o organograma' e gerar comportamentos estranhos de produto
- Defina limiares de habilidade por eixo (ex.: fine-tuning de encoders e data engineering com Hugging Face bastam no treinamento) em vez de nota máxima em tudo
- Com o avanço do open source e de modelos comerciais, não é mais preciso escrever a própria plataforma de ML/serving
- Inner loop técnico fraco compromete a execução; loop de domínio fraco impede product-market fit
- Generalistas vencem nas fases iniciais de transformação; especialistas empurram os últimos ~5% de performance em estágios maduros
- Substitua requisitos estáticos por protótipos funcionais que elicitem edge cases e encurtem o feedback loop entre PMs e engenheiros
- Domain experts devem escrever os casos de uso e as evaluations com alfabetização em LLMs, não apenas dar feedback
- Coloque engenheiros em calls com clientes; recusa em falar com cliente é oportunidade de aprendizado
- Institua cadências semanais de 30 minutos de aprendizado sobre prioridades do time e da empresa
- Contrate pessoas por dois motivos: reter contexto e agir sobre contexto — expertise humana é necessária para verificar a execução de agentes
- Humanos devem permanecer responsáveis pelos sistemas construídos ('não se pode responsabilizar uma máquina')
- Verifique tendências por primeiros princípios: a onda 'não contrate juniores' contrasta com a YC reunindo ~2.000 jovens em escola de IA
- Faça perguntas de entrevista relevantes à vaga; LeetCode perdeu valor como avaliação com LLMs resolvendo
- Já se tem ~90% da tecnologia necessária; fax, cheques e a lentidão da digitalização de prontuários médicos mostram que adoção, não tecnologia, é o limite

> **Deep dive:** `medium` — Oferece frameworks acionáveis de desenho de equipe (eixos de trade-off de habilidades, inner/outer loops, contratação orientada a gargalo), mas permanece no nível organizacional/gerencial sem densidade arquitetural ou novidade em harness, context-engineering ou evals de agentes.
