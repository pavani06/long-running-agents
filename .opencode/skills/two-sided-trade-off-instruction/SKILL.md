---
name: two-sided-trade-off-instruction
description: "Reescreve instrucoes de face unica (que declaram so o custo de uma acao: 'escalonar custa $8', 'evite reembolsos', 'nunca repasse detalhes') em instrucoes de duas faces que declaram o trade-off completo: o custo da acao E o contra-custo de evita-la erradamente (exposicao a chargeback, perda de confianca do cliente, caso mal resolvido), deixando o modelo exercer julgamento por caso. Elimina single-objective overfit — under-escalation causado por otimizar o unico objetivo declarado no prompt — e resolve conflito prompt-vs-eval alinhando o framing da instrucao com o comportamento que o eval define como correto. Usar ao escrever ou revisar policy de escalonamento, refund, handoff, recusa ou qualquer acao cuja frequencia o prompt controla; quando o agente nunca (ou sempre) executa a acao mesmo em casos onde o oposto e correto; ou quando prompt e eval divergem sobre o comportamento desejado. Dispara com: 'two-sided trade-off', 'counter-cost', 'custo de escalonar', 'balanced instruction', 'under-escalation', 'over-optimization', 'single objective', 'instruction economics', 'escalation cost', 'refund policy prompt', 'trade-off instruction', 'both sides instruction', 'prompt overfit', 'agente nunca escala', 'instrucao balanceada', 'cost of not escalating', 'custo do contra-argumento', 'prompt de face unica'."
license: MIT
compatibility: opencode
metadata:
  audience: agent-implementers
  workflow: prompt-design
  priority: medium
  source: "The Prompting Playbook — Pattern 5: Two-Sided Trade-off Instruction"
---

## What I Do

Eu converto instrucoes de face unica em instrucoes de duas faces. Uma instrucao de face unica declara apenas um lado do trade-off de uma acao — tipicamente o custo ("escalonar para um humano custa $8 por caso", "reembolsos afetam a metrica do time") — e o modelo trata esse unico objetivo declarado como a funcao a otimizar. O resultado e overfit: o agente para de escalar, reembolsar ou repassar MESMO nos casos em que a acao e claramente correta, porque o prompt so descreveu o preco de agir e nunca o preco de nao agir.

A instrucao de duas faces declara o trade-off completo:

1. **A acao cuja frequencia o prompt deve controlar** — escalar, reembolsar, repassar para humano, recusar.
2. **O custo da acao** — dinheiro, metricas do time, latencia.
3. **O contra-custo de evita-la erradamente** — exposicao a fraude/chargeback, confianca do cliente, caso mal resolvido que retorna amanha.
4. **O comportamento que o eval espera** — o framing da instrucao deve casar com o que o suite define como correto, caso por caso.

O output e uma instrucao balanceada que transfere a decisao do prompt para o julgamento do modelo, por caso. Modelos atuais sao bons em julgar trade-offs quando os dois lados estao declarados; a instrucao de face unica esconde metade da funcao de decisao e o modelo otimiza o que ve.

## When to Use Me

Carregue esta skill quando:

- Voce esta escrevendo ou revisando a policy de escalonamento, reembolso, handoff ou recusa no prompt de um agente de producao (o bloco de policy do [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]])
- Um agente em producao nunca executa a acao que o prompt menciona (under-escalation) mesmo em casos ambíguos de alto risco onde escalar e obviamente correto — o sintoma classico de single-objective overfit
- O inverso: um agente executa a acao em excesso porque o prompt so declara o lado do beneficio, nunca o custo
- O prompt diz "evite X" mas o eval espera X em casos boundary — conflito prompt-vs-eval em que os dois artefatos divergem sobre o comportamento desejado
- Uma migracao de modelo tornou uma instrucao antiga perigosa: modelos mais novos, mais instruccionais, over-complacem proibicoes de face unica escritas para modelos antigos
- Voce quer que o modelo exerca julgamento por caso em vez de seguir uma regra cega, e precisa do formato de instrucao que habilita esse julgamento

Nao use quando:

- O comportamento DEVE ser deterministico — compliance, seguranca, regras regulatorias. Nesses casos a regra permanece binaria; converter invariante em julgamento e exatamente o erro inverso. Use o teste de decisao do [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] ("se a falha ainda existe com um modelo melhor, e invariante candidato") para separar o que e julgamento do que e invariante
- Voce nao conhece os dois lados bem o suficiente para declara-los (sem o contra-custo quantificado ou qualificado, a instrucao balanceada vira uma de face unica com decoracao)
- Nao existe eval que defina o comportamento correto — sem eval, "caso por caso" e imcomunicavel e o framing nao tem contra o que ser alinhado (veja [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]])
- O problema e o mecanismo runtime de escalonamento (como escalar, para qual fila, com qual contexto) — isso e o [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]; esta skill governa o economics da decisao de escalar (se e quando), nao o mecanismo

