---
name: magnitude-direction-verifier-split
description: "Separa o sinal de melhoria do agente em dois componentes independentes: magnitude (o quanto o modelo acredita que uma mudanca importa, extraida de self-distillation delta, log-ratio, atencao, ou confianca interna) e direcao (para onde a mudanca deve ir, determinada por verificador externo, testes, ou revisao humana). Combina magnitude × direcao em um plano de correcao ponderado: gaste esforco de correcao onde o agente tem conviccao FORTE e o verificador confirma a direcao; reduza ou escale quando a direcao e incerta. Previne information leakage (agente aprende a imitar formato sem substancia) e overconfidence collapse (self-distillation puro sem verificacao externa). Usar ao projetar loops de melhoria de agente, ao implementar self-distillation com verificacao, ao calibrar feedback de producao, ou quando o agente produz outputs com formato correto mas conteudo errado. Dispara com: 'magnitude direction', 'verifier split', 'trust but verify', 'confidence direction', 'correction weight', 'self-distillation verifier', 'RLSD', 'magnitude signal', 'direction signal', 'weighted correction', 'verification gate', 'confidence extraction', 'model confidence + verifier', 'split correction plan', 'audit trail magnitude'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: evaluation
  priority: high
  source: "The Imitation Game — State of Policy Distillation in Language (Pattern 6: Magnitude-Direction Verifier Split)"
---

## What I Do

Eu formalizo o principio "trust but verify" para loops de melhoria de agentes. Em vez de tratar o sinal de aprendizado como um bloco unico (o modelo diz X, portanto corrija para Y), eu separo dois sinais que tem fontes, confiabilidades e mecanicas diferentes:

1. **Magnitude** -- extraida do modelo internamente. Responde a pergunta: **"onde o agente acredita que a mudanca importa?"** E um sinal de intensidade: quao forte e a conviccao do modelo sobre quais partes do output sao relevantes para o outcome. Fontes de magnitude incluem:
   - Delta de self-distillation: diferenca entre a distribuicao do modelo com e sem informacao privilegiada
   - Log-ratio: log(P_privilegiado / P_sem_privilegio) por token
   - Hotspot de atencao: tokens ou passos que receberam atencao desproporcional do modelo
   - Intensidade de discordancia: variancia entre multiplos rollouts do mesmo agente para o mesmo prompt
   - Score de confianca interna: probabilidade atribuida pelo modelo a propria saida

2. **Direcao** -- determinada por um verificador externo. Responde a pergunta: **"a mudanca deve ir para frente ou para tras?"** E um sinal de sinal (positivo/negativo) e classe (correcao/reforco/neutro). Fontes de direcao incluem:
   - Verificador determinista: testes, asserts, validacao de schema, diff contra expected output
   - Avaliador externo: outro modelo, agente, ou council que avalia o output sem acesso a confianca interna do agente
   - Revisao humana: aprovacao, rejeicao, ou correcao manual
   - Metrica de producao: outcome observado (ex: usuario clicou, compra concluida, ticket resolvido)

O plano de correcao ponderado combina os dois:

```
correction_weight(token, step) = magnitude(token, step) × direction_signal(token, step)
```

onde `direction_signal` e +1 (reforcar), -1 (corrigir), ou 0 (neutro/incerto). O resultado e um plano que concentra esforco de correcao onde o modelo TEM conviccao (magnitude alta) E o verificador CONFIRMA a direcao (direction definida). Onde a magnitude e alta mas a direcao e incerta, o plano escala para revisao humana em vez de aplicar uma correcao as cegas.

A audit trail registra separadamente a evidencia de confianca (de onde veio a magnitude) e a evidencia de correcao (de onde veio a direcao), permitindo investigar *por que* uma correcao foi aplicada -- se foi por conviccao do modelo, por verificacao externa, ou por ambos.

## When to Use Me

Carregue esta skill quando:

