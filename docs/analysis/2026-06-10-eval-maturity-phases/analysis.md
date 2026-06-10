---
title: "Analise de Conhecimento Nao-Obvio: The Maturity Phases of Running Evals"
type: analysis
date: 2026-06-10
domain: eval-maturity
aliases: []
tags: [analise, evals, maturity-model]
last_updated: 2026-06-10
---

# Analise de Conhecimento Nao-Obvio: The Maturity Phases of Running Evals

> Fonte: Phil Hetzel, Braintrust - "The maturity phases of running evals" (Braintrust, 2026-06-10)
> Extraido: 2026-06-10
> Regras: sem marketing, anedotas, historias pessoais, filler ou repeticao

---

## 1. Frameworks & Models

### 1.1 Modelo de Maturidade em 5 Fases

O framework central e uma sequencia de maturidade para adocao de evals em agentes de IA: ad hoc testing -> spot check evals -> structured evals with metrics -> production-grounded evals -> continuous eval-driven development. A fonte apresenta o modelo como progressao observada em empresas que saem de nenhum processo estruturado ate evals integradas ao fluxo de desenvolvimento, com tipos de eval, maturidade organizacional e sinais de transicao por fase (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:23`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:37`).

Componentes do modelo:

- **Fase 1 - Ad hoc testing**: prompt testado manualmente algumas vezes e enviado para producao com base em sensacao. Nao ha avaliacao estruturada, repetibilidade, cobertura nem capacidade de distinguir melhoria de regressao. O sinal de saida e uma mudanca que parecia boa piorar o produto e so ser descoberta por reclamacao de usuarios (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:25`).
- **Fase 2 - Spot check evals**: o time escreve 10, 20 ou 50 casos em uma planilha ou script simples e os roda manual ou semi-automaticamente. O ganho e repetibilidade; a limitacao e que os casos refletem o que o time ja conhece, nao unknown unknowns. O sinal de saida e dor operacional para rodar manualmente ou falhas reportadas fora do set (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:27`).
- **Fase 3 - Structured evals with metrics**: o time define o que "bom" significa em termos mensuraveis, com test set, criterios de scoring e metricas acompanhadas ao longo do tempo. Entram accuracy, distribuicao de latencia e custo por eval run. O risco e acreditar em scores que nao representam uso real ou criterios mal calibrados. O sinal de saida e score que nao correlaciona com feedback de usuarios (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:29`).
- **Fase 4 - Production-grounded evals**: o eval set passa a ser construido por amostragem de trafego real de producao, captura, armazenamento e replay de interacoes reais. A distribuicao de teste passa a coincidir com a distribuicao de uso. Entram A/B tests, canary deployments com eval gates e dashboards que correlacionam eval scores com metricas de producao. O sinal de saida e volume suficiente e representatividade aparente, mas ainda com edge cases escapando (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`).
- **Fase 5 - Continuous eval-driven development**: evals viram parte nativa do workflow de desenvolvimento. Cada PR tem resultados de eval anexados, suites de regressao crescem automaticamente, existem tiers de eval por custo/profundidade, e falhas de producao geram novos casos de teste. A caracteristica-chave e o sistema de eval ser self-improving, melhorando sem curadoria manual continua (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:33`).

### 1.2 Modelo de Transicao por Dor, Nao por Calendario

Cada fase tem um sinal de maturidade baseado em dor real: usuario reclama, spot checks ficam caros de rodar, scores nao predizem satisfacao, ou edge cases escapam apesar de producao representativa. Isso torna o modelo operacional: a pergunta nao e "qual fase queremos declarar?", mas "qual dor atual prova que a fase presente saturou?" (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:25`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:27`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:29`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`).

### 1.3 Maturidade como Acoplamento de Infraestrutura e Organizacao

O modelo nao trata evals como ferramenta isolada. Cada fase exige infraestrutura tecnica e pratica organizacional acumulada da fase anterior. A fonte afirma explicitamente que pular fases tende a produzir infra que ninguem usa, porque o time nao criou o musculo de rodar evals e agir sobre eles (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:35`).

---

## 2. Patterns & Architectures

### 2.1 Eval Sampling from Production Traffic

**Problema**: test sets hand-crafted ficam presos ao que o time ja sabe e podem nao representar comportamento real do usuario.

