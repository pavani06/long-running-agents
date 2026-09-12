---
title: "Stanford CS153 Frontier Systems | Mati Staniszewski from ElevenLabs on The Future of Voice Systems"
type: "extract"
source: "youtube"
video_id: "vfF011ko89o"
url: "https://www.youtube.com/watch?v=vfF011ko89o"
channel: "Stanford Online"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-cs153-frontier-systems-mati-staniszewski-from-elevenlabs-on-the-future--vfF011ko89o.txt]]"
tags: ["agents", "arquitetura", "context-engineering", "model-selection", "runtime", "production", "governanca", "verification", "tracing", "stack-tooling", "investimentos", "process", "decision-discipline", "analise"]
thesis: "A ElevenLabs escalou de um único componente de text-to-speech para uma plataforma de áudio completa ao preferir arquiteturas em cascata (STT → LLM → TTS) pela confiabilidade enterprise, reservando modelos fundidos para casos guiados por latência, e ancorando precificação no valor entregue ao cliente e não no custo."
concepts: ["dublagem por IA (AI dubbing)", "arquitetura em cascata (transcrição → LLM → TTS)", "modelos fundidos/omni (speech-to-speech direto)", "clonagem e recreação de voz", "expressividade e detecção de emoção no áudio", "tradeoff qualidade/confiabilidade/latência", "fusão de tokens de texto com tokens de áudio", "guardrails e rastreabilidade de etapas do pipeline", "voice marketplace e contribuição da comunidade", "product-led growth (PLG)", "forward-deployed engineering", "precificação orientada a valor (capturar ~1/10 do valor)", "watermarking e detecção de áudio gerado por IA", "abandono de autenticação por voz", "times pequenos (<10 pessoas) com mandato independente", "personalização de preferências de interação por usuário"]
tools: ["ElevenLabs", "Tortoise (tortoise-tts)", "ChatGPT Advanced Voice Mode", "CSM (conversational speech model, open source da Sesame)", "Discord", "Slack", "NVIDIA Inception Program"]
people: ["Mati (fundador/CEO ElevenLabs)", "Piotr (cofundador ElevenLabs)", "Anjney Midha (Anj)", "ElevenLabs", "Discord", "Google", "Palantir", "Nat Friedman", "James Betker", "OpenAI", "Sesame", "Brendan Iribe (ex-Oculus)", "Ankit (ex-Ubiquity6)", "Ubiquity6", "Midjourney", "Anthropic", "Javier Milei", "Lex Fridman", "Zelenskyy", "Narendra Modi", "Deutsche Telekom", "Revolut", "Klarna", "Michael Caine", "Matthew McConaughey", "CS 153"]
claims: ["Comece por um único componente do pipeline (ex.: só o TTS) em vez do sistema completo, para validar simultaneamente potencial de pesquisa e demanda real do cliente", "Para casos enterprise nos próximos anos, prefira arquitetura em cascata: ela permite rastrear o que ocorreu em cada etapa, aplicar guardrails e chamar ferramentas com confiabilidade", "Modelos fundidos vencem em latência (~300ms de resposta) mas sacrificam confiabilidade e capacidade de tool-calling — escolha conforme o caso de uso", "Considere misturar abordagens dentro da mesma interação: fused para consultas informativas, cascata quando houver autenticação ou execução de ações", "Detecte emoções na etapa de transcrição e passe-as como contexto ao LLM para gerar respostas com entrega emocional adequada e controlável", "O gargalo da expressividade é dado rotulado de emoção/entrega — invista em grandes exercícios de rotulagem antes de treinar o modelo", "Em treino de modelos fundidos, a fusão de tokens entre espaço de texto e espaço de áudio é o passo mais difícil, e a dependência de LLMs open-source limita a inteligência do sistema", "Precifique a partir do valor entregue ao cliente (capture cerca de 1/10 dele), nunca a partir do custo de execução", "Forward-deployed engineering junto a grandes clientes torna a receita enterprise previsível; PLG self-serve é menos previsível", "Não use voz como fator de autenticação — sistemas bancários devem abandonar voice authentication", "Bake-in de segurança no próprio modelo (tracabilidade de quem gerou, moderação pré-geração, watermarking, detecção pública de áudio sintético) é a estratégia para deepfakes e licenciamento de vozes", "Mantenha times com menos de 10 pessoas com ownership e decisões independentes — velocidade de aprendizado supera processo formal", "Vozes-agentes podem ser usadas ofensivamente contra golpistas (waste-their-time bots) como contramedida", "Procure créditos gratuitos de compute em programas de aceleração (ex.: NVIDIA Inception) para os primeiros experimentos; modelos pequenos (centenas de milhões de parâmetros) bastam para validar a direção", "Patentes raramente valem a pena em pesquisa que se obsoleta rapidamente; esteja pronto para defender ataques de patent trolls", "Fique próximo da comunidade de criadores/desenvolvedores: casos de uso adotados ali difundem para o resto do mundo 6–18 meses depois"]
deep_dive: "medium"
deep_dive_reason: "Há decisões arquiteturais concretas e acionáveis (cascata vs fundida, os três eixos de tradeoff, fusão de tokens, pipeline de emoção como contexto), mas grande parte do conteúdo é narrativa histórica e métricas promocionais da empresa."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-the-ai-native-company-how-one-founder-becomes-a--Lri2LNYtERM|Stanford CS153 Frontier Systems | The AI Native Company: How One Founder Becomes a 1000x Engineer]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-scale-agi-and-the-future-of-everything--F_7M4Hc-usM|Stanford CS153 Frontier Systems | Scale, AGI, and the Future of Everything]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-webinar-large-language-models-get-the-hype-but-compound-systems-are-the--vRTcE19M-KE|Stanford Webinar - Large Language Models Get the Hype, but Compound Systems Are the Future of AI]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-interfaces-of-the-future-design-review--DBhSfROq3wU|AI Interfaces Of The Future | Design Review]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-andreas-blattmann-from-black-forest-labs-on-visu--CBaLU0dDEY8|Stanford CS153 Frontier Systems | Andreas Blattmann from Black Forest Labs on Visual Intelligence]]"]
theme: "Estratégias corporativas de agentes"
---