- Voce esta implementando self-distillation em um agente e quer prevenir information leakage (o agente aprende a imitar o formato de saidas com informacao privilegiada sem realmente entender o conteudo)
- Um agente produz outputs que "parecem certos" (formato correto, tom apropriado) mas falham em verificacao de conteudo -- o sintoma classico de self-distillation sem verificacao de direcao
- Voce tem um sinal interno de confianca do modelo (log-ratios, atencao, scores) mas nao confia que ele sozinho determina correcao -- voce precisa de um verificador externo para decidir a direcao
- O custo de verificacao externa e alto e voce quer concentra-lo onde o modelo tem alta conviccao (magnitude alta → vale a pena verificar; magnitude baixa → provavelmente nao importa)
- Voce esta projetando um loop de melhoria continua onde o agente aprende com os proprios erros, mas quer evitar que o agente reforce os proprios vieses (o verificador externo quebra o ciclo de auto-confirmacao)
- Ha divergencia entre o que o modelo "acredita" (alta confianca) e o que o avaliador externo "confirma" (direcao contraria) -- voce precisa de uma politica de escalacao para esses casos
- Voce quer uma audit trail que separe "o modelo estava confiante" de "o verificador confirmou que estava certo" -- para investigacao de falhas e calibracao de confianca
- O [[docs/canonical/generator-evaluator|Generator-Evaluator]] produz um veredito binario (pass/fail) mas voce precisa de um sinal mais granular: nao so "esta errado", mas "onde esta errado e quanto esforco dedicar a corrigir"

Nao use quando:

- Nao ha sinal de magnitude disponivel (o modelo nao produz scores de confianca, log-ratios, ou atencao) -- sem magnitude, o split colapsa para verificacao externa pura
- Nao ha verificador externo disponivel (testes, avaliador, ou humano) -- sem direcao, o split colapsa para self-distillation puro, que e exatamente o cenario de information leakage que este padrao previne
- A tarefa e puramente deterministica e a verificacao externa e barata e completa -- nesse caso, a magnitude nao adiciona valor; confie apenas na direcao
- O custo de extracao de magnitude (calcular log-ratios, rodar multiplos rollouts) e proibitivo para o contexto operacional -- use [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] para decidir quando o custo se justifica
- Voce ja tem um sistema de verificacao que naturalmente pondera por importancia (ex: um avaliador que produz scores por token) -- o split magnitude-direcao e uma arquitetura, nao uma duplicacao de funcionalidade existente

## The Anti-Pattern

```
ANTI-PATTERN: Self-distillation puro sem verificacao externa de direcao,
resultando em information leakage e overconfidence collapse.

Cenario:
  1. Um time treina um agente de suporte usando self-distillation:
     o agente opera com contexto completo (logs, documentos internos,
     playbooks de troubleshooting) e destila o proprio comportamento
     para operar com contexto reduzido (apenas o ticket do cliente).
  2. O agente aprende a produzir outputs que TEM O FORMATO de respostas
     bem-informadas: menciona documentos internos, cita playbooks, usa
     linguagem tecnica apropriada. As metricas de similaridade com o
     professor sao boas.
  3. Em producao, o agente encontra um ticket sobre um produto que ele
     nunca viu. Sem o contexto completo, ele nao sabe a resposta. Mas
     aprendeu que "respostas bem-informadas" tem certas caracteristicas
     de formato. Ele produz uma resposta que PARECE bem-informada --
     cita um documento interno que nao existe, recomenda um playbook
     irrelevante, usa linguagem tecnica correta para o dominio errado.
  4. O cliente le a resposta, parece profissional, segue a recomendacao,
     e o problema piora. O agente estava confiante (alta magnitude) e
     nao havia verificador externo para detectar que a direcao estava
     errada.
  5. O time descobre o problema apenas quando o cliente reporta. Nao ha
     audit trail separando "o modelo estava confiante" de "o verificador
     confirmou" -- porque nao havia verificador.

Cenario alternativo (overconfidence via verificador fraco):
  1. O time adiciona um verificador externo, mas ele e um unico modelo
     que avalia com um prompt simples: "Esta resposta esta correta?"
  2. O verificador, sendo o mesmo modelo base do agente, compartilha os
     mesmos vieses. Quando o agente produz uma resposta com formato
     correto mas conteudo errado, o verificador avalia como "correta"
     porque o formato e familiar.
  3. O agente recebe direction = +1 (reforcar) para uma resposta errada.
     A magnitude e alta (o agente estava confiante). O plano de correcao
     ponderado REFORCA o comportamento errado com peso maximo.
  4. O agente se torna progressivamente mais confiante em respostas
     erradas -- exatamente o oposto do objetivo.

Consequencia:
  - Information leakage: o agente aprendeu o formato, nao o conteudo
  - Overconfidence collapse: sem verificador independente, a confianca
    do modelo reforca os proprios erros
  - Custo de correcao post-hoc: uma vez que o comportamento errado foi
    reforcado, desfaze-lo requer desaprendizado, nao apenas correcao
  - Perda de confianca do time: "o agente parece bom mas nao e confiavel"
```