**Mecanica**: capturar interacoes reais de producao, armazenar payloads suficientes para replay, samplear exemplos representativos e usa-los como base dos eval sets. O objetivo e alinhar distribuicao de teste e distribuicao real, nao apenas aumentar numero de casos (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`).

### 2.2 PR Gates com Eval Results Anexados

**Problema**: mudancas em prompts, agentes ou criterio de scoring podem entrar sem que o reviewer veja regressao quantitativa.

**Mecanica**: todo PR inclui resultados de eval, permitindo review de qualidade junto com diff de codigo. Isso transforma eval de atividade separada em criterio de merge e materializa a politica "we don't ship without evals" no fluxo diario (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:33`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:35`).

### 2.3 Eval Tiers por Frequencia, Custo e Profundidade

**Problema**: uma unica suite de eval nao atende simultaneamente feedback rapido, protecao de PR e cobertura profunda.

**Mecanica**: separar evals em tiers: fast evals em cada commit, medium evals em cada PR e deep evals agendados. O padrao permite feedback proporcional ao risco e ao custo: barato e rapido no inner loop, mais caro e abrangente fora do caminho critico (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:33`).

### 2.4 Auto-Generated Regression Cases from Production Failures

**Problema**: falhas descobertas em producao se repetem quando dependem de memoria humana para virar teste.

**Mecanica**: quando uma falha de producao e identificada, ela entra automaticamente na suite de regressao como novo caso de eval. O sistema passa a ter data flywheel: cada incidente aumenta cobertura futura e reduz dependencia de curadoria manual (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:33`).

### 2.5 Canary Deployments with Eval Gates

**Problema**: deploys completos amplificam regressao antes que o time observe impacto real.

**Mecanica**: liberar mudancas gradualmente e bloquear/promover rollout com base em eval gates e metricas correlacionadas a producao. A fonte coloca canary deployments junto com A/B testing e dashboards de correlacao na fase de production-grounded evals, onde existe trafego e infra de replay suficientes (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`).

### 2.6 Dashboards Correlacionando Eval Scores e Production Metrics

**Problema**: eval score isolado pode parecer bom enquanto usuarios experimentam regressao.

**Mecanica**: acompanhar scores ao longo do tempo junto com metricas de producao para validar se o proxy de qualidade esta calibrado. O dashboard nao e so reporting; ele e mecanismo de auditoria da validade dos evals (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`).

---

## 3. Operational Lessons

### 3.1 Nao Pule Fases

Tentar ir direto para continuous eval-driven development falha porque a automacao pressupoe habitos anteriores: escrever casos, roda-los, confiar em metricas, comparar com producao e agir sobre regressao. Sem esse musculo, a organizacao constroi infraestrutura que ninguem usa (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:35`).

### 3.2 Compromisso Organizacional Importa Mais que Tooling

O gargalo principal nao e escolher Braintrust ou construir in-house; e transformar eval em parte obrigatoria do desenvolvimento. A fonte aponta times bem-sucedidos como aqueles em que lideranca sustenta a regra de nao enviar sem evals (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:29`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:35`).

### 3.3 Repetibilidade Vem Antes de Metricas Sofisticadas

Spot checks sao imaturos, mas criam a primeira propriedade essencial: rodar os mesmos casos novamente. Sem essa base, accuracy, latency e cost tracking da fase 3 nao tem objeto estavel para medir (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:27`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:29`).

### 3.4 Eval Score Precisa Correlacionar com Feedback de Usuario

Um score que nao prediz user feedback e uma falsa seguranca. A transicao para production-grounded evals e disparada exatamente quando metricas estruturadas deixam de bater com o que usuarios reportam (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:29`).

### 3.5 Producao e o Melhor Gerador de Casos, Mas So Depois de Volume Suficiente

Production-grounded evals sao um unlock porque alinham distribuicoes, mas dependem de volume e infraestrutura para captura, storage e replay. Antes disso, amostragem de producao pode ser ruidosa ou nao representativa (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`).

### 3.6 O Estado Maduro E Self-Improving, Nao Apenas Automatizado

