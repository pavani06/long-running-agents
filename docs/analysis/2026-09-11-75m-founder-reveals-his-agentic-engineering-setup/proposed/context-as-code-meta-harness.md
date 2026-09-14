---
type: proposed-canonical-doc
status: proposed
created_by: analyze-and-improve F4 (creation != promotion)
source: 2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md
slug: 2026-09-11-75m-founder-reveals-his-agentic-engineering-setup
video_id: ''
pattern: Context as Code (meta harness)
phase3_verdict: Missing
intended_destination: docs/canonical/context-as-code-meta-harness.md
evidence:
- file: extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md
  line: 14
  quote: context as code
- file: extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md
  line: 17
  quote: Armazene todo o trabalho da equipe como markdown em repos por domínio de
    negócio... ('context base' em vez de codebase)
---

# (PROPOSTA) Context as Code (Meta Harness) — Proposta de Padrão

> ⚠️ Proposta em quarentena — criada por análise, **não promovida**. Destino pretendido (se aprovada): `docs/canonical/context-as-code-meta-harness.md`.

**Fonte:** `2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md` · **padrão:** Context as Code (meta harness) · **Fase-3:** Missing

---

## Problema

Repositórios ricos em código mas pobres em significado são indigestos para agentes de IA: sem artefatos que expliquem por que cada feature existe, o agente precisa inferir intenção a partir da implementação, o que gera respostas genéricas, mudanças que violam decisões de design e perda de contexto em sessões longas. O conhecimento fica implícito na cabeça dos mantenedores ou em canais efêmeros.

## Mecanismo

Tratar o repositório como um *context base*, não apenas como um code base:

- **Artefatos markdown estruturados**: epics, specs por feature, decisões de arquitetura (ADRs), convenções de código e glossário do domínio, versionados junto com o código.
- **Parseabilidade**: estrutura previsível (cabeçalhos, campos, frontmatter) para que agentes consigam localizar e carregar apenas o contexto relevante.
- **Sincronização**: a mudança de código exige a atualização do artefato correspondente (e vice-versa); o contexto pode ser validado por lint/CI tanto quanto o código.
- **Inversão de investimento**: mais tempo na engenharia do markdown (definir intenção, restrições, critérios de aceite) do que na execução manual do código — o agente executa; o humano curadoria o contexto.

## Trade-offs

- **Custo upfront**: exige disciplina para escrever e manter documentação estruturada antes de colocar agentes para trabalhar.
- **Competição com entrega**: a engenharia do contexto disputa o tempo de desenvolvimento de features; sem patrocínio, degrada rapidamente.
- **Teto de qualidade**: o output do agente nunca supera a qualidade do contexto fornecido — contexto desatualizado produz mudanças confiantes e erradas.
- **Risco de cerimônia**: se os artefatos não forem consumidos por nenhum fluxo (agente, revisão, onboarding), viram burocracia morta.

## Como se aplicaria aqui

Como proposta (este padrão não existe no repositório hoje), a adoção começaria assim:

1. **Inventário**: mapear features/módulos existentes e identificar onde a intenção é implícita.
2. **Estrutura mínima**: criar um diretório de contexto com epics, specs e convenções, cada artefato com formato parseável (campos fixos: objetivo, restrições, critérios de aceite, status).
3. **Gatilho de sincronização**: regra de contribuição — PRs que alteram comportamento precisam referenciar/atualizar o artefato correspondente; CI valida links e estrutura.
4. **Consumo real**: definir como agentes carregam esses artefatos (prompt de sistema, indexação seletiva) para que o contexto seja usado, não apenas armazenado.
5. **Humanos na primeira e última milha**: mantenedores escrevem/aprovam a intenção; agentes executam e propõem; humano revisa o resultado.

Pontos a validar por revisão humana: formato exato dos artefatos, onde residiriam no repositório e quais fluxos de agente os consumiriam de fato.
