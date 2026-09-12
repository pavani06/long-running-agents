---
title: "Yann LeCun on What Comes After LLMs"
type: "extract"
source: "youtube"
video_id: "ngBraLDqzdI"
url: "https://www.youtube.com/watch?v=ngBraLDqzdI"
channel: "Unsupervised Learning: With Jacob Effron"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI.txt]]"
tags: ["arquitetura", "agents", "agentic-coding", "verification", "governanca", "instituicoes", "data-platform", "roadmap", "analise-estrutural"]
thesis: "LLMs são úteis para manipulação de linguagem, mas não são caminho para inteligência nível humano; sistemas inteligentes exigem modelos de mundo baseados em JEPA capazes de prever consequências de ações e planejar por busca — a tese que LeCun agora escala via AMI Labs."
concepts: ["modelos de mundo como predição das consequências das próprias ações", "JEPA (Joint Embedding Predictive Architecture)", "arquiteturas não-generativas de embedding conjunto vs. generativas", "planejamento por busca/otimaização vs. predição autorregressiva de tokens", "Sistema 1 vs. Sistema 2 (ciência cognitiva)", "limites do aprendizado por imitação e eficiência de dados", "generalização zero-shot de tarefas", "predição em nível de representação abstrata vs. pixels", "VLA (vision-language-action) como fracasso", "linguagem como substrato do raciocínio (matemática e código)", "segurança intrínseca de LLMs e alucinação", "aprendizado federado por consenso de vetores de parâmetros", "soberania de IA e diversidade de assistentes", "modelos fenomenológicos de processos industriais complexos"]
tools: ["JEPA / I-JEPA / V-JEPA", "DINO v1/v2/v3", "MAE (masked autoencoders)", "BERT", "AMI Labs (Advanced Machine Intelligence)", "Tapestry", "GPT-4", "Llama 1/2/3/4", "ChatGPT", "Google Genie", "Linux", "MoCo/SIAM"]
people: ["Yann LeCun", "Meta / FAIR", "GenAI (Meta)", "Mark Zuckerberg", "Andrew Bosworth", "Geoffrey Hinton", "Yoshua Bengio", "OpenAI", "Anthropic", "Google", "Linus Torvalds", "Sun Microsystems", "HP", "Dell", "Microsoft/Azure", "Jerry Torque (ex-OpenAI, citado)"]
claims: ["Sistemas agentivos exigem capacidade de prever consequências das próprias ações e planejar por busca; LLMs autorregressivos não têm nenhuma das duas e por isso não levam a inteligência humanoide", "Arquiteturas de embedding conjunto não-generativas (JEPA, DINO) superam consistentemente abordagens generativas (autoencoders, MAE) para aprender representações de imagens e vídeo", "VLA models são hoje vistos como fracasso — pouco confiáveis e famintos por dados — e robótica por imitação é frágil e cara por tarefa; modelos de mundo permitem planejar tarefas novas com pouco ou nenhum dado", "Planejamento eficiente deve ocorrer em espaço de representações abstratas, não em espaço de tokens; LLMs de código/matemática só 'planejam' via busca em tokens com verificação externa (rodar código, checar prova)", "LLMs brilham exatamente onde a linguagem é o substrato do raciocínio: são bons programadores, mas não arquitetos de software nem cientistas da computação; o trabalho humano sobe um nível de abstração (decidir o que construir)", "LLMs são intrinsecamente inseguros: alucinação não é eliminável e agentes LLM não preveem consequências de ações; coding agents funcionam porque código é verificável contra especificação — o que não se generaliza", "Tapestry: modelo fundacional aberto treinado por aprendizado federado — contribuidores trocam vetores de parâmetros rumo a um consenso global sem expor dados locais, permitindo fine-tuning soberano por idioma, cultura, valores e viés político", "Plataformas tendem naturalmente a abrir (Linux varreu Solaris/HP-UX/Windows NT na infra da internet); OpenAI/Anthropic seriam os Sun Microsystems de ontem, e dados públicos de texto já se esgotaram (resta licenciamento e sintéticos), abrindo espaço para o aberto alcançar a fronteira", "Roadmap AMI: em ~1 ano metodologia geral para treinar modelos JEPA hierárquicos em múltiplas modalidades; em 12–18 meses demos de modelos de mundo condicionados a ação em robótica, controle de processos industriais e saúde; caso de uso precoce é modelar dinâmica de sistemas complexos (motores a jato, plantas químicas, linhas de manufatura, pacientes)", "A percepção de que é preciso mudança de paradigma ficará óbvia para o mercado até o início de 2027", "O alarmismo de risco existencial (ex.: Anthropic) tem motivação comercial para influenciar regulação; o risco real é mau uso humano dos LLMs, não dominação por IA"]
deep_dive: "medium"
deep_dive_reason: "Há densidade apreciável de tese arquitetural (JEPA, planejamento em espaço abstrato, limites agentivos e de segurança dos LLMs) e de mecanismo de plataforma (federado no Tapestry), mas o conteúdo permanece conceitual/estratégico em formato de podcast, sem detalhe operacional de harness, evals ou implementação, e com tom parcialmente promocional da AMI."
---

