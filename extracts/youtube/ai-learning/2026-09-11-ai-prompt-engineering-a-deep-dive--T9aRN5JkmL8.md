---
title: "AI prompt engineering: A deep dive"
type: "extract"
source: "youtube"
video_id: "T9aRN5JkmL8"
url: "https://www.youtube.com/watch?v=T9aRN5JkmL8"
channel: "Anthropic"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ai-prompt-engineering-a-deep-dive--T9aRN5JkmL8.txt]]"
tags: ["evals", "context-engineering", "verification", "error-handling", "process", "testes-qa", "decision-discipline", "analise"]
thesis: "Prompt engineering é essencialmente comunicação clara somada a disciplina de engenharia experimental — tratar prompts como código, ler outputs de perto, antecipar casos extremos e dar contexto honesto e prescritivo ao modelo em vez de recorrer a truques de persona."
concepts: ["prompt engineering como programação em linguagem natural", "iteração com estado limpo (restart button) como núcleo do lado 'engineering'", "prompts como código: versionamento e rastreamento de experimentos", "edge cases e entradas incomuns na construção de evals", "leitura atenta de outputs do modelo ('look at your data' equivalente)", "teoria da mind: como o modelo interpreta instruções e como usuários reais escrevem", "calibração de confiança e queda de confiabilidade fora de distribuição", "alto sinal por query vs grandes datasets de baixo sinal", "role prompting vs honestidade/prescrição de contexto real", "chain of thought: raciocínio estruturado vs mero espaço de computação", "diferenças de intuição entre modelos pretrained e pós-treinados (RLHF)", "multi-shot prompting menos eficaz em imagens do que em texto", "dar 'saídas' explícitas ao modelo (tags 'unsure') para entradas inesperadas", "analogia da pessoa competente da agência de temp sem contexto da empresa", "transferência de prompt de texto para domínio visual (grade sobre imagem + mapa ASCII)"]
tools: ["Claude", "Claude.ai", "API da Anthropic", "Slack", "Game Boy emulator", "Pokemon Red", "prompt generator da Anthropic", "Streamboard"]
people: ["Anthropic", "Alex (DevRel Anthropic)", "David Hershey", "Amanda Askell", "Zack Witten", "Karpathy", "Stanford (CS231n)"]
claims: ["Trate prompts como código: use controle de versão e rastreie experimentos, pois textos escritos agora operam como software", "Teste explicitamente casos extremos (dataset vazio, padrão ausente, entrada não-dataset) antes de considerar o prompt pronto", "Antes de executar um prompt, peça ao modelo que aponte ambiguidades e lacunas nas instruções sem segui-las — frequentemente revela o que falta", "Quando o modelo erra, pergunte por que errou e peça uma versão editada das instruções; com frequência ele próprio identifica e corrige a falha", "Prefira alguns centenas de testes bem construídos a milhares genéricos: em prompting cada query carrega alto sinal", "Dê ao modelo uma 'saída' explícita (ex.: outputar tag 'unsure') para entradas inesperadas em vez de forçar uma resposta, o que também melhora a qualidade dos dados", "Antecipe o tráfego real dos usuários (typos, sem pontuação, frases soltas) nos evals, não entradas idealizadas", "Seja honesto e prescritivo sobre o contexto real do modelo (produto, empresa, papel na aplicação) em vez de personas genéricas; modelos atuais sabem o que são evals de LLM", "Truque prático: descreva a tarefa a um colega, transcreva o áudio e cole no prompt — frequentemente supera o prompt artesanal", "Use a analogia da pessoa competente de agência de temp sem contexto como primeiro rascunho do prompt", "Verifique lendo os outputs se o modelo realmente cumpre instruções como 'pense passo a passo', em vez de presumir cumprimento literal", "Chain of thought faz trabalho real além de prover espaço de computação: preencher com 'um e ah' por 100 tokens antes de responder não produz o mesmo efeito", "Estruturar e iterar com o modelo sobre como apresentar o raciocínio melhora os resultados", "Intuições de prompting em texto não transferem bem para imagens; multi-shot é menos eficaz em domínio visual", "Não sobreaplique intuições de modelos pretrained a modelos RLHF (ex.: efeito cascata de typos); modelos pós-treinados toleram entradas com erros", "Use modelos pretrained para gerar entradas realistas com typos para testes, já que modelos RLHF são polidos demais para isso", "Reconheça quando desistir: se após um fim de semana de esforço só se avança de 'nenhum sinal' para 'algum sinal' (caso Pokemon), esperar o próximo modelo é melhor investimento de tempo", "A qualidade do prompting pode decidir vida ou morte de um experimento (top 5% vs top 0.1% de performance); invista tempo proporcional ao que dedica ao código"]
deep_dive: "medium"
deep_dive_reason: "Mesa-redonda de praticantes de elite entrega técnicas acionáveis de prompting, evals e calibração de confiança com alguma novidade (experimento Pokemon, teste de preenchimento de tokens), mas permanece no nível de ofício conversacional sem profundidade arquitetural em harness, agent-fleets ou governança."
---

