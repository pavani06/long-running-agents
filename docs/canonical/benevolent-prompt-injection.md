---
title: Benevolent Prompt Injection (proposta)
type: canonical
aliases:
- benevolent prompt injection
tags:
- context-engineering
last_updated: '2026-09-15'
relates-to: []
sources:
- 2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md
---

# Benevolent Prompt Injection (proposta)

**Type:** Canonical Pattern
**Source:** `2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md` — adaptado para long-running-agents
**Classification:** Missing — ausente no repo; originado da análise da fonte (padrão: Benevolent Prompt Injection).

---

## Problema

Sessões de agente começam zeradas: sem memória, sem intenção do projeto, sem convenções. O resultado é trabalho inconsistente entre execuções e saídas de qualidade "de novato" — o agente reinventa decisões já tomadas, ignora padrões estabelecidos e precisa de correção manual repetida. O custo humano se acumula em cada sessão, em vez de ser pago uma única vez.

## Mecanismo

Um hook de início de sessão (start hook) injeta automaticamente um pacote de contexto em toda interação de agente antes de qualquer tarefa. O pacote tipicamente contém:

- Intenção: objetivos do repositório, decisões de arquitetura vigentes, o que é aceito e o que é rejeitado.
- Convenções: estilo, nomenclatura, estrutura de diretórios, padrões de revisão.
- Processo: regras de engajamento — como o agente deve planejar, validar e reportar; o que exige aprovação humana.

A injeção é automática e obrigatória, não opcional. Com isso, toda sessão opera como um engenheiro sênior informado, seguindo processo baseado em regras em vez de heurísticas genéricas de treinamento. O contexto vira código: versionado, revisável e validável.

## Trade-offs

- Qualidade do pacote: a injeção só é tão boa quanto o contexto injetado. Pacote desatualizado produz confiança falsa e decisões erradas em escala.
- Custo de janela: contexto grande consome tokens e reduz espaço para a tarefa; há um teto prático de quanto injetar por sessão.
- Mascarar lacunas: contexto rico pode esconder que o agente não sabe algo — erros de raciocínio ficam mais difíceis de detectar porque a saída parece informada.
- Manutenção: o pacote precisa de dono e ciclo de atualização, senão vira dívida.

## Como se aplicaria aqui

Este repositório teria um artefato de contexto (por exemplo, em docs/canonical/ ou similar) contendo intenção, convenções e processo, e um hook de sessão que o injeta automaticamente em toda execução de agente — CI, coding assistants ou agentes locais. Recomendações de adoção:

1. Definir um único pacote fonte (markdown versionado), nunca contextos paralelos divergentes.
2. Manter o pacote enxuto: intenção e regras de processo, não enciclopédia; medir consumo de tokens por sessão.
3. Validar no CI que o pacote existe, está atualizado (staleness check) e é referenciado pelo hook.
4. Revisar o pacote por PR como qualquer código; mudança de convenção exige atualização simultânea do pacote.
5. Instrumentar falhas: quando o agente erra apesar da injeção, corrigir o pacote, não apenas o prompt pontual.

Estado atual: padrão ausente — esta é uma proposta inicial para discussão via PR; nenhum artefato ou hook correspondente deve ser assumido como existente até aprovado.
