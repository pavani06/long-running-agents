---
title: "Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering"
type: "extract"
source: "youtube"
video_id: "b2GqTDWtg6s"
url: "https://www.youtube.com/watch?v=b2GqTDWtg6s"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s.txt]]"
tags: ["agents", "multi-agent", "error-handling", "monitoramento", "observability", "governanca", "production", "process", "analise-estrutural", "agent-tooling", "data-platform", "testes-qa"]
thesis: "A experiência da Bloomberg ao escalar produtos agenticos mostra que cada agente deve assumir fragilidade dos sistemas upstream (fazendo suas próprias checagens de segurança em vez de handshakes de release) e que a fatoração da arquitetura e dos times deve começar vertical e só extrair horizontais compartilhados quando os agentes amadurecem."
concepts: ["arquitetura semi-agentic (autonomia parcial por falta de confiança total)", "guardrails como checagens não-opcionais codificadas em múltiplos pontos", "multiplicação de erros em composições de LLMs causando fragilidade", "resiliência downstream vs. comunicação out-of-band de mudanças de versão", "espectro tool vs. agent (paper Cognitive Architectures for Language Agents)", "reverse Conway's law entre software e estrutura organizacional", "times verticalmente vs. horizontalmente alinhados", "quebra de agentes monolíticos em agentes menores especializados", "sumarização de transcrições de earnings calls com QA pré-definida por setor", "decomposição de queries sobre dados estruturados (ex.: CPI dos EUA, mensal vs. trimestral)", "evolução de índices esparsos para densos e híbridos", "circuit breakers, remediação e CI/CD para saídas de IA publicadas"]
tools: ["LLM proprietário da Bloomberg (construído em 2022, paper em 2023)", "ChatGPT", "produto de sentimento de notícias da Bloomberg (2009)", "produto de sumarização de earnings calls", "front-end NLP para ferramentas de dados/analytics", "documentação de API de multiplicação de matrizes (estilo BLAS/GEMM) como referência de robustez"]
people: ["Bloomberg", "Global Head of Engineering da Bloomberg", "grupo de ML da Bloomberg (~400 pessoas, 50 times, Londres/Nova York/Princeton/Toronto)"]
claims: ["Trate sistemas upstream baseados em LLM como frágeis: implemente suas próprias checagens de segurança em vez de depender da acurácia upstream ou de ciclos de release coordenados com consumidores downstream.", "Guardrails (ex.: bloquear pedidos de conselho financeiro, verificar factibilidade) devem ser codificados como chamadas obrigatórias em múltiplos pontos, sem autonomia do agente decidir chamá-los.", "Erros de um único caractere (dados mensais vs. trimestrais) ficam imperceptíveis quando o downstream não expõe a tabela, então exponha dados intermediários para permitir detecção humana de erros compostos.", "Melhorias upstream 'melhores na média' não garantem melhora para o caso de uso específico de cada consumidor downstream.", "Comece com times verticalmente alinhados e stack colapsada para iterar rápido; extraia horizontais compartilhados (ex.: guardrails) apenas depois de entender o que cada agente faz bem e onde falha.", "Saídas de IA publicadas e idênticas para todos os clientes exigem monitoramento contínuo, workflows de remediação, circuit breakers e CI/CD, pois erros têm impacto desproporcional.", "Adotar vocabulário compartilhado (tool vs. agent) via paper de referência alinha a organização internamente.", "Estratégia de pivot: construir sobre modelos open-weight disponíveis em vez de treinar LLM próprio, dado o avanço da comunidade open source.", "Agentes monolíticos devem ser fatorados em agentes especializados (ex.: compreensão de query/contexto de sessão e decisão de informações necessárias; geração de resposta bem-formada) refletindo isso na estrutura de times.", "Non-negotiables do domínio (precisão, completude, disponibilidade, proteção de dados de contribuidores/clientes, transparência) devem ser respeitados independentemente do uso de IA."]
deep_dive: "medium"
deep_dive_reason: "A palestra entrega lições práticas valiosas sobre resiliência downstream, guardrails e timing de fatoração organizacional, mas em nível conceitual e confirmatório, sem densidade de detalhes arquiteturais, harness ou evals que justificassem tier alto."
---

# Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering

## Tese
A experiência da Bloomberg ao escalar produtos agenticos mostra que cada agente deve assumir fragilidade dos sistemas upstream (fazendo suas próprias checagens de segurança em vez de handshakes de release) e que a fatoração da arquitetura e dos times deve começar vertical e só extrair horizontais compartilhados quando os agentes amadurecem.

## Conceitos-chave
- arquitetura semi-agentic (autonomia parcial por falta de confiança total)
- guardrails como checagens não-opcionais codificadas em múltiplos pontos
- multiplicação de erros em composições de LLMs causando fragilidade
- resiliência downstream vs. comunicação out-of-band de mudanças de versão
- espectro tool vs. agent (paper Cognitive Architectures for Language Agents)
- reverse Conway's law entre software e estrutura organizacional
- times verticalmente vs. horizontalmente alinhados
- quebra de agentes monolíticos em agentes menores especializados
- sumarização de transcrições de earnings calls com QA pré-definida por setor
- decomposição de queries sobre dados estruturados (ex.: CPI dos EUA, mensal vs. trimestral)
- evolução de índices esparsos para densos e híbridos
- circuit breakers, remediação e CI/CD para saídas de IA publicadas

## Ferramentas & pessoas
**Ferramentas:** LLM proprietário da Bloomberg (construído em 2022, paper em 2023), ChatGPT, produto de sentimento de notícias da Bloomberg (2009), produto de sumarização de earnings calls, front-end NLP para ferramentas de dados/analytics, documentação de API de multiplicação de matrizes (estilo BLAS/GEMM) como referência de robustez

**Pessoas/orgs:** Bloomberg, Global Head of Engineering da Bloomberg, grupo de ML da Bloomberg (~400 pessoas, 50 times, Londres/Nova York/Princeton/Toronto)

## Claims acionáveis
- Trate sistemas upstream baseados em LLM como frágeis: implemente suas próprias checagens de segurança em vez de depender da acurácia upstream ou de ciclos de release coordenados com consumidores downstream.
- Guardrails (ex.: bloquear pedidos de conselho financeiro, verificar factibilidade) devem ser codificados como chamadas obrigatórias em múltiplos pontos, sem autonomia do agente decidir chamá-los.
- Erros de um único caractere (dados mensais vs. trimestrais) ficam imperceptíveis quando o downstream não expõe a tabela, então exponha dados intermediários para permitir detecção humana de erros compostos.
- Melhorias upstream 'melhores na média' não garantem melhora para o caso de uso específico de cada consumidor downstream.
- Comece com times verticalmente alinhados e stack colapsada para iterar rápido; extraia horizontais compartilhados (ex.: guardrails) apenas depois de entender o que cada agente faz bem e onde falha.
- Saídas de IA publicadas e idênticas para todos os clientes exigem monitoramento contínuo, workflows de remediação, circuit breakers e CI/CD, pois erros têm impacto desproporcional.
- Adotar vocabulário compartilhado (tool vs. agent) via paper de referência alinha a organização internamente.
- Estratégia de pivot: construir sobre modelos open-weight disponíveis em vez de treinar LLM próprio, dado o avanço da comunidade open source.
- Agentes monolíticos devem ser fatorados em agentes especializados (ex.: compreensão de query/contexto de sessão e decisão de informações necessárias; geração de resposta bem-formada) refletindo isso na estrutura de times.
- Non-negotiables do domínio (precisão, completude, disponibilidade, proteção de dados de contribuidores/clientes, transparência) devem ser respeitados independentemente do uso de IA.

> **Deep dive:** `medium` — A palestra entrega lições práticas valiosas sobre resiliência downstream, guardrails e timing de fatoração organizacional, mas em nível conceitual e confirmatório, sem densidade de detalhes arquiteturais, harness ou evals que justificassem tier alto.
