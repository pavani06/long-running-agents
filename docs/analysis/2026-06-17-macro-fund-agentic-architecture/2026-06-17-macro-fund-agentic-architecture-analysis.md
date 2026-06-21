---
title: "Arquitetura Agêntica — Gestora Macro Multi-Mercado como Instância de On-Policy Distillation"
type: analysis
date: 2026-06-17
aliases: ["macro-fund-agents", "gestora-macro-agentes", "OPD-investimentos", "comite-pre-compromisso", "exposure-bias-investimentos"]
tags: ["agentes-orquestracao", "context-engineering", "evals", "error-handling", "harness-engineering"]
relates-to:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]"
  - "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"
  - "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]"
  - "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]"
---

# Arquitetura Agêntica — Gestora Macro Multi-Mercado

> Sessão: 2026-06-17
> Origem: raciocínio conversacional sobre como arquiteturas agênticas mapeiam para uma gestora de investimentos multimercado macro, cruzado com os mecanismos de on-policy distillation descritos em [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]].
> **Pendência crítica**: este modelo precisa ser cruzado com a estrutura ideal existente no repositório — especialmente os patterns em `.opencode/skills/` que já implementam partes desse loop. Ver Seção 5.

---

## 1. O Isomorfismo Central

O loop OPD formalizado na análise de distilação:

```
[Prompt x] → [Student Rollout] → [Teacher Scoring: KL Loss] → [Gradient Update] → [Novo Student]
```

Tem um equivalente estrutural direto numa gestora macro:

```
[Regime/Contexto] → [Thesis + Execution] → [Market Response + P&L] → [Thesis Quality Assessment] → [Strategy Update] → [Refined PM]
```

A implicação não-óbvia: qualquer gestora que calibra estratégia em dados históricos está fazendo **off-policy training**. O backtest gap é o exposure bias gap — os prefixos de treinamento (preços históricos sem o impacto das próprias posições) divergem dos prefixos de produção (onde o fundo é agente que move o mercado). Em trajetórias longas, um erro de regime precoce gera drawdown O(eT²) pelo mesmo mecanismo de compounding de erro descrito na análise de distilação.

---

## 2. A Estrutura de Papéis e seus Mapeamentos

### 2.1 Analistas — Fornecedores de PI com Mandato Adversarial

Os analistas não são uma camada paralela. Eles são o fornecedor de **Privileged Information (PI)** que entra no PM como input — o equivalente ao "professor com informação privilegiada" no OPSD.

O fluxo correto:
```
[Analista: PI completa — dados, modelos, alt-data, cenários]
    ↓ (ingestão da tese — ocorre ANTES da execução)
[PM: context window com research digest]
    ↓ (execução ao vivo — PI não está mais disponível)
[Mercado: resposta on-policy]
```

**Problema estrutural identificado**: o mandato natural do analista é confirmatório — ele aprende o que o PM quer ouvir. Sem mandato explícito para trazer cenários adversariais, o loop vira câmara de eco. O analista passa a ser um gerador de rock tokens: consome esforço sem mover a distribuição do PM.

**Solução**: separar os outputs do analista em dois fluxos com pipelines distintos:
- Cenários confirmatórios (reforçam a prior do PM)
- Cenários adversariais (falsificadores explícitos — o que quebraria a tese)

Mapeamento para o repositório: [[.opencode/skills/shadow-review-pipeline/SKILL.md|shadow-review-pipeline]] implementa o padrão de revisão adversarial paralela. A lógica é transferível diretamente para o mandato do analista.

### 2.2 PMs — Prior + Update Bayesiano + Mode-Seeking Natural

Os PMs não são estudantes em branco. Têm **prior formada por ciclos e estilo próprio** (pi_theta). Os cenários do analista são um update bayesiano sobre essa prior — não substituem ela.

O problema estrutural: o PM naturalmente faz mode-seeking (reverse KL). Cenários que contradizem sua prior são tratados como ruído. Pass@1 (tese principal) fica nítida; Pass@k (capacidade de considerar alternativas) cai. Quando a primeira estratégia falha, o PM não tem fallback porque "desaprendeu" as alternativas.

**O calibration gap PI→Execução**: o PM desenvolve convicção calibrada na presença do analista (com PI). Em produção, age com essa convicção herdada mas sem a PI que a sustentava. A solução estrutural: o PM deve persistir não apenas a conclusão ("long EURUSD") mas os **falsificadores explícitos** — o que quebraria a tese — que são os marcadores de incerteza que a compressão normal suprime.

