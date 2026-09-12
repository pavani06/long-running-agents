---
title: "O treinamento secreto da IA que vai mudar tudo | Vetto AI"
type: "extract"
source: "youtube"
video_id: "Z4BXg02i8sI"
url: "https://www.youtube.com/watch?v=Z4BXg02i8sI"
channel: "The Bosses Room"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-o-treinamento-secreto-da-ia-que-vai-mudar-tudo-vetto-ai--Z4BXg02i8sI.txt]]"
tags: ["agents", "agent-tooling", "agentic-coding", "multi-agent", "evals", "data-platform", "knowledge-management", "model-selection", "testes-qa", "verification", "escalation", "governanca", "process", "investimentos", "analise"]
thesis: "O treinamento de modelos de fronteira migrou da entrega de dados brutos para 'receitas' criadas por especialistas de domínio (fluxos ponta a ponta + grades de correção), transformando expertise humana em substrato pago e bem remunerado de treinamento, avaliação e supervisão de modelos e agentes."
concepts: ["Shift de 'bolo' para 'receita': laboratórios agora pedem a metodologia de geração de dados, não só o artefato", "Expert de domínio documentando trajetórias ponta a ponta (ex.: M&A com centenas de passos) marcando certo/errado e generalizável/específico", "Grade de correção (rubric) como conversor de julgamento humano em sinal de treinamento; penalizar resposta certa alcançada por raciocínio errado", "Verificadores e rubricas para evitar colapso em soluções locais/demais específicas e incentivar comportamento generalizável", "Amostragem global de experts para representar realidade distribuída (ex.: regras financeiras não generalizáveis entre países)", "Forças atuais dos modelos: coding e matemática; foco dos labs em problemas de horizonte longo (meses) tipo pesquisa", "Gap persistente em casos agênticos: controle de computador, terminal, APIs, MCP, agentes chamando agentes, exigindo supervisão", "Retorno logarítmico das scaling laws (mais dado/compute = melhoria marginal decrescente)", "Human-in-the-loop como camada permanente: definir qualidade, exceções e accountability (analogia dos radiologistas; humanos pagos para ser accountable em sistemas autônomos, ex.: Waymo)", "Automação de suporte: 80-90% resolvida por IA, ~10% de casos cinzentos escalonados a humanos", "Interfaces: de UI clicável para terminal + API + agentes em VM 24/7 e wearables (óculos como agente audível)", "Ciclo de shipping do Vale (1 feature/dia; réplica de ChatGPT em uma semana) vs. 'AI-first' brasileiro como mero uso de chatbot", "Primeiros princípios como método (anedota da bateria de Musk: custo dos insumos vs. custo de manufatura)"]
tools: ["Veto (empresa de data-for-AI, ex-Start)", "ChatGPT/OpenAI", "Gemini/DeepMind", "Anthropic", "Meta", "Mistral", "Cohere", "xAI", "MCP", "Telegram (bot orquestrando agentes)", "GitHub", "Meta Glasses", "Máquina virtual 24/7 rodando agentes", "Starlink", "Y Combinator (transcrito como 'Wcominator')", "Benchmark de pesquisa em navegador"]
people: ["Alê ('Mega', ITA, Veto)", "Igor (co-host, ex-Kroton/Cogna)", "Bruno (host)", "Elon Musk", "Garry Tan", "João Fonseca", "Waymo", "ITA", "Kroton/Cogna", "James Brown (referência à música The Boss)"]
claims: ["Especialistas podem ganhar €60-100/hora (ou R$200-300 por task aprovada, no caso de travel experts) criando dados de treinamento/avaliação para labs de fronteira via Veto", "Lab clientes têm perfil Anthropic/Meta/DeepMind/OpenAI/Mistral/Cohere/xAI, e a Veto treina os modelos que usuários usam no dia a dia", "Coding e matemática são os pontos fortes atuais dos modelos; nutrição/wellness e domínios 'não rentáveis' ainda performam mal", "Casos de uso agênticos (tool use, controle de computador, orquestração entre agentes) ainda exigem supervisão e estruturas robustas para funcionar", "Em benchmarks de pesquisa em navegador, modelos já performam 80-90% e superam humanos em muitas tarefas, tornando-se úteis no dia a dia corporativo", "Melhoria por dado/compute é logarítmica, mas ainda há quem acredite e invista em scaling laws puras", "O trabalho de expert é definir certo/errado, aceitável/inaceitável e o que é generalizável — inclusive sinalizar etapas em que um humano continua necessário no fluxo", "Suporte ao cliente já opera com 80-90% de automação e ~10% de escalonamento humano para casos-limite", "Workflow pessoal viável hoje: só terminal + APIs (sem UI), bot no Telegram comandando VM com agentes 24/7, e óculos com IA como guia/assistente audível", "No Vale, o padrão de velocidade esperado é ~1 feature/dia por engenheiro e uma réplica completa do ChatGPT em até uma semana; 'AI-first' de verdade é abstrair camadas da empresa em agentes e contratar humanos para supervisioná-los", "Veto já opera em dezenas de milhões de dólares de receita, com Igor investindo indiretamente via fundo", "Combinar pensamento por primeiros princípios com exposição às premissas do Vale é a alavanca recomendada para times brasileiros competirem globalmente"]
deep_dive: "medium"
deep_dive_reason: "Há insights acionáveis e densos sobre geração de dados por experts, rubrics/evals, gaps agênticos e human-in-the-loop, mas o formato é conversacional, com pouca profundidade arquitetural (harness, context-engineering, fleets) e conteúdo parcialmente redundante ou anedótico."
---