## The Pattern

```
PATTERN: Split magnitude (modelo interno) e direcao (verificador externo)
em sinais independentes, combinar em plano de correcao ponderado, escalar
conflitos para revisao humana.

Fluxo:

  Agente produz output (trajetoria, resposta, plano)
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. EXTRACAO DE MAGNITUDE (MODELO INTERNO)                │
  │                                                         │
  │ Para cada token, passo, ou segmento do output:           │
  │                                                         │
  │   Calcule o sinal de magnitude usando uma ou mais        │
  │   fontes:                                               │
  │                                                         │
  │   a) Self-distillation delta:                             │
  │      magnitude = |log P_PI(token) - log P_noPI(token)|   │
  │      (diferenca entre visao privilegiada e sem privilegio)│
  │                                                         │
  │   b) Log-ratio (RLSD-style):                             │
  │      magnitude = |log(P_teacher/P_student)|               │
  │      (razao entre distribuicao do professor e do agente) │
  │                                                         │
  │   c) Attention hotspot:                                  │
  │      magnitude = attention_weight(token) / mean_attention│
  │      (tokens que receberam atencao desproporcional)      │
  │                                                         │
  │   d) Disagreement intensity:                             │
  │      magnitude = variance entre k rollouts do agente     │
  │      (onde o agente hesita ou diverge)                   │
  │                                                         │
  │   e) Internal confidence score:                          │
  │      magnitude = 1 - entropy(token_distribution)         │
  │      (quao certo o modelo esta sobre a escolha do token) │
  │                                                         │
  │   Normalize: magnitude em [0, 1] por segmento            │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. EXTRACAO DE DIRECAO (VERIFICADOR EXTERNO)             │
  │                                                         │
  │ Para o mesmo output, execute verificacao externa:        │
  │                                                         │
  │   a) Verificador determinista:                            │
  │      direction = teste.passou ? +1 : -1                  │
  │      (asserts, schema validation, diff contra expected)  │
  │                                                         │
  │   b) Avaliador externo (modelo/agente independente):     │
  │      direction = avaliador.rubrica(output) ∈ {+1,0,-1}  │
  │      (correto, incerto, incorreto)                       │
  │                                                         │
  │   c) Council de avaliacao:                               │
  │      direction = aggregate(k_avaliadores) com threshold  │
  │      (consenso → direcao definida; discordancia → 0)     │
  │                                                         │
  │   d) Revisao humana:                                     │
  │      direction = humano.aprovou ? +1 : humano.corrigiu   │
  │                 ? (correcao especifica) : 0              │
  │                                                         │
  │   e) Outcome de producao:                                │
  │      direction = outcome_positivo ? +1 : -1              │
  │      (metrica de negocio observada)                      │
  │                                                         │
  │   CRITICO: o verificador NAO deve ter acesso a magnitude.│
  │   A direcao e determinada apenas pelo output e pelo      │
  │   criterio de correcao, nao pela confianca do modelo.    │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. COMBINACAO: PLANO DE CORRECAO PONDERADO               │
  │                                                         │
  │ Para cada token/passo/segmento:                          │
  │                                                         │
  │   IF direction is defined (≠ 0):                         │
  │     correction_weight = magnitude × direction            │
  │                                                         │
  │     IF correction_weight > HIGH_THRESHOLD:               │
  │       → CORRECAO PRIORITARIA (aplicar com peso maximo)   │
  │       (modelo confiante + verificador confirma)          │
  │                                                         │
  │     ELSE IF correction_weight > LOW_THRESHOLD:           │
  │       → CORRECAO NORMAL (aplicar com peso proporcional)  │
  │                                                         │
  │     ELSE:                                                │
  │       → CORRECAO MINIMA (aplicar com peso reduzido)      │
  │       (modelo incerto ou verificador pouco confiante)    │
  │                                                         │
  │   ELSE (direction == 0, incerto):                        │
  │     IF magnitude > HIGH_THRESHOLD:                       │
  │       → ESCALAR para revisao humana                      │
  │       (modelo confiante mas verificador nao decide)      │
  │     ELSE:                                                │
  │       → DEFERIR (adiar correcao, acumular para batch)    │
  │       (modelo incerto e verificador incerto)             │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. AUDIT TRAIL                                            │
  │                                                         │
  │ Para cada correcao aplicada, escalada, ou deferida:      │
  │                                                         │
  │   Registre separadamente:                                │
  │   - EVIDENCIA DE MAGNITUDE:                              │
  │       * Fonte (self-distillation, log-ratio, atencao)    │
  │       * Valor bruto e normalizado                        │
  │       * Segmento/token especifico                        │
  │   - EVIDENCIA DE DIRECAO:                                │
  │       * Fonte (teste, avaliador, council, humano)        │
  │       * Valor (+1, 0, -1) e confianca do verificador     │
  │       * Criterio de correcao aplicado                    │
  │   - DECISAO:                                             │
  │       * correction_weight final                          │
  │       * Acao tomada (corrigir, escalar, deferir)         │
  │       * Timestamp e versao do modelo/verificador         │
  │                                                         │
  │   Esta separacao permite investigar:                     │
  │   - "O modelo estava confiante mas errado?"              │
  │     → magnitude alta, direction = -1                    │
  │   - "O verificador detectou algo que o modelo nao viu?"  │
  │     → magnitude baixa, direction definida               │
  │   - "O verificador e o modelo discordam?"                │
  │     → magnitude alta, direction contraria               │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 5. CALIBRACAO E FEEDBACK                                 │
  │                                                         │
  │ Periodicamente (ex: semanal ou a cada N correcoes):      │
  │                                                         │
  │   - Compare magnitude vs. outcome real:                   │
  │       O modelo e bem-calibrado? (magnitude alta →        │
  │       outcome positivo?)                                 │
  │   - Compare direction vs. outcome real:                   │
  │       O verificador acerta a direcao? (direction = +1    │
  │       → outcome positivo?)                               │
  │   - Detecte vies sistematico:                            │
  │       O verificador tende a concordar com magnitude      │
  │       alta? (possivel vies de formato)                   │
  │   - Ajuste thresholds de escalacao:                      │
  │       HIGH_THRESHOLD muito baixo → muitas escalacoes     │
  │       desnecessarias; muito alto → correcoes erradas     │
  │       passam sem escalacao                               │
  └─────────────────────────────────────────────────────────┘
```