Mapeamento: [[.opencode/skills/magnitude-direction-verifier-split/SKILL.md|magnitude-direction-verifier-split]] já implementa a separação entre convicção interna (magnitude) e sinal externo de validação (direção). Esta skill é o RLSD split aplicado ao PM.

### 2.3 Comitê — Pré-Compromisso antes da Revelação

O comitê é onde o problema de design mais sutil aparece. **Pesos determinísticos conhecidos corrompem o sinal antes da agregação**: participantes calibram sua expressão de confiança ao sistema de pesos, não à sua incerteza real.

Mapeamento direto para OPD: information leakage. Quando o estudante consegue ver o mecanismo de scoring do professor, aprende a imitar a forma dos outputs de alto peso em vez do raciocínio subjacente.

**A estrutura correta**:
```
① Cada participante comite posição + incerteza SEM ver os outros (timestamp-locked)
② Sistema agrega com mecanismo OPACO (pesos não revelados, calibrados por acurácia histórica de divergências)
③ Debate acontece sobre as DIVERGÊNCIAS — não sobre a média
```

Princípios:
- **As divergências são o sinal primário**, não ruído a ser resolvido. Comprimir o comitê numa posição única antes do sizing é epistemic suppression.
- **Calibração opaca**: pesos internos atualizados pela acurácia histórica das divergências, nunca revelados — senão os participantes otimizam os pesos, degradando o sinal.
- **Multi-teacher averaging vs routing**: a média de teachers com visões divergentes produz algo que nenhum deles diria. O debate sobre divergências implementa routing, não averaging.

