---
title: "Stanford CS230 | Autumn 2025 | Lecture 1: Introduction to Deep Learning"
type: "extract"
source: "youtube"
video_id: "_NLHFoVNlbg"
url: "https://www.youtube.com/watch?v=_NLHFoVNlbg"
channel: "Stanford Online"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-cs230-autumn-2025-lecture-1-introduction-to-deep-learning--_NLHFoVNlbg.txt]]"
tags: ["agentic-coding", "agent-tooling", "model-selection", "decision-discipline", "process", "production", "curriculo-conteudo", "investimentos"]
thesis: "Visão geral da primeira aula de CS230 (Stanford, set/2025): Andrew Ng argumenta que fundamentos de CS, ML e deep learning continuam essenciais porque prompting de LLMs não resolve tudo — é preciso descer à camada de deep learning para dados não textuais, para fine-tuning de modelos menores a fim de reduzir custos em escala, e para conduzir desenvolvimento disciplinado de projetos de ML."
concepts: ["scaling laws e previsibilidade de performance com escala de dados/compute", "hierarquia de abstrações: fundamentos de CS → machine learning → deep learning → GenAI (transformers)", "deep learning vs redes neurais como questão de 'branding'", "hyperparameter tuning como habilidade prática decisiva", "processo de desenvolvimento disciplinado para projetos de ML (diagnósticos antes de coletar dados ou comprar GPUs)", "dados estruturados vs não estruturados", "fine-tuning de modelos pré-treinados vs treinamento from scratch vs apenas prompting", "suficiência de dados em projetos greenfield (treinar com pouco dado primeiro para calibrar)", "economia de proof-of-concept (testar ~20 ideias baratas para achar 1-2 boas)", "sandbox para prototipagem rápida com requisitos de segurança reduzidos", "'move fast and be responsible'", "curva de custo de inferência de LLMs em produtos com product-market fit", "flipped classroom", "diferença entre protótipo rápido e software de produção", "o valor de fundamentos de CS para usar bem IA-assistida (analogia com 'linguagem da arte' e Midjourney)"]
tools: ["CUDA / GPUs", "TensorFlow", "PyTorch", "Claude Code", "Gemini CLI", "OpenAI Codex", "Cursor", "Windsurf", "Qodo", "ChatGPT", "Claude", "Gemini", "Meta Llama", "Midjourney", "Slack", "Excel / Google Sheets"]
people: ["Andrew Ng (instrutor, implícito)", "Kian (Katanforoosh, co-instrutor)", "Ian Goodfellow", "Percy Liang", "Tommy Nelson", "Stanford", "Baidu", "OpenAI", "Meta"]
claims: ["Prompting de LLMs resolve bem aplicações de texto; para áudio, imagem/vídeo e dados estruturados, desça à camada de deep learning e treine/fine-tune modelos diretamente", "Quando a conta de LLM explode com o crescimento de usuários, fine-tune modelos menores para dobrar a curva de custo e viabilizar o serviço", "Em projetos greenfield sem referências, colete poucos dados e treine um modelo inicial para calibrar quanta data é realmente necessária (às vezes 100 exemplos bastam)", "Use ambiente sandbox para protótipos locais sem dados sensíveis: requisitos de segurança/escalabilidade podem ser menores, acelerando decisões", "Prefira agentes de coding para protótipos rápidos e seja mais cuidadoso em código de produção (ex.: incidente real de migração de banco que apagou registros)", "Se o custo do proof-of-concept é baixo, não há angst em fazer 20 PoCs para achar as 1-2 ideias que funcionam", "Decisões de projeto ML (coletar mais dados vs comprar GPUs vs mudar arquitetura) devem vir de diagnósticos sistemáticos, não de hype de notícias", "A saída de um sistema ML depende do código (100% controlável) e dos dados (imprevisíveis, 'weird and wonderful') — só construindo o sistema você descobre o que há nos dados", "'Move fast and be responsible': velocidade responsável de execução permite descobrir e corrigir problemas antes", "Construa redes neurais from scratch em Python puro antes de usar frameworks que escondem detalhes", "Scaling laws tornam ganhos de performance previsíveis, o que justificou investimentos em data centers e modelos gigantes", "Habilidade de tuning de hyperparâmetros diferencia engenheiros e determina velocidade de entrega", "Ranking de produtividade: sem experiência e sem IA < 10 anos de experiência sem IA < recém-graduado com IA < 10 anos de experiência com IA", "Não contrate engenheiros que não usam IA-assisted coding; Ng escolheu um quase-graduado fluent em GenAI sobre um full-stack com 10 anos sem IA", "'Não aprenda a programar' é o pior conselho de carreira: quando codar fica mais fácil (punch cards → COBOL → IDEs → IA), mais pessoas deveriam programar", "Empresas não sabem entrevistar para habilidades de GenAI, agravando o gap entre demanda por essas skills e curículos desatualizados"]
deep_dive: "medium"
deep_dive_reason: "Há várias afirmações acionáveis relevantes (fine-tuning para reduzir custo de inferência, sandbox para prototipagem, disciplina de decisão em projetos ML, heurísticas de contratação com agentes de código), mas é uma aula introdutória e parcialmente promocional do curso, sem densidade arquitetural em harness, context-engineering, evals ou governança de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-building-the-real-world-infrastructure-for-ai-with-google-cisco-a16z--OsLRf6r5U9E|Building the Real-World Infrastructure for AI, with Google, Cisco & a16z]]", "[[extracts/youtube/ai-learning/2026-09-11-jeff-dean-the-1-rule-for-building-in-ai--CxXgV54KzpQ|Jeff Dean: The 1% Rule for Building in AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-webinar-large-language-models-get-the-hype-but-compound-systems-are-the--vRTcE19M-KE|Stanford Webinar - Large Language Models Get the Hype, but Compound Systems Are the Future of AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-jensen-huang-from-nvidia-on-the-compute-behind-i--tsQB0n0YV3k|Stanford CS153 Frontier Systems | Jensen Huang from NVIDIA on the Compute Behind Intelligence]]"]
theme: "Estratégias corporativas de agentes"
---

