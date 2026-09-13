---
title: "Analyze-and-Improve v4 — pipeline autônoma, HTTP-portátil e machine-gated"
type: plan
date: 2026-09-13
tags:
  - harness-engineering
  - agentes-orquestracao
  - context-engineering
  - evals
  - governanca
  - agentic-coding
aliases:
  - analyze-and-improve v4
  - ingest-and-improve rewrite
  - pipeline de conhecimento autonoma
relates-to:
  - "[[docs/system-of-record|System of Record]]"
  - "[[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve (v3)]]"
  - "[[.opencode/skills/harness-analyze-and-improve/SKILL|harness-analyze-and-improve]]"
  - "[[AGENTS|AGENTS]]"
---

# Analyze-and-Improve v4 — pipeline autônoma, HTTP-portátil e machine-gated

> **Status:** design aprovado (2026-09-13), pré-implementação. Fonte de verdade do rewrite.
> **Escopo deste doc:** desenho e decisões. Nenhum código foi escrito ainda.

## 1. Motivação

A skill `analyze-and-improve` (v3) é o motor evolutivo do repositório: transforma
conhecimento externo (transcripts, talks, papers) em artefatos concretos
(canonical docs, skills, exercises, integração curricular). A **qualidade da
entrega é excelente**, mas o custo operacional é alto:

- **É orquestração de agentes, não um programa.** Cada fase é um sub-agente
  opencode (`ultrabrain`/`deep`/`quick`) fazendo exploração aberta do repo.
- **Acopla runtime interativo:** depende de sessão opencode + `task()` +
  notificações de background + a auth do host → **exige o operador no terminal
  por muito tempo**.
- **Gates humanos bloqueiam no meio:** commit gate por batch, decisão de
  incremental, prompts de estado — tudo síncrono.

Objetivo: **rodar diariamente no GitHub Actions, sem o operador no terminal, sem
perder qualidade.**

## 2. A tensão central

**A qualidade e o custo vêm das mesmas coisas** (raciocínio profundo por fase,
contexto de repo, verificação). Não se corta o caro sem cortar a qualidade. A
estratégia não é cortar, é **separar, cachear e mover o gate**:

- **separar** o plano determinístico (código) do plano de julgamento (LLM);
- **cachear/pré-computar** o contexto do repo (retrieval + modelo mental incremental);
- **mover o gate** de "humano no terminal" para "máquina adversarial + escalação-fina",
  porque o operador **não tem capacidade de revisar** os diffs no volume necessário.

## 3. Decisões travadas

| Dimensão | Decisão |
|---|---|
| **Topologia** | **só-LRA** — cadeia inteira (fonte → análise → produto) dentro de `long-running-agents`. Elimina o Step -1 (dual-path `/mnt/c` vs `/home`, vault registry) do `ingest-and-improve`. |
| **Runtime** | **HTTP portátil** — sem opencode `task()`. Cada fase = chamada(s) de modelo + aplicação determinística por código. |
| **Extensão da automação** | **Fases 0–6 full-auto** (não-supervisionado). |
| **Gate de qualidade** | Máquina no lugar do humano: **gates determinísticos + evaluator adversarial (LLM) + quarentena**, com **escalação-fina**. |
| **Contexto do repo** | **Busca híbrida**: retrieval dense (default) + grep (complemento lexical) + **grep-verify** (evaluator), com **1 rodada "pedir mais"** nomeada pelo modelo. |
| **Modelos** | **gerador = GLM 5.3** (`ZAI_API_KEY`) · **evaluator = OpenAI** (`OPENAI_API_KEY`). Provedores diferentes = adversarial real. Chaves já existentes. |
| **Memória do repo** | **`mapa-mental-repo/` (global comprimido)** + **índice semântico por seção (recall local)**, unificados pelo git delta scan. |
| **Aterrissagem** | **auto-merge PR** (auditoria/revert) + **Issue rolante de quarentena** (escalação). |
| **Migração** | **greenfield** em `scripts/analyze-and-improve/`; skill opencode **intacta como fallback**; **fatia vertical 0–3 primeiro**, validada A/B contra `12-factor-agents`. |

