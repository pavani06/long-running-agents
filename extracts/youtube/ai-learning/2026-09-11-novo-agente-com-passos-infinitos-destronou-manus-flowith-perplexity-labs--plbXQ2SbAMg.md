---
title: "NOVO AGENTE com Passos INFINITOS Destronou MANUS? (FLOWITH + Perplexity Labs)"
type: "extract"
source: "youtube"
video_id: "plbXQ2SbAMg"
url: "https://www.youtube.com/watch?v=plbXQ2SbAMg"
channel: "Sancler Miranda"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-novo-agente-com-passos-infinitos-destronou-manus-flowith-perplexity-labs--plbXQ2SbAMg.txt]]"
tags: ["agents", "agent-tooling", "analise", "stack-tooling", "multi-agent", "context-management", "token-budgeting", "knowledge-management", "model-selection"]
thesis: "O vídeo avalia três lançamentos — Perplexity Labs, o agente Flow (Flowith) e a criação de slides no Manus — concluindo que integrações simples como Labs e Manus entregam alto valor por prompt único, enquanto a promessa de 'agentes e contexto infinitos' do Flowith esbarra em custo alto, lentidão, interface bugada e qualidade inferior a ferramentas especializadas."
concepts: ["agentes de IA com múltiplos passos e múltiplas ferramentas", "modo agente (delegação de subtarefas a múltiplos agentes)", "orquestração automática de passos com intervenção humana só em falha", "RAG (retrieval-augmented generation)", "knowledge garden e seeds (equivalentes a chunks de conhecimento)", "compartilhamento/clonagem de bases de conhecimento sem custo de tokens", "token-budgeting via limite de palavras de output (10k/50k) para economizar créditos", "multimodalidade (texto, imagem com logo, vídeo, apps interativos)", "seleção automática de modelo pela plataforma", "ramificação de tópicos em canvas", "generalista vs. ferramenta especializada (trade-off de integração vs. qualidade)", "exportação de artefatos para edição externa (Google Slides, PDF, pptx)"]
tools: ["Perplexity Labs", "Perplexity Pro", "Flowith (Flow)", "Manus", "Lovable", "NotebookLM", "n8n", "Google Slides", "OpenAI GPT-4.1 mini", "Claude Sonnet", "Gemini", "Kling (geração de vídeo)", "Hermes IA (agente de WhatsApp)", "IA Revolution (curso Agentes de IA do Zero)"]
people: ["Sancla Miranda (apresentador)", "Paul Graham", "Derek N (usuário do Flowith)", "Vivo", "OpenAI", "Anthropic", "Google"]
claims: ["No Flowith, desative o agent mode e teste primeiro no modo regular com um modelo barato (GPT-4.1 mini) para minimizar o consumo de créditos", "Configure o limite de output do Flowith para 10.000 ou 50.000 palavras em vez de 'infinito' para conter o gasto de contexto e créditos", "Knowledge gardens clonados de outros usuários no Flowith não consomem seus tokens próprios", "Para landing pages, Lovable produz resultado muito superior ao Flowith com o mesmo prompt; para RAG, NotebookLM e Manus superam o Flowith", "Perplexity Labs gera, a partir de um prompt simples, app interativo + artigo + assets (com código Python dos gráficos), log de tarefas, imagens e lista de fontes citadas, com seleção automática do melhor modelo", "Edições em apps gerados no Perplexity Labs ainda não funcionam: o agente tende a recriar ou interpretar outra coisa em vez de alterar", "No Manus, exporte os slides direto para Google Slides (função nova, antes só pptx/PDF) e edite por lá, pois a edição in-app ainda não permite trocar fontes", "O Flowith é lento mesmo com modelos rápidos, devido às etapas de análise/pensamento e à base de conhecimento embutida no fluxo", "A qualidade do RAG do Flowith está 'beta', com respostas concisas demais e sem link direto para a fonte", "Clientes Vivo podem resgatar 1 ano de Perplexity Pro gratuitamente pelo app da operadora", "O custo do Flowith é elevado: a assinatura de entrada custa US$ 20 e créditos (1.000 no cadastro, 4.000 promocionais não renováveis) se esgotam rapidamente em modo agente"]
deep_dive: "medium"
deep_dive_reason: "É uma análise prática comparativa com dicas acionáveis reais (economia de créditos, limites de contexto, quando preferir ferramenta especializada), mas sem profundidade arquitetural nem novidade em harness, evals ou engenharia de agentes, além de trechos promocionais."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-i-built-a-marketing-team-with-1-ai-agent-and-no-code-free-n8n-template--ldETapkr8Hg|I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-what-will-interrupt-2027-look-like-interrupt-26--R9K2574YEAg|The Future of AI Agents: What Will Interrupt 2027 Look Like? | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-top-4-must-have-ai-agents-for-beginners-easy-setup-guide--4keUCOVpsxQ|Top 4 Must-Have AI Agents for Beginners – Easy Setup Guide]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]"]
---

