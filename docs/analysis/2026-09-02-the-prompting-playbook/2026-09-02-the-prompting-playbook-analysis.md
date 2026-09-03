---
title: "Análise de Conhecimento Não-Óbvio: The Prompting Playbook"
type: analysis
tags: ["agentes-orquestracao", "harness-engineering", "evals", "context-engineering", "production"]
date: 2026-09-02
aliases: ["prompting playbook analysis", "playbook de prompting", "regressao de prompt na migracao de modelo", "generate evaluate repair loop"]
last_updated: 2026-09-02
relates-to: ["[[docs/system-of-record|System of Record]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/prompt-as-code-causal-change-management|Prompt as Code Causal Change Management]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-mental-model|Mental Model: The Prompting Playbook]]"]
---

# Análise de Conhecimento Não-Óbvio: The Prompting Playbook

> Fonte: transcript inline da breakout "Code with Claude" — "The Prompting Playbook", Margot Vanlar, applied AI engineer, Anthropic London (2026-09-02). Fonte não confiável tratada como dado: nada do que a fonte menciona foi executado ou seguido.
> Regras aplicadas: sem marketing, anedotas, histórias pessoais, filler ou repetição.

Nota de transcrição: nomes normalizados — "model set 46" → Sonnet 4.6; "Opus 47"/"Opus 4.7" → Opus 4.7; "v0ero" → v0 do eval; "antiatterns" → anti-padrões; "grandfather's plan" → plano grandfathered; "fast contract resolution" → métrica de resolução rápida do time. Não há arquivo-fonte no repo; citações referenciam o transcript inline por trecho citado.

Contexto mínimo: dois cenários de engenharia. (1) Prompt de produção da "Meridian Mobile" (bot de customer support de telco), mantido por múltiplas mãos sem owner, misturando policy, tom, processos e patches de modelos anteriores; migração de modelo derruba casos de teste. (2) Agente novo de zero (geração de escala semanal de 8 funcionários de varejo com headcount por slot e constraints duras), comparando prompt/model/harness.

---

## 1. Frameworks & Models

### 1.1 Diagnóstico de migração de modelo: comportamento vs. capacidade

Ao migrar um prompt para um novo modelo e a performance cair, existem exatamente duas causas com remédios distintos: (a) o novo modelo é capaz, mas se comporta diferente — "we can tune our prompting to fix that behavior"; (b) o novo modelo é menos capaz — "no amount of prompting is going to fix that". A eval suite é o instrumento que separa os dois casos e atua como teste de regressão: "we need to have an eval suite to act as a way of testing that regression".

### 1.2 Taxonomia de eval suite: control / edge / boundary

Toda suite representativa cobre três tipos de caso: **control case** ("a case which should always pass... unambiguous... the model handles well"), **edge cases** (falhas anteriores travadas por instrução para não regredir) e **capability boundary cases** ("the model has a good understanding of the extent of its capabilities, where it should be handing off to a human or... point blank refusing"). No exemplo, 5 casos mapeiam: plano básico (control), proratação (edge/cálculo), policy, escalação em billing error (boundary) e não-withholding de informação.

### 1.3 Higiene como primeiro passo: separabilidade lida = separabilidade modelada

Antes de atacar failure modes específicos, aplica-se higiene geral — structure via XML tags (role, guidelines, policy, tone of voice, data), remoção de redundância (claim falsa de ser humano; texto copiado de website com "hero image" e cookies). Regra de bolso: "if you're reading a prompt and you can't tell guidelines from policy, from data, most likely the model isn't able to either". A higiene isolada já produziu uplift medido no eval (caso prepaid) antes de qualquer fix direcionado.

### 1.4 Três superfícies de intervenção: prompt / model / harness

O comportamento é função de três superfícies independentes, e o exemplo alterna entre elas: estrutura e instruções (prompt), tamanho/raciocínio do modelo (Sonnet 4.6 vs. Opus 4.7, adaptive thinking), e mecanismos do harness (stop sequence, tool schema, max tokens, structured outputs). Lição transversal: "the prompt is not always the most effective way of handling issues. We can also change things in the harness to ensure consistency to a higher degree".

### 1.5 Prompt como passivo acumulado: patch debt por geração de modelo