## 4. Arquitetura-alvo

### 4.1 Dois planos

**Plano de controle (código puro, testável — `scripts/analyze-and-improve/`):**
git/delta scan, queue/diff stateless, geração de manifesto, recontagem de índices,
`validate-obsidian`, grep-verify de citações, compilação de código dos artefatos,
checagem de duplicação por embeddings, rotação do `mapa-mental-repo`, quarentena,
abertura/auto-merge de PR, atualização da Issue de quarentena.

**Plano de julgamento (chamadas HTTP):** apenas o raciocínio real — Fases
0,1,2,3,4,6 (gerador GLM) + o evaluator adversarial (OpenAI).

### 4.2 Contexto do repo (Fases 0/3): busca híbrida

- **Dense (default):** retrieval top-k por **seção** (chunk por heading) sobre
  `docs/canonical`/`docs/decisions`/`curriculum`/`.opencode/skills`, com **piso de
  cosseno calibrado** para a distribuição do próprio repo (distinta da dos vídeos).
- **Sparse (complemento):** grep pontual para identificadores exatos (nome de
  arquivo, número de ADR, API, símbolo).
- **1 rodada "pedir mais":** se faltar contexto, o modelo **nomeia** os greps/arquivos
  exatos num campo estruturado; o código busca e faz a 2ª chamada. Limite 1–2 rodadas.
- **grep-verify:** o evaluator confirma que cada `file:line` citado existe e contém
  o alegado (reusa o *citation sampling* do Step 6 do harness atual).
- **Por que importa:** o pior modo de falha da pipeline é classificar **Missing** o
  que já existe sob outro nome → duplicação. Retrieval cobre o eixo conceitual onde
  o grep falha; as mitigações (k generoso + piso + grep-verify) são a rede de segurança.

### 4.3 Fases

| Fase | Papel | Mecanismo v4 |
|---|---|---|
| **0** Modelo mental | orientação global | incremental via delta scan; alimenta `mapa-mental-repo` + índice |
| **1** Extração | conhecimento da fonte | lê o **transcript cru completo**; sem repo |
| **2** Padrões | síntese | sobre o output da Fase 1 |
| **3** Classificação | Missing/Partial/Exists/Better | **retrieval híbrido** monta contexto → modelo classifica com evidência → **grep-verify** |
| **4** Criação | canonical/skills/exercises | modelo retorna **conteúdo completo → quarentena** |
| **5** Integração | índices | **determinística** a partir do manifesto |
| **6** Integração curricular | enriquece módulos existentes | **splice por seção** (código localiza a seção, modelo revisa só ela, código faz o splice; gate exige diff localizado) |

### 4.4 Gate de qualidade (substitui o operador)

1. **Determinístico (barato, sempre):** `validate-obsidian`; grep-verify de citações;
   compilação do código de exercises/skills; **duplicação por cosseno** (novo canonical
   acima do limiar vs existente → segura).
2. **Evaluator adversarial (OpenAI, ≠ gerador):** pontua cada artefato contra rubrica
   fixa (fidelidade à fonte, evidência real, não-duplicação, aderência ao formato).
   Nota mínima para passar.
3. **Quarentena:** o que não passa vai para `docs/analysis/<slug>/proposed/` — **nunca**
   contamina as camadas autoritativas (`docs/canonical`, `curriculum`).
4. **Escalação-fina:** Issue rolante lista os artefatos segurados + o motivo (qual gate
   falhou) + link. O operador olha só as exceções, se/quando quiser.

### 4.5 Input, estado e ritmo

- **Fonte** = o transcript (`raw/youtube/.../*.txt`), máxima fidelidade.
- **Gatilho/filtro** = extratos **`deep_dive: high`** (a triagem já construída).
- **Estado stateless** = marcador **`analyzed: docs/analysis/<slug>/`** escrito de volta
  no frontmatter do extrato quando a pipeline roda a fonte. Diff = `high` sem marcador.
