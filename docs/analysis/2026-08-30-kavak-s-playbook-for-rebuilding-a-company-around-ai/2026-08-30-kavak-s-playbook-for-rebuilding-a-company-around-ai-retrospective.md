---
title: "Retrospective: Kavak Playbook Run + QI Loop — Learnings for Harness, Orchestration, Execution and Method"
type: analysis
tags: [harness-engineering, agentes-orquestracao, governanca, curriculo-conteudo]
date: 2026-08-30
aliases: ["retrospectiva kavak playbook", "kavak run retrospective", "licoes qi loop"]
relates-to: ["[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Knowledge Extraction]]", "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification|Classification]]", "[[docs/plans/2026-08-30-qi-loop-kavak-fixes|QI Loop Plan]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"]
sources: ["Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md"]
---

# Retrospective: Kavak Playbook Run + QI Loop

**Escopo:** tudo aprendido na sessão de 2026-08-30 que serve para melhorar o harness (`analyze-and-improve` + `harness-analyze-and-improve`), o funcionamento do pipeline, a inteligência de orquestração, a execução e o método de construir skills. Fontes: o run completo (Phases 0-6, commit `2e38fea`), o review-work 5-lane (4 FAIL), o QI loop iter 1 (epic #145, issues #146-#156, commits `dfb67d8`/`e2d2a0d`, 15/15 critérios PASS).

**Números da sessão:** pipeline ~35min de tempo de agentes (vs 66min de referência), 14 patterns, 13 canonical docs, 1 skill, 2 exercises, +494 linhas de curriculum na Phase 6, 11 findings P0/P1 todos resolvidos em 1 iteração do loop, 43+21+6 arquivos commitados em 3 commits (`2e38fea`, `dfb67d8`, `e2d2a0d`).

---

## 1. Harness — infraestrutura

### 1.1 Evidência de execução é o elo mais fraco
`test-results.json` saiu do run com `evidence: []` nas fases 5-6, `evaluated_by: harness-orchestrator` (auto-avaliação) e `duration_seconds`/`completed_at` nulos. O review-work classificou como MAJOR: "PASS sem evidência independente". Correção aplicada no QI loop (REC-008), mas a causa raiz é do harness.

**Ação recomendada (harness):** o Step "Advance" deve exigir, para marcar `passes=true`: (a) `evidence[]` com paths que existem em disco (check automático), (b) `evaluated_by` diferente do orquestrador quando houver evaluator delegado, (c) timestamps preenchidos mecanicamente (`date -u` no início/fim de cada fase — o dado existe, só não é gravado).

### 1.2 Módulos "automáticos" que ninguém chama
`eval.py` (golden-free pós-Phase 4) e `trajectory.py` estão documentados como "Automático" no SKILL.md, mas nada no fluxo os invoca — não rodaram no run e nem nos runs de junho. Contrato que não se auto-executa é ficção.

**Ação:** ou wire real (o Step 6 do harness chama `eval.py` e grava as 4 métricas no test-results; trajectory inicializado no Step 1 grava na saída), ou remova do SKILL.md. Estado intermediário aceitável: campo `skipped_modules` no test-results (implementado no QI loop) tornando o desvio visível.

### 1.3 Módulos que funcionaram (manter e anunciar)
- **Cache Phase 1+2 por hash:** verificado em produção (`~/.kc_analyze_cache/<hash>/phase-1/`+`phase-2/`, `has_phase` OK). Re-runs da mesma fonte pulam direto para Phase 3.
- **Map-reduce na Phase 1** (fonte 33k chars → 4 chunks paralelos + REDUCE): ~5min contra ~13min serial estimado.
- **Batch split na Phase 3** (14 patterns → lotes 8+6 paralelos): evitou o timeout de agente único; 4,5min.
- **Phase 4 com 4 agentes paralelos:** 13 canonical docs + skill + exercise em ~6min.
**Ação:** documentar esses números como baseline no SKILL.md (expectativa de duração por fase) — dá ao orquestrador um detector de anomalia ("fase demorou 3x o baseline").

### 1.4 Duração auditável
O claim "~35min" não era auditável (timestamps manuais, janela real 19:56→21:00). O wall-clock inclui gaps entre fases (intervenção humana, espera de gate) — legítimo, mas deve ser separado.

**Ação:** harness grava `started_at`/`ended_at` por fase (parcialmente feito no QI loop) + soma `duration_seconds` num campo `pipeline_agent_time` e `pipeline_wall_clock`. Claims de performance citam esses campos.

---

## 2. Pipeline — funcionamento das fases

### 2.1 Gates de checklist não se auto-executam
O Passo 0c ("sempre executar", SKILL.md:352) foi pulado silenciosamente: o mental model nunca chegou a `mapa-mental-repo/`, e o checklist do gate (:390) não impediu o avanço. Detectado só pelo review adversarial.

**Ação:** gates com efeito em disco (0c é copy de arquivo) viram verificação mecânica pós-fase: "arquivo existe em `mapa-mental-repo/`?" antes de marcar a fase PASS. O QI loop já tratou o sintoma; o harness deve tratar a classe.

### 2.2 Desvio de contrato deve ser documentado, nunca silencioso
O gate literal exige skill+exercise para CADA Missing; o run fez seletivo (precedente de 2026-06-26) sem registrar a decisão. F11. Correção: o desvio foi executado por completo (Sidekick ganhou skill + exercise-08) — mas a lição é o registro: **todo desvio de gate vira linha no `gate.notes` do manifest no momento da decisão**, não depois.

### 2.3 Contagem manual é bug garantido
Duas vezes erradas na mesma sessão: resumo final (9 PC; correto 11 PC — 4H+7M) e o reviewer do goal também errou (2 BI; correto 1). A derivação programática do `classification.yaml` acertou de primeira e virou o método.

**Ação (harness):** a Phase 3 gera a linha de distribuição por script (python sobre o YAML), embutida no classification.md — o orquestrador não escreve números à mão nunca mais.

### 2.4 Artefatos gerados por LLM precisam de validação estática
`SpecialtyAgent` (tipo inexistente) no exercise-07; 4 capabilities no curriculum vs 5 no canonical. Ambos passaram pelos gates porque nenhum gate valida símbolos/consistência entre artefatos irmãos.

**Ação:** pós-Phase 4, dois checks mecânicos: (a) todo identificador referenciado nos code blocks existe como definição no mesmo arquivo; (b) listas "espelhadas" (capabilities, domínios) entre canonical e curriculum derivam da mesma fonte. Barato e teria pegado os dois.

### 2.5 Phase 6 cirúrgica funciona — proteger o invariante
0 arquivos novos, `docs/canonical/` intocado, PT-BR preservado, 13/13 patterns, +494 linhas, só `edit`. É o invariante mais valioso da fase e resistiu ao run real.

### 2.6 Drift de índices é sistêmico
INDEX/README/MASTER_PLAN já tinham drift pré-existente (exercise-06 ausente da tree; "17 exercícios" contando tópicos+koda; 19 violações de validator de junho). A Phase 5 incrementa contagens sobre baselines errados (+1 sobre 16 já errado).

**Ação:** Phase 5 deriva contagens do disco (ls + grep) em vez de incrementar sobre o número antigo; e o repo precisa de uma passada única de saneamento dos índices (backlog).

---

## 3. Orquestração — inteligência

### 3.1 Artefatos auto-contidos são memória entre sessões
A invenção mais valiosa do ciclo: issues com body auto-contido (contexto, passos, aceite, origem) tornam o epic executável por **qualquer sessão futura sem a conversa**. Generaliza: todo handoff entre fases/sessões deve viver em artefato durável (issue, arquivo), nunca só no histórico.

### 3.2 Handoff comentado no fechamento
Cada issue fechada leva comentário com evidências + o que a próxima precisa. Custo ~1 parágrafo; benefício: retomada zero-contexto e auditoria finding→REC→tarefa→commit→issue.

### 3.3 Autorização única vs gates por fase
O operador experiente prefere autorizar o ciclo uma vez ("lance como epic autônomo") a aprovar gate a gate — os gates do quality-improvement-loop viraram atrito e foram convertidos (desvio documentado). Para ciclos com recomendações incertas, os gates protegem. Regra prática: gates por fase na primeira execução de um tipo de trabalho; autorização única quando o padrão já tem uma execução de referência bem-sucedida.

### 3.4 Confiança por verificação, nunca por relatório
Dois sub-agentes reportaram sucesso com detalhes; os checks em disco confirmaram — e é o check em disco que fecha issue. Em um caso o relatório do reviewer do goal continha erro (2 BI; correto 1) — também não foi aceito sem derivação. Orquestrador que não re-verifica vira repetidor de sub-agentes.

### 3.5 Paralelização como padrão, não otimização
Ondas paralelas (4 agentes de Phase 4; lotes de Phase 3; chunks de Phase 1; issues independentes do QI loop) cortaram o wall clock ~47% vs referência. A regra do orquestrador: ao planejar, explicitar o grafo de dependências ANTES de delegar — o que não depende, dispara junto.

### 3.6 Review adversarial com anti-sycophancy pega erro real
O review 5-lane encontrou 11 findings verdadeiros (incluindo 2 P0 de segurança que ninguém tinha visto: key em argv/herança e prompt injection). O custo do review (~40min) pagou-se no primeiro achado. Veredito FAIL em 4 lanes não é fracasso do run — é o review funcionando.

---

## 4. Execução e segurança

### 4.1 Chave de API — regra completa (F1, P0)
- Nunca em argv (`/proc/*/cmdline` vaza para processos locais) → stdin via `printf '%s' "$KEY" | curl --data-urlencode "api_key@-"`.
- Nunca `source`/`set -a` de `.env` (executa código arbitrário e exporta tudo) → parser data-only (`grep | cut | tr`).
- `unset` da variável antes de fallbacks — `uvx`/`nix` executam código de terceiros herdando o ambiente.
- Temp em `mktemp -d` + `trap rm -rf EXIT` — nada persiste em `/tmp` com nome previsível.
- Documentar o mecanismo na SKILL.md do tier (o contrato de interface inclui segurança).

### 4.2 Conteúdo externo é dado não-confiável (F2, P0)
Transcript de YouTube entra no pipeline agentic com poder de escrita e commit. Regras incorporadas à wrapper: delimitação `<untrusted_source>` com instrução anti-instrução explícita, proibição de executar procedimentos citados no conteúdo, Phase 1 com superfície mínima (escrita só no output_dir). Generaliza para papers, artigos e qualquer fonte ingerida.

### 4.3 Modo silencioso engole diagnóstico
`curl -sf` suprime o corpo do erro → o log "SerpApi failed: " sai vazio (confirmado no live run: err file 0 bytes). Fail-quiet dificulta o fallback decision-making. Padrão melhor: capturar HTTP status separadamente do body e logar o status mesmo em modo silencioso (backlog P2).

### 4.4 Bugs pré-existentes se registram, não se consertam em escopo alheio
Tier 2 aceita stderr-text como transcript (`youtube_transcript_api` sai 0 com erro no stdout) — descoberto no teste do QI loop, documentado na issue, NÃO corrigido (fora do escopo). Padrão: descoberta fora de escopo vira registro rastreável (issue/backlog), nunca drive-by fix.

### 4.5 Stage discipline em ambiente sujo
`/mnt/c` carrega ruído permanente (`.obsidian/`, concepts/ de junho, `.understand-anything/`). O único estágio seguro é a lista explícita de arquivos da sessão — `git add -A` é proibido por natureza aqui. E a proteção `.gitignore` só vale depois de commitada (janela de clone fresco — F3).

---

## 5. Método de construir (skills e sistema)

### 5.1 Workflow validado → skill (skillify)
O modo epic-autônomo nasceu como instrução de sessão; virou skill (`qi-epic`) no mesmo dia. O pipeline de captura: executar → revisar → destilar as regras que sobreviveram à execução real → SKILL.md com triggers + delegação aos motores + anti-padrões + smoke script + state.json. **Referência executada é a melhor especificação.**

### 5.2 MECE entre skills
`qi-epic` não reimplementa review-work nem quality-improvement-loop — delega e adiciona a camada de entrega (epic/issues no GitHub). Skills que copiam lógica de irmãs criam dois lugares para atualizar; skills que delegam criam um.

### 5.3 Skills repo-local vs globais
`youtube-transcript` vive no `.opencode/skills/` do Raw-Knowledge (não aparece globalmente); `analyze-and-improve` vive no nível do usuário WSL. Em ambiente híbrido (WSL + Linux home), a localização da skill define onde ela é visível — documentar a localização esperada no SKILL.md evita a busca que fizemos no começo da sessão.

### 5.4 Environment portability é contrato explícito
O script assumia NixOS (`nix run`/`uvx`); roda em WSL/Ubuntu onde `nix`/`uvx` não existem. O padrão `command -v` fallback tornou o tier 1 e 3 portáveis e os tiers 2/4 parcialmente quebrados — aceitável, mas deve estar documentado por host. E o `target-repo` hardcoded na wrapper viola a regra global de portabilidade de assets (backlog).

### 5.5 Correção de ídioma próprio
O refactor da skill mega-expert usou o idioma do próprio arquivo (`SpecialistAgent.certified(run_eval)` + `min_margin()`), não o idioma do exercício/canonical (`BenchmarkResult`) — mesmo conceito, shapes diferentes por artefato. Ao corrigir um artefato, usar os símbolos e convenções DELE.

---

## 6. Backlog vivo (P2/P3 — não bloqueiam, estão registrados)

| Item | Origem |
|---|---|
| Tier 2 aceita stderr-text como transcript (exit 0) | descoberta QI T1 |
| `TRANSCRIPT_LANG` só vale para SerpApi; fallbacks forçam `en` | review |
| Acúmulo de `/tmp/*_err.$$` nos fallbacks (tier 1 resolvido) | review |
| `curl -sf` engole o motivo do erro | review + live run |
| Estilo inconsistente exercise-06 (ASCII sem emoji) vs 07/08 (emojis+acentos) | QA |
| `AGENTS.md` do RK enumera METHOD sem `serpapi` | Code |
| Frontmatter de `07-multi-agent-coordination.md` (`last_updated`, `relates-to`) desatualizado pós-insert | Code |
| MASTER_PLAN chama de "exercícios" contagem que inclui tópicos+koda | QA |
| `target-repo` hardcoded na wrapper (regra global de portabilidade) | Context |
| `nix`/`uvx` ausentes no WSL — tiers 2/4 parcialmente quebrados neste host | Context |
| Saneamento único dos índices (exercise-06 na tree; contagens por disco) | Context |
| `gitignore /tmp/` entry é no-op (pattern relativo à raiz) | QA |

---

## 7. Ações priorizadas para o harness

| # | Ação | Resolve | Esforço |
|---|---|---|---|
| 1 | Advance do harness exige evidence existente em disco + timestamps mecânicos | 1.1, 1.4, F8 | P |
| 2 | Wire real (ou remoção) de eval.py/trajectory.py | 1.2, F8 | M |
| 3 | Distribuição da Phase 3 gerada por script embutida no md | 2.3, F10 | P |
| 4 | Checks pós-Phase 4: símbolos citados vs definidos; listas espelhadas consistentes | 2.4, F5, F6 | M |
| 5 | Gate 0c mecânico: arquivo em `mapa-mental-repo/` antes do PASS | 2.1, F4 | P |
| 6 | Phase 5 deriva contagens de índice do disco, não incrementa baseline | 2.6 | M |
| 7 | Baseline de duração por fase documentado (detector de anomalia) | 1.3 | P |

P = horas; M = 1-2 sessões. Itens 1, 3 e 5 são os de maior razão impacto/esforço.

---

*Retrospective gerada no encerramento do QI Loop iter 1 (epic #145). Próxima revisão agendada: após o próximo run da rotina ingest-and-improve, para validar se as correções de processo mantêm os gates verdes sem reintroduzir atrito.*