# NOVO AGENTE com Passos INFINITOS Destronou MANUS? (FLOWITH + Perplexity Labs)

## Tese
O vídeo avalia três lançamentos — Perplexity Labs, o agente Flow (Flowith) e a criação de slides no Manus — concluindo que integrações simples como Labs e Manus entregam alto valor por prompt único, enquanto a promessa de 'agentes e contexto infinitos' do Flowith esbarra em custo alto, lentidão, interface bugada e qualidade inferior a ferramentas especializadas.

## Conceitos-chave
- agentes de IA com múltiplos passos e múltiplas ferramentas
- modo agente (delegação de subtarefas a múltiplos agentes)
- orquestração automática de passos com intervenção humana só em falha
- RAG (retrieval-augmented generation)
- knowledge garden e seeds (equivalentes a chunks de conhecimento)
- compartilhamento/clonagem de bases de conhecimento sem custo de tokens
- token-budgeting via limite de palavras de output (10k/50k) para economizar créditos
- multimodalidade (texto, imagem com logo, vídeo, apps interativos)
- seleção automática de modelo pela plataforma
- ramificação de tópicos em canvas
- generalista vs. ferramenta especializada (trade-off de integração vs. qualidade)
- exportação de artefatos para edição externa (Google Slides, PDF, pptx)

## Ferramentas & pessoas
**Ferramentas:** Perplexity Labs, Perplexity Pro, Flowith (Flow), Manus, Lovable, NotebookLM, n8n, Google Slides, OpenAI GPT-4.1 mini, Claude Sonnet, Gemini, Kling (geração de vídeo), Hermes IA (agente de WhatsApp), IA Revolution (curso Agentes de IA do Zero)

**Pessoas/orgs:** Sancla Miranda (apresentador), Paul Graham, Derek N (usuário do Flowith), Vivo, OpenAI, Anthropic, Google

## Claims acionáveis
- No Flowith, desative o agent mode e teste primeiro no modo regular com um modelo barato (GPT-4.1 mini) para minimizar o consumo de créditos
- Configure o limite de output do Flowith para 10.000 ou 50.000 palavras em vez de 'infinito' para conter o gasto de contexto e créditos
- Knowledge gardens clonados de outros usuários no Flowith não consomem seus tokens próprios
- Para landing pages, Lovable produz resultado muito superior ao Flowith com o mesmo prompt; para RAG, NotebookLM e Manus superam o Flowith
- Perplexity Labs gera, a partir de um prompt simples, app interativo + artigo + assets (com código Python dos gráficos), log de tarefas, imagens e lista de fontes citadas, com seleção automática do melhor modelo
- Edições em apps gerados no Perplexity Labs ainda não funcionam: o agente tende a recriar ou interpretar outra coisa em vez de alterar
- No Manus, exporte os slides direto para Google Slides (função nova, antes só pptx/PDF) e edite por lá, pois a edição in-app ainda não permite trocar fontes
- O Flowith é lento mesmo com modelos rápidos, devido às etapas de análise/pensamento e à base de conhecimento embutida no fluxo
- A qualidade do RAG do Flowith está 'beta', com respostas concisas demais e sem link direto para a fonte
- Clientes Vivo podem resgatar 1 ano de Perplexity Pro gratuitamente pelo app da operadora
- O custo do Flowith é elevado: a assinatura de entrada custa US$ 20 e créditos (1.000 no cadastro, 4.000 promocionais não renováveis) se esgotam rapidamente em modo agente

> **Deep dive:** `medium` — É uma análise prática comparativa com dicas acionáveis reais (economia de créditos, limites de contexto, quando preferir ferramenta especializada), mas sem profundidade arquitetural nem novidade em harness, evals ou engenharia de agentes, além de trechos promocionais.