## The Anti-Pattern

```
ANTI-PATTERN: Instrucao de face unica que declara so o custo da acao,
fazendo o modelo over-otimizar o unico objetivo declarado e nunca agir.

Cenario:
  1. Um time de suporte escreve no prompt do agente:
     "Escalating a case to tier-2 human support costs $8 per case
      and hurts the team's resolution-rate metric. Avoid
      unnecessary escalations."
  2. O modelo le UM objetivo: minimizar escalonamentos. Nenhuma
     outra funcao de custo foi declarada, entao essa e a funcao
     inteira.
  3. A taxa de escalonamento cai de 12% para 0.3%. O time comemora
     a "economia".
  4. Meses depois, os numeros reais: chargebacks por fraude nao
     detectada subiram (casos ambíguos de verificacao pararam de
     escalar), clientes VIP irritados churnaram (o agente respondeu
     com script em vez de escalar), e tickets mal resolvidos
     retornam como reabertura.
  5. O eval confirma: o suite tem casos boundary onde escalar e a
     resposta correta — o agente falha em todos, porque o prompt
     ensinou o oposto.
  6. O time diagnostica "modelo fraco em julgamento" e discute
     trocar de modelo. O modelo estava otimizando exatamente o que
     o prompt declarou. A funcao de custo estava incompleta, nao o
     modelo.

Consequencia:
  - Single-objective overfit: o modelo otimiza o unico lado visivel
    do trade-off
  - O contra-custo migra para metricas que o prompt nao ve
    (chargeback, churn, reabertura) — o custo nao desapareceu,
    trocou de lugar
  - Prompt e eval divergem: o eval falha em casos boundary que o
    prompt proibe acertar
  - Diagnostico errado ("modelo ruim") leva a gastar emCapability
    onde o fix era uma instrucao completa
```

## The Pattern

```
PATTERN: Declarar os dois lados do trade-off na mesma instrucao,
alinhando o framing com o que o eval define como correto, e deixar
o modelo julgar por caso.

Fluxo:

  Instrucao de face unica identificada (ou policy nova a escrever)
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 1: Identificar a acao e elencar os dois lados      │
  │                                                         │
  │   ACAO: escalar / reembolsar / repassar / recusar        │
  │   CUSTO DE AGIR: $8 por caso, metrica do time, latencia  │
  │   CONTRA-CUSTO DE NAO AGIR ERRADAMENTE: chargeback medio │
  │     $120, conta VIP = milhares, caso reaberto = 2x custo │
  │                                                         │
  │ Se um dos lados nao pode ser declarado (nao conhecido),  │
  │ pare: instrucao balanceada sem contra-custo e face unica │
  │ com decoracao.                                          │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 2: Escrever a instrucao de duas faces              │
  │                                                         │
  │ Ambos os lados no MESMO bloco, adjacentes, com numeros   │
  │ quando houver. A regra de julgamento explicita compara   │
  │ os dois lados:                                          │
  │                                                         │
  │   <policy name="escalation">                             │
  │   Escalating to tier-2 human support costs ~$8 and adds  │
  │   ~10 minutes. NOT escalating an ambiguous high-risk     │
  │   case costs more: average fraud chargeback is $120; a   │
  │   lost VIP account is thousands. Judgment rule: escalate │
  │   whenever the expected cost of NOT escalating exceeds   │
  │   the cost of escalating.                                │
  │   </policy>                                              │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 3: Alinhar o framing com o eval                    │
  │                                                         │
  │   - Leia os casos do suite onde a acao e correta e onde  │
  │     e incorreta. A instrucao deve autorizar o primeiro   │
  │     conjunto e desencorajar o segundo — mesmo vocabulario │
  │     de risco, mesmas classes de caso.                    │
  │   - Se o eval espera escalonamento em caso ambíguo, a    │
  │     instrucao nao pode chamar o mesmo caso de            │
  │     "unnecessary". Conflito prompt-vs-eval = framing     │
  │     desalinhado, resolvido aqui e nao no eval.           │
  │   - Casos boundary novos (quando agir e quando nao)      │
  │     entram no suite como avaliacao da calibracao.        │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 4: Registrar a mudanca como mudanca causal         │
  │                                                         │
  │ A reescrita e uma mudanca de prompt como qualquer outra: │
  │ trigger (under-escalation observado), diagnostico        │
  │ (instrucao de face unica), intencao (declarar contra-    │
  │ custo) — registrada via [[docs/canonical/prompt-as-code- │
  │ causal-change-management|Prompt-as-Code Causal Change    │
  │ Management]], com rollback.                              │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ PASSO 5: Revalidar pos-migracao de modelo                │
  │                                                         │
  │ Modelos mais instruccionais over-complacem proibicoes    │
  │ antigas. Toda migracao de modelo re-testa os casos       │
  │ boundary: o balanceamento ainda produz a frequencia      │
  │ esperada de acao?                                       │
  └─────────────────────────────────────────────────────────┘
```

