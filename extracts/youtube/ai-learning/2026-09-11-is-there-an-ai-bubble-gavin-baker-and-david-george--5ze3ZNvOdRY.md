---
title: "\"Is there an AI bubble?” Gavin Baker and David George"
type: "extract"
source: "youtube"
video_id: "5ze3ZNvOdRY"
url: "https://www.youtube.com/watch?v=5ze3ZNvOdRY"
channel: "a16z"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-is-there-an-ai-bubble-gavin-baker-and-david-george--5ze3ZNvOdRY.txt]]"
tags: ["investimentos", "macroeconomia", "analise", "analise-estrutural", "agents", "stack-tooling"]
thesis: "Não estamos em uma bolha de IA: diferentemente da bolha de telecom de 2000 (com 97% de fibra escura), não existem 'GPUs escuros', o ROIC dos maiores gastadores subiu e o capex é financiado pelas empresas mais lucrativas da história, ainda que os labs de fronteira tenham margens brutas estruturalmente menores e a disputa se concentre em Nvidia vs. Google TPU."
concepts: ["analogia dark fiber vs. GPUs escuros", "ROIC (retorno sobre capital investido) como teste de bolha", "round-tripping de deals", "capex de data centers vs. sistema interestadual dos EUA", "scaling laws e bitter lesson", "test-time compute", "compressão de margem bruta como marca de sucesso em IA", "inovação sustentadora vs. disruptiva (Mag 7)", "flywheel de RL pós-treinamento com base de usuários", "mercadoria vs. silício customizado (ASIC/TPU/Trainium)", "precificação por resultados (outcome-based pricing)", "verified rewards em atendimento ao cliente", "economia de fabricantes de aeronaves vs. companhias aéreas", "humanoides em robótica (aprendizado por vídeo e teleoperação)", "Google como dono do gargalo de distribuição (Chrome)"]
tools: ["ChatGPT", "Gemini", "GPT-5", "Grok", "TPU (Google)", "Trainium (Amazon)", "Chrome", "CUDA", "NVLink", "InfiniBand", "Ethernet", "Cursor", "Figma", "Netscape Navigator", "Optimus (Tesla)"]
people: ["Gavin Baker (Atreides)", "David George (a16z)", "Nvidia", "Google/DeepMind", "Anthropic", "xAI", "OpenAI", "Meta", "Amazon (Annapurna)", "Microsoft", "AMD", "Broadcom", "Marvell", "Intel", "Tesla", "Cisco", "Level 3", "Global Crossing", "WorldCom", "Jensen Huang", "Larry Page", "Mark Zuckerberg", "Elon Musk", "Andrej Karpathy", "Richard Sutton", "Decagon", "IBM"]
claims: ["Use ROIC dos maiores gastadores de GPU (todos públicos) como métrica para julgar bolha: alta de ~10 pontos desde o ramp-up de capex indica ROI positivo até agora", "Compare valuations: Cisco no pico valia 150-180x lucros vs. Nvidia a ~40x, portanto o setup de 2000 não se repete", "Round-tripping Nvidia-OpenAI é objetivo, mas em escala pequena e guiado por dinâmica competitiva contra o TPU do Google, não por necessidade de financiamento", "Espere margens brutas estruturalmente menores em labs de fronteira vs. SaaS (80-90%) devido a scaling laws e test-time compute; trate queda de margem bruta como sinal de adoção real de IA, não de fracasso", "Empresas de SaaS aplicativo com negócios lucrativos existentes deveriam rodar produtos de IA a break-even para alcançar líderes (ex.: desafiar o Cursor em coding) antes que o líder acumule tokens demais", "Reasoning/RL pós-treinamento mudou a economia dos modelos: bases de usuários grandes agora alimentam um flywheel, tornando arriscado apostar contra quem já tem distribuição", "Não use GPT-5 como evidência do fim das scaling laws: é um modelo menor desenhado por economia operacional", "Aposte que a maioria dos programas de ASIC customizados falhará em ~3 anos, especialmente se o Google vender TPUs externamente; Broadcom e AMD estão efetivamente indo ao mercado juntos contra a Nvidia (fabric Ethernet aberto + MI como second source)", "Precificação por resultados deve se expandir: atendimento ao cliente com verified rewards (resolução na primeira chamada) e affiliate fees para agentes de consumo, espremendo a ineficiência da publicidade", "Empresas de IA que lançaram browsers próprios podem se arrepender: o dono do Chrome (5B de usuários) pode entrar depois e melhor", "Em robótica, espere Tesla vs. chineses (como em carros) e considere encerrado o debate humanoides vs. não-humanoides devido ao aprendizado por vídeo e teleoperação por tutores humanos", "Trate IA como potencial inovação sustentadora para a Mag 7 (dados, compute, distribuição, caixa, talento), mas existencial: quem não executar pode virar IBM"]
deep_dive: "medium"
deep_dive_reason: "Contém análise densa e original de estrutura de mercado, chips e modelos de negócio de IA, mas é uma conversa de investimento/macro sem profundidade arquitetural em harness, context-engineering, evals, agent-fleets, governança ou ontologia."
---