# Yann LeCun on What Comes After LLMs

## Tese
LLMs são úteis para manipulação de linguagem, mas não são caminho para inteligência nível humano; sistemas inteligentes exigem modelos de mundo baseados em JEPA capazes de prever consequências de ações e planejar por busca — a tese que LeCun agora escala via AMI Labs.

## Conceitos-chave
- modelos de mundo como predição das consequências das próprias ações
- JEPA (Joint Embedding Predictive Architecture)
- arquiteturas não-generativas de embedding conjunto vs. generativas
- planejamento por busca/otimaização vs. predição autorregressiva de tokens
- Sistema 1 vs. Sistema 2 (ciência cognitiva)
- limites do aprendizado por imitação e eficiência de dados
- generalização zero-shot de tarefas
- predição em nível de representação abstrata vs. pixels
- VLA (vision-language-action) como fracasso
- linguagem como substrato do raciocínio (matemática e código)
- segurança intrínseca de LLMs e alucinação
- aprendizado federado por consenso de vetores de parâmetros
- soberania de IA e diversidade de assistentes
- modelos fenomenológicos de processos industriais complexos

## Ferramentas & pessoas
**Ferramentas:** JEPA / I-JEPA / V-JEPA, DINO v1/v2/v3, MAE (masked autoencoders), BERT, AMI Labs (Advanced Machine Intelligence), Tapestry, GPT-4, Llama 1/2/3/4, ChatGPT, Google Genie, Linux, MoCo/SIAM

**Pessoas/orgs:** Yann LeCun, Meta / FAIR, GenAI (Meta), Mark Zuckerberg, Andrew Bosworth, Geoffrey Hinton, Yoshua Bengio, OpenAI, Anthropic, Google, Linus Torvalds, Sun Microsystems, HP, Dell, Microsoft/Azure, Jerry Torque (ex-OpenAI, citado)

## Claims acionáveis
- Sistemas agentivos exigem capacidade de prever consequências das próprias ações e planejar por busca; LLMs autorregressivos não têm nenhuma das duas e por isso não levam a inteligência humanoide
- Arquiteturas de embedding conjunto não-generativas (JEPA, DINO) superam consistentemente abordagens generativas (autoencoders, MAE) para aprender representações de imagens e vídeo
- VLA models são hoje vistos como fracasso — pouco confiáveis e famintos por dados — e robótica por imitação é frágil e cara por tarefa; modelos de mundo permitem planejar tarefas novas com pouco ou nenhum dado
- Planejamento eficiente deve ocorrer em espaço de representações abstratas, não em espaço de tokens; LLMs de código/matemática só 'planejam' via busca em tokens com verificação externa (rodar código, checar prova)
- LLMs brilham exatamente onde a linguagem é o substrato do raciocínio: são bons programadores, mas não arquitetos de software nem cientistas da computação; o trabalho humano sobe um nível de abstração (decidir o que construir)
- LLMs são intrinsecamente inseguros: alucinação não é eliminável e agentes LLM não preveem consequências de ações; coding agents funcionam porque código é verificável contra especificação — o que não se generaliza
- Tapestry: modelo fundacional aberto treinado por aprendizado federado — contribuidores trocam vetores de parâmetros rumo a um consenso global sem expor dados locais, permitindo fine-tuning soberano por idioma, cultura, valores e viés político
- Plataformas tendem naturalmente a abrir (Linux varreu Solaris/HP-UX/Windows NT na infra da internet); OpenAI/Anthropic seriam os Sun Microsystems de ontem, e dados públicos de texto já se esgotaram (resta licenciamento e sintéticos), abrindo espaço para o aberto alcançar a fronteira
- Roadmap AMI: em ~1 ano metodologia geral para treinar modelos JEPA hierárquicos em múltiplas modalidades; em 12–18 meses demos de modelos de mundo condicionados a ação em robótica, controle de processos industriais e saúde; caso de uso precoce é modelar dinâmica de sistemas complexos (motores a jato, plantas químicas, linhas de manufatura, pacientes)
- A percepção de que é preciso mudança de paradigma ficará óbvia para o mercado até o início de 2027
- O alarmismo de risco existencial (ex.: Anthropic) tem motivação comercial para influenciar regulação; o risco real é mau uso humano dos LLMs, não dominação por IA

> **Deep dive:** `medium` — Há densidade apreciável de tese arquitetural (JEPA, planejamento em espaço abstrato, limites agentivos e de segurança dos LLMs) e de mecanismo de plataforma (federado no Tapestry), mas o conteúdo permanece conceitual/estratégico em formato de podcast, sem detalhe operacional de harness, evals ou implementação, e com tom parcialmente promocional da AMI.
