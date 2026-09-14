---
title: "Não-Colapso de Proveniência de Evidência no Analyze-and-Improve"
type: adr
status: proposed
date: 2026-09-14
deciders: ["pavan"]
tags: ["governanca", "evals", "agentes-orquestracao", "harness"]
aliases: ["evidence provenance ADR", "nao-colapso de evidencia", "evidence domains ADR", "analyze-and-improve evidence ADR"]
last_updated: 2026-09-14
relates-to:
  - "[[../canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[../canonical/eval-tier-stratification|Eval Tier Stratification]]"
  - "[[../canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]"
  - "[[../canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[../system-of-record|System of Record]]"
sources:
  - "https://github.com/pavani06/long-running-agents/issues/257"
  - "https://github.com/pavani06/long-running-agents/issues/288"
  - "https://github.com/pavani06/long-running-agents/pull/292"
---

# ADR: Não-Colapso de Proveniência de Evidência no Analyze-and-Improve

## Contexto

O `analyze-and-improve` (EPIC pavani06/long-running-agents#257) pergunta "o repo já
cobre X?" e responde num eixo único de veredito: `Missing | Partial | Exists | Better`.
O eval-harness metamórfico (#288) rodou o PoC de 50 casos e deu **Tier B = NO-GO**:
Gate A (identificação) passou (recall 100%, false-merge 0), mas Gate B (invariância
de veredito) ficou em 70% e Gate C (evidência grep-verificável) em 43%.

A investigação da dispersão (#292) trouxe duas descobertas estruturais que este ADR
registra:

1. **O repo já mantém separação epistêmica; o motor a colapsa.** A precedência do
   `system-of-record` (AGENTS.md Rule 8) já ordena **decisions (ADRs) > canonical >
   evidence > analysis** — ou seja, "decidido" ≠ "canônico" ≠ "validado" são estados
   distintos por design. O motor os achata num único eixo. Contraexemplo formal já
   presente no repo: `docs/canonical/error-context-hygiene.md` carrega
   *"Classification: Missing — no equivalent mechanism exists in the repo"* — isto é
   `documented = true` **e** `implemented = false`, uma proposição que o eixo único
   `Exists/Missing` é incapaz de expressar.
2. **O Gate C é um sintoma agregado, ainda não caracterizado.** Ao indexar código
   (`index_scope=docs+code`), o Gate B subiu 70%→90% (a dispersão era
   retrieval/cobertura), mas o Gate C **caiu** 43%→10%. O Gate C mistura pelo menos
   três fatores — correção do retrieval × correção da citação/localização × adequação
   do verificador (`grep_verify` exige quote a ±2 linhas, hostil a código) — e o
   significado causal da queda não está caracterizado.

Estas descobertas foram destiladas num diálogo adversarial de três vias (operador +
dois modelos). Este ADR congela o que já está sustentado e delimita explicitamente o
que **não** está.

## Decisão

Registram-se **três princípios (invariantes)** e **um modelo candidato explicitamente
não-normativo**.

### Princípio 1 — Não-colapso de proveniência
Evidências de natureza epistêmica distinta (documentada, decidida, implementada,
validada) **não podem ser colapsadas de forma que se perca sua proveniência antes da
formação do veredito**. O veredito pode agregar; a agregação não pode apagar de qual
domínio veio cada evidência. Sustentado pela precedência já existente no
`system-of-record` e pelo contraexemplo `error-context-hygiene`.

### Princípio 2 — Fronteira de missão
O `analyze-and-improve` **pode detectar e propor remediação para deltas induzidos por
uma fonte** (o comportamento que já tem: Fases 4/6). Ele **não** é o sistema
responsável por **garantir coerência global contínua** do repo (monitorar eternamente
canonical × code × tests × ADR). Observar `documented=true, implemented=false` e propor
uma mudança é escopo dele; ser o subsistema que garante consistência do repo inteiro,
como propriedade permanente, é outra capability.

### Princípio 3 — Não promover eval a arquitetura sem inferência causal sustentada
Nenhuma decisão arquitetural será justificada **exclusivamente** por melhora de score
de um instrumento. A invariante: os *failure modes* **materialmente relevantes** do
instrumento precisam estar **suficientemente caracterizados para sustentar inferência
causal** antes que um resultado de eval justifique mudança arquitetural. (O 70→90 e o
Gate C foram números informativos cujo significado causal estava em aberto — este
princípio previne agir sobre eles às cegas.)

A decomposição **E/R/V** — evidence correctness × reference correctness × verifier
outcome — é apenas o **instrumento candidato de caracterização para o experimento
atual**, não parte normativa da invariante: outro experimento pode caracterizar seus
failure modes materialmente relevantes por outro meio.

### Modelo candidato (L2) — NÃO normativo
`documented / decided / implemented / validated` entram como **candidate evidence
dimensions**, sujeitas a revisão pela taxonomia empírica. A taxonomia pode revelar
eixos adicionais (`observed`, `tested`, `operational`, `deprecated`, `superseded`) ou
mostrar que `validated` está amplo demais. **Este ADR congela a *separação* (Princípio
1), não o número nem os nomes dos eixos.**

## Opções Consideradas

| Opção | Complexidade | Custo | Pros | Contras |
|-------|-------------|-------|------|---------|
| **A (adotada): registrar invariantes agora, L2 candidato, implementação diferida** | Baixa | Zero de código | Congela o vocabulário e os limites sem ossificar ontologia; ancorado na governança existente | Princípio sem mecanismo pode virar letra morta se não for enforçado |
| B: manter o eixo único `Exists/Missing` (status quo) | Zero | Zero | Nada a fazer | Inexpressável (contraexemplo `error-context-hygiene`); colapsa a proveniência que o repo separa |
| C: implementar veredito multidimensional já | Alta | Alto (retrieval × classificação × verificação por domínio) | Expressivo | Prematuro: multiplica ~4× o problema de citação **ainda não caracterizado** (Gate C); expande a missão sem decisão do dono do épico |
| D: tornar `docs+code` o default de produção do índice | Média | Médio | Melhora Gate B (70→90) | Pode divergir o eval do sistema avaliado ("ensinar pro teste"); o significado causal do Gate C segue aberto |

## Análise de Trade-offs

- **Dimensão decisiva:** o que já está *sustentado* (a separação epistêmica) vem da
  governança do próprio repo, não do resultado do eval — logo é ADR-worthy agora,
  independente do Gate C. O que **não** está sustentado (o número/nome dos eixos, se o
  gargalo é verifier/attribution/retrieval, se code entra em produção) fica
  explicitamente fora da decisão.
- **Risco aceito (A):** princípios sem mecanismo. Mitigação: o Princípio 3 é
  enforçável (exige caracterização causal do instrumento antes de agir, por qualquer
  meio adequado), e o Princípio 1 tem lastro na Rule 8.
- **Custo de reverter:** baixo — é doc de princípio; nenhum código depende dele.
- **Anti-escopo explícito:** não autorizado por este ADR — verifier AST-aware,
  pipeline provenance-aware, veredito multidimensional, matriz de experimentos
  D1/D2/D3. Todos são **hipóteses condicionais** ao dataset E/R/V.

## Consequências

- **Próximo passo autorizado (e único):** instrumentar um *dataset E/R/V durável* (por
  variante: evidência recuperada com `source_type`/`path`/`symbol`/`line`/`quote`,
  citação selecionada, resultado da verificação com método+razão), emitido como
  artifact da execução (não commitado no repo — é output derivado, fora da ontologia
  autoritativa), e rodar **uma** corrida instrumentada.
- **Parar e trazer a distribuição E/R/V** antes de qualquer outra mudança. A taxonomia
  **poda** o espaço de experimentos (decide qual intervenção, se alguma, vale pagar) —
  não inaugura uma bateria fixa.
- **Produção inalterada.** O índice de produção segue docs-only; `docs+code` permanece
  instrumento diagnóstico.
- **Tier B segue NO-GO.** Este ADR não move o gate — registra o vocabulário e os
  limites com que a próxima decisão será tomada.
