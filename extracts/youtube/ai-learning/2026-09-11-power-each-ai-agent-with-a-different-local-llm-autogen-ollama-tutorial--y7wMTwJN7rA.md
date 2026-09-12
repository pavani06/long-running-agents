---
title: "Power Each AI Agent With A Different LOCAL LLM (AutoGen + Ollama Tutorial)"
type: "extract"
source: "youtube"
video_id: "y7wMTwJN7rA"
url: "https://www.youtube.com/watch?v=y7wMTwJN7rA"
channel: "Matthew Berman"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-power-each-ai-agent-with-a-different-local-llm-autogen-ollama-tutorial--y7wMTwJN7rA.txt]]"
tags: ["agents", "multi-agent", "frameworks", "model-selection", "agent-tooling", "stack-tooling", "runtime", "arquitetura", "process"]
thesis: "É possível rodar um sistema multiagente do AutoGen inteiramente local em hardware de consumo, conectando cada agente a um modelo open-source distinto (ex.: Mistral como orquestrador e Code Llama como codificador) via Ollama e proxies LiteLLM que expõem endpoints compatíveis com a API da OpenAI."
concepts: ["Multi-agent group chat com GroupChatManager orquestrando agentes", "Roteamento de modelo por agente (modelo geral para orquestração, modelo especializado para código)", "Inferência local de modelos open-source via Ollama com troca de modelos em memória", "Proxy LiteLLM simulando a API da OpenAI em portas separadas por modelo", "User Proxy Agent com execução de código e modos de human_input_mode", "Mensagens de terminação e desafios de tuning com modelos open-source", "Config lists e llm_config por agente no AutoGen", "Ambiente conda e verificação de interpretador Python para dependências pip", "Cache do AutoGen (.cache) interferindo em re-execuções"]
tools: ["AutoGen (pyautogen)", "Ollama", "LiteLLM", "Conda", "Python 3.11", "Visual Studio Code", "Mistral", "Code Llama", "DeepSeek Coder", "WizardCoder", "Orca 2", "StarCoder", "Dolphin 2.2", "Samantha Mistral", "Nous Hermes", "Zephyr", "SQLCoder", "Yi"]
people: ["Eric Hartford"]
claims: ["Cada agente do AutoGen pode ser alimentado por um modelo diferente rodando localmente, permitindo agentes verticalizados com fine-tunes específicos", "LiteLLM envolve o Ollama expondo um endpoint compatível com a API da OpenAI, alocando automaticamente portas distintas (ex.: localhost:8000) para cada modelo servido", "A chave de configuração do AutoGen mudou recentemente para base_url (antes api_url) para apontar o endpoint da API", "Mensagens de terminação exigem ajuste fino com modelos open-source: espaços em branco residuais e falhas do modelo em emitir 'terminate' corretamente causam loops irrelevantes", "Definir human_input_mode='NEVER' no User Proxy Agent faz com que ele execute o código gerado automaticamente sem intervenção humana", "Ollama enfileira múltiplos modelos solicitados simultaneamente e os alterna dentro/fora da memória em 1-2 segundos", "O setup completo funciona em um MacBook Pro M2 Max com 32GB de RAM, sem GPU dedicada", "O GroupChatManager deve usar o modelo geral (Mistral) enquanto agentes especializados usam modelos de domínio como Code Llama", "Deletar a pasta oculta .cache do projeto remove o cache do AutoGen que mascarava resultados de novas execuções", "Instalar via 'python -m pip install' após verificar 'which python' garante que os pacotes vão para o ambiente conda correto"]
deep_dive: "low"
deep_dive_reason: "É um tutorial passo-a-passo de configuração inicial com pouca densidade de insight arquitetural, sem evals, harness, governança ou novidade além do padrão básico de atribuir um modelo por agente, com execuções parcialmente falhas e tuning deixado para um futuro vídeo."
---

# Power Each AI Agent With A Different LOCAL LLM (AutoGen + Ollama Tutorial)

## Tese
É possível rodar um sistema multiagente do AutoGen inteiramente local em hardware de consumo, conectando cada agente a um modelo open-source distinto (ex.: Mistral como orquestrador e Code Llama como codificador) via Ollama e proxies LiteLLM que expõem endpoints compatíveis com a API da OpenAI.

## Conceitos-chave
- Multi-agent group chat com GroupChatManager orquestrando agentes
- Roteamento de modelo por agente (modelo geral para orquestração, modelo especializado para código)
- Inferência local de modelos open-source via Ollama com troca de modelos em memória
- Proxy LiteLLM simulando a API da OpenAI em portas separadas por modelo
- User Proxy Agent com execução de código e modos de human_input_mode
- Mensagens de terminação e desafios de tuning com modelos open-source
- Config lists e llm_config por agente no AutoGen
- Ambiente conda e verificação de interpretador Python para dependências pip
- Cache do AutoGen (.cache) interferindo em re-execuções

## Ferramentas & pessoas
**Ferramentas:** AutoGen (pyautogen), Ollama, LiteLLM, Conda, Python 3.11, Visual Studio Code, Mistral, Code Llama, DeepSeek Coder, WizardCoder, Orca 2, StarCoder, Dolphin 2.2, Samantha Mistral, Nous Hermes, Zephyr, SQLCoder, Yi

**Pessoas/orgs:** Eric Hartford

## Claims acionáveis
- Cada agente do AutoGen pode ser alimentado por um modelo diferente rodando localmente, permitindo agentes verticalizados com fine-tunes específicos
- LiteLLM envolve o Ollama expondo um endpoint compatível com a API da OpenAI, alocando automaticamente portas distintas (ex.: localhost:8000) para cada modelo servido
- A chave de configuração do AutoGen mudou recentemente para base_url (antes api_url) para apontar o endpoint da API
- Mensagens de terminação exigem ajuste fino com modelos open-source: espaços em branco residuais e falhas do modelo em emitir 'terminate' corretamente causam loops irrelevantes
- Definir human_input_mode='NEVER' no User Proxy Agent faz com que ele execute o código gerado automaticamente sem intervenção humana
- Ollama enfileira múltiplos modelos solicitados simultaneamente e os alterna dentro/fora da memória em 1-2 segundos
- O setup completo funciona em um MacBook Pro M2 Max com 32GB de RAM, sem GPU dedicada
- O GroupChatManager deve usar o modelo geral (Mistral) enquanto agentes especializados usam modelos de domínio como Code Llama
- Deletar a pasta oculta .cache do projeto remove o cache do AutoGen que mascarava resultados de novas execuções
- Instalar via 'python -m pip install' após verificar 'which python' garante que os pacotes vão para o ambiente conda correto

> **Deep dive:** `low` — É um tutorial passo-a-passo de configuração inicial com pouca densidade de insight arquitetural, sem evals, harness, governança ou novidade além do padrão básico de atribuir um modelo por agente, com execuções parcialmente falhas e tuning deixado para um futuro vídeo.
