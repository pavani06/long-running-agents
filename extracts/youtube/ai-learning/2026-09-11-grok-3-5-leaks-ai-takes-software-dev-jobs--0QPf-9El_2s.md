---
title: "Grok 3.5 Leaks! AI Takes Software Dev Jobs!"
type: "extract"
source: "youtube"
video_id: "0QPf-9El_2s"
url: "https://www.youtube.com/watch?v=0QPf-9El_2s"
channel: "David Shapiro"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-grok-3-5-leaks-ai-takes-software-dev-jobs--0QPf-9El_2s.txt]]"
tags: ["agents", "analise", "macroeconomia", "roadmap", "stack-tooling"]
thesis: "A narrativa sobre IA saiu da bolha de entusiastas para evidências mainstream: AGI virou disputa semântica num gradiente contínuo, vagas de desenvolvedores caíram cerca de 35% abaixo do pré-pandemia com substituição por IA, chatbots cruzaram o abismo de adoção rumo à maioria inicial e computer-using agents em máquinas virtuais são o próximo estágio, com vantagem competitiva definida por escala de compute e dados."
concepts: ["AGI como gradiente contínuo e alvo em movimento (sem definição matemática consensuada)", "fadiga de alarme e negação fora da bolha de entusiastas de IA", "curva de adoção cruzando o abismo (inovadores, adotantes iniciais, maioria inicial, céticos)", "curva sigmoide de adoção cumulativa versus curva de sino da taxa de adoção", "computer-using agents (CUA) como camada de abstração acima dos chatbots", "deploy de agente em máquina virtual dedicada e desktop virtual como serviço", "substituição de trabalhadores por IA e compressão das vagas de nível inicial", "escalada de compute como principal vantagem competitiva em LLMs", "longevity escape velocity e mortalidade por causas exógenas", "vazamentos de benchmarks não confirmados e verificação de fontes"]
tools: ["Indeed (dados de vagas)", "Grok 3.5 (checkpoint inicial vazado, xAI)", "ChatGPT", "GPT-2 / GPT-3 / GPT-3.5 (fine-tuning de chatbots)", "o3 (OpenAI)", "Microsoft Copilot", "Computer Use", "Operator", "VirtualBox", "KVM", "VMware", "Tesla Dojo", "Tesla FSD", "Google Docs (chatbot integrado)", "Twitter/X (fonte de dados de treinamento)"]
people: ["Google DeepMind (CEO)", "Forbes", "xAI", "Elon Musk", "OpenAI", "Sam Altman", "Anthropic", "Ilya Sutskever", "Strawberry Man (leaker no X)", "Gnome Brown (OpenAI, divulgou gráficos)", "DeepSeek", "Qwen (citado como Quinn)", "Tesla"]
claims: ["Postagens de vagas para desenvolvedores de software nos EUA estão a cerca de 63% dos níveis pré-pandemia (queda de ~35%), padrão confirmado globalmente apesar de diferenças metodológicas de coleta de dados.", "O número absoluto de desenvolvedores ainda cresce, mas a apenas 1-2% ao ano, e as primeiras vagas a desaparecer são as de nível inicial, tornando a carreira júnior um caminho de alto risco.", "Os nichos que seguem contratando com força são especialistas de domínio e funções de IA/robótica — recomendação prática para quem entra ou está no setor de software.", "Leak não confirmado de checkpoint inicial do Grok 3.5: AIME24 95% contra 84%, AIME 2025 92%, GPQA Diamond 88%, SimpleQA 58% e MMU acima dos concorrentes, superando o3.", "A vantagem competitiva em modelos migrou de gênios individuais (ex-Ilya na OpenAI) para escala de compute, dados e hyperscaling; a corrida entre empresas dos EUA e da China é o que acelera o ritmo atual.", "Chatbots cruzaram o abismo de adoção: cerca de 70% das empresas Fortune 500 já usam chatbots em pelo menos uma função e a adoção deve atingir ~50% das empresas em 1-2 anos.", "Computer-using agents estão hoje na fase de inovadores; o melhor padrão de deploy previsto é o agente operando sua própria máquina virtual (VirtualBox, KVM, VMware), evoluindo para desktop virtual contratável via web com interface de chat ou voz.", "Eliminando aging e doenças, os EUA manteriam ~85,3 mortes por 100 mil habitantes por causas externas, implicando expectativa de vida de ~800 anos; reduzir para 10-20 por 100 mil elevaria a expectativa para ~7.000 anos.", "Anthropic estaria perdendo market share por reter lançamentos e dobrar a aposta em segurança enquanto OpenAI, xAI e concorrentes chineses correm por participação de mercado."]
deep_dive: "medium"
deep_dive_reason: "Reúne dados acionáveis de mercado de trabalho, um roadmap de adoção e um insight arquitetural leve (CUA em VM dedicada), mas é essencialmente um comentário de notícias sem densidade técnica em harness, context-engineering, evals, agent-fleets ou governança."
---