Mapeamento: [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — o padrão de conselho com scoring independente, aggregation policy, e escalação de divergências é exatamente este mecanismo.

### 2.4 Sizing — RLSD Split

```
Magnitude = convicção agregada do comitê (self-distillation: quanto cada posição importa)
Direção   = debate sobre divergências (verifier: qual direção é correta)
Verifier  = P&L da posição inicial pequena (externo, não o próprio PM)
```

A incerteza estruturada do comitê deve chegar **intacta** ao sizing. A divergência entre analista e PM sobre o mesmo cenário é o sinal de que a incerteza real do sistema é maior do que qualquer participante expressa individualmente.

### 2.5 Middle Office — Teacher Scoring On-Policy

O Middle Office é o único ponto onde o teacher scoring ocorre de forma objetiva. Ele precisa produzir P&L **atribuído por componente da tese** — não P&L agregado do portfólio.

Sem atribuição por thesis leg, o loop de calibração do comitê não tem dados para funcionar. Quem disse "compra duration" e quem disse "vende dólar" precisam ter seus P&L rastreados separadamente.

**Esta é a maior fricção operacional**: o Middle Office normalmente não codifica posições com referência à tese que as originou.

### 2.6 Head — Orquestrador + Regime Detector

O Head tem duas funções no sistema:
1. **Regime Classifier**: detecta quando o contexto macro mudou e invalida prior de PMs. É o mecanismo de re-ancoragem em prefixo confiável quando há prefix drift.
2. **Enforcer do protocolo de pré-compromisso**: sem comprometimento político do Head, o protocolo vai ser contornado. Esta é uma decisão organizacional, não técnica.

---

## 3. O Risco Sistêmico Central — Prefix Drift como Cascata

O mecanismo de prefix drift no OPD (erro precoce → tokens subsequentes fora do suporte do professor → supervisão vira ruído) é idêntico ao mecanismo de cascata de perdas numa gestora macro:

```
Erro de regime precoce (wrong macro call)
    → portfólio em estado fora do suporte dos modelos de risco
    → feedback do Middle Office degrada de informativo → ruidoso → prejudicial
    → PM aprende com ruído e reforça comportamento errado
    → drawdown O(eT²)
```

O gradiente SNR collapse associado é particularmente perigoso: nas situações onde o PM mais precisa aprender (draw extremo), o sinal de aprendizado é exatamente zero — porque todo rollout contém um erro precoce que contamina o resto.

**Antídoto estrutural**: os falsificadores explícitos preservados do comitê devem ser os triggers de re-ancoragem. Quando o mercado cruza um falsificador, o Head aciona regime reassessment — não espera o P&L confirmar o erro.

Mapeamento: [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — o padrão de classificar falhas em classes e mapear cada classe para o guardrail mínimo se aplica aqui. Um falsificador cruzado é uma classe de falha que aciona o guardrail de regime reassessment.

---

## 4. O Template de Cenário como Fundação

Sem um template estruturado, nada fecha o loop. Campos obrigatórios mínimos:

| Campo | Conteúdo | Por que é obrigatório |
|---|---|---|
| `thesis` | Tese base (direcional + ativo + prazo) | Objeto do comitê |
| `falsifiers` | O que no mercado provaria que a tese está errada | Anti-epistemic suppression |
| `adversarial_scenario` | O cenário que mataria a tese | Mandato estrutural do analista |
| `confidence` | Distribuição de probabilidade, não ponto único | Preserva incerteza para sizing |
| `time_horizon` | Janela de avaliação | Define o verifier correto |
| `pi_sources` | Quais fontes de PI sustentam a tese | Rastreabilidade do calibration gap |

O campo `falsifiers` é o mais difícil de obter culturalmente — exige que analistas e PMs se comprometam com o que os tornaria errados. Sem ele, o loop de calibração do comitê não tem objeto.

---

## 5. Cruzamento com a Estrutura Ideal do Repositório — PENDÊNCIA CRÍTICA

**Este é o ponto que precisa ser trabalhado na próxima sessão.**

O repositório já possui implementações parciais de cada componente deste modelo. A arquitetura macro não é nova — é uma instanciação de domínio dos patterns canônicos existentes. O que precisa ser mapeado explicitamente:

### 5.1 Skills que já implementam partes do loop

| Componente macro | Skill existente | Gap |
|---|---|---|
| RLSD split (PM) | [[.opencode/skills/magnitude-direction-verifier-split/SKILL.md|magnitude-direction-verifier-split]] | Aplicação para sizing de posição, não apenas output validation |
| Curriculo de autonomia (analista→PM) | [[.opencode/skills/autonomy-curriculum-sampling/SKILL.md|autonomy-curriculum-sampling]] | Lambda dial entre supervisão densa e rollout autônomo |
| Comitê adversarial | [[.opencode/skills/shadow-review-pipeline/SKILL.md|shadow-review-pipeline]] | Mandato adversarial para analista, não apenas code review |
| Presença do Head | [[.opencode/skills/presence-in-the-loop-metric/SKILL.md|presence-in-the-loop-metric]] | Calibrar quando Head intervém vs. deixa o sistema rodar |
| Loop de PM | [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] | Os 4 componentes (prompt=template, context=PI, dispatch=execução, loop=feedback) |
| Conselho de avaliação | [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] | Pré-compromisso + aggregation opaca + escalação de divergências |
| Detecção de drift | [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] | Falsificador cruzado como trigger de regime reassessment |

### 5.2 O que não existe e precisaria ser construído

- **Template de cenário estruturado** com campo `falsifiers` obrigatório — não existe análogo no repositório
- **Protocolo de pré-compromisso** com timestamp-lock — o repositório tem gates de aprovação mas não para agregação de opinião distribuída
- **P&L attribution por thesis leg** — integração com Middle Office não tem análogo; mais próximo é [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] como template
- **Calibração opaca de pesos** por acurácia histórica de divergências — o Multi-Model Evaluation Council tem calibration loop mas não com opacidade estrutural

### 5.3 A questão a responder na próxima sessão

O repositório define a "estrutura ideal" de agentes long-running com patterns de harness, context management, evals, e loop ownership. A questão é: **qual é o mapeamento completo entre esses patterns abstratos e a implementação concreta de cada role numa gestora macro?**

Especificamente:
- O `owned-agent-control-loop` com seus 4 componentes (prompt, context builder, dispatch, loop) mapeia para qual role e com qual granularidade?
- O `serializable-pause-resume-state` — como o estado de prior do PM é serializado entre sessões de mercado?
- Os tiers de eval (fast/medium/deep) mapeiam para qual frequência de feedback (tick, sessão, ciclo)?
- O `autonomy-curriculum-sampling` (observe→assist→own) define o onboarding de um PM agent novo?

---

## 6. Sequência de Construção

```
1. Template de cenário com falsifiers obrigatórios
   └─ validar culturalmente num ciclo de 4-6 semanas antes de automatizar

2. Protocolo de pré-compromisso (timestamp-lock)
   └─ medir resistência — se o Head não enforça, o protocolo não existe

3. Integração Middle Office → P&L por thesis leg
   └─ maior fricção operacional; sem isso a calibração não tem dados

4. Mecanismo de calibração opaco
   └─ só faz sentido quando há histórico suficiente de divergências avaliadas

5. Agentes IA em cada camada
   └─ APENAS após o loop humano estar validado e fechado
   └─ ordem: analista agent → PM agent → committee aggregator → sizing engine
```

**O erro clássico**: construir os agentes antes do processo humano estar validado. O que se automatiza é um loop que ainda não fecha.