- **Seeding único** dos históricos: casar os pacotes `docs/analysis/` existentes com os
  `deep_dive: high` (levantamento 2026-09-13: **~9 já analisados**, **~85 net-new**;
  2–3 ambíguos precisam de confirmação do operador — ex.: dois vídeos "harness-engineering"
  casando com o mesmo pacote; "need-less-code" vs "simpler-than-you-think").
- **Ritmo:** **3 fontes/run diário**, só sobre o pendente → backlog ~85 em ~28 dias;
  depois incremental.

### 4.6 Aterrissagem

- **Auto-merge PR** por run: o bot abre um PR e auto-mergeia quando os gates ficam verdes.
  Zero fricção para o operador, mas preserva o diff (auditoria + revert) — importa mais aqui
  porque escreve nas camadas autoritativas sem supervisão.
- **Issue rolante** ("Analyze-and-improve — quarantine digest") atualizada a cada run.

## 5. Modos de falha que o desenho protege

- **Duplicação** (Missing falso) → retrieval híbrido + checagem de duplicação por cosseno.
- **Auto-aprovação enviesada** (gerador julgando a si mesmo) → evaluator de outro provedor.
- **Corrupção de camada autoritativa** → quarentena + splice por seção (Fase 6 nunca reescreve arquivo inteiro).
- **Perda de contexto/rot** → mapa-mental incremental + índice atualizados pelo delta scan.
- **Drift silencioso sem ninguém olhar** → gate adversarial obrigatório + escalação-fina.

## 6. Plano de migração

**Abordagem:** greenfield, fatia vertical, opencode como fallback (cutover incremental).

**Primeiro passo — fatia vertical Fases 0–3 (read-only) para 1 fonte:**
1. Plano de controle (diff/queue/estado + git delta scan) + **índice semântico do repo**
   (calibrar o floor do repo).
2. Fase 1 (extração) → 0 (modelo mental incremental) → 2 (padrões) → 3 (classificação
   com retrieval + grep-verify).
3. Evaluator adversarial + quarentena + PR/Issue.
4. **Validação A/B:** rodar contra `12-factor-agents` e comparar o pacote gerado com o
   histórico (`docs/analysis/2026-06-09-12-factor-agents/`). Só prosseguir se a qualidade
   se sustentar.

**Depois:** construir 4 → 5 → 6 (as fases que mutam o produto), cada uma atrás do gate
adversarial + quarentena, com o splice por seção na Fase 6.

**Por que 0–3 primeiro:** são read-only (só escrevem em `docs/analysis/`), então
exercitam **toda** a arquitetura no menor risco, de-riscando os maiores desconhecidos
(qualidade do retrieval, calibração do evaluator, GLM-via-HTTP vs opencode) antes das
fases perigosas.

## 7. Verificações na implementação (não resolvidas aqui)

- Calibração do **floor** do índice do repo (distribuição própria, distinta da dos vídeos).
- **Rubrica** do evaluator adversarial — afinar até bater com o julgamento do operador.
- **A/B de qualidade** GLM-via-HTTP vs pacote opencode histórico (gate para prosseguir).
- Chunking por seção: granularidade e limites de splice na Fase 6.

## 8. Blocos reaproveitáveis (do que já foi construído)

- Clientes HTTP GLM/OpenAI, diff stateless, encadeamento `workflow_run`, commit em lote,
  worktree isolado, fluxo `issue-review`/`issue-finish`.
- O **índice semântico** (mesma técnica de embeddings da camada de conexões) como motor
  de retrieval das Fases 0/3.
- A triagem **`deep_dive`** como seletor de fontes.

## 9. Não-objetivos / riscos aceitos

- **Não** aposentar a skill opencode até a v4 provar qualidade A/B.
- **Não** automatizar sobre repositórios que não sejam o `long-running-agents` (só-LRA).
- Risco aceito: **auto-merge sem revisão humana** — mitigado exclusivamente pelo gate
  adversarial + quarentena + escalação-fina. Se o gate se provar fraco na calibração,
  a fronteira de automação recua (ex.: Fase 6 volta a exigir aprovação) antes de degradar
  o produto.

---

*Design aprovado via sessão de grilling em 2026-09-13. Próximo passo sob comando: "começa a fatia 0–3".*