# Grok 3.5 Leaks! AI Takes Software Dev Jobs!

## Tese
A narrativa sobre IA saiu da bolha de entusiastas para evidências mainstream: AGI virou disputa semântica num gradiente contínuo, vagas de desenvolvedores caíram cerca de 35% abaixo do pré-pandemia com substituição por IA, chatbots cruzaram o abismo de adoção rumo à maioria inicial e computer-using agents em máquinas virtuais são o próximo estágio, com vantagem competitiva definida por escala de compute e dados.

## Conceitos-chave
- AGI como gradiente contínuo e alvo em movimento (sem definição matemática consensuada)
- fadiga de alarme e negação fora da bolha de entusiastas de IA
- curva de adoção cruzando o abismo (inovadores, adotantes iniciais, maioria inicial, céticos)
- curva sigmoide de adoção cumulativa versus curva de sino da taxa de adoção
- computer-using agents (CUA) como camada de abstração acima dos chatbots
- deploy de agente em máquina virtual dedicada e desktop virtual como serviço
- substituição de trabalhadores por IA e compressão das vagas de nível inicial
- escalada de compute como principal vantagem competitiva em LLMs
- longevity escape velocity e mortalidade por causas exógenas
- vazamentos de benchmarks não confirmados e verificação de fontes

## Ferramentas & pessoas
**Ferramentas:** Indeed (dados de vagas), Grok 3.5 (checkpoint inicial vazado, xAI), ChatGPT, GPT-2 / GPT-3 / GPT-3.5 (fine-tuning de chatbots), o3 (OpenAI), Microsoft Copilot, Computer Use, Operator, VirtualBox, KVM, VMware, Tesla Dojo, Tesla FSD, Google Docs (chatbot integrado), Twitter/X (fonte de dados de treinamento)

**Pessoas/orgs:** Google DeepMind (CEO), Forbes, xAI, Elon Musk, OpenAI, Sam Altman, Anthropic, Ilya Sutskever, Strawberry Man (leaker no X), Gnome Brown (OpenAI, divulgou gráficos), DeepSeek, Qwen (citado como Quinn), Tesla

## Claims acionáveis
- Postagens de vagas para desenvolvedores de software nos EUA estão a cerca de 63% dos níveis pré-pandemia (queda de ~35%), padrão confirmado globalmente apesar de diferenças metodológicas de coleta de dados.
- O número absoluto de desenvolvedores ainda cresce, mas a apenas 1-2% ao ano, e as primeiras vagas a desaparecer são as de nível inicial, tornando a carreira júnior um caminho de alto risco.
- Os nichos que seguem contratando com força são especialistas de domínio e funções de IA/robótica — recomendação prática para quem entra ou está no setor de software.
- Leak não confirmado de checkpoint inicial do Grok 3.5: AIME24 95% contra 84%, AIME 2025 92%, GPQA Diamond 88%, SimpleQA 58% e MMU acima dos concorrentes, superando o3.
- A vantagem competitiva em modelos migrou de gênios individuais (ex-Ilya na OpenAI) para escala de compute, dados e hyperscaling; a corrida entre empresas dos EUA e da China é o que acelera o ritmo atual.
- Chatbots cruzaram o abismo de adoção: cerca de 70% das empresas Fortune 500 já usam chatbots em pelo menos uma função e a adoção deve atingir ~50% das empresas em 1-2 anos.
- Computer-using agents estão hoje na fase de inovadores; o melhor padrão de deploy previsto é o agente operando sua própria máquina virtual (VirtualBox, KVM, VMware), evoluindo para desktop virtual contratável via web com interface de chat ou voz.
- Eliminando aging e doenças, os EUA manteriam ~85,3 mortes por 100 mil habitantes por causas externas, implicando expectativa de vida de ~800 anos; reduzir para 10-20 por 100 mil elevaria a expectativa para ~7.000 anos.
- Anthropic estaria perdendo market share por reter lançamentos e dobrar a aposta em segurança enquanto OpenAI, xAI e concorrentes chineses correm por participação de mercado.

> **Deep dive:** `medium` — Reúne dados acionáveis de mercado de trabalho, um roadmap de adoção e um insight arquitetural leve (CUA em VM dedicada), mas é essencialmente um comentário de notícias sem densidade técnica em harness, context-engineering, evals, agent-fleets ou governança.
