---
title: "Estudo de Caso 2: Browser DAW (Digital Audio Workstation)"
type: curriculum-case-study
aliases: []
tags: [curriculo-conteudo, caso-de-estudo]
last_updated: 2026-06-10
---
# Estudo de Caso 2: Browser DAW (Digital Audio Workstation)

**Nível de Complexidade:** Nível 3–4  
**Duração de Runtime:** 3h 50min  
**Foco:** State Persistence · File-Based Coordination · Continuous Build

---

## Problema

Construir uma ferramenta de produção musical no browser, com: timeline de áudio, controles de sintetizador, gravação e playback sincronizado. O desafio central não é apenas a complexidade técnica — é a necessidade de que múltiplos agentes compartilhem estado ao longo de horas, sem perder coerência.

---

## Solução: Sistema de 3 Agentes com Estado em Arquivo

Browser DAW: 3-Agent System

├── Planner Agent (estrategista)

│   ├─ Input: Requisitos do projeto musical

│   ├─ Output: Build plan com 4 sprints

│   └─ Tempo: 5 minutos ($0.46)

│

├── Generator Agent (construtor)

│   ├─ Constrói um sprint por vez

│   ├─ Lê e escreve state files continuamente

│   ├─ Sem resets de contexto (modelo Opus 4.6)

│   └─ Tempo: \~90 min por sprint

│

└── Evaluator Agent (crítico)

    ├─ Executa o áudio gerado

    ├─ Testa interações do usuário

    ├─ Avalia contra rubrica

    └─ Tempo: 5–10 min por sprint

---

## Arquitetura de State Persistence

A grande inovação deste caso é o uso de arquivos JSON como fonte de verdade compartilhada entre agentes:

project-files/

│

├── state.json                    \# Estado central do projeto

│   {

│     "project\_name": "Summer Song",

│     "bpm": 120,

│     "tracks": \[

│       {"id": "synth1", "notes": \[...\]},

│       {"id": "drums", "notes": \[...\]}

│     \],

│     "timeline\_length": 8

│   }

│

├── generator\_progress.md         \# Progresso em tempo real

│   "Construindo: Synth controls"

│   "Concluído: Timeline UI, Note entry"

│   "Próximo: Audio playback"

│

├── evaluator\_findings.md         \# Findings do Evaluator

│   "Sprint 1 Results:"

│   "✓ Timeline renderiza 8 compassos"

│   "✗ Notas não sincronizam com playback"

│   "→ Recomendação: Implementar audio clock"

│

└── audit\_log.json                \# Log imutável de mudanças

    \[timestamps de cada alteração de estado\]

**Por que arquivos e não variáveis em memória?** Agentes não compartilham memória entre chamadas. Arquivos são o único canal confiável de comunicação entre agentes independentes — persistem entre sessões, sobrevivem a falhas e criam um audit trail natural.

---

## Sprint Plan (Gerado pelo Planner)

Sprint 1: Timeline UI \+ Note Entry (2h 7min)

  ├─ Componentes: Timeline bar, note grid, input

  ├─ Stack: React \+ Web Audio API

  └─ Contrato: Usuário consegue inserir notas na grid

Sprint 2: Synth Controls \+ Knobs (45min)

  ├─ Componentes: Oscillator controls, envelope

  ├─ Estado: Parâmetros salvos em state.json

  └─ Contrato: Mudanças no synth afetam o som em tempo real

Sprint 3: Recording \+ Playback Sync (45min)

  ├─ Componentes: Record button, playback engine

  ├─ Desafio: Sincronizar audio clock com visual timeline

  └─ Contrato: Playback renderiza exatamente o que foi gravado

---

## Resultados com Breakdown de Custo

Runtime total: 3 horas 50 minutos

Custo total:   $124.70

Breakdown por fase:

├─ Planner:                      5 min    ($0.46)

├─ Generator Sprint 1:          2h 7min   ($71.08)

├─ Evaluator Sprint 1:          8.8 min   ($3.24)

├─ Generator Sprint 2:         45 min     ($25.00)

├─ Evaluator Sprint 2:          5 min     ($1.50)

├─ Generator Sprint 3:         45 min     ($23.00)

└─ Evaluator Sprint 3:          5 min     ($1.42)

Output final:

✓ Timeline editor completo

✓ Synth controls com knobs

✓ Funcionalidade de gravação

✓ Playback com sincronização

✓ UI polida e responsiva

✓ Handles real music workflows

---

## Padrões-Chave Utilizados

1. **Multi-Agent Coordination:** Planner → Generator → Evaluator com responsabilidades claras  
2. **File-Based State:** JSON files persistem estado entre sessões e agentes  
3. **Continuous Build:** Opus 4.6 habilita build de 2+ horas sem reset de contexto  
4. **Progressive Evaluation:** Cada sprint avaliado antes do próximo começar  
5. **Harness Simplification:** Modelo mais capaz reduz overhead de orquestração

---

## Lições Aprendidas

1. **State files são poderosos:** Serialização JSON previne bloat de contexto e cria rastreabilidade  
2. **Continuous build funciona:** Modelos de última geração suportam builds de 2+ horas  
3. **Qualidade melhora com iteração:** Passar por múltiplos sprints gera sistemas coerentes  
4. **Features emergentes:** O Generator adicionou capacidades não previstas no spec original  
5. **Naming é arquitetura:** Bons nomes de arquivo previnem confusão de estado entre agentes

---

## Aplicação no KODA

O padrão DAW mapeia elegantemente para os sistemas do KODA:

| Conceito DAW | Conceito KODA |
| :---- | :---- |
| Timeline | Histórico de conversa (sequencial) |
| Synth controls | Catálogo de produtos (opções configuráveis) |
| Recording | Histórico de pedidos (o que aconteceu) |
| Playback | Replay de conversa (verificação de precisão) |
| state.json | session\_state.json (estado da conversa) |
| audit\_log.json | order\_audit.json (rastreabilidade de pedidos) |

---

---