A diferenca entre CI com evals e fase 5 e que a suite cresce automaticamente conforme novas falhas aparecem. O valor esta no feedback loop que converte incidentes em regressao permanente, nao apenas em rodar testes com frequencia (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:33`).

---

## 4. Tradeoffs

| Decisao | Beneficio | Custo |
|---|---|---|
| Ad hoc testing para velocidade inicial | Sai de zero rapidamente e valida uma ideia sem infra | Sem repetibilidade, cobertura ou nocao confiavel de regressao; usuarios viram detector de falhas |
| Spot checks manuais ou semi-automaticos | Cria repetibilidade com baixo custo inicial | Escala mal, nao roda em CI/deploy e cobre principalmente casos conhecidos |
| Structured metrics sobre test set curado | Permite acompanhar accuracy, latency e custo ao longo do tempo | Scores podem ser enganosos se test set ou criterio nao representam uso real |
| Hand-crafted test cases vs. production-sampled cases | Casos manuais sao rapidos e direcionados para falhas conhecidas | Nao capturam unknown unknowns; casos de producao exigem volume, captura, storage e replay |
| Automated eval gates vs. julgamento humano ad hoc | Bloqueia regressao de forma consistente e auditavel | Exige confianca em metricas calibradas e compromisso organizacional para nao bypassar gates |
| Fast/medium/deep eval tiers vs. suite unica | Balanceia feedback rapido, protecao de PR e cobertura profunda | Mais complexidade operacional para manter tiers, agenda e interpretacao de resultados |
| Canary com eval gates vs. deploy completo | Reduz blast radius e valida mudanca contra sinais reais | Exige pipeline de rollout, metricas de producao e criterio de promocao/rollback |
| Auto-gerar casos de falhas de producao vs. curadoria manual | Cria suite self-improving e evita repeticao de incidentes | Pode incorporar ruido se classificacao de falha ou expected behavior nao for bem definido |

---

## 5. Failure Patterns

1. **Shipping by feel**: mudanca parece boa em teste manual, piora producao e so e descoberta por reclamacao. Causa: ausencia de eval estruturado. Mitigacao: criar spot check set repetivel (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:25`).
2. **Spot check blind spot**: casos escritos pelo time cobrem apenas cenarios conhecidos, enquanto unknown unknowns escapam. Causa: test set derivado de memoria interna, nao de distribuicao real. Mitigacao: evoluir para metricas estruturadas e depois production sampling (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:27`).
3. **Manual eval bottleneck**: o set cresce ate ficar doloroso de rodar manualmente. Causa: maturidade sem automacao. Mitigacao: integrar evals a CI, PR ou deployment pipeline (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:27`).
4. **Metric theater**: accuracy, latency ou custo sao acompanhados, mas nao predizem experiencia real. Causa: test set nao representativo ou criterio de scoring frouxo/estrito demais. Mitigacao: calibrar scores contra user feedback e metricas de producao (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:29`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`).
5. **Premature eval platform**: time tenta construir fase 5 antes de aprender a operar fases 2-4. Causa: infra desacoplada de habito organizacional. Mitigacao: maturar sequencialmente e agir sobre cada tipo de sinal antes de automatizar tudo (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:35`).
6. **Representative-looking production set still misses edges**: mesmo com dados reais, edge cases escapam. Causa: volume ou sampling ainda insuficiente para cauda longa. Mitigacao: continuous loop onde falhas de producao viram novos casos de regressao (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:31`, `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:33`).
7. **Eval infra nobody uses**: ferramentas e pipelines existem, mas nao influenciam shipping. Causa: lideranca nao sustenta "no ship without evals" e o time nao criou pratica de agir sobre resultados. Mitigacao: gate organizacional explicito e resultados de eval no workflow de desenvolvimento (`/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-06-10-the-maturity-phases-of-running-evals-phil-hetzel-braintrust.md:35`).

---

## 6. Synthesis

O principio unificador e que eval maturity nao e uma escala de ferramenta, mas uma escala de confianca operacional. Cada fase remove uma fonte diferente de ilusao: a Fase 1 remove a ilusao de que feeling detecta regressao; a Fase 2 remove a ilusao de que memoria humana basta; a Fase 3 remove a ausencia de metricas; a Fase 4 remove a ilusao de que um test set manual representa usuarios; a Fase 5 remove a dependencia de curadoria manual para lembrar falhas passadas.

O insight cross-cutting mais forte e que a distribuicao importa tanto quanto o score. Um sistema pode ter metricas, dashboards e gates e ainda estar errado se os casos avaliados nao vierem da distribuicao que o produto realmente enfrenta. Por isso production-grounded evals sao o ponto de inflexao: elas transformam eval de checklist interno em espelho do uso real.

Tres consequencias para agentes long-running:

- **Evals sao memoria institucional**: cada falha que vira regressao reduz dependencia de lembranca humana e protege contra reincidencia.
- **Gates so funcionam quando o proxy e confiavel**: bloquear PR por score ruim e util apenas se o score correlaciona com satisfacao, falha ou metricas reais.
- **Maturidade e sequencial porque confianca e acumulativa**: nao ha como automatizar com seguranca uma pratica que o time ainda nao sabe interpretar manualmente.