# O treinamento secreto da IA que vai mudar tudo | Vetto AI

## Tese
O treinamento de modelos de fronteira migrou da entrega de dados brutos para 'receitas' criadas por especialistas de domínio (fluxos ponta a ponta + grades de correção), transformando expertise humana em substrato pago e bem remunerado de treinamento, avaliação e supervisão de modelos e agentes.

## Conceitos-chave
- Shift de 'bolo' para 'receita': laboratórios agora pedem a metodologia de geração de dados, não só o artefato
- Expert de domínio documentando trajetórias ponta a ponta (ex.: M&A com centenas de passos) marcando certo/errado e generalizável/específico
- Grade de correção (rubric) como conversor de julgamento humano em sinal de treinamento; penalizar resposta certa alcançada por raciocínio errado
- Verificadores e rubricas para evitar colapso em soluções locais/demais específicas e incentivar comportamento generalizável
- Amostragem global de experts para representar realidade distribuída (ex.: regras financeiras não generalizáveis entre países)
- Forças atuais dos modelos: coding e matemática; foco dos labs em problemas de horizonte longo (meses) tipo pesquisa
- Gap persistente em casos agênticos: controle de computador, terminal, APIs, MCP, agentes chamando agentes, exigindo supervisão
- Retorno logarítmico das scaling laws (mais dado/compute = melhoria marginal decrescente)
- Human-in-the-loop como camada permanente: definir qualidade, exceções e accountability (analogia dos radiologistas; humanos pagos para ser accountable em sistemas autônomos, ex.: Waymo)
- Automação de suporte: 80-90% resolvida por IA, ~10% de casos cinzentos escalonados a humanos
- Interfaces: de UI clicável para terminal + API + agentes em VM 24/7 e wearables (óculos como agente audível)
- Ciclo de shipping do Vale (1 feature/dia; réplica de ChatGPT em uma semana) vs. 'AI-first' brasileiro como mero uso de chatbot
- Primeiros princípios como método (anedota da bateria de Musk: custo dos insumos vs. custo de manufatura)

## Ferramentas & pessoas
**Ferramentas:** Veto (empresa de data-for-AI, ex-Start), ChatGPT/OpenAI, Gemini/DeepMind, Anthropic, Meta, Mistral, Cohere, xAI, MCP, Telegram (bot orquestrando agentes), GitHub, Meta Glasses, Máquina virtual 24/7 rodando agentes, Starlink, Y Combinator (transcrito como 'Wcominator'), Benchmark de pesquisa em navegador

**Pessoas/orgs:** Alê ('Mega', ITA, Veto), Igor (co-host, ex-Kroton/Cogna), Bruno (host), Elon Musk, Garry Tan, João Fonseca, Waymo, ITA, Kroton/Cogna, James Brown (referência à música The Boss)

## Claims acionáveis
- Especialistas podem ganhar €60-100/hora (ou R$200-300 por task aprovada, no caso de travel experts) criando dados de treinamento/avaliação para labs de fronteira via Veto
- Lab clientes têm perfil Anthropic/Meta/DeepMind/OpenAI/Mistral/Cohere/xAI, e a Veto treina os modelos que usuários usam no dia a dia
- Coding e matemática são os pontos fortes atuais dos modelos; nutrição/wellness e domínios 'não rentáveis' ainda performam mal
- Casos de uso agênticos (tool use, controle de computador, orquestração entre agentes) ainda exigem supervisão e estruturas robustas para funcionar
- Em benchmarks de pesquisa em navegador, modelos já performam 80-90% e superam humanos em muitas tarefas, tornando-se úteis no dia a dia corporativo
- Melhoria por dado/compute é logarítmica, mas ainda há quem acredite e invista em scaling laws puras
- O trabalho de expert é definir certo/errado, aceitável/inaceitável e o que é generalizável — inclusive sinalizar etapas em que um humano continua necessário no fluxo
- Suporte ao cliente já opera com 80-90% de automação e ~10% de escalonamento humano para casos-limite
- Workflow pessoal viável hoje: só terminal + APIs (sem UI), bot no Telegram comandando VM com agentes 24/7, e óculos com IA como guia/assistente audível
- No Vale, o padrão de velocidade esperado é ~1 feature/dia por engenheiro e uma réplica completa do ChatGPT em até uma semana; 'AI-first' de verdade é abstrair camadas da empresa em agentes e contratar humanos para supervisioná-los
- Veto já opera em dezenas de milhões de dólares de receita, com Igor investindo indiretamente via fundo
- Combinar pensamento por primeiros princípios com exposição às premissas do Vale é a alavanca recomendada para times brasileiros competirem globalmente

> **Deep dive:** `medium` — Há insights acionáveis e densos sobre geração de dados por experts, rubrics/evals, gaps agênticos e human-in-the-loop, mas o formato é conversacional, com pouca profundidade arquitetural (harness, context-engineering, fleets) e conteúdo parcialmente redundante ou anedótico.