### Formula de Correcao Ponderada (RLSD-style)

O mecanismo matematico central, adaptado de RLSD:

```
Para cada token t na trajetoria:

  magnitude_t = |log(P_teacher(y_t | x, PI, y_<t) / P_student(y_t | x, y_<t))|

  direction_t = sign(advantage_verifier(t))
    onde advantage_verifier(t) e determinado por:
    - Teste deterministico: +1 se output passa, -1 se falha
    - Avaliador externo: +1 se rubrica ≥ threshold, -1 se < threshold
    - Council: +1 se majority vote com agreement > 0.66, 0 se split
    - Humano: +1 se aprovado, -1 se rejeitado, 0 se ambivalente

  correction_weight_t = magnitude_t ^ direction_t
    = magnitude_t se direction = +1 (reforcar)
    = 1 / magnitude_t se direction = -1 (corrigir: peso alto =
      tokens errados que o modelo considera importantes)
    = 0 se direction = 0 (incerto: nao aplicar correcao)
```

### Tabela de Decisao: Magnitude × Direcao

| Magnitude | Direcao | Interpretacao | Acao |
|---|---|---|---|
| Alta | +1 (correto) | Modelo confiante E verificador confirma que esta certo. Melhor cenario. | **REFORCAR**: aplicar correcao maxima positiva. Adicionar a exemplos/demonstracoes. |
| Alta | -1 (incorreto) | Modelo confiante MAS esta errado. Cenario mais perigoso (overconfidence). | **CORRIGIR FORTE**: aplicar correcao maxima negativa. Prioridade maxima de correcao. Registrar como caso de overconfidence. |
| Alta | 0 (incerto) | Modelo acredita que importa, mas verificador nao consegue decidir direcao. | **ESCALAR**: enviar para revisao humana. Nao aplicar correcao automatica. |
| Baixa | +1 (correto) | Modelo incerto, mas output esta correto. O modelo nao "sabe" que esta certo. | **REFORCAR LEVE**: correcao positiva com peso baixo. Oportunidade de aumentar confianca do modelo. |
| Baixa | -1 (incorreto) | Modelo incerto E output errado. Erro de baixa conviccao. | **CORRIGIR LEVE**: correcao negativa com peso baixo. Pode ser ruido -- acumular para batch. |
| Baixa | 0 (incerto) | Nem o modelo nem o verificador tem sinal claro. | **DEFERIR**: adiar. Acumular para revisao periodica em batch. |

