---
title: "Analise de Conhecimento Nao-Obvio: The Imitation Game — Policy Distillation in Language Model Training"
type: analysis
date: 2026-06-16
aliases: ["OPD analysis", "on-policy distillation", "policy distillation", "OPSD", "distillacao on-policy", "self-distillation"]
tags: ["analise", "agentes-orquestracao", "context-engineering", "evals", "error-handling", "harness-engineering"]
relates-to:
  - "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]"
  - "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]"
  - "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]"
  - "[[docs/canonical/two-implementations-goal-test|Two Implementations Goal Test]]"
  - "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"
  - "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]"
  - "[[docs/canonical/token-economics-gap-filling|Token Economics Gap Filling]]"
  - "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]"
  - "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long Session Evals]]"
  - "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]"
  - "[[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis|12FA Analysis]]"
  - "[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis|Context Mgmt Analysis]]"
---

# Analise de Conhecimento Nao-Obvio: On-Policy Distillation

> Fonte: Chinmay Karkar — "The Imitation Game: State of Policy Distillation in Language Model training" (blog, 2026-06-16)
> Extraido: 2026-06-16
> Path original: `raw-knowledge/sources/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language.md`
> Regras: sem marketing, anedotas, historias pessoais, repeticao; foco em mecanicas nao-obvias

---

## 1. Frameworks & Modelos

### 1.1 O Loop On-Policy como Acoplamento entre Geracao de Dados e Treinamento

A extracao central: on-policy distillation (OPD) acopla a distribuicao de treinamento a distribuicao de inferencia fazendo o proprio estudante gerar os dados sobre os quais recebe supervisao do professor (Fonte: l44-53, "On-Policy KD Objective").

O loop formalizado:

```
[Prompt x] -> [Student Rollout: y ~ pi_theta(·|x)] -> [Teacher Scoring: pi_T(·|x, y_<t)] -> [KL Loss] -> [Gradient Update] -> [Novo Student]
```

A implicacao nao-obvia: o estudante **sempre e treinado nos prefixos que ele mesmo gera**. Nao existe gap entre a distribuicao dos inputs de treinamento e dos inputs de inferencia. Isso fecha o que o autor chama de **exposure bias gap**: a discrepancia entre prefixos gerados pelo professor (durante off-policy training) e prefixos gerados pelo estudante (durante inferencia). Em trajetorias longas (1000+ tokens), um unico erro precoce pode empurrar o prefixo para uma regiao do espaco de tokens onde o modelo nunca foi supervisionado, e o erro acumula quadraticamente (Fonte: l122-144, "Error Compounding: The Quadratic Tax of Off-Policy Training").

A relevancia para sistemas agenticos e direta: agentes long-running geram suas proprias trajetorias de ferramentas durante a execucao. O gap entre "dados de treinamento estaticos" e "prefixos auto-gerados em producao" e exatamente o mesmo mecanismo. Um agente que nunca foi treinado nos seus proprios prefixos de erro esta condenado ao O(eT^2) — cada ma decisao torna a proxima mais provavel.

### 1.2 Forward KL (Mode-Covering) vs Reverse KL (Mode-Seeking) como Dois Regimes de Aprendizado

A literatura de OPD e fundamentalmente uma disputa sobre qual divergencia usar (Fonte: l66-69, "Forward vs reverse KL"):

| Direcao | Formula | Comportamento | Quando usar |
|---|---|---|---|
| Forward KL | D_KL(pi_T || pi_theta) | Mode-covering: estudante tem que cobrir toda massa do professor | Professor muito maior que estudante, distribuicao unimodal |
| Reverse KL | D_KL(pi_theta || pi_T) | Mode-seeking: estudante pode ignorar modos que nao consegue representar | Estudante menor, distribuicao multimodal, quer especializacao |

A intuicao geometrica (Fonte: l106-116, Figure 1): forward KL espalha a massa do estudante sobre todos os modos do professor — o que e ineficiente quando o estudante e menor. Reverse KL concentra a massa no modo que o estudante melhor representa e ignora o resto.

Para agentes, a escolha entre mode-covering e mode-seeking mapeia para a tensao entre **cobertura de casos de borda** (forward KL — o agente tenta cobrir todos os cenarios possiveis) e **especializacao em caminhos confiaveis** (reverse KL — o agente foca no que executa bem). O tradeoff e identico ao dilema exploracao vs. exploracao em RL.