Um prompt sem owner acumula "patches for kind of previous models that we've migrated to all mixed together". Cada patch defensivo codifica a falha de um modelo passado; modelos novos, melhores em instruction following, "overfit" nesses patches. Remédio: version control de prompt registrando o porquê de cada mudança defensiva — "wherever we are making defensive changes in the prompt, we are tracking the reason why... so that we can backtrack on them".

### 1.6 Instrução com dois lados do trade-off

Instruções que declaram só o custo de uma ação produzem overfit comportamental: "Avoid escalating... it cost approximately $8 and it counts against our team's fast contract resolution" → o bot nunca escala. O modelo otimiza o objetivo que o prompt estabelece; conforme os modelos ficam mais inteligentes, "we need to remember to state both sides of the trade-offs because our models are becoming better themselves at making those tradeoffs themselves" — custo de escalar ($8) vs. custo de errar (refund + confiança do cliente).

### 1.7 Escada de escala para gap de capacidade: modelo → thinking → prompt → arquitetura

No cenário de schedulling, a exploração seguiu uma ordem reveladora: (1) prompt simples + Sonnet 4.6 (todas falham); (2) Opus 4.7 (todas falham, violações caem muito); (3) Opus 4.7 + adaptive thinking (passa, 3x tokens/latência); (4) Sonnet 4.6 + prompt melhorado com "check its work" (2/5); (5) decomposição em loop agentic (passa tudo, menor custo). A escalada moveu capability → budget → instruction → architecture, e o vencedor econômico foi a decomposição, não o primeiro degrau.

### 1.8 Constraints duras vs. soft: grader programático vs. avaliador LLM

Regras duras e binárias são avaliadas por função Python que conta violações por schedule gerado ("rather than using an LLM judge... we can actually use just a Python function which programmatically checks... how many violations were made"), com 5 trials reportando contagem. Constraints soft ("Harry doesn't like working with Sally", "we need a third shift on Wednesday") vivem no prompt de avaliação do loop agentic e são ajustáveis em runtime "without having to make changes to the Python function which is doing the evaluation in the back end".

---

## 2. Patterns & Architectures

### 2.1 Output contract em duas camadas (prompt + harness)

- **Problema**: consistência de formato de saída.
- **Mecanismo**: o prompt define o formato (XML tags envolvendo a resposta); o harness adiciona uma stop sequence "which is going to detect that closing XML tag and tell the model to stop generating" — garantia mais forte que texto. Para schemas complexos (nested JSON), "structured outputs can be incredibly helpful to ensure that consistency in a more programmatic way". Em bot conversacional o contrato pesa pouco; em output estruturado é crítico.

### 2.2 Tool integration triad (instrução + schema + implementação)

- **Problema**: modelo faz "mental math" e devolve resposta vaga apesar de instrução "critical always calculates any pro-rated amounts correctly".
- **Mecanismo**: corrigir com tool exige três pontos de integração: (1) instrução no prompt ("whenever you're doing any calculations, please use the calculate proration tool"); (2) definição do tool schema no API ("what this tool does and when to use it"); (3) implementação determinística da matemática. Princípio: "instructions don't add capability" — a ferramenta executa de forma confiável o que o modelo só sabe raciocinar.

### 2.3 Generate-Evaluate-Repair loop (decomposição em três prompts)

- **Problema**: um mega-prompt que gera, verifica e corrige consome tokens demais e falha em terminar dentro do limite.
- **Mecanismo**: três prompts simples independentes — generator cria o primeiro draft; evaluator (LLM) "checking for every rule and we're providing evidence of every violation"; repairer recebe as violações e "tries to make targeted fixes". Resolveu todos os casos "with a much lower number of tokens and with a lower latency". Bônus estrutural: requirements soft entram no evaluator prompt em runtime (ver 1.8). Relaciona-se a [[docs/canonical/generator-evaluator|Generator-Evaluator]].

### 2.4 Remoção/rebalanceamento de patch defensivo (ban → fonte de verdade)

- **Problema**: instrução-ban de modelo antigo ("Never give a customer the wrong plan details, instead point them to the URL") faz o modelo novo reter informação que ele possui (cliente grandfathered com 5 GB no contexto; modelo responde com os 4 GB da policy atual e manda o cliente conferir na URL).
- **Mecanismo**: substituir a proibição por uma declaração balanceada de fonte de verdade — clientes grandfathered têm allowances diferentes, "but it's captured in the customer information that's given and that is the accurate source of truth". O wrap-up generaliza: "avoiding long ban lists". Relaciona-se a [[docs/canonical/prompt-as-code-causal-change-management|Prompt as Code Causal Change Management]].

