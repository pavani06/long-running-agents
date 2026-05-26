# Estudo de Caso 1: Retro Game Maker

**Nível de Complexidade:** Nível 2–3  
**Duração de Runtime:** 6+ horas  
**Foco:** Planner/Generator/Evaluator · Sprint Contracts · Context Management

---

## Problema

Um desenvolvedor precisa construir uma aplicação web de criação de jogos retrô a partir de um único comando: *"Build a retro game maker with sprite editor and level designer."* O escopo é vasto — editor de sprites, designer de fases, modo de jogo, ferramentas de animação e suporte a IA. A tentação natural é atacar tudo de uma vez com um único agente. O resultado foi um fracasso previsível.

---

## Abordagem Inicial (Falha)

Agente Único:

├─ Recebe o prompt

├─ Tenta construir tudo simultaneamente

├─ Contexto esgotado após 2 horas

├─ Resultado: App quebrado e incompleto

└─ Custo: $200 \+ 6 horas desperdiçadas

**Por que falhou:** Um agente único não consegue manter coerência sobre um projeto tão extenso. Sem separação de responsabilidades, o contexto se fragmenta, o código de módulos anteriores é esquecido e a qualidade degrada progressivamente.

---

## Solução: Multi-Agent Harness com Sprint Contracts

A solução dividiu o trabalho em três papéis distintos, operando em ciclos iterativos:

FASE 1 — Planner (5 minutos)

├─ Input: "Build a retro game maker"

├─ Processo: Decompõe em 10 sprints estruturados

├─ Output: spec.md com escopo, critérios de aceitação e sequência

└─ Sprints definidos: Sprite Editor → Level Designer → Play Mode

                     → Animation Tool → Export → AI Assist

                     → Sound → Multiplayer → Marketplace → Polish

FASE 2 — Generator (Sprint 1: 2 horas)

├─ Input: Sprint 1 do spec.md

├─ Processo: Constrói o Sprite Editor com React \+ Canvas

├─ Output: Código funcional \+ documentação do que foi construído

└─ Sem knowledge de sprints futuros (contexto isolado)

FASE 3 — Evaluator (Sprint 1: 10 minutos)

├─ Input: Código do Generator \+ rubrica de aceitação

├─ Processo: Testa se o usuário consegue criar sprites

├─ Grades: Cada critério da rubrica pontuado de 0–10

└─ Output: Aprovado / Ajustes necessários → Generator revisa

REPETE para Sprints 2–10 (total \~4 horas adicionais)

### Sprint Contract (Exemplo — Sprint 1\)

\#\# Sprint 1: Sprite Editor

\#\#\# Input esperado

\- Canvas 16x16 com grid visível

\- Paleta de 16 cores

\#\#\# Critérios de Aceitação

1\. Usuário consegue desenhar pixel a pixel

2\. Ferramenta de borracha funcional

3\. Exportação como PNG

4\. Preview em tamanho real

\#\#\# Definição de "Done"

\- Todos os 4 critérios com nota ≥ 7/10 na avaliação

\- Zero erros no console do browser

---

## Arquitetura

Harness Controller

│

├── spec.md (compartilhado por todos os agentes)

│

├── Sprint Loop (x10)

│   ├── Generator Agent

│   │   ├── Lê: spec.md \+ sprint\_N\_contract.md

│   │   ├── Escreve: sprint\_N\_output/

│   │   └── Contexto resetado a cada sprint

│   │

│   └── Evaluator Agent

│       ├── Lê: sprint\_N\_output/ \+ rubrica

│       ├── Grava: sprint\_N\_eval.md

│       └── Decide: Approve / Request Revision

│

└── Final Assembly Agent

    ├── Integra todos os sprints

    └── Produz: game-maker-final/

---

## Gerenciamento de Estado

project-state/

├── spec.md                    \# Plano mestre (imutável após Fase 1\)

├── sprint\_progress.json       \# Sprint atual, status de cada um

├── sprint\_1\_eval.md           \# Avaliação do Sprint 1

├── sprint\_2\_eval.md           \# Avaliação do Sprint 2

└── sprint\_N\_output/           \# Código gerado por sprint

    ├── index.html

    ├── sprite-editor.js

    └── styles.css

O isolamento de contexto por sprint é a chave: o Generator não carrega o código dos sprints anteriores — apenas o contrato do sprint atual. Isso previne o colapso de contexto que derrubou a abordagem inicial.

---

## Resultados

Abordagem Anterior (Agente Único):

├─ Conclusão: Nunca (contexto esgotado)

├─ Output: App quebrado

├─ Custo: $200 jogados fora

└─ Qualidade: Inutilizável

Abordagem Generator/Evaluator (10 Sprints):

├─ Conclusão: 6 horas de runtime

├─ Output: Game maker completamente funcional

├─ Features: Sprite editor, level designer, play mode, AI assist

├─ Custo: $200 — mas com valor entregue

└─ Qualidade: Coerente, polido, com features extras emergentes

---

## Padrões-Chave Utilizados

1. **Planner:** Decomposição antecipada em 10 sprints com escopo claro  
2. **Sprint Contracts:** Critérios de aceitação explícitos por sprint  
3. **Generator/Evaluator:** Separação entre construção e verificação de qualidade  
4. **Trace Reading:** Debug estruturado quando um sprint falha  
5. **Context Management:** Reset de contexto entre sprints previne degradação

---

## Lições Aprendidas

1. **Planejamento funciona:** A decomposição em sprints preveniu o colapso de contexto fatal  
2. **Separação de concerns:** O Evaluator capturou problemas que o Generator não viu  
3. **Contratos importam:** Critérios claros \= output consistente e previsível  
4. **Iteração vence:** Multi-pass supera amplamente a tentativa única  
5. **Token budgeting:** Sprints evitam o desperdício de contexto acumulado

---

## Aplicação no KODA

Este padrão mapeia diretamente para o ciclo de vendas do KODA no WhatsApp:

- **Planner:** Mapeia a jornada do cliente em etapas (descoberta → recomendação → pedido → fulfillment)  
- **Generator:** Executa cada etapa da conversa com foco total  
- **Evaluator:** Verifica a precisão do pedido antes de enviar para fulfillment  
- **Sprint Contracts:** Define o que "conversa bem-sucedida" significa em cada etapa

---

---

