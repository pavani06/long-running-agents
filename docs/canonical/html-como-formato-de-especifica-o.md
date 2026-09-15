---
title: HTML como formato de especificação
type: canonical
aliases:
- html como formato de especificação
tags:
- context-engineering
last_updated: '2026-09-15'
relates-to: []
sources:
- 2026-09-11-how-we-claude-code--IlqJqcl8ONE.md
---

# HTML como formato de especificação

**Type:** Canonical Pattern
**Source:** `2026-09-11-how-we-claude-code--IlqJqcl8ONE.md` — adaptado para long-running-agents
**Classification:** Missing — ausente no repo; originado da análise da fonte (padrão: HTML como formato de especificação).

---

## Problema

Especificações escritas em markdown deixam de cumprir sua função de documento de feedback quando crescem acima de aproximadamente 200 linhas. O usuário (ou o colega revisor) não lê o documento por inteiro; o agente que gerou não recebe feedback específico; e a especificação regressa ao papel de artefato morto. Em repositórios de currículo e templates, onde cada lição carrega especificação, checklist e rubric, o problema se multiplica: o mesmo texto precisa informar três públicos (o aluno, o avaliador humano e o agente avaliador) e o markdown linear não escala para isso.

## Mecanismo

Substituir markdown por arquivos HTML densos e ergonômicos para especificações longas ou visualmente ricas. O HTML permite:

- Layout com seções colapsáveis, navegação lateral e destaque seletivo, reduzindo o custo de leitura de documentos longos.
- Design directions exploráveis: variantes, estados e opções de UI apresentados lado a lado para o revisor escolher, em vez de descritos em prosa.
- Verificação nativa embutida: contratos de dados no DOM (por exemplo, atributos data-* que codificam requisitos), de modo que um agente com Playwright MCP possa validar a própria especificação de ponta a ponta sem camada externa.
- Fixtures e estados de exemplo embutidos no mesmo arquivo, eliminando a divergência entre spec e fixtures.

O fluxo de trabalho recomendado muda junto: em vez de o usuário escrever a spec, o agente entrevista o usuário para extrair requisitos e devolve uma spec HTML que o usuário revisa visualmente. A spec vira produto de duas pontas.

## Trade-offs


- Custo de tokens inicial maior: gerar HTML denso custa mais do que gerar markdown equivalente.
- Custo de manutenção: HTML hand-editado degrada; exige disciplina ou regeneração por agente.
- Ferramental: o CI precisa validar HTML (links, estrutura), não apenas markdown; navegadores substituem leitores de terminal.
- No longo prazo, menos iterações e feedback mais eficaz compensam o custo inicial: o revisor entende mais rápido, aponta problemas mais cedo e o agente verifica contra o contrato embutido em vez de reinterpretar prosa.

## Como se aplicaria aqui

Este repositório é majoritariamente markdown curricular e já demonstra consciência do problema em três pontos:

- curriculum/02-nivel-2-practical-patterns/03-rubric-design.md distingue especificação (o quê construir), checklist (se foi construído) e rubric (quão bem). O HTML como formato de especificação atuaria na primeira camada: uma spec HTML com contratos no DOM permitiria que o checklist fosse verificado mecanicamente pelo próprio artefato, em vez de lido manualmente.
- curriculum/03-nivel-3-advanced-architecture/exercises/exercise-05-persona-based-documentation.md organiza documentação por personas (frontend-architect.md, security-engineer.md, ux-engineer.md). Documentos de persona tendem a passar de 200 linhas; candidatos naturais a migrar para HTML denso com navegação por persona.
- curriculum/08-tools-templates/knowledge-graph-template.md e architecture-decision-record-template.md mostram que o repo já lida com formatação visual sensível (diagramas, paletas, checklists). O padrão estenderia essa prática: ADRs com decisões visuais e knowledge graphs poderiam ser entregues como HTML explorável.

Aplicação concreta como proposta: (1) definir um template HTML de especificação em curriculum/08-tools-templates/, análogo ao ADR template existente; (2) piloto em um exercício avançado do nível 3, convertendo a especificação mais longa para HTML com estados e contratos no DOM; (3) documentar no próprio template o trade-off de tokens, coerente com a tabela de formatos estruturados já usada no nível 1. Ressalva: nenhum arquivo HTML de especificação existe hoje no repo; esta é uma proposta de adoção, não descrição de mecanismo vigente.