### 1.3 Self-Distillation como Dissociacao entre Professor e Modelo Externo

On-Policy Self-Distillation (OPSD) remove a premissa de que o professor e um modelo maior. Professor e estudante compartilham os mesmos pesos; a unica diferenca e que o professor recebe **privileged information (PI)** que o estudante nao ve: uma solucao de referencia, um stack trace, um documento, ou ate uma instrucao de estilo (Fonte: l312-320, "On Policy Self Distillation").

```
[Student View: pi_theta(·|x)]  <--- mesmo modelo --->  [Teacher View: pi_theta(·|x, PI)]
```

O per-token log-ratio entre as duas visoes se torna o sinal de aprendizado (Fonte: l340-348, Self-Distilled Reasoner). O gradiente nao flui atraves do log-ratio — ele e tratado como constante para evitar que a variancia exploda.

A implicacao para agentes: qualquer fonte de informacao que o agente teria em tempo de design mas nao em tempo de execucao pode atuar como PI. Exemplos: um playbook de troubleshooting, um diagrama de arquitetura, um log de sessao completa. O self-distillation permite "assar" esse conhecimento nos pesos do agente durante o treinamento para que ele nao precise carrega-lo no context window durante a execucao.

### 1.4 A Taxonomia de PI como Espectro de Confianca

Os metodos OPSD revelam um espectro de "quanto confiar no sinal de PI" (Fonte: l415, l464):

| Metodo                  | PI                           | Confianca no PI                              | Mecanismo de Gate                                               |
| ----------------------- | ---------------------------- | -------------------------------------------- | --------------------------------------------------------------- |
| Self-Distilled Reasoner | Solucao de referencia        | Alta (por construcao)                        | Nenhum                                                          |
| SDPO                    | Feedback textual do ambiente | Alta (verifier-grounded)                     | Nenhum                                                          |
| GATES                   | Documento recuperado         | Media (pode estar errado)                    | Consensus gate: so destila quando k rollouts do tutor concordam |
| CRISP                   | Instrucao "be concise"       | Alta (shared latent rule)                    | Nenhum                                                          |
| RLSD                    | PI + verifier binario        | Media (PI da magnitude, verifier da direcao) | Split: magnitude do self-distillation, sinal do verifier        |

***Para agentes, isso e um catalogo de estrategias de "como usar conhecimento parcial em runtime". O padrao do GATES — amostrar multiplas execucoes do tutor e so confiar quando ha consenso — e diretamente aplicavel a validacao de saidas de sub-agentes ou a verificacao de planos gerados***.

---

## 2. Padroes de Implementacao

### 2.1 Teacher-Mixed Sampling como Ponte entre Off-Policy e On-Policy

MiniLLM introduz um mecanismo de amostragem mista: em vez de usar rollouts puros do estudante (que sao lixo no inicio do treinamento), amostra de `p_tilde = alpha * p_T + (1-alpha) * q_theta` e corrige com importance sampling (Fonte: l177-178, "Teacher-mixed sampling").

GKD formaliza isso como um unico dial de mistura lambda entre dataset supervisionado e rollouts do estudante (Fonte: l187-205). DistiLLM transforma lambda em um schedule adaptativo: comeca off-policy (amostras do professor sao baratas e estaveis) e migra para on-policy conforme o estudante estabiliza (Fonte: l224).

Para agentes, isso e uma estrategia de **curriculo de autonomia**: comecar com supervisao densa (rollouts de um operador humano ou de um agente experiente), depois aumentar progressivamente a proporcao de rollouts auto-gerados. O dial lambda e o grau de autonomia do agente.

### 2.2 Log-Ratio como Advantage sem Reward Model Explicito

Um padrao recorrente em OPSD: o per-token log-ratio entre a visao com PI e a visao sem PI atua como advantage:

```
A_t = log P_T(y_t | x, PI, y_<t) - log P_S(y_t | x, y_<t)
```

Este advantage substitui o "reward minus baseline" do RL tradicional (Fonte: l340-348). E denso (per-token, nao per-trajectory), nao requer reward model, e usa o proprio professor como sinal de supervisao.

A implicacao para agentes: qualquer diferenca entre duas visoes do mesmo modelo pode gerar um sinal de aprendizado. Um agente rodando com acesso a logs completos (visao PI) vs. um agente rodando com contexto truncado (visao sem PI) pode usar o log-ratio entre as duas visoes para aprender a operar com contexto reduzido — exatamente o problema de context management em agentes long-running.