# Stanford CS153 Frontier Systems | Mati Staniszewski from ElevenLabs on The Future of Voice Systems

## Tese
A ElevenLabs escalou de um único componente de text-to-speech para uma plataforma de áudio completa ao preferir arquiteturas em cascata (STT → LLM → TTS) pela confiabilidade enterprise, reservando modelos fundidos para casos guiados por latência, e ancorando precificação no valor entregue ao cliente e não no custo.

## Conceitos-chave
- dublagem por IA (AI dubbing)
- arquitetura em cascata (transcrição → LLM → TTS)
- modelos fundidos/omni (speech-to-speech direto)
- clonagem e recreação de voz
- expressividade e detecção de emoção no áudio
- tradeoff qualidade/confiabilidade/latência
- fusão de tokens de texto com tokens de áudio
- guardrails e rastreabilidade de etapas do pipeline
- voice marketplace e contribuição da comunidade
- product-led growth (PLG)
- forward-deployed engineering
- precificação orientada a valor (capturar ~1/10 do valor)
- watermarking e detecção de áudio gerado por IA
- abandono de autenticação por voz
- times pequenos (<10 pessoas) com mandato independente
- personalização de preferências de interação por usuário

## Ferramentas & pessoas
**Ferramentas:** ElevenLabs, Tortoise (tortoise-tts), ChatGPT Advanced Voice Mode, CSM (conversational speech model, open source da Sesame), Discord, Slack, NVIDIA Inception Program

**Pessoas/orgs:** Mati (fundador/CEO ElevenLabs), Piotr (cofundador ElevenLabs), Anjney Midha (Anj), ElevenLabs, Discord, Google, Palantir, Nat Friedman, James Betker, OpenAI, Sesame, Brendan Iribe (ex-Oculus), Ankit (ex-Ubiquity6), Ubiquity6, Midjourney, Anthropic, Javier Milei, Lex Fridman, Zelenskyy, Narendra Modi, Deutsche Telekom, Revolut, Klarna, Michael Caine, Matthew McConaughey, CS 153

## Claims acionáveis
- Comece por um único componente do pipeline (ex.: só o TTS) em vez do sistema completo, para validar simultaneamente potencial de pesquisa e demanda real do cliente
- Para casos enterprise nos próximos anos, prefira arquitetura em cascata: ela permite rastrear o que ocorreu em cada etapa, aplicar guardrails e chamar ferramentas com confiabilidade
- Modelos fundidos vencem em latência (~300ms de resposta) mas sacrificam confiabilidade e capacidade de tool-calling — escolha conforme o caso de uso
- Considere misturar abordagens dentro da mesma interação: fused para consultas informativas, cascata quando houver autenticação ou execução de ações
- Detecte emoções na etapa de transcrição e passe-as como contexto ao LLM para gerar respostas com entrega emocional adequada e controlável
- O gargalo da expressividade é dado rotulado de emoção/entrega — invista em grandes exercícios de rotulagem antes de treinar o modelo
- Em treino de modelos fundidos, a fusão de tokens entre espaço de texto e espaço de áudio é o passo mais difícil, e a dependência de LLMs open-source limita a inteligência do sistema
- Precifique a partir do valor entregue ao cliente (capture cerca de 1/10 dele), nunca a partir do custo de execução
- Forward-deployed engineering junto a grandes clientes torna a receita enterprise previsível; PLG self-serve é menos previsível
- Não use voz como fator de autenticação — sistemas bancários devem abandonar voice authentication
- Bake-in de segurança no próprio modelo (tracabilidade de quem gerou, moderação pré-geração, watermarking, detecção pública de áudio sintético) é a estratégia para deepfakes e licenciamento de vozes
- Mantenha times com menos de 10 pessoas com ownership e decisões independentes — velocidade de aprendizado supera processo formal
- Vozes-agentes podem ser usadas ofensivamente contra golpistas (waste-their-time bots) como contramedida
- Procure créditos gratuitos de compute em programas de aceleração (ex.: NVIDIA Inception) para os primeiros experimentos; modelos pequenos (centenas de milhões de parâmetros) bastam para validar a direção
- Patentes raramente valem a pena em pesquisa que se obsoleta rapidamente; esteja pronto para defender ataques de patent trolls
- Fique próximo da comunidade de criadores/desenvolvedores: casos de uso adotados ali difundem para o resto do mundo 6–18 meses depois

> **Deep dive:** `medium` — Há decisões arquiteturais concretas e acionáveis (cascata vs fundida, os três eixos de tradeoff, fusão de tokens, pipeline de emoção como contexto), mas grande parte do conteúdo é narrativa histórica e métricas promocionais da empresa.