### Fontes de Magnitude por Disponibilidade

| Cenario | Fonte Recomendada | Custo | Precisao |
|---|---|---|---|
| Self-distillation disponivel (agente opera com/sem PI) | Log-ratio PI vs. no-PI | Medio (requer duas passagens) | Alta (sinal denso per-token) |
| Apenas um modelo, sem professor | Entropia da distribuicao de saida | Baixo (uma passagem) | Media (confianca ≠ importancia) |
| Multiplos rollouts viaveis | Variancia entre rollouts | Alto (k passagens) | Alta (discordancia revela incerteza) |
| Modelo com atencao acessivel | Peso de atencao por token | Baixo (byproduct da inferencia) | Media (atencao pode ser difusa) |
| Sem acesso interno ao modelo | Heuristica de importancia (ex: tokens de decisao, verbos de acao) | Muito baixo | Baixa (heuristica, nao sinal do modelo) |

## Implementation Rules

1. **O verificador e cego a magnitude.** Se o verificador sabe quais tokens o modelo considera importantes, ele pode ser influenciado por essa informacao -- exatamente o vies que o split previne. O verificador recebe apenas o output e os criterios de avaliacao, nunca os scores de confianca. Implemente isso via [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]].

2. **Use multiplos verificadores para direcao de alta criticidade.** Um unico verificador (especialmente um unico modelo) compartilha vieses com o agente. Para decisoes de alta magnitude com direcao incerta, use [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] com diversidade de modelos e threshold de consenso. Se o council discorda (direction = 0), escale para humano.

