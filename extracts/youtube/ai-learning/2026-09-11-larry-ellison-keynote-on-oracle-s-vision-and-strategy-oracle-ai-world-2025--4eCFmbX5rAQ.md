---
title: "Larry Ellison Keynote on Oracle's Vision and Strategy: Oracle AI World 2025"
type: "extract"
source: "youtube"
video_id: "4eCFmbX5rAQ"
url: "https://www.youtube.com/watch?v=4eCFmbX5rAQ"
channel: "Oracle"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-larry-ellison-keynote-on-oracle-s-vision-and-strategy-oracle-ai-world-2025--4eCFmbX5rAQ.txt]]"
tags: ["agents", "agentic-coding", "arquitetura", "context-engineering", "data-platform", "model-selection", "multi-agent", "state", "production", "investimentos", "knowledge-management"]
thesis: "Larry Ellison argumenta que a IA multimodal é a tecnologia de maior valor já criada e que a diferenciação da Oracle está em unir infraestrutura massiva de treinamento (data centers de gigawatts) à capacidade de os modelos raciocinarem sobre dados privados via RAG vetorial no Oracle Database, gerando agentes que automatizam ecossistemas inteiros como o de saúde."
concepts: ["modelos multimodais compostos por múltiplas redes neurais especializadas (CNN para visão, ViT para reconhecimento, transformer para linguagem/raciocínio)", "RAG (Retrieval-Augmented Generation) sobre dados privados", "vetorização de dados e vector index no banco de dados", "raciocínio multietapa (dedução, inferência, cálculo, estratégia, regras)", "modelos em tempo real vs. modelos tolerantes a latência (compute local no carro/robô)", "geração de agentes de IA a partir de linguagem natural (vibe coding) vs. linguagem declarativa", "aplicações geradas stateless, escaláveis, seguras e sem ponto único de falência", "automação de ecossistemas inteiros (paciente, provedor, pagador, regulador, farmacêuticas, bancos, governos)", "acoplamento entre melhor cuidado e reembolso (best possible care fully reimbursable)", "autenticação biométrica substituindo senhas", "monitoramento médico IoT domiciliar e em ambulância", "leitura completa de imagens diagnósticas por IA", "agentes conectados por workflows entre empresas"]
tools: ["Oracle AI Database", "Oracle AI Data Platform", "Oracle Database", "Oracle Cloud Infrastructure (OCI)", "OCI Object Store", "APEX", "NVIDIA GB200", "Grok", "ChatGPT", "Llama", "Gemini", "Claude (Anthropic)", "Tesla Optimus", "Cerner", "Amazon Object Store", "NHS"]
people: ["Larry Ellison", "Oracle", "OpenAI", "Elon Musk", "Sam Altman", "Mark Zuckerberg", "NVIDIA", "Google DeepMind", "Anthropic", "Tesla", "NHS (Reino Unido)", "Ford", "Safra Catz"]
claims: ["O Oracle Database vetoriza dados próprios e externos (OCI Object Store, Amazon) criando vector indexes para que qualquer modelo escolhido (Grok, ChatGPT, Llama, Gemini) raciocine sobre dados privados mantendo-os privados", "A Oracle treinou a primeira versão do Grok e alega treinar mais modelos multimodais que qualquer outra empresa", "O cluster de Abilene, Texas para OpenAI terá 450.000+ NVIDIA GB200s, ~1,2 GW de potência, 8 prédios em 1.000 acres, entregue em menos de um ano com energia da rede e turbinas a gás locais", "Modelos em tempo real (dirigir carros) exigem compute local de baixíssima latência, enquanto geração de código tolera latência de rede", "A maioria das novas aplicações Oracle são agentes gerados por IA conectados por workflows, e por serem gerados são stateless, seguras, escaláveis para milhões de usuários e sem buracos de segurança", "A Oracle adicionou linguagem declarativa de geração por IA ao APEX como alternativa mais precisa ao inglês no vibe coding", "O código do Cerner (25 anos) está sendo reescrito em 3 anos com geração por IA: clínicas prontas, hospitais agudos no próximo ano, mais HR/contabilidade/bancários específicos para hospitais", "O agente de saúde calcula o melhor cuidado totalmente reembolsável cruzando via RAG literatura médica, exames do EHR e regras de seguro/pagador (ex.: NHS não paga Ozempic exceto acima de certo IMC)", "O agente pode fornecer ao banco dados sobre recebíveis de reembolso com probabilidade estimada, viabilizando empréstimos a hospitais com pouco caixa", "Autenticação biométrica (face, voz, digital) pode eliminar senhas e cartões de crédito fraudulentos", "IA lê imagens diagnósticas de forma mais completa e precisa que humanos, encontrando achados que ninguém procurava", "Oracle vetorizou seus próprios dados de clientes e usou RAG para prever quais clientes comprarão qual produto nos próximos seis meses e gerar um agente que envia e-mails com as três melhores referências customizadas"]
deep_dive: "medium"
deep_dive_reason: "Keynote promocional de alto nível, mas com insights arquiteturais moderadamente acionáveis (RAG vetorial no banco de dados, agentes gerados stateless, acoplamento cuidado-reembolso, real-time vs. latência) sem profundidade técnica em harness, evals ou orquestração de frotas de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-satya-nadella-ai-is-the-future-of-the-firm--BKx0Dp8y-6g|Satya Nadella: AI Is the Future of the Firm]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-ms-e435-economics-of-the-ai-supercycle-spring-2026-infrasctructure-ente--sRvrXL83N-c|Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Infrasctructure, Enterprise AI, SaaS]]", "[[extracts/youtube/ai-learning/2026-09-11-microsoft-ceo-satya-nadella-on-the-future-of-ai--w87UvmMcmW4|Microsoft CEO Satya Nadella on the Future of AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-jensen-huang-from-nvidia-on-the-compute-behind-i--tsQB0n0YV3k|Stanford CS153 Frontier Systems | Jensen Huang from NVIDIA on the Compute Behind Intelligence]]"]
theme: "Estratégias corporativas de agentes"
---

