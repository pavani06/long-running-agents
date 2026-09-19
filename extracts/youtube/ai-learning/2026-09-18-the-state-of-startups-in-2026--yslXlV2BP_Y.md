---
title: "The State of Startups in 2026"
type: "extract"
source: "youtube"
video_id: "yslXlV2BP_Y"
url: "https://www.youtube.com/watch?v=yslXlV2BP_Y"
channel: "Y Combinator"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-18-the-state-of-startups-in-2026--yslXlV2BP_Y.txt]]"
tags: ["analise", "investimentos", "instituicoes", "agentic-coding", "agents", "harness", "model-selection", "data-platform", "macroeconomia"]
thesis: "Agentic coding e modelos cada vez melhores estão reestruturando o ecossistema de startups — deslocando os batches do YC para hard tech (8%→20%), agentes end-to-end que executam o trabalho completo e fundadores solo/experientes — enquanto emerge uma economia stealth de dados e ambientes de RL vendidos aos labs e uma pressão para que systems of record se tornem AI harnesses."
concepts: ["hard tech: 'átomos vs bits'", "agentic coding (pós-Opus 4.5, ~1 ano funcionando)", "agentes end-to-end que 'fazem o trabalho' vs point solutions SaaS", "system of record → AI harness ('harness wars')", "MCP como vetor de comoditização de dados", "venda de dados e ambientes de RL para labs de fronteira", "fine-tuning vertical de modelos-fundação (open-weight quase-fronteira)", "modelos-fundação de robótica e suas diferenças vs LLMs (3D, tempo real)", "fundadores solo e ressurgência do fundador experiente (30-50 anos)", "defesa dual-use e reshoring/manufatura nos EUA", "computação de baixa precisão (FP2, ternário) e switches ópticos em data centers", "data flywheel a partir de transcripts e dados de uso proprietários", "harness + modelo determinam o output (benchmarks sensíveis ao harness)"]
tools: ["Claude Code", "Codex", "OpenCode", "Slack (AI harness)", "MCP", "GPT-6", "Claude Opus 4.5", "Astra (modelo)", "Fable (modelo)", "ARC-AGI-3 (benchmark; transcrito 'RKGI')", "River AI", "Tinker", "Physical Intelligence (π)", "Seedance", "TikTok", "Juicebox", "Exosat", "Beyond Reach Labs", "Icarus", "Nine Mothers", "Nox Metal", "Lamb Labs", "Bot (hardware ternário)", "Dipole Labs", "Boost Robotics", "Ultra", "Praxis Robotics", "Deep Reach", "Human Archive", "Scale", "Mercor", "Datacurve", "Nvidia A100/H100/B300", "Stripe", "Salesforce", "Snowflake", "StarCloud"]
people: ["Y Combinator (The Light Cone)", "Diana (YC)", "Jared Friedman (YC)", "Gary Tan (YC)", "Palmer Luckey", "Anduril", "Peter Steinberger", "Boris Chernyy", "Toby Lütke", "Shopify", "Apoorva Mehta", "Instacart", "Brian Armstrong", "Coinbase", "Parker Conrad", "Paul Graham", "SpaceX", "Nvidia", "Google", "Meta", "Departamento de Guerra dos EUA", "Forças Especiais dos EUA"]
claims: ["Participação de hard tech no batch do YC subiu de 8% para 20% em ~18 meses: robótica 1%→6-7%, manufatura industrial 4%→10%, defesa 1,5%→5%, semicondutores/fotônica 1%→~4%, energia 1%→~3%", "Receita mediana ao fim do batch saltou de US$8K para US$20K MRR, com empresas saindo de zero para 7 dígitos de receita em 3 meses (antes levava ~18+ meses)", "Mais de 12 empresas do YC faturam cada >US$10M/ano vendendo dados ou ambientes de RL aos labs, algumas com centenas de milhões; labs gastariam ~US$1B/ano, incluindo contratos de 8-9 dígitos por dados egocêntricos/robótica", "Systems of record devem se tornar AI harnesses (onde os agentes fazem o trabalho), ou perdem o moat de dados via MCP; Slack + dados de colaboração é o exemplo de mega-moat", "Modelo sozinho não define output: com harness customizado, Astra teria passado de 90% no benchmark (ARC-AGI-3) vs dígitos baixos meses antes", "Empresas 'end-to-end' que executam o trabalho completo subiram de 10% para 25%+ do batch e concentram o crescimento de receita (ex.: corretagem de seguros, intake clínico, billing médico)", "Todas as empresas YC que usam modelos da Physical Intelligence precisam fine-tuná-los por vertical (ex.: cabeamento de data center); fine-tuning de open-weight quase-fronteira com dados proprietários (River AI, Tinker) é a vantagem emergente, potencialmente maior em robótica por restrições de tempo real", "Fundadores solo subiram de 5% para ~18-19% do batch; agentic coding reduz a barra de execução, mas os bem-sucedidos ainda adicionam co-founders após tração, com dinâmica de equity diferente", "Fundadores experientes (30-50 anos, ex.: Peter Steinberger) estão desempenhando melhor porque gestão de engenharia transfere-se à orquestração de ~20 sessões paralelas de agentes de código, e 'saber o que construir' é o high-order bit", "Releases de novos modelos (ex.: GPT-6) consertam retroativamente bugs antes insolúveis; workflow prático: pedir ao agente que revise todos os itens não resolvidos de sessões anteriores", "Preço por hora de A100 aprecia com a demanda; oportunidades ao longo do stack: construção de data centers, energia/baterias, switches ópticos (Dipole Labs) e silício alternativo à Nvidia, incluindo ternário (Bot), já que LLMs toleram FP2", "Startups de defesa dual-use e reshoring crescem a taxas de software (ex.: Nox Metal em Detroit) atendendo compradores de defense-tech ignorados por fornecedores legados — padrão 'Stripe da cadeia de suprimentos de defesa'", "Moats de SaaS permanecem intactos onde o system of record serve clientes-agentes (Salesforce, Snowflake): agentes usarão software muito mais que humanos", "Transcripts de uso proprietários (Claude Code, TikTok→Seedance) estão sendo convertidos em vantagem de treinamento — estratégia replicável de data flywheel"]
deep_dive: "medium"
deep_dive_reason: "Há densidade relevante de estatísticas acionáveis e teses estratégicas (harness como moat, fine-tuning vertical, economia de dados/RL), mas é essencialmente uma análise de tendências de mercado sem profundidade arquitetural em harness, context-engineering ou evals."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-17-the-state-of-ai-models-moats-and-the-consumer-renaissance--zEZ0rQ8Ef-Y|The State of AI: Models, Moats, and the Consumer Renaissance]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-startup-ideas-you-can-now-build-with-ai--K4s6Cgicw_A|Startup Ideas You Can Now Build With AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-ms-e435-economics-of-the-ai-supercycle-spring-2026-infrasctructure-ente--sRvrXL83N-c|Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Infrasctructure, Enterprise AI, SaaS]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-o-treinamento-secreto-da-ia-que-vai-mudar-tudo-vetto-ai--Z4BXg02i8sI|O treinamento secreto da IA que vai mudar tudo | Vetto AI]]", "[[extracts/youtube/ai-learning/2026-09-11-24h-inside-a-30m-silicon-valley-ai-startup-with-no-employees--OpsGJaijG10|24h Inside a $30M Silicon Valley AI Startup with No Employees]]", "[[extracts/youtube/ai-learning/2026-09-11-vertical-ai-agents-could-be-10x-bigger-than-saas--ASABxNenD_U|Vertical AI Agents Could Be 10X Bigger Than SaaS]]", "[[extracts/youtube/ai-learning/2026-09-11-as-tecnologias-que-vao-mudar-o-mundo-na-proxima-decada-market-makers-368--xzp1yHH_vAg|AS TECNOLOGIAS QUE VÃO MUDAR O MUNDO NA PRÓXIMA DÉCADA | Market Makers #368]]", "[[extracts/youtube/ai-learning/2026-09-11-grok-3-5-leaks-ai-takes-software-dev-jobs--0QPf-9El_2s|Grok 3.5 Leaks! AI Takes Software Dev Jobs!]]"]
theme: "Análises do Futuro da IA"
---

# The State of Startups in 2026

## Tese
Agentic coding e modelos cada vez melhores estão reestruturando o ecossistema de startups — deslocando os batches do YC para hard tech (8%→20%), agentes end-to-end que executam o trabalho completo e fundadores solo/experientes — enquanto emerge uma economia stealth de dados e ambientes de RL vendidos aos labs e uma pressão para que systems of record se tornem AI harnesses.

## Conceitos-chave
- hard tech: 'átomos vs bits'
- agentic coding (pós-Opus 4.5, ~1 ano funcionando)
- agentes end-to-end que 'fazem o trabalho' vs point solutions SaaS
- system of record → AI harness ('harness wars')
- MCP como vetor de comoditização de dados
- venda de dados e ambientes de RL para labs de fronteira
- fine-tuning vertical de modelos-fundação (open-weight quase-fronteira)
- modelos-fundação de robótica e suas diferenças vs LLMs (3D, tempo real)
- fundadores solo e ressurgência do fundador experiente (30-50 anos)
- defesa dual-use e reshoring/manufatura nos EUA
- computação de baixa precisão (FP2, ternário) e switches ópticos em data centers
- data flywheel a partir de transcripts e dados de uso proprietários
- harness + modelo determinam o output (benchmarks sensíveis ao harness)

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Codex, OpenCode, Slack (AI harness), MCP, GPT-6, Claude Opus 4.5, Astra (modelo), Fable (modelo), ARC-AGI-3 (benchmark; transcrito 'RKGI'), River AI, Tinker, Physical Intelligence (π), Seedance, TikTok, Juicebox, Exosat, Beyond Reach Labs, Icarus, Nine Mothers, Nox Metal, Lamb Labs, Bot (hardware ternário), Dipole Labs, Boost Robotics, Ultra, Praxis Robotics, Deep Reach, Human Archive, Scale, Mercor, Datacurve, Nvidia A100/H100/B300, Stripe, Salesforce, Snowflake, StarCloud

**Pessoas/orgs:** Y Combinator (The Light Cone), Diana (YC), Jared Friedman (YC), Gary Tan (YC), Palmer Luckey, Anduril, Peter Steinberger, Boris Chernyy, Toby Lütke, Shopify, Apoorva Mehta, Instacart, Brian Armstrong, Coinbase, Parker Conrad, Paul Graham, SpaceX, Nvidia, Google, Meta, Departamento de Guerra dos EUA, Forças Especiais dos EUA

## Claims acionáveis
- Participação de hard tech no batch do YC subiu de 8% para 20% em ~18 meses: robótica 1%→6-7%, manufatura industrial 4%→10%, defesa 1,5%→5%, semicondutores/fotônica 1%→~4%, energia 1%→~3%
- Receita mediana ao fim do batch saltou de US$8K para US$20K MRR, com empresas saindo de zero para 7 dígitos de receita em 3 meses (antes levava ~18+ meses)
- Mais de 12 empresas do YC faturam cada >US$10M/ano vendendo dados ou ambientes de RL aos labs, algumas com centenas de milhões; labs gastariam ~US$1B/ano, incluindo contratos de 8-9 dígitos por dados egocêntricos/robótica
- Systems of record devem se tornar AI harnesses (onde os agentes fazem o trabalho), ou perdem o moat de dados via MCP; Slack + dados de colaboração é o exemplo de mega-moat
- Modelo sozinho não define output: com harness customizado, Astra teria passado de 90% no benchmark (ARC-AGI-3) vs dígitos baixos meses antes
- Empresas 'end-to-end' que executam o trabalho completo subiram de 10% para 25%+ do batch e concentram o crescimento de receita (ex.: corretagem de seguros, intake clínico, billing médico)
- Todas as empresas YC que usam modelos da Physical Intelligence precisam fine-tuná-los por vertical (ex.: cabeamento de data center); fine-tuning de open-weight quase-fronteira com dados proprietários (River AI, Tinker) é a vantagem emergente, potencialmente maior em robótica por restrições de tempo real
- Fundadores solo subiram de 5% para ~18-19% do batch; agentic coding reduz a barra de execução, mas os bem-sucedidos ainda adicionam co-founders após tração, com dinâmica de equity diferente
- Fundadores experientes (30-50 anos, ex.: Peter Steinberger) estão desempenhando melhor porque gestão de engenharia transfere-se à orquestração de ~20 sessões paralelas de agentes de código, e 'saber o que construir' é o high-order bit
- Releases de novos modelos (ex.: GPT-6) consertam retroativamente bugs antes insolúveis; workflow prático: pedir ao agente que revise todos os itens não resolvidos de sessões anteriores
- Preço por hora de A100 aprecia com a demanda; oportunidades ao longo do stack: construção de data centers, energia/baterias, switches ópticos (Dipole Labs) e silício alternativo à Nvidia, incluindo ternário (Bot), já que LLMs toleram FP2
- Startups de defesa dual-use e reshoring crescem a taxas de software (ex.: Nox Metal em Detroit) atendendo compradores de defense-tech ignorados por fornecedores legados — padrão 'Stripe da cadeia de suprimentos de defesa'
- Moats de SaaS permanecem intactos onde o system of record serve clientes-agentes (Salesforce, Snowflake): agentes usarão software muito mais que humanos
- Transcripts de uso proprietários (Claude Code, TikTok→Seedance) estão sendo convertidos em vantagem de treinamento — estratégia replicável de data flywheel

> **Deep dive:** `medium` — Há densidade relevante de estatísticas acionáveis e teses estratégicas (harness como moat, fine-tuning vertical, economia de dados/RL), mas é essencialmente uma análise de tendências de mercado sem profundidade arquitetural em harness, context-engineering ou evals.