### 2.3 AOPD: Separacao Assimetrica entre Tokens Positivos e Negativos

AOPD parte da observacao de que o gradiente de tokens com advantage negativo tem caudas pesadas, variancia extrema, e stagnacao em zero — comportamentos qualitativamente diferentes dos tokens com advantage positivo (Fonte: l255-274).

A solucao: separar a loss em duas, roteando tokens negativos/zero-advantage para um forward KL top-K (mais estavel) e mantendo OPD padrao para os positivos. O gate G_t decide a rota com base em `P_T(y_t) <= P_S(y_t)`.

Para agentes, isso mapeia para **tratamento assimetrico de feedback negativo**. Quando um agente falha, a correcao nao deve ser simetrica ao reforco do sucesso — erros tem mecanicas diferentes (caudas pesadas, dominancia de gradiente, estagnacao). A solucao estrutural: rotear falhas para um pipeline de correcao diferente do pipeline de reforco.

### 2.4 CRISP: PI como Instrucao de Estilo para Compressao Automatica

CRISP mostra que PI pode ser uma unica instrucao ("be concise") e o reverse KL automaticamente comprime problemas faceis mais que problemas dificeis — sem heuristicas de token budget (Fonte: l417-433).

O mecanismo: o professor condicionado em "be concise" coloca massa em tokens mais densos; o reverse KL faz o estudante mode-seek para esses tokens. Em problemas dificeis, a instrucao de concisao compete com a necessidade de raciocinio longo, e o modelo naturalmente preserva a deliberacao.

Para agentes, isso sugere que **compressao de contexto pode ser emergente em vez de programada**. Em vez de escrever heuristicas de "quando truncar", pode-se usar uma visao do agente com instrucao de compressao como professor e deixar o reverse KL aprender a comprimir automaticamente. A implicacao e que o agente aprenderia a ser sucinto em tarefas faceis e verboso apenas quando necessario — exatamente o comportamento desejado em sistemas de context management.

### 2.5 RLSD: Split entre Magnitude do Self-Distillation e Direcao do Verifier

RLSD propoe que self-distillation puro sofre de "information leakage": o estudante aprende a imitar outputs com formato de PI mesmo sem PI, e isso colapsa em producao (Fonte: l435-464).

A solucao: usar o log-ratio do self-distillation como **magnitude** do update (quanto empurrar cada token), mas usar um **verifier externo** para decidir a **direcao** (sinal) do update. O weight por token e `w_t = (P_T/P_S)^sign(A)` onde A e o advantage do verifier.

Este e o padrao arquitetonico mais relevante para agentes: **separacao entre intensidade de conviccao e direcao de correcao**. Um agente pode ter alta conviccao interna sobre quais tokens sao importantes (magnitude do self-distillation), mas ainda precisa de um sinal externo (humano, teste, verifier deterministico) para saber se a direcao esta correta. E a formalizacao matematica do "trust but verify".

---

## 3. Licoes Operacionais

### 3.1 Token-Level KL nao e Sequence-Level KL — e a Diferenca Importa

O objeto que a literatura de OPD quer minimizar e o KL no nivel de sequencia. O que ela otimiza na pratica e um estimador amostrado no nivel de token. Os dois divergem, e a divergencia piora com acoplamento temporal forte entre tokens (exatamente o regime de raciocinio longo) (Fonte: l483-495, "The token-level KL is a fragile proxy").

A licao: em agentes, metrica proxy != metrica real. O score de um passo individual do agente nao captura se a trajetoria completa e boa. Assim como o token-level KL superestima o sequence-level KL em cenarios com forte dependencia temporal, uma metrica de "taxa de acerto por tool call" pode divergir da metrica real de "taxa de sucesso da tarefa completa". A verificacao precisa ser no nivel da trajetoria, nao do passo.

### 3.2 Prefix Drift Silencioso: o Professor Degrada sem Avisar

Quando o estudante comete um erro precoce, os tokens subsequentes saem do suporte do professor. A distribuicao do professor passa de "picos informativos" para "plana/quase-uniforme", e o estudante destila esse ruido como se fosse sinal (Fonte: l497-509, "Prefix drift and the unreliable teacher").

