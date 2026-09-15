---
title: Benevolent Prompt Injection
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

# Benevolent Prompt Injection

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

Este repositório já pratica a forma sempre-ligada do padrão: `AGENTS.md` é injetado como regras obrigatórias no início de toda sessão de agente (Rule 0–3 + Project Context) e aponta para guias operacionais em `.opencode/skills/`. Este padrão nomeia essa prática e a estende para injeção ciente-de-tarefa, ancorado nos mecanismos que já existem — sem implementar um novo hook nem criar arquitetura nova.

**Onde o contexto de sessão/projeto já vive**

- `AGENTS.md` — regras mandatórias + Project Context, sempre carregado no começo da sessão (a injeção "sempre-ligada" que já existe hoje).
- `.opencode/skills/` — definições de agente e skills operacionais (ex.: `.opencode/skills/karpathy-guidelines`).
- `docs/decisions/` — ADRs aceitos (o "porquê" das decisões vigentes).
- `docs/system-of-record.md` — precedência entre as camadas de contexto.
- `mapa-mental-repo/` — modelos mentais por fonte (contexto destilado do corpus bruto).
- `docs/canonical/` — padrões curados (incluindo este).

**Quais artefatos um start hook benevolente consumiria**

- Sempre: `AGENTS.md` (regras + Project Context).
- Ciente-de-tarefa: os ADRs relevantes em `docs/decisions/`, os padrões relacionados em `docs/canonical/`, o skill aplicável em `.opencode/skills/` e o modelo mental da fonte em `mapa-mental-repo/`.

**O que seria injetado no início da sessão/agente**

As regras obrigatórias de `AGENTS.md` (já injetadas pelo harness hoje) mais o subconjunto ciente-de-tarefa: as decisões vigentes (ADRs), os padrões canônicos aplicáveis e a ordem de precedência de `docs/system-of-record.md` — para que a sessão comece sabendo o que já foi decidido e o que é aceito/rejeitado, em vez de inferir.

**Que comportamento concreto do agente isso muda ou previne**

- Previne re-derivar decisões já registradas em `docs/decisions/`: o agente parte dos ADRs em vez de reinventá-los.
- Previne violar as regras de `AGENTS.md` (Rule 0 uma-tarefa-por-sessão; Rule 2 mudança-mínima; Rule 3 tocar-só-o-necessário).
- Previne duplicar um padrão que já existe em `docs/canonical/`: reuso em vez de recriação.
- Previne ignorar a precedência de `docs/system-of-record.md` ao resolver conflitos entre camadas.

O efeito líquido: a saída da sessão parte do estado informado do repositório em vez de heurísticas genéricas — exatamente a inconsistência "de novato" descrita no Problema. A mecânica de um hook de sessão concreto (o que dispara a injeção e como) é uma decisão de implementação à parte, fora do escopo deste padrão.