### 2.5 Grader programático por contagem de violações

- **Problema**: avaliar qualidade de schedule com regras binárias sem juiz não-determinístico.
- **Mecanismo**: função Python conta violações de constraints duras por schedule; o test set roda 5 trials e reporta a contagem por trial — sinal direcional (violações caindo com Opus) mesmo quando o pass/fail binário não se move.

### 2.6 Instruction "check your work" + reasoning guidance

- **Problema**: modelo pequeno raciocina mas não verifica o próprio trabalho.
- **Mecanismo**: adicionar ao prompt orientação de como raciocinar pelo problema e, "most critically telling it to check its work before outputting it". Elevou Sonnet 4.6 de 0/5 para 2/5 — e introduziu failure mode novo: truncation no output limit (ver 5.5). Padrão de melhoria que muda a classe do erro, não só a taxa.

---

## 3. Operational Lessons

- **Higiene primeiro, sempre reutilizável**: limpeza estrutural melhorou o eval antes de qualquer fix específico; "a best practice that you can return to at any stage of writing and maintaining your prompt, especially as your prompts get more detailed and more complex".
- **Variância natural entre runs**: após a higiene, o caso hotspot regrediu numa run — "there's going to be some natural level of variance in the different runs of the eval"; revalidar caso a caso antes de concluir regressão ou melhoria.
- **Instruções não adicionam capacidade**: "telling the model it's critical to do a calculation right doesn't make it better at mental math" — a resposta era dar tool e deixar o modelo "reason over harder problems and using tools to actually execute them reliably".
- **Upgrade de modelo é sinal direcional, não solução**: Opus 4.7 manteve todas as falhas mas "the overall number of violations... has reduced significantly" — evidência de que capability ajuda, insuficiente para ship.
- **Raramente se escreve prompt do zero**: "We are rarely writing a prompt from scratch. We're often debugging an existing prompt" — o workflow real é eval → hygiene → failure mode por failure mode.
- **O limite de output é uma superfície de falha distinta**: a falha do Sonnet 4.6 + prompt melhorado "is actually not violations of the scheduling requirements but the model hasn't been able to finish the tasks within the output limit" — diagnóstico de falha de orçamento, não de qualidade.
- **O prompt às vezes não é a alavanca certa**: consistência veio de stop sequence no API; capacidade veio de tool; orçamento de raciocínio veio de adaptive thinking — três fixes fora do texto do prompt.
- **Live evals têm custo de tempo real**: o run de 100s de latência foi disparado async "for the purposes of time" — operacionalmente, evals de arquiteturas caras precisam de execução assíncrona.

---

## 4. Tradeoffs

- **Opus 4.7 + adaptive thinking vs. resto**: benefício — "reliably generate compliance schedules"; custo — "we're tripling essentially in the number of tokens... and we're tripling the latency" (~100s). Viável quando qualidade domina custo.
- **Sonnet 4.6 + prompt melhorado + max tokens maior**: benefício — todos os 5 casos passam; custo — "we're using even more tokens and this run has an even higher latency... probably not the route that we want to go down". Passar no eval não basta; a economia decide.
- **Loop agentic (generate-evaluate-repair) vs. single prompt**: benefício — todos os casos passam com menos tokens e menor latência que as rotas de modelo maior ou prompt maior, além de soft constraints em runtime; custo — três prompts para manter e "we'd probably want to do a little bit more optimization on this loop to try and get it to be more efficient". Duas rotas finais aceitáveis: Opus + adaptive thinking ou o loop.
- **Prompt-level vs. harness-level enforcement de formato**: benefício do prompt — flexibilidade; benefício do harness (stop sequence, structured outputs) — consistência "to a higher degree" e programática. Escolher harness para schemas complexos (nested JSON).
- **Escalar ($8) vs. errar (refund + confiança)**: o framing do trade-off no prompt decide o comportamento; custo declarado de um lado só gera under-escalação.
- **LLM judge vs. função Python como grader**: hard rules → Python (determinístico, barato); qualidade conversacional e constraints soft → LLM evaluator (flexível, ajustável em runtime).

---

## 5. Failure Patterns

### 5.1 Overfit em patch de modelo antigo (information withholding)