A implicacao para agentes e um mecanismo de falha em cascata: um agente que comete um erro de tool call no passo 3 pode gerar prefixos nos passos 4-10 que nenhum supervisor (humano ou modelo) consegue avaliar utilmente. O supervisor, confrontado com um cenario que nunca viu, produz feedback essencialmente aleatorio. O agente aprende com ruido e reforca o comportamento errado.

O "gradient SNR collapse" associado (Fonte: l509) e particularmente perigoso: nos prompts onde o agente mais precisa aprender (taxa de acerto ~0%), o sinal de aprendizado e exatamente zero — porque todo rollout contem um erro precoce que contamina o resto.

### 3.3 Local Teachability Collapse: o Sinal Degrada Gradualmente

Mesmo quando o professor permanece calibrado, a margem do professor (o quanto ele "sabe" em cada posicao) decai ao longo da trajetoria. Existe um ponto de mudanca onde o gradiente para de carregar informacao util, mesmo que nada tenha "quebrado" (Fonte: l511-521).

A licao para agentes: supervisao nao e binaria (util/inutil) — e continua e decrescente. Existe um ponto otimo alem do qual continuar supervisionando e contraproducente (adiciona ruido e custo computacional sem melhorar o aprendizado). Em agentes long-running, isso sugere que **a janela de supervisao deve ser adaptativa por trajetoria**, nao fixa por posicao.

### 3.4 Rock Tokens: ~18% dos Tokens Consomem ~40% do Esforco sem Melhorar o Modelo

Uma descoberta empirica: aproximadamente 18% dos tokens em OPD exibem loss persistentemente alta que nunca diminui, absorvendo uma fracao desproporcional da norma do gradiente (Fonte: l523-533, "Rock Tokens").

Para agentes, isso e um alerta sobre **alocacao de esforco de otimizacao**. Se um agente gasta 40% do seu ciclo de melhoria em comportamentos que nunca melhoram (seja por limitacao do modelo, ruido nos dados, ou mecanica intrinseca), esse esforco e desperdicado. A licao operacional: medir nao apenas "o que o agente aprendeu", mas "onde o agente esta gastando seu orcamento de aprendizado sem retorno".

### 3.5 O Gap de Calibracao PI: Confianca Condicionada em Informacao Invisivel

Em OPSD, o professor calcula confianca sob informacao (PI) que o estudante nao tera em producao. A confianca do professor `P(correct | x, PI)` nao e um target valido para a confianca de producao `P(correct | x)` — e o estudante herda overconfidence, especialmente nos problemas mais dificeis onde PI mais ajuda (Fonte: l547-559).

Em agentes, isso e o equivalente a treinar com acesso a um "oraculo de debugging" e depois implantar sem ele. O agente aprende a ser confiante nos cenarios onde o oraculo dava a resposta — mas em producao, sem o oraculo, essa confianca e miscalibrada. A licao: **a calibracao deve ser medida na distribuicao de producao, nao na de treinamento**, e qualquer sinal de supervisor com acesso a informacao privilegiada introduz um vies de calibracao que precisa ser corrigido separadamente.

### 3.6 Epistemic Suppression: Compressao Apaga Marcadores de Incerteza

CRISP e metodos de compressao de raciocinio suprimem desproporcionalmente hedging phrases e uncertainty markers — exatamente os tokens de alta entropia que a visao PI-conditioned do professor dropa (Fonte: l561). O resultado: traces mais curtas, porem **mais confiantemente erradas** nos passos elididos.

Para agentes que comprimem contexto ou resumem historico: a compressao pode estar removendo exatamente os sinais de "eu nao tenho certeza sobre isso" que sao cruciais para o proximo passo do agente. Um resumo de contexto que omite hedging e mais curto, mas transmite uma certeza falsa que leva a decisoes piores downstream.

---

## 4. Tradeoffs