### Tabela: Lados de Trade-off por Acao Tipica

| Acao | Custo de agir (lado 1) | Contra-custo de nao agir erradamente (lado 2) |
|---|---|---|
| Escalar para humano | $8/caso, latencia +10min, metrica do time | Chargeback por fraude ($120+), churn de VIP, caso reaberto (2x custo) |
| Conceder reembolso | Margem perdida, abuso incentivo | Chargeback forcado (custo + taxa), reclamacao publica, churn |
| Repassar detalhes do plano ao cliente | Risco de interpretacao errada | Information withholding: cliente cancela por no satisfazer pedido legitimo que os dados em contexto suportam |
| Recusar tarefa fora de escopo | Custa uma resposta | Refusa de tarefa que o agente TEM capacidade de resolver, perda de confianca |

### Tabela de Decisao: Regra Dura vs Instrucao de Duas Faces

| Situacao | Forma da instrucao | Racional |
|---|---|---|
| Compliance/seguranca/regulatorio ("nunca exponha PII") | Regra dura, invariante | Nao existe trade-off a julgar; violacao e inaceitavel em qualquer caso |
| Dominio de risco com custo conhecido nos dois lados | Instrucao de duas faces | O julgamento por caso e o valor; os numeros habilitam a comparacao |
| Acao com contra-custo desconhecido | Nao reescreva ainda | Face unica com decoracao; elicite o contra-custo primeiro |
| Frequencia errada em producao mas prompt sem custo declarado | Adicione os dois lados | O overfit pode estar no lado do beneficio (agir demais) — mesma correcao, lados trocados |

## Implementation Rules

1. **Os dois lados no mesmo bloco, adjacentes.** Custo no bloco de policy e contra-custo em outra secao do prompt recria o overfit parcialmente: o modelo pondera o que esta junto. A regra de julgamento ("escale quando o custo esperado de nao escalar exceder o custo de escalar") fecha a comparacao.

2. **Assimetria numerica num lado so recria o overfit.** "$8 por caso" sem os "$120 de chargeback" deixa a funcao de custo visivelmente inclinada para um lado. Quantifique os dois lados ou qualifique os dois lados — nunca numero de um lado e adjetivo do outro.

3. **Nao converta invariante em julgamento.** Antes de balancear, aplique o teste do [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]: se o comportamento correto e o mesmo em todos os casos (compliance, seguranca), a regra binaria permanece. A instrucao de duas faces e para o espaco onde casos legitimos existem nos dois lados.

4. **O framing segue o eval, nao o contrario.** Quando prompt e eval divergem sobre o comportamento correto, ou o eval esta certo (a instrucao e reescrita para casa com ele) ou o eval esta errado (o caso e reclassificado). Nunca deixe os dois divergirem em silencio: o modelo aprende um e o suite mede outro.

5. **Comportamento fica menos deterministico — cubra com eval.** A instrucao de duas faces converte regra em julgamento; a variancia aumenta por design. Os casos boundary (quando agir / quando nao agir) precisam entrar no suite como casos proprios, no espirito do [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]].

6. **Registre a reescrita como mudanca causal.** "Por que esta instrucao declara contra-custo?" precisa ter resposta auditavel daqui a seis meses — trigger, diagnostico, intencao, via [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]. Instrucao balanceada sem registro vira o proximo patch defensivo misterioso.

7. **Migracao de modelo re-testa o balanceamento.** Modelos mais novos over-complacem instrucoes face-unica antigas e recalibram o ponto de equilibrio de julgamento. O gate de migracao do [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] deve incluir os casos boundary da acao balanceada na comparacao pre-pos.

## Integration with Existing Repo Infrastructure

O two-sided trade-off instruction preenche a lacuna de design de instrucao na infraestrutura de escalonamento e avaliacao do repositorio (hoje toda arquitetural, nunca instrucional):

