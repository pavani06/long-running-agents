---
title: HTML como camada de revisão de especificações
type: canonical
aliases:
- html como camada de revisão
- especificação renderizada para revisão
tags:
- context-engineering
last_updated: '2026-09-15'
relates-to: []
sources:
- 2026-09-11-how-we-claude-code--IlqJqcl8ONE.md
---

# HTML como camada de revisão de especificações

**Type:** Canonical Pattern
**Source:** `2026-09-11-how-we-claude-code--IlqJqcl8ONE.md` — adaptado para long-running-agents
**Classification:** Missing — ausente no repo; originado da análise da fonte.

---

## Problema

Especificações longas em Markdown deixam de cumprir sua função de documento de feedback quando crescem muito (na fonte, acima de ~200 linhas): o revisor humano não lê o documento por inteiro, o agente que o gerou não recebe feedback específico, e a spec regressa a artefato morto. Em currículo e templates — onde cada lição carrega especificação, checklist e rubric — o mesmo texto precisa informar três públicos (aluno, avaliador humano, agente avaliador), e o Markdown linear e longo fica difícil de consumir para revisão.

O insight da fonte é sobre **consumo humano da revisão**, não sobre o formato de armazenamento: quando o Markdown longo fica difícil de ler e comentar, uma representação renderizada ajuda a revisão.

## Mecanismo

Quando uma spec longa ou visualmente rica em Markdown fica difícil de consumir, gerar uma **representação renderizada para revisão** (tipicamente HTML) **derivada da fonte Markdown** — não substituir a fonte por HTML. A vista renderizada pode oferecer:

- Seções colapsáveis, navegação lateral e destaque seletivo, reduzindo o custo de leitura de documentos longos.
- Design directions exploráveis: variantes, estados e opções apresentados lado a lado para o revisor escolher, em vez de descritos em prosa.
- Fixtures e estados de exemplo embutidos, tornando a revisão concreta.
- Opcionalmente, contratos no DOM (atributos `data-*`) que um agente com navegador pode verificar — como apoio à revisão, não como nova fonte de verdade.

O fluxo muda junto: o agente entrevista o usuário, produz a spec **na fonte Markdown** e uma **vista renderizada** para revisão visual; os comentários do revisor voltam para a fonte Markdown. A representação renderizada é um canal de revisão/comunicação de duas pontas, sobre a fonte versionada.

## Princípio: fonte de verdade e versionabilidade

Markdown continua a **fonte de verdade**: versionado, diffável, revisável por PR e validado pelo CI (`validate-obsidian`). A representação renderizada (HTML) é uma **vista derivada e regenerável** para consumo humano/agente — nunca a fonte autoritativa. Isso preserva a versionabilidade que o repositório já exige e evita dupla fonte de verdade.

**Este padrão NÃO é uma regra de migrar specs longas de Markdown para HTML.** É uma opção de representação: renderizar uma camada de revisão quando o Markdown longo fica difícil de consumir, mantendo o Markdown como fonte.

## Trade-offs

- Custo de tokens para gerar a vista renderizada; justifica-se quando o documento é longo ou visual, não por padrão.
- Risco de divergência se o HTML for tratado como fonte editável — mitigado tratando-o como derivado/regenerável a partir do Markdown, não como fonte paralela.
- Ferramental: revisar a vista exige navegador; o CI continua validando o **Markdown-fonte** (links, estrutura, convenção), não o HTML derivado.
- Benefício: o revisor entende mais rápido e aponta problemas mais cedo, e um agente pode verificar contra o contrato embutido em vez de reinterpretar prosa — compensando o custo quando o documento é longo/visual.

## Como se aplicaria aqui

Este repositório é majoritariamente Markdown curricular e já demonstra consciência do problema em três pontos (a fonte permanece Markdown; a camada renderizada seria derivada dela):

- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` distingue especificação (o quê construir), checklist (se foi construído) e rubric (quão bem). Uma **vista renderizada da spec** facilitaria a revisão da primeira camada; contratos embutidos poderiam apoiar a verificação do checklist — sem tornar o HTML a fonte da lição.
- `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-05-persona-based-documentation.md` organiza documentação por personas (frontend-architect, security-engineer, ux-engineer). Documentos de persona longos são candidatos naturais a uma **vista renderizada com navegação por persona**, mantendo os `.md` como fonte.
- `curriculum/08-tools-templates/knowledge-graph-template.md` e `architecture-decision-record-template.md` já lidam com formatação visual sensível (diagramas, checklists). O padrão estenderia essa prática entregando uma **vista explorável** desses artefatos para revisão, derivada do Markdown.

Aplicação concreta como proposta: (1) um template de **render de revisão** em `curriculum/08-tools-templates/` (uma renderização da spec Markdown, não um novo formato-fonte); (2) piloto renderizando para revisão a spec mais longa de um exercício de nível 3, mantendo o `.md` como fonte; (3) documentar o trade-off de tokens. Ressalva: nenhuma vista HTML de spec existe hoje no repo; esta é uma proposta de adoção como **camada de revisão**, não descrição de mecanismo vigente, e não é regra de migração de formato.