| Decisao | Ganho | Custo |
|---|---|---|
| On-policy (gerar proprio dado) vs. Off-policy (dataset fixo) | Erro O(eT) linear em vez de O(eT^2) quadratico; sem exposure bias | Custo computacional de gerar rollouts a cada passo; rollouts inuteis no inicio do treinamento |
| Reverse KL (mode-seeking) vs. Forward KL (mode-covering) | Estudante foca no que consegue representar bem; evita espalhar massa em modos inalcancaveis | Colapso de diversidade: Pass@k cai; estudante perde estrategias alternativas |
| Self-distillation (mesmo modelo como professor) vs. Teacher externo | Nao requer modelo maior; aproveita conhecimento latente do proprio modelo | Risco de information leakage: estudante imita forma de outputs com PI sem ter PI |
| PI como sinal unico vs. PI + verifier externo | Simplicidade: um unico loop de destilacao | PI pode estar errado e nao ha como saber; calibracao sofre |
| Compressao de raciocinio (CRISP) vs. Preservacao de traco completo | Menor custo de inferencia; compressao adaptativa por dificuldade | Supressao de hedging e uncertainty markers; traces mais curtas porem mais confiantemente erradas |
| Multi-teacher averaging vs. Multi-teacher routing | Ensemble natural; cobertura de todos os dominios | Distribuicao media e mais plana que qualquer teacher individual; em caso de discordancia, empurra para algo que nenhum teacher diria |
| Token-level supervision vs. Sequence-level supervision | Sinal denso, per-token; credit assignment fino | Vies em relacao ao target sequencial real; gradiente noise em trajetorias longas |
| Student rollout puro vs. Teacher-mixed sampling | Fechamento completo do exposure bias gap | Rollouts sao lixo no inicio; gradiente SNR colapsa nos prompts mais dificeis |

---

## 5. Padroes de Falha

### 5.1 Token-Level KL como Proxy Fragil

**Mecanismo**: O token-level sampled KL e viesado em relacao ao sequence-level KL que a teoria quer minimizar. O vies piora com acoplamento temporal forte entre tokens — exatamente o regime de raciocinio longo (Fonte: l483-495).

**Consequencia agentica**: Um agente avaliado por "taxa de acerto por passo" pode estar otimizando um proxy que diverge da metrica real de "taxa de sucesso da tarefa completa". Quanto mais longa a trajetoria do agente, pior o vies.

### 5.2 Prefix Drift e Colapso de SNR do Gradiente

**Mecanismo**: Um erro precoce do estudante empurra a trajetoria para fora do suporte do professor. O sinal do professor degrada de informativo -> ruidoso -> prejudicial. Em prompts onde a taxa de acerto do estudante e ~0%, todo rollout contem um erro precoce e o gradiente SNR desaparece (Fonte: l497-509).

**Consequencia agentica**: O agente aprende zero exatamente nas tarefas onde mais precisa aprender. E um loop de morte: falha -> recebe supervisao ruidosa -> nao melhora -> continua falhando.

### 5.3 Colapso de Diversidade (Pass@1 sobe, Pass@k desce)

**Mecanismo**: Reverse KL agressivo concentra massa em uma unica estrategia de raciocinio por prompt. Greedy decoding melhora, mas sampling perde diversidade (Fonte: l535-545).

**Consequencia agentica**: Um agente otimizado para a melhor resposta perde a capacidade de explorar alternativas. Em cenarios onde a primeira estrategia falha (tool call errado, parsing incorreto), o agente nao tem fallback porque "desaprendeu" as estrategias alternativas.

### 5.4 Information Leakage no Self-Distillation

**Mecanismo**: O estudante aprende a imitar a **forma** dos outputs condicionados em PI (padroes lexicos, estrutura, confianca) mesmo quando nao tem PI, colapsando em producao (Fonte: l435-438).

**Consequencia agentica**: Um agente treinado com acesso a logs completos pode aprender a "parecer que tem acesso a logs" em vez de aprender a raciocinar sem eles. Em producao, produz outputs com formato de quem tem informacao privilegiada, mas o conteudo e incorreto.

### 5.5 Overconfidence por Gap de Calibracao PI

**Mecanismo**: O professor condicionado em PI tem confianca mais alta que o estudante sem PI. Destilar essa confiança como target produz um estudante overconfident — pior nos problemas mais dificeis onde PI mais ajuda (Fonte: l547-559).

**Consequencia agentica**: Um agente treinado com supervisor oraculo desenvolve calibracao irreal. Em producao, age com certeza injustificada, ignora sinais de erro, e nao escala para humanos porque "tem certeza" que esta certo.

### 5.6 Epistemic Suppression por Compressao

**Mecanismo**: Compressao de raciocinio suprime hedging e uncertainty markers porque sao tokens de alta entropia que a visao com PI dropa. O resultado e uma trace mais curta que transmite certeza falsa (Fonte: l561).

**Consequencia agentica**: Resumo de contexto que omite hedging induz o agente a tratar informacao incerta como certa. Decisoes baseadas em resumos overconfident propagam erros com confianca.

---

## 6. Sintese