3. **Magnitude sem verificacao e information leakage.** O cenario onde magnitude existe mas direction e sempre +1 (ou nao e verificada) e equivalente a self-distillation puro -- o modelo aprende a imitar o formato sem garantia de correcao. Se voce nao tem um verificador externo, nao implemente metade do padrao. E melhor nao ter magnitude do que ter magnitude sem direcao.

4. **O threshold de escalacao define o custo operacional.** HIGH_THRESHOLD controla quantos casos vao para revisao humana. Muito baixo → overload de revisao, custo alto. Muito alto → correcoes erradas passam sem escalacao, risco alto. Comece conservador (threshold baixo, muitas escalacoes) e ajuste para cima conforme o verificador prova confiabilidade.

5. **A audit trail e a unica defesa contra deterioracao silenciosa.** Sem audit trail separando magnitude e direcao, e impossivel diagnosticar por que uma correcao foi aplicada incorretamente. A audit trail permite detectar: (a) vies de verificador (direction sistematicamente errada), (b) overconfidence do modelo (magnitude alta + direction negativa frequente), (c) divergencia modelo-verificador (conflitos frequentes).

6. **A magnitude deve ser normalizada por segmento, nao globalmente.** Um token com magnitude 0.8 em uma trajetoria curta e simples pode ser menos importante que um token com magnitude 0.3 em uma trajetoria longa e complexa. Normalize dentro do escopo relevante (por passo, por trajetoria, ou por classe de tarefa), nao globalmente.

7. **O custo de extracao de magnitude deve ser proporcional ao valor da correcao.** Calcular log-ratios per-token para toda trajetoria e caro. Use [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]: tier fast (heuristica de importancia) para todas as trajetorias; tier medium (entropia ou atencao) para trajetorias com baixa confianca do verificador; tier deep (log-ratio com multiplos rollouts) apenas para trajetorias com alta magnitude e direcao incerta.

8. **Conflitos magnitude-direcao sao o sinal mais valioso.** Quando magnitude e alta e direction e -1 (modelo confiante, mas errado), voce encontrou um caso de overconfidence -- exatamente o que o padrao existe para detectar. Esses casos devem ser priorizados para analise: o que o modelo "aprendeu" que o torna confiante em algo errado? O verificador esta correto ou e um falso negativo?

## Integration with Existing Repo Infrastructure

O magnitude-direction-verifier-split conecta a infraestrutura de avaliacao e geracao do repositorio, adicionando a dimensao de confianca interna que falta ao Generator-Evaluator e aos mecanismos de verificacao existentes:

| Componente Existente | Como o Magnitude-Direction Verifier Split complementa |
|---|---|
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Generator-Evaluator produz um veredito binario (pass/fail) que serve como direction signal. O split adiciona a magnitude: o Generator tambem exporta seus scores de confianca interna, e o Evaluator fornece a direcao. A combinacao produz um plano de correcao ponderado em vez de um veredito binario. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A avaliacao ancorada em constraints fornece direction signals deterministicos e especificos (constraint X violada no passo Y). O split adiciona magnitude: para cada constraint violada, qual a conviccao do modelo sobre os tokens/passos envolvidos? Isso prioriza quais violacoes corrigir primeiro. |
| [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] | A compartimentalizacao garante que o verificador (direction) nao ve a magnitude. E o mecanismo de selagem que torna o split seguro: sem compartimentalizacao, o verificador pode ser influenciado pela confianca do modelo. |
| [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] | O council fornece direction signals com diversidade de modelos. Quando o council discorda (direction = 0), o split escala para revisao humana se a magnitude for alta. O council reduz o risco de um unico verificador enviesado. |
| [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] | A estratificacao define quando usar extracao de magnitude cara (log-ratio, multiplos rollouts) vs. barata (entropia, heuristica). Tiers fast/medium/deep mapeiam para fontes de magnitude de baixo/medio/alto custo. |
| [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] | A correlacao eval→producao valida se a direcao do verificador (medida em eval) corresponde ao outcome real (medido em producao). Se a direcao do verificador nao correlaciona com outcomes, o plano de correcao ponderado esta aplicando correcoes na direcao errada. |
| [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] | Falhas de producao onde magnitude era alta e direction era +1 (overconfidence) sao os casos mais valiosos para o regression flywheel: o modelo estava confiante e errado, e o verificador nao detectou. Esses casos devem gerar novos casos de regressao e possivelmente recalibrar o verificador. |
| [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] | Conflitos magnitude-direcao (alta magnitude, direction contraria) sao uma classe de falha especifica: overconfidence collapse. O loop de classificacao pode categorizar esses conflitos e rotear para recalibracao do verificador ou ajuste do threshold de escalacao. |
| [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] | O context stack suporta a operacao do split: a visao privilegiada (para calcular magnitude) usa camadas adicionais do stack; a visao runtime (para direcao) usa o stack padrao. A diferenca entre as duas visoes e a propria fonte de magnitude. |
| [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] | O feedback writeback do OS e o destino das correcoes ponderadas: correcoes com peso alto sao escritas como memoria confiavel; correcoes com peso baixo sao escritas como sugestoes; conflitos sao escritos como itens de revisao. |

