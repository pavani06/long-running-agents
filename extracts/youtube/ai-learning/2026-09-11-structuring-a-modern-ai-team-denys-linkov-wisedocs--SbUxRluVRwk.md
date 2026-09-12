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
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-openais-cpo-on-how-ai-changes-must-have-skills-moats-coding-startup-playbooks-mo--scsW6_2SPC4|OpenAI’s CPO on how AI changes must-have skills, moats, coding, startup playbooks, more | Kevin Weil]]", "[[extracts/youtube/ai-learning/2026-09-11-a-leaders-guide-to-advanced-team-structures-in-an-agentic-world-aws-events--O7u6myBRsns|A leader’s guide to advanced team structures in an agentic world | AWS Events]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-the-ai-native-company-how-one-founder-becomes-a--Lri2LNYtERM|Stanford CS153 Frontier Systems | The AI Native Company: How One Founder Becomes a 1000x Engineer]]", "[[extracts/youtube/ai-learning/2026-09-11-why-netflix-is-betting-on-systems-thinkersnot-specialistsin-the-ai-era-elizabeth--t0GiTyz4syY|Why Netflix is betting on systems thinkers—not specialists—in the AI era | Elizabeth Stone (CPTO)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-o-treinamento-secreto-da-ia-que-vai-mudar-tudo-vetto-ai--Z4BXg02i8sI|O treinamento secreto da IA que vai mudar tudo | Vetto AI]]", "[[extracts/youtube/ai-learning/2026-09-11-how-companies-are-building-their-own-intelligence-sonya-huang-sequoia-capital--bMMv0bZzONg|How Companies Are Building Their Own Intelligence | Sonya Huang, Sequoia Capital]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-harvard-professor-reveals-the-hidden-ai-formula-for-explosive-startup-growth--wNUIhCI_jsw|Ex-Harvard Professor Reveals the Hidden AI Formula for Explosive Startup Growth]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-master-ai-powered-creativity-in-just-13-minutes-jeremy-utley--wv779vmyPVY|How to Master AI Powered Creativity in Just 13 Minutes | Jeremy Utley]]", "[[extracts/youtube/ai-learning/2026-09-11-the-only-trait-for-success-in-the-ai-erahow-to-build-it-carnegie-mellon-universi--xWYb7tImErI|The Only Trait for Success in the AI Era—How to Build It | Carnegie Mellon University Po-Shen Loh]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-read-like-a-pro-with-ai--VeU6gScy92s|How To Read Like A Pro (With AI)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-ai-product-going-viral-with-doctors-openevidence-with-ceo-daniel-nadler--huR0Oa2odxA|The AI Product Going Viral With Doctors: OpenEvidence, with CEO Daniel Nadler]]", "[[extracts/youtube/ai-learning/2026-09-11-ontology-in-ai-the-hidden-skill-that-makes-architecture-and-your-career-work--J0hj0ms2ddo|Ontology in AI: The Hidden Skill That Makes Architecture and Your Career Work]]"]
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