### Principio unificador: OPD como Teoria de "Como Aprender com Seus Proprios Erros"

A literatura de OPD e, no fundo, uma formalizacao de um problema universal em sistemas agenticos: como um sistema aprende com as proprias trajetorias sem depender de dados estaticos que nao refletem sua distribuicao real de operacao. As respostas que a literatura oferece formam um catalogo de mecanicas transferiveis:

1. **Feche o exposure bias gap**: treine na distribuicao de inferencia, nao na de treinamento. Para agentes, isso significa que rollouts de producao (com erros, prefixos estranhos, tool calls que falharam) sao dados de treinamento mais valiosos que datasets curados.

2. **Separe magnitude de direcao**: o RLSD split (self-distillation da magnitude do update, verifier da direcao) e um padrao arquitetonico geral. Em agentes: o modelo pode saber **quais tokens sao importantes** (alta conviccao interna), mas precisa de um sinal externo para saber **se esta indo na direcao certa**.

3. **Gate o sinal de supervisao por confiabilidade**: GATES mostra que "so destilar quando o supervisor tem consenso interno" melhora a qualidade. Em sistemas multi-agente: nao tratar toda saida de sub-agente como igualmente confiavel; amostrar multiplas vezes e usar consenso como gate.

4. **Meça o que voce nao esta medindo**: o token-level KL diverge do sequence-level KL; Pass@1 sobe mas Pass@k desce; a calibracao em treinamento nao e a calibracao em producao. Em agentes: metricas de passo individual nao capturam qualidade de trajetoria; taxa de acerto em benchmark nao captura calibracao em producao.

5. **A supervisao tem prazo de validade**: local teachability collapse mostra que o sinal de supervisao decai ao longo da trajetoria. Em agentes: continuar aplicando o mesmo criterio de avaliacao em todos os passos da trajetoria e contraproducente — a janela de supervisao deve ser adaptativa.

### Implicacoes para sistemas agenticos long-running

- **Context management como self-distillation**: se o agente tem acesso ao contexto completo em treinamento (PI = full context) mas opera com contexto truncado em producao (no-PI view), o self-distillation pode transferir conhecimento do contexto completo para os pesos, reduzindo a dependencia de contexto em runtime.
- **Error cascades como prefix drift**: o mecanismo de prefix drift em OPD (erro precoce -> tokens subsequentes fora do suporte do professor -> supervisao vira ruido) e identico ao mecanismo de cascata de erros em agentes. A solucao estrutural e a mesma: deteccao precoce de drift e re-ancoragem em um prefixo confiavel.
- **Multi-teacher OPD como especializacao de sub-agentes**: o padrao industrial "specialise then unify" (treinar experts por dominio com RL/SFT, depois unificar via multi-teacher OPD) e um template para treinar sub-agentes especializados e depois destila-los em um unico agente deployable.
- **Cross-tokenizer OPD como interoperabilidade de agentes**: o problema de "professor e estudante tem tokenizers diferentes" e analogo a "dois agentes tem vocabularios de acao diferentes". As solucoes da literatura (optimal transport, dual-space projection, vocabulary alignment) sao candidatas a mecanicas de traducao entre agentes heterogeneos.
- **A fronteira atual**: PI + verifier (RLSD) parece ser o consenso emergente — self-distillation fornece densidade de sinal, verifier fornece grounding. Para agentes, isso sugere que o futuro nao e "agente 100% autonomo" nem "agente 100% supervisionado", mas um hibrido onde o agente gera sua propria densidade de aprendizado e um verificador externo (deterministico ou humano) decide a direcao.

### Limites da traducao ML -> agentes

As seguintes conexoes sao mais tenues e dependem de premissas nao verificadas:

- A analogia entre "tokenizer mismatch" e "agent action space mismatch" e sugestiva, mas os metodos de cross-tokenizer OPD (optimal transport, dual-space projection) foram validados apenas em espacos de tokens discretos, nao em espacos de acao estruturados.
- O fenomeno de "rock tokens" (tokens que nunca melhoram) pode nao ter um analogo direto em agentes, ja que acoes de agente sao semanticas e discretas, enquanto rock tokens sao um fenomeno estatistico de distribuicoes de token.
- A matematica de "teacher capability gap" (se o professor nao e muito melhor que o estudante, OPD degenera) e uma limitacao fundamental que se aplica igualmente a qualquer sistema de aprendizado por imitacao, incluindo agentes que aprendem com supervisores fracos.
