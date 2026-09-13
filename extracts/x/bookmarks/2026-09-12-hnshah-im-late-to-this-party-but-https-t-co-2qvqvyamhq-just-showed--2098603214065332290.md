---
title: "Lançamento agent-native com demo de Excel"
type: "extract"
source: "x"
status_id: "2098603214065332290"
handle: "hnshah"
url: "https://x.com/hnshah/status/2098603214065332290"
created_at: "2026-09-12T02:42:51.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-hnshah-im-late-to-this-party-but-https-t-co-2qvqvyamhq-just-showed--2098603214065332290.json]]"
tags: ["agents", "agent-loop", "context-management", "memory-architecture", "verification"]
topic: "Lançamento agent-native com demo de Excel"
summary: "Tweet destaca um lançamento 'agent-native' em que o agente analisa publicamente um modelo financeiro em Excel e o próprio output vira a demo; o transcript mostra parsing do xlsx, rastreamento de cadeias de fórmulas entre abas e resposta a um cenário what-if sobre ending cash, com caveat explícito e uma limitação clara de reuso de contexto."
key_points: ["Padrão de lançamento agent-native: o agente executa o trabalho em público e o resultado serve como demo, permitindo que qualquer um veja a ferramenta fazer o trabalho antes de tocar o produto.", "Técnica concreta de análise: unzip do xlsx, leitura de workbook.xml/sharedStrings.xml (214 strings indexadas) e construção de mapa de rótulos a partir da coluna A nas 18 abas.", "Rastreamento de cadeias de fórmulas entre 5 abas e 12 trimestres (ex.: 'Operating Expenses'!B10 = B8*B9 ligando Workforce e Assumptions), recalculando o ending cash de Q4 FY27 em $121,3M contra $119,8M do plano.", "Disciplina epistêmica: o agente explicita que o significado de cada linha é inferido da coluna A e nunca declarado no arquivo — limitação declarada em vez de ocultada.", "Limitação estrutural: cenários follow-up não reutilizam nada, porque as cadeias vivem no contexto do agente e não persistem no arquivo — evidência do problema de memória/estado entre consultas."]
entities: ["@hnshah", "Veyra Systems"]
content_type: "tool"
revisit: "medium"
grounded_in: "article"
links: ["https://cfo.ai"]
media: []
---

# Lançamento agent-native com demo de Excel

**@hnshah** · [2098603214065332290](https://x.com/hnshah/status/2098603214065332290) · `tool`

## Resumo
Tweet destaca um lançamento 'agent-native' em que o agente analisa publicamente um modelo financeiro em Excel e o próprio output vira a demo; o transcript mostra parsing do xlsx, rastreamento de cadeias de fórmulas entre abas e resposta a um cenário what-if sobre ending cash, com caveat explícito e uma limitação clara de reuso de contexto.

## Pontos-chave
- Padrão de lançamento agent-native: o agente executa o trabalho em público e o resultado serve como demo, permitindo que qualquer um veja a ferramenta fazer o trabalho antes de tocar o produto.
- Técnica concreta de análise: unzip do xlsx, leitura de workbook.xml/sharedStrings.xml (214 strings indexadas) e construção de mapa de rótulos a partir da coluna A nas 18 abas.
- Rastreamento de cadeias de fórmulas entre 5 abas e 12 trimestres (ex.: 'Operating Expenses'!B10 = B8*B9 ligando Workforce e Assumptions), recalculando o ending cash de Q4 FY27 em $121,3M contra $119,8M do plano.
- Disciplina epistêmica: o agente explicita que o significado de cada linha é inferido da coluna A e nunca declarado no arquivo — limitação declarada em vez de ocultada.
- Limitação estrutural: cenários follow-up não reutilizam nada, porque as cadeias vivem no contexto do agente e não persistem no arquivo — evidência do problema de memória/estado entre consultas.

## Links
- https://cfo.ai

## Entidades
@hnshah, Veyra Systems

> **Revisit:** `medium` · **fonte:** `article`