| Componente Existente | Como o Two-Sided Trade-off Instruction complementa |
|---|---|
| [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] | O bloco de policy do harness prompt e onde a instrucao balanceada vive. O canonical enumera policy como bloco distinto (:22); esta skill define o formato do conteudo de policy para acoes com trade-off: dois lados declarados, regra de julgamento explicita. |
| [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] | O ladder e o mecanismo runtime: classify, retry, safe fallback, escalates to a human with summarized context (:29). Esta skill e o complemento instrucional: a decisao de ESCALAR (economics, por caso) vive no prompt como trade-off de duas faces; o ladder executa a escalada decidida. |
| [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]] | Quando o agente decide escalar (instrucao balanceada), o help API garante que a resolucao volta e o loop fecha (:30-32). Frequency governada pelo prompt; mecanismo de retorno governado pelo loop fechado. |
| [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]] | O routing gate decide por tipo de tarefa o que vai para humano (:37); a instrucao de duas faces decide por caso, dentro do turno, para acoes cujo trade-off varia com o contexto. Complementares: gate = roteamento estrutural; instrucao = julgamento economico. |
| [[docs/canonical/generator-evaluator|Generator-Evaluator]] | O Evaluator e a fonte da verdade sobre o comportamento correto por caso (veredito approve/reject com feedback, :31). O framing da instrucao balanceada e validado contra esses vereditos: o que o Evaluator reprova por "devia ter escalado" e o contra-custo que o prompt precisa declarar. |
| [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] | A camada semantica (Layer 2, :45-59) e onde os casos boundary da acao balanceada sao avaliados: escalonou quando devia? omitiu quando nao devia? Sem essa camada, "julgamento por caso" nao e verificavel. |
| [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] | A matriz de verificacao (:31-33) ancora cada caso boundary como linha com pass/fail — o caso vira regressao permanente do balanceamento. |
| [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] | Fornece o teste que separa o que permanece regra dura (invariante: falha existe com qualquer modelo) do que vira instrucao de duas faces (julgamento: casos legitimos nos dois lados). Sem esse teste, balancear tudo e tao errado quanto balancear nada. |
| [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]] | A reescrita de face unica para duas faces e uma mudanca de prompt como qualquer outra: tres perguntas causais obrigatorias (:32-59), rollback (:80-85). O registro preserva o porque do balanceamento para auditorias futuras. |
| [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] | O gate de migracao compara candidato vs atual por categoria (:43-59); os casos boundary da acao balanceada entram nessa comparacao — under-escalation pos-migracao e regressao de categoria, nao ruido. |

## Quality Gates

Antes de declarar a instrucao de duas faces como pronta, verifique:

- [ ] A acao, o custo de agir E o contra-custo de nao agir erradamente estao declarados no MESMO bloco de instrucao, adjacentes
- [ ] Os dois lados tem a mesma forca de evidencia (numero com numero, ou qualificado com qualificado) — sem assimetria numerica de um lado so
- [ ] A regra de julgamento por caso esta explicita ("aja quando o custo esperado de nao agir exceder o custo de agir"), nao implicita
- [ ] O comportamento passou pelo teste de invariante: o que e compliance/seguranca PERMANECEU regra dura e nao foi balanceado
- [ ] O framing foi lido contra o eval: os casos onde o suite espera a acao sao autorizados pela instrucao, e os casos onde nao espera sao desencorajados — sem contradicao prompt-vs-eval
- [ ] Casos boundary (quando agir / quando nao agir) foram adicionados ao suite de avaliacao como casos proprios
- [ ] A reescrita foi registrada como mudanca causal (trigger, diagnostico, intencao) com rollback disponivel
- [ ] A frequencia da acao em producao (ou no suite) sera medida antes/depois — o balanceamento e uma hipotese ate a medida
- [ ] A migracao de modelo futura incluira os casos boundary na comparacao pre-pos do gate

## References

- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]:92-110 — Pattern 5: Two-Sided Trade-off Instruction (inputs, outputs, benefits, limitations)
- [[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|The Prompting Playbook Classification]]:91-103 — Classificacao como Missing (Medium integration value), com NOT_FOUND das buscas que confirmam a ausencia
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:22 — policy como bloco distinto do harness prompt, destino da instrucao balanceada
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29 — mecanismo runtime de escalada (adjacente: mecanismo, nao economics)
- [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]]:30-32 — escalonamento terminal e o loop que fecha
- [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]:37 — roteamento por julgamento de produto (adjacente: estrutural, nao instrucional)
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31 — veredito com feedback como fonte do comportamento correto
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:67 — teste de decisao invariante vs julgamento
- [[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]:32-59 — perguntas causais obrigatorias para a reescrita
- [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]:43-59 — comparacao por categoria onde os casos boundary entram
- [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]:45-59 — camada semantica que avalia o julgamento por caso

---

*Created: 2026-09-02 | Source: The Prompting Playbook — Pattern 5 (Missing, Medium value)*