# Stanford CS230 | Autumn 2025 | Lecture 1: Introduction to Deep Learning

## Tese
Visão geral da primeira aula de CS230 (Stanford, set/2025): Andrew Ng argumenta que fundamentos de CS, ML e deep learning continuam essenciais porque prompting de LLMs não resolve tudo — é preciso descer à camada de deep learning para dados não textuais, para fine-tuning de modelos menores a fim de reduzir custos em escala, e para conduzir desenvolvimento disciplinado de projetos de ML.

## Conceitos-chave
- scaling laws e previsibilidade de performance com escala de dados/compute
- hierarquia de abstrações: fundamentos de CS → machine learning → deep learning → GenAI (transformers)
- deep learning vs redes neurais como questão de 'branding'
- hyperparameter tuning como habilidade prática decisiva
- processo de desenvolvimento disciplinado para projetos de ML (diagnósticos antes de coletar dados ou comprar GPUs)
- dados estruturados vs não estruturados
- fine-tuning de modelos pré-treinados vs treinamento from scratch vs apenas prompting
- suficiência de dados em projetos greenfield (treinar com pouco dado primeiro para calibrar)
- economia de proof-of-concept (testar ~20 ideias baratas para achar 1-2 boas)
- sandbox para prototipagem rápida com requisitos de segurança reduzidos
- 'move fast and be responsible'
- curva de custo de inferência de LLMs em produtos com product-market fit
- flipped classroom
- diferença entre protótipo rápido e software de produção
- o valor de fundamentos de CS para usar bem IA-assistida (analogia com 'linguagem da arte' e Midjourney)

## Ferramentas & pessoas
**Ferramentas:** CUDA / GPUs, TensorFlow, PyTorch, Claude Code, Gemini CLI, OpenAI Codex, Cursor, Windsurf, Qodo, ChatGPT, Claude, Gemini, Meta Llama, Midjourney, Slack, Excel / Google Sheets

**Pessoas/orgs:** Andrew Ng (instrutor, implícito), Kian (Katanforoosh, co-instrutor), Ian Goodfellow, Percy Liang, Tommy Nelson, Stanford, Baidu, OpenAI, Meta

## Claims acionáveis
- Prompting de LLMs resolve bem aplicações de texto; para áudio, imagem/vídeo e dados estruturados, desça à camada de deep learning e treine/fine-tune modelos diretamente
- Quando a conta de LLM explode com o crescimento de usuários, fine-tune modelos menores para dobrar a curva de custo e viabilizar o serviço
- Em projetos greenfield sem referências, colete poucos dados e treine um modelo inicial para calibrar quanta data é realmente necessária (às vezes 100 exemplos bastam)
- Use ambiente sandbox para protótipos locais sem dados sensíveis: requisitos de segurança/escalabilidade podem ser menores, acelerando decisões
- Prefira agentes de coding para protótipos rápidos e seja mais cuidadoso em código de produção (ex.: incidente real de migração de banco que apagou registros)
- Se o custo do proof-of-concept é baixo, não há angst em fazer 20 PoCs para achar as 1-2 ideias que funcionam
- Decisões de projeto ML (coletar mais dados vs comprar GPUs vs mudar arquitetura) devem vir de diagnósticos sistemáticos, não de hype de notícias
- A saída de um sistema ML depende do código (100% controlável) e dos dados (imprevisíveis, 'weird and wonderful') — só construindo o sistema você descobre o que há nos dados
- 'Move fast and be responsible': velocidade responsável de execução permite descobrir e corrigir problemas antes
- Construa redes neurais from scratch em Python puro antes de usar frameworks que escondem detalhes
- Scaling laws tornam ganhos de performance previsíveis, o que justificou investimentos em data centers e modelos gigantes
- Habilidade de tuning de hyperparâmetros diferencia engenheiros e determina velocidade de entrega
- Ranking de produtividade: sem experiência e sem IA < 10 anos de experiência sem IA < recém-graduado com IA < 10 anos de experiência com IA
- Não contrate engenheiros que não usam IA-assisted coding; Ng escolheu um quase-graduado fluent em GenAI sobre um full-stack com 10 anos sem IA
- 'Não aprenda a programar' é o pior conselho de carreira: quando codar fica mais fácil (punch cards → COBOL → IDEs → IA), mais pessoas deveriam programar
- Empresas não sabem entrevistar para habilidades de GenAI, agravando o gap entre demanda por essas skills e curículos desatualizados

> **Deep dive:** `medium` — Há várias afirmações acionáveis relevantes (fine-tuning para reduzir custo de inferência, sandbox para prototipagem, disciplina de decisão em projetos ML, heurísticas de contratação com agentes de código), mas é uma aula introdutória e parcialmente promocional do curso, sem densidade arquitetural em harness, context-engineering, evals ou governança de agentes.