## Quality Gates

Antes de declarar o split magnitude-direcao como operacional, verifique:

- [ ] Pelo menos uma fonte de magnitude esta implementada e produz scores normalizados em [0, 1] por segmento (token, passo, ou trajetoria)
- [ ] Pelo menos uma fonte de direcao externa e independente esta implementada (teste deterministico, avaliador externo, council, ou revisao humana)
- [ ] O verificador NAO tem acesso aos scores de magnitude (compartimentalizacao selada)
- [ ] A audit trail registra separadamente: evidencia de magnitude (fonte, valor, segmento), evidencia de direcao (fonte, valor, criterio), e decisao final (correction_weight, acao)
- [ ] HIGH_THRESHOLD e LOW_THRESHOLD estao definidos e documentados com justificativa
- [ ] Politica de escalacao esta definida: magnitude alta + direcao incerta → revisao humana (quem, como, prazo)
- [ ] O custo de extracao de magnitude esta calibrado por tier (fast/medium/deep) e nao excede o orcamento operacional
- [ ] Calibracao periodica esta agendada: comparar magnitude vs. outcome real, direction vs. outcome real, detectar vies sistematico
- [ ] Casos de overconfidence (magnitude alta, direction = -1) sao priorizados para analise e geram itens de backlog ou regressao
- [ ] O verificador foi validado independentemente: taxa de acerto da direcao > 0.80 em um conjunto de teste separado do conjunto de treinamento do agente
- [ ] Se usando council para direcao, o threshold de consenso esta definido (ex: majority vote com agreement > 0.66) e a politica de discordancia (direction = 0) esta documentada

## References

- [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]:126-132 — RLSD: split entre self-distillation magnitude e verifier direction, formula w_t = (P_T/P_S)^sign(A)
- [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]:132 — "E a formalizacao matematica do trust but verify"
- [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]:140-163 — Pattern 6: Magnitude-Direction Verifier Split (inputs, outputs, benefits, limitations)
- [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|Policy Distillation Classification]]:200-234 — Classificacao como Missing (High integration value)
- [[docs/canonical/generator-evaluator|Generator-Evaluator]] — direcao externa via separacao geracao/avaliacao
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — direction signals deterministicos por constraint
- [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] — selagem que impede verificador de ver magnitude
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — direction com diversidade de modelos e threshold de consenso
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — estratificacao de custo para fontes de magnitude
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — validacao de que direcao em eval prediz outcome em producao
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — overconfidence cases como entrada para regression
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — conflitos magnitude-direcao como classe de falha
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] — suporte a visao privilegiada vs. runtime para extracao de magnitude
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] — destino das correcoes ponderadas no feedback writeback

---

*Created: 2026-06-16 | Source: The Imitation Game — State of Policy Distillation in Language — Pattern 6 (Missing, High value)*