# Larry Ellison Keynote on Oracle's Vision and Strategy: Oracle AI World 2025

## Tese
Larry Ellison argumenta que a IA multimodal é a tecnologia de maior valor já criada e que a diferenciação da Oracle está em unir infraestrutura massiva de treinamento (data centers de gigawatts) à capacidade de os modelos raciocinarem sobre dados privados via RAG vetorial no Oracle Database, gerando agentes que automatizam ecossistemas inteiros como o de saúde.

## Conceitos-chave
- modelos multimodais compostos por múltiplas redes neurais especializadas (CNN para visão, ViT para reconhecimento, transformer para linguagem/raciocínio)
- RAG (Retrieval-Augmented Generation) sobre dados privados
- vetorização de dados e vector index no banco de dados
- raciocínio multietapa (dedução, inferência, cálculo, estratégia, regras)
- modelos em tempo real vs. modelos tolerantes a latência (compute local no carro/robô)
- geração de agentes de IA a partir de linguagem natural (vibe coding) vs. linguagem declarativa
- aplicações geradas stateless, escaláveis, seguras e sem ponto único de falência
- automação de ecossistemas inteiros (paciente, provedor, pagador, regulador, farmacêuticas, bancos, governos)
- acoplamento entre melhor cuidado e reembolso (best possible care fully reimbursable)
- autenticação biométrica substituindo senhas
- monitoramento médico IoT domiciliar e em ambulância
- leitura completa de imagens diagnósticas por IA
- agentes conectados por workflows entre empresas

## Ferramentas & pessoas
**Ferramentas:** Oracle AI Database, Oracle AI Data Platform, Oracle Database, Oracle Cloud Infrastructure (OCI), OCI Object Store, APEX, NVIDIA GB200, Grok, ChatGPT, Llama, Gemini, Claude (Anthropic), Tesla Optimus, Cerner, Amazon Object Store, NHS

**Pessoas/orgs:** Larry Ellison, Oracle, OpenAI, Elon Musk, Sam Altman, Mark Zuckerberg, NVIDIA, Google DeepMind, Anthropic, Tesla, NHS (Reino Unido), Ford, Safra Catz

## Claims acionáveis
- O Oracle Database vetoriza dados próprios e externos (OCI Object Store, Amazon) criando vector indexes para que qualquer modelo escolhido (Grok, ChatGPT, Llama, Gemini) raciocine sobre dados privados mantendo-os privados
- A Oracle treinou a primeira versão do Grok e alega treinar mais modelos multimodais que qualquer outra empresa
- O cluster de Abilene, Texas para OpenAI terá 450.000+ NVIDIA GB200s, ~1,2 GW de potência, 8 prédios em 1.000 acres, entregue em menos de um ano com energia da rede e turbinas a gás locais
- Modelos em tempo real (dirigir carros) exigem compute local de baixíssima latência, enquanto geração de código tolera latência de rede
- A maioria das novas aplicações Oracle são agentes gerados por IA conectados por workflows, e por serem gerados são stateless, seguras, escaláveis para milhões de usuários e sem buracos de segurança
- A Oracle adicionou linguagem declarativa de geração por IA ao APEX como alternativa mais precisa ao inglês no vibe coding
- O código do Cerner (25 anos) está sendo reescrito em 3 anos com geração por IA: clínicas prontas, hospitais agudos no próximo ano, mais HR/contabilidade/bancários específicos para hospitais
- O agente de saúde calcula o melhor cuidado totalmente reembolsável cruzando via RAG literatura médica, exames do EHR e regras de seguro/pagador (ex.: NHS não paga Ozempic exceto acima de certo IMC)
- O agente pode fornecer ao banco dados sobre recebíveis de reembolso com probabilidade estimada, viabilizando empréstimos a hospitais com pouco caixa
- Autenticação biométrica (face, voz, digital) pode eliminar senhas e cartões de crédito fraudulentos
- IA lê imagens diagnósticas de forma mais completa e precisa que humanos, encontrando achados que ninguém procurava
- Oracle vetorizou seus próprios dados de clientes e usou RAG para prever quais clientes comprarão qual produto nos próximos seis meses e gerar um agente que envia e-mails com as três melhores referências customizadas

> **Deep dive:** `medium` — Keynote promocional de alto nível, mas com insights arquiteturais moderadamente acionáveis (RAG vetorial no banco de dados, agentes gerados stateless, acoplamento cuidado-reembolso, real-time vs. latência) sem profundidade técnica em harness, evals ou orquestração de frotas de agentes.