# AI prompt engineering: A deep dive

## Tese
Prompt engineering é essencialmente comunicação clara somada a disciplina de engenharia experimental — tratar prompts como código, ler outputs de perto, antecipar casos extremos e dar contexto honesto e prescritivo ao modelo em vez de recorrer a truques de persona.

## Conceitos-chave
- prompt engineering como programação em linguagem natural
- iteração com estado limpo (restart button) como núcleo do lado 'engineering'
- prompts como código: versionamento e rastreamento de experimentos
- edge cases e entradas incomuns na construção de evals
- leitura atenta de outputs do modelo ('look at your data' equivalente)
- teoria da mind: como o modelo interpreta instruções e como usuários reais escrevem
- calibração de confiança e queda de confiabilidade fora de distribuição
- alto sinal por query vs grandes datasets de baixo sinal
- role prompting vs honestidade/prescrição de contexto real
- chain of thought: raciocínio estruturado vs mero espaço de computação
- diferenças de intuição entre modelos pretrained e pós-treinados (RLHF)
- multi-shot prompting menos eficaz em imagens do que em texto
- dar 'saídas' explícitas ao modelo (tags 'unsure') para entradas inesperadas
- analogia da pessoa competente da agência de temp sem contexto da empresa
- transferência de prompt de texto para domínio visual (grade sobre imagem + mapa ASCII)

## Ferramentas & pessoas
**Ferramentas:** Claude, Claude.ai, API da Anthropic, Slack, Game Boy emulator, Pokemon Red, prompt generator da Anthropic, Streamboard

**Pessoas/orgs:** Anthropic, Alex (DevRel Anthropic), David Hershey, Amanda Askell, Zack Witten, Karpathy, Stanford (CS231n)

## Claims acionáveis
- Trate prompts como código: use controle de versão e rastreie experimentos, pois textos escritos agora operam como software
- Teste explicitamente casos extremos (dataset vazio, padrão ausente, entrada não-dataset) antes de considerar o prompt pronto
- Antes de executar um prompt, peça ao modelo que aponte ambiguidades e lacunas nas instruções sem segui-las — frequentemente revela o que falta
- Quando o modelo erra, pergunte por que errou e peça uma versão editada das instruções; com frequência ele próprio identifica e corrige a falha
- Prefira alguns centenas de testes bem construídos a milhares genéricos: em prompting cada query carrega alto sinal
- Dê ao modelo uma 'saída' explícita (ex.: outputar tag 'unsure') para entradas inesperadas em vez de forçar uma resposta, o que também melhora a qualidade dos dados
- Antecipe o tráfego real dos usuários (typos, sem pontuação, frases soltas) nos evals, não entradas idealizadas
- Seja honesto e prescritivo sobre o contexto real do modelo (produto, empresa, papel na aplicação) em vez de personas genéricas; modelos atuais sabem o que são evals de LLM
- Truque prático: descreva a tarefa a um colega, transcreva o áudio e cole no prompt — frequentemente supera o prompt artesanal
- Use a analogia da pessoa competente de agência de temp sem contexto como primeiro rascunho do prompt
- Verifique lendo os outputs se o modelo realmente cumpre instruções como 'pense passo a passo', em vez de presumir cumprimento literal
- Chain of thought faz trabalho real além de prover espaço de computação: preencher com 'um e ah' por 100 tokens antes de responder não produz o mesmo efeito
- Estruturar e iterar com o modelo sobre como apresentar o raciocínio melhora os resultados
- Intuições de prompting em texto não transferem bem para imagens; multi-shot é menos eficaz em domínio visual
- Não sobreaplique intuições de modelos pretrained a modelos RLHF (ex.: efeito cascata de typos); modelos pós-treinados toleram entradas com erros
- Use modelos pretrained para gerar entradas realistas com typos para testes, já que modelos RLHF são polidos demais para isso
- Reconheça quando desistir: se após um fim de semana de esforço só se avança de 'nenhum sinal' para 'algum sinal' (caso Pokemon), esperar o próximo modelo é melhor investimento de tempo
- A qualidade do prompting pode decidir vida ou morte de um experimento (top 5% vs top 0.1% de performance); invista tempo proporcional ao que dedica ao código

> **Deep dive:** `medium` — Mesa-redonda de praticantes de elite entrega técnicas acionáveis de prompting, evals e calibração de confiança com alguma novidade (experimento Pokemon, teste de preenchimento de tokens), mas permanece no nível de ofício conversacional sem profundidade arquitetural em harness, agent-fleets ou governança.
