---
type: proposed-canonical-doc
status: proposed
aliases:
- benevolent prompt injection
relates-to: []
created_by: analyze-and-improve F4 (creation != promotion)
source: 2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md
slug: 2026-09-11-75m-founder-reveals-his-agentic-engineering-setup
video_id: ''
pattern: Benevolent Prompt Injection
phase3_verdict: Missing
intended_destination: docs/canonical/benevolent-prompt-injection.md
evidence:
- file: curriculum/07-implementation-guides/03-harness-design-checklist.md
  line: 1014
  quote: Proteção contra prompt injection | Conteúdo de cliente e tool output é delimitado
    e não pode redefinir instruções do sistema.
---

# (PROPOSTA) Proposta: Benevolent Prompt Injection — Injeção Automática de Contexto em Sessões de Agente (Padrão Ausente)

> ⚠️ Proposta em quarentena — criada por análise, **não promovida**. Destino pretendido (se aprovada): `docs/canonical/benevolent-prompt-injection.md`.

**Fonte:** `2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md` · **padrão:** Benevolent Prompt Injection · **Fase-3:** Missing

---

## Problema

Cada nova sessão de agente de IA começa 'sem memória': sem conhecimento do workspace, das convenções do projeto, dos artefatos já produzidos e dos erros já corrigidos. O resultado é repetição de erros, decisões inconsistentes com convenções existentes e rediscovery custoso do contexto do projeto a cada sessão. O conhecimento tácito que um engenheiro sênior do projeto carregaria precisa ser reensinado manualmente — ou é simplesmente ignorado.

## Mecanismo

Um hook de inicialização intercepta o início de cada sessão de agente e injeta automaticamente um pacote de contexto curado, tipicamente composto por:

1. **Mapa do workspace** — estrutura do repositório, propósito de cada área, entrypoints.
2. **Artefatos canônicos** — documentos de decisão, convenções de código, glossário do domínio, estado atual do projeto.
3. **Regras operacionais** — o que o agente deve e não deve fazer, padrões a seguir, erros conhecidos a evitar.

A injeção é 'benevolente' porque, ao contrário de um injection adversário, o conteúdo é curado pelos mantenedores e serve para fazer o agente 'acordar' operando como um engenheiro sênior do projeto, não como um novato. A premissa subjacente: em um fluxo AI-native, o contexto estruturado é o ativo central; a injeção transforma esse ativo em memória operacional reutilizável.

## Trade-offs

- **Custo de manutenção**: o pacote de contexto é código (metadado) e precisa ser mantido. Convenções que mudam sem atualização do pacote criam divergência entre o que o agente 'sabe' e a realidade.
- **Erro em escala**: contexto desatualizado injeta conhecimento errado em *toda* sessão automaticamente — o mesmo mecanismo que propaga boas convenções propaga desinformação com eficiência. Um humano lendo docs desatualizados erra ocasionalmente; um agente injetado erra consistentemente.
- **Custo de janela de contexto**: pacotes grandes consomem tokens em cada sessão; há tensão entre completude e economia.
- **Falso senso de memória**: o agente tem contexto, não memória verdadeira; mudanças no repositório após a geração do pacote não são percebidas automaticamente.

## Como se aplicaria aqui

> **Status: PROPOSTA em quarentena — o padrão foi classificado como ausente neste repositório. Não há evidência de implementação; o que segue é como o padrão *se aplicaria*, para decisão humana.**

A adoção exigiria, nesta ordem:

1. **Curadoria do pacote de contexto**: identificar quais documentos e convenções já existem no repositório (se é que existem) que comporiam a injeção — mapa do workspace, convenções de contribuição, decisões de arquitetura. Se esses artefatos não existirem, este padrão não é o primeiro passo; a escrita da documentação canônica o é.
2. **Definição do hook**: escolher o ponto de inicialização das sessões de agente usadas no fluxo deste repositório (configuração da ferramenta de agente, wrapper de sessão, ou instrução de sistema versionada no repo).
3. **Ciclo de manutenção**: estabelecer responsabilidade e gatilho de atualização do pacote (ex.: revisão a cada mudança relevante de convenção), mitigando o trade-off principal — injeção de contexto desatualizado em escala.
4. **Validação**: medir se sessões com injeção reduzem repetição de erros e violações de convenção antes de tornar o mecanismo obrigatório.

Recomenda-se tratar este documento como hipótese a validar por revisão humana, não como descrição de estado atual.