# "Is there an AI bubble?” Gavin Baker and David George

## Tese
Não estamos em uma bolha de IA: diferentemente da bolha de telecom de 2000 (com 97% de fibra escura), não existem 'GPUs escuros', o ROIC dos maiores gastadores subiu e o capex é financiado pelas empresas mais lucrativas da história, ainda que os labs de fronteira tenham margens brutas estruturalmente menores e a disputa se concentre em Nvidia vs. Google TPU.

## Conceitos-chave
- analogia dark fiber vs. GPUs escuros
- ROIC (retorno sobre capital investido) como teste de bolha
- round-tripping de deals
- capex de data centers vs. sistema interestadual dos EUA
- scaling laws e bitter lesson
- test-time compute
- compressão de margem bruta como marca de sucesso em IA
- inovação sustentadora vs. disruptiva (Mag 7)
- flywheel de RL pós-treinamento com base de usuários
- mercadoria vs. silício customizado (ASIC/TPU/Trainium)
- precificação por resultados (outcome-based pricing)
- verified rewards em atendimento ao cliente
- economia de fabricantes de aeronaves vs. companhias aéreas
- humanoides em robótica (aprendizado por vídeo e teleoperação)
- Google como dono do gargalo de distribuição (Chrome)

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, Gemini, GPT-5, Grok, TPU (Google), Trainium (Amazon), Chrome, CUDA, NVLink, InfiniBand, Ethernet, Cursor, Figma, Netscape Navigator, Optimus (Tesla)

**Pessoas/orgs:** Gavin Baker (Atreides), David George (a16z), Nvidia, Google/DeepMind, Anthropic, xAI, OpenAI, Meta, Amazon (Annapurna), Microsoft, AMD, Broadcom, Marvell, Intel, Tesla, Cisco, Level 3, Global Crossing, WorldCom, Jensen Huang, Larry Page, Mark Zuckerberg, Elon Musk, Andrej Karpathy, Richard Sutton, Decagon, IBM

## Claims acionáveis
- Use ROIC dos maiores gastadores de GPU (todos públicos) como métrica para julgar bolha: alta de ~10 pontos desde o ramp-up de capex indica ROI positivo até agora
- Compare valuations: Cisco no pico valia 150-180x lucros vs. Nvidia a ~40x, portanto o setup de 2000 não se repete
- Round-tripping Nvidia-OpenAI é objetivo, mas em escala pequena e guiado por dinâmica competitiva contra o TPU do Google, não por necessidade de financiamento
- Espere margens brutas estruturalmente menores em labs de fronteira vs. SaaS (80-90%) devido a scaling laws e test-time compute; trate queda de margem bruta como sinal de adoção real de IA, não de fracasso
- Empresas de SaaS aplicativo com negócios lucrativos existentes deveriam rodar produtos de IA a break-even para alcançar líderes (ex.: desafiar o Cursor em coding) antes que o líder acumule tokens demais
- Reasoning/RL pós-treinamento mudou a economia dos modelos: bases de usuários grandes agora alimentam um flywheel, tornando arriscado apostar contra quem já tem distribuição
- Não use GPT-5 como evidência do fim das scaling laws: é um modelo menor desenhado por economia operacional
- Aposte que a maioria dos programas de ASIC customizados falhará em ~3 anos, especialmente se o Google vender TPUs externamente; Broadcom e AMD estão efetivamente indo ao mercado juntos contra a Nvidia (fabric Ethernet aberto + MI como second source)
- Precificação por resultados deve se expandir: atendimento ao cliente com verified rewards (resolução na primeira chamada) e affiliate fees para agentes de consumo, espremendo a ineficiência da publicidade
- Empresas de IA que lançaram browsers próprios podem se arrepender: o dono do Chrome (5B de usuários) pode entrar depois e melhor
- Em robótica, espere Tesla vs. chineses (como em carros) e considere encerrado o debate humanoides vs. não-humanoides devido ao aprendizado por vídeo e teleoperação por tutores humanos
- Trate IA como potencial inovação sustentadora para a Mag 7 (dados, compute, distribuição, caixa, talento), mas existencial: quem não executar pode virar IBM

> **Deep dive:** `medium` — Contém análise densa e original de estrutura de mercado, chips e modelos de negócio de IA, mas é uma conversa de investimento/macro sem profundidade arquitetural em harness, context-engineering, evals, agent-fleets, governança ou ontologia.