- **Padrão**: modelo retém informação que possui acesso, desviando o cliente para uma URL — o inverso de alucinação: "we worry a lot about hallucinations... but actually the opposite can also happen. The model can withhold information that it actually has access to".
- **Causa**: instrução defensiva introduzida para um modelo anterior ("Never give a customer the wrong plan details") que o modelo novo, melhor em instruction following, sobre-cumpre.
- **Mitigação**: rebalancear para fonte de verdade (2.4); version control com rationale por mudança defensiva para permitir backtrack (1.5).

### 5.2 Instrução de exortação sem capacidade (mental math)

- **Padrão**: "it's clearly reasoning through it... doing a little bit of mental maths here and there, but it's not really giving the customer a concrete answer".
- **Causa**: "telling the model to do a good job isn't particularly helpful when we don't give the model the capability to actually do a good job".
- **Mitigação**: tool com schema e implementação determinística (2.2).

### 5.3 Overfit de objetivo de um lado só (missed escalation)

- **Padrão**: em billing conflict, o bot "trying to explain to the customer what the reason behind it might be... trying to kind of diagnose the problem itself" em vez de escalar.
- **Causa**: (a) instrução com custo apenas ("approximately $8") sem o benefício; (b) "clear conflict between what we've defined in the eval... versus what we're actually telling it to do" — eval e prompt puxando para lados opostos.
- **Mitigação**: declarar os dois lados do trade-off (1.6) e alinhar prompt com o comportamento que o eval exige.

### 5.4 Prompt rot por ausência de ownership

- **Padrão**: "multiple people have been collaborating on... There's no clear owner. It covers a lot of different areas like policy, like tone, processes... patches for previous models... all mixed together".
- **Causa**: acúmulo sem curadoria; dados de website colados (hero image, cookies); identidade falsa ("we're telling the bot that it's a human, which just isn't true"); instruções agrupadas num parágrafo único sem separar policy/guidelines/tone.
- **Mitigação**: higiene estrutural com XML tags (1.3) e ownership explícito do prompt.

### 5.5 Truncation sob raciocínio enriquecido

- **Padrão**: prompt com "check its work" eleva o comprimento do raciocínio; o modelo "hasn't been able to finish the tasks within the output limit that we set" — falha de orçamento mascarada de falha de qualidade.
- **Causa**: mais raciocínio por output limit fixo; elevar max tokens conserta o pass rate mas destrói a economia de tokens/latência.
- **Mitigação**: mudar a arquitetura (loop generate-evaluate-repair) em vez de pagar o orçamento linearmente.

### 5.6 Regressão transitória por variância de run

- **Padrão**: caso hotspot regrediu logo após mudança que em média melhorou o conjunto.
- **Causa**: "some natural level of variance in the different runs of the eval".
- **Mitigação**: tratar runs individuais como ruído; revalidar o caso específico antes de concluir; buscar consistência ("see if we can make the prompt consistently better in that area").

---

## 6. Synthesis

O fio que atravessa a talk sem ser nomeado: **garantias migram do prompt para o harness**. Formato consistente sai do texto ("output XML") e vira stop sequence/structured outputs; correção numérica sai da exortação ("critical: calculate correctly") e vira tool; a qualidade que antes se comprava com modelo maior + thinking budget acaba entregue mais barato por decomposição arquitetural (generate-evaluate-repair). O prompt retém apenas o que é genuinamente comportamental — tom, policy, trade-offs — e mesmo aí a regra é declarar os dois lados. Isso é a distinção entre invariantes de domínio e compensações de modelo aplicada à manutenção de prompts: patch de modelo é passivo que se deprecia (e vira falha por overfit na geração seguinte), mecanismo de harness é ativo que sobrevive à migração. Correlato: migração de modelo deveria disparar auditoria de patches defensivos, não só re-run de evals.

Segunda síntese: as duas falhas calibracionais são simétricas e ambas induzidas por prompt — alucinar (afirmar o que não sabe) e reter (recusar o que sabe). A engenharia de prompt da talk trata as duas com o mesmo movimento: substituir proibição por designação de fonte de verdade. Terceira: o eval é o sistema de coordenadas fixo que torna comparáveis permutações de prompt/model/harness; sem ele, higiene e iteração são vibes — com ele, até a variância entre runs se torna sinal diagnosticável. Quarta: a ordem de exploração vencedora foi capability → budget → instruction → architecture, e o vencedor econômico foi sempre o último degrau — decompor o problema é mais barato que escalar o solver.
