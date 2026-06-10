---
aliases: ["rubricas multi", "arquitetura rubricas", "multidimensional rubrics"]
---

# Rubricas Multidimensionais: O Que a Arquitetura do Seu Sistema Precisa Garantir para um Evaluator Funcionar

**Avaliar output de agente com um único critério é como julgar um piloto só pela velocidade. Quando o sistema lida com dinheiro, saúde e confiança, cada dimensão de qualidade exige uma fonte de verdade diferente — e a arquitetura precisa entregar cada uma delas.**

---

## 1. O Dia em Que o Evaluator Aprovou o Que Não Devia

Era uma terça-feira de abril. Ana, cliente do KODA — um agente de vendas que opera via WhatsApp — entrou com um pedido simples: precisava de whey protein. Ela também deu três informações críticas: tinha alergia severa a lactose, orçamento máximo de R$ 80 e preferia chocolate.

O Generator do KODA processou a conversa e produziu três recomendações. Ana escolheu a primeira: Whey Isolado Sem Lactose, R$ 79,90. O Generator registrou a alergia, respeitou o orçamento, e o pedido seguiu para o Evaluator.

O Evaluator fez o que estava programado para fazer: verificou se os campos estavam preenchidos, se o produto existia no catálogo e se o preço era válido. Tudo passou. O pedido foi aprovado.

Três dias depois, Ana abriu a embalagem e leu o rótulo: "Este produto é preparado em instalação que processa leite. Risco de contaminação cruzada: moderado." Ela tinha alergia severa — já tinha ido parar no pronto-socorro duas vezes. Escreveu furiosa exigindo reembolso e deixou uma avaliação pública de uma estrela.

O que deu errado? O Evaluator não era incompetente. Ele simplesmente não tinha instruções para verificar a dimensão que importava: segurança alérgica. Ele avaliou o pedido em uma dimensão só — "os dados básicos estão corretos?" — e aprovou o que deveria ter sido bloqueado.

Esse caso, extraído do módulo de Rubric Design do currículo long-running-agents (`curriculum/02-nivel-2-practical-patterns/03-rubric-design.md`), ilustra o problema central que este artigo ataca: **um Evaluator que avalia em uma dimensão só é um risco arquitetural, não uma limitação de modelo.** A pergunta que arquitetos e líderes técnicos precisam fazer não é "nosso Evaluator é bom?", mas "nosso sistema entrega ao Evaluator as fontes de verdade que cada dimensão exige?"

---

## 2. Por Que Uma Dimensão Só Não Basta

O currículo do long-running-agents estabelece uma distinção fundamental que escapa a muitos sistemas em produção: validação e avaliação não são a mesma coisa.

Validação pergunta: "o output viola uma regra mínima?" Avaliação pergunta: "quão bom é o output para o objetivo real?" (`curriculum/05-core-concepts/08-evaluation-rubrics.md:119-143`).

Um checklist de validação — produto existe, preço é positivo, campos estão preenchidos — responde a primeira pergunta e é necessário. Mas ele é cego para a segunda. O caso de Ana passou na validação e falhou na avaliação. O produto existia, o preço estava correto, os campos estavam preenchidos. Nenhuma regra mínima foi violada. Ainda assim, o output era perigoso.

É aqui que entra o conceito de rubrica multidimensional. Uma rubrica de avaliação é um conjunto estruturado de critérios que mede qualidade em vários eixos simultaneamente. Em vez de perguntar "está correto?", pergunta "quão correto, quão seguro, quão completo, quão claro e quão adequado ao contexto?" (`curriculum/05-core-concepts/08-evaluation-rubrics.md:73-77`).

Cada eixo é uma dimensão independente. Cada dimensão responde a uma pergunta diferente. E — este é o ponto arquitetural crítico — **cada dimensão exige uma fonte de verdade diferente**. O sistema precisa garantir que o Evaluator tenha acesso a cada uma dessas fontes no momento da avaliação.

Os componentes de uma rubrica multidimensional são sete (`curriculum/05-core-concepts/08-evaluation-rubrics.md:85-91`):

- **Dimensions**: os aspectos avaliados (correctness, safety, completeness, clarity, traceability, consistency).
- **Weights**: o peso relativo de cada dimensão no score final.
- **Scoring levels**: a escala usada para pontuar (tipicamente 1-5 ou 0-100).
- **Thresholds**: limites que transformam score em decisão (approve, revise, reject).
- **Anchors**: descrições concretas do que significa cada nível de score.
- **Evidence rules**: fatos que o Evaluator precisa citar para justificar a nota.
- **Decision policy**: a ação tomada a partir do score e dos gates.

O diagrama conceitual do fluxo é claro: o output do agente entra na rubrica, é decomposto em dimensões independentes, cada dimensão recebe um score, scores são ponderados, e o resultado é comparado contra thresholds para produzir uma decisão (`curriculum/05-core-concepts/08-evaluation-rubrics.md:95-115`).

Mas entre o diagrama e a produção, existe uma lacuna que a maioria das implementações não fecha: **como o sistema garante que o Evaluator consegue, de fato, medir cada dimensão?**

---

## 3. As Dimensões Que Importam e o Que Cada Uma Exige da Arquitetura

O template operacional de rubrica do long-running-agents (`curriculum/08-tools-templates/evaluation-rubric-template.md:424-479`) define oito dimensões de qualidade. Para cada uma, o template especifica quais sinais o Evaluator deve procurar. Mas a pergunta de arquitetura é anterior: **o sistema entrega esses sinais ao Evaluator?**

### Correctness: o output está factualmente correto?

Sinais esperados: preço, estoque, restrição alimentar, regra de promoção, status do pedido. O critério de qualidade é objetivo: "o Evaluator consegue apontar uma evidência no input ou no trace para justificar o score" (`evaluation-rubric-template.md:425-429`).

**O que a arquitetura precisa garantir:** O Evaluator precisa receber, junto com o draft do Generator, as fontes de verdade contra as quais vai conferir — o price snapshot, o inventory snapshot, o catálogo de produtos, as regras de promoção vigentes. Se esses dados chegam desatualizados ou incompletos, o score de correctness é uma ficção. Isso implica versionamento das fontes de verdade e acoplamento temporal entre o snapshot usado pelo Generator e o recebido pelo Evaluator.

### Safety: o output evita dano?

Sinais esperados: alergias, contraindicações, cobrança indevida, privacidade, compliance. Safety é gate criterion — se falhar, bloqueia o output independentemente do score nas outras dimensões (`evaluation-rubric-template.md:439-443`).

**O que a arquitetura precisa garantir:** O perfil de risco do cliente precisa estar disponível como dado estruturado, não diluído na conversa. Se a alergia de Ana está apenas na transcrição da conversa e a conversa já tem 40 minutos, a informação pode ter saído da janela de contexto. O sistema precisa promover restrições críticas do plano da conversa para o plano do estado persistente — um princípio que conecta diretamente com o padrão canônico de State Persistence e com o de Head-Tail Context Truncation (`docs/canonical/serializable-pause-resume-state.md`, `docs/canonical/head-tail-context-truncation.md`).

### Completeness: o output cobre tudo que a tarefa exige?

Sinais esperados: produto, motivo da recomendação, próximos passos, campos obrigatórios, limitações (`evaluation-rubric-template.md:431-436`).

**O que a arquitetura precisa garantir:** O contrato do que "completo" significa para aquela tarefa precisa existir como artefato estruturado — tipicamente um Sprint Contract (`curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md`). O Evaluator compara o output contra os promised deliverables do contrato. Se o contrato é implícito ou verbal, completeness é impossível de medir.

### Traceability: a decisão pode ser auditada depois?

Sinais esperados: referências a dados usados, reasons, checks, source ids (`evaluation-rubric-template.md:459-463`).

**O que a arquitetura precisa garantir:** O Evaluator precisa ter acesso ao trace do Generator — quais dados foram consultados, quais regras foram aplicadas, qual raciocínio foi seguido. Sem esse trilho, o Evaluator pode aprovar um output que "parece correto" sem conseguir verificar se as fontes citadas realmente existem. Isso exige que Generator e Evaluator compartilhem um protocolo de trace, não apenas um protocolo de input/output.

### Consistency: o output não contradiz estado anterior?

Sinais esperados: preferências, orçamento, endereço, canal, histórico de reclamações (`evaluation-rubric-template.md:466-471`).

**O que a arquitetura precisa garantir:** O estado do cliente precisa ser persistido, versionado e carregado no contexto do Evaluator. Se o cliente disse na semana passada que prefere entrega em São Paulo e hoje o output sugere retirada em loja, o Evaluator precisa detectar a inconsistência. Isso exige que o sistema mantenha state files versionados e os ofereça como input ao Evaluator — mesmo que a conversa atual não mencione explicitamente esses dados.

### Recoverability: o output orienta recuperação quando algo falha?

Sinais esperados: pedido de dado faltante, fallback seguro, escalonamento humano (`evaluation-rubric-template.md:473-478`).

**O que a arquitetura precisa garantir:** O harness precisa definir o que é recoverable e o que é blocking. Se o Generator produziu um output com dado faltante, o Evaluator deve conseguir sinalizar "peça o campo X e reenvie" em vez de simplesmente rejeitar. Isso transforma o Evaluator de um juiz binário em um componente que participa do fluxo de recuperação — e exige que o feedback do Evaluator seja estruturado (campo faltante, motivo, ação esperada), não textual.

O padrão que emerge é claro: **cada dimensão da rubrica é uma exigência de contrato de dados entre o sistema e o Evaluator.** Se o contrato não é cumprido, o score daquela dimensão é ruído. E scores ruidosos produzem decisões piores do que intuição humana — porque vestem o erro com aparência de rigor.

Há uma consequência adicional que merece destaque: a escolha das dimensões não é neutra em relação à arquitetura de coordenação. O KODA documenta quatro estratégias de coordenação entre Generator, Evaluator e decisão — file-based, in-memory, API-based e queue-based — e cada uma favorece um perfil diferente de avaliação (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:134-148`). Se o sistema usa coordenação in-memory, o Evaluator só tem acesso ao que está naquela chamada; dimensões que exigem estado persistido (consistency, traceability) ficam comprometidas. Se o sistema usa file-based, cada avaliação deixa rastro no sistema de arquivos — o que habilita auditabilidade, mas exige locking e versionamento para evitar race conditions. A escolha da estratégia de coordenação é, na prática, uma pré-condição para quais dimensões a rubrica pode medir com confiabilidade.

---

## 4. Gates: Quando Uma Dimensão Bloqueia Tudo

Nem todas as dimensões têm o mesmo peso. Algumas são condição necessária; outras são condição desejável. A arquitetura da rubrica precisa distinguir esses dois tipos explicitamente.

O template do long-running-agents define dois mecanismos de decisão que operam em paralelo (`evaluation-rubric-template.md:348-356`):

**Gate criteria**: falhas que bloqueiam aprovação mesmo que o score total ponderado seja alto. Exemplos: alergia ignorada, preço incorreto, JSON inválido, promessa médica indevida. Um gate violado produz rejeição imediata, sem análise das outras dimensões.

**Weighted composite**: o score final é a soma ponderada dos scores de cada dimensão. Correctness pode valer 40%, Safety 30%, Completeness 15%, Clarity 10%, Traceability 5%. Os pesos refletem o risco real de cada dimensão para o negócio.

A lógica de decisão combina os dois: primeiro verificam-se os gates; se todos passarem, aplica-se o weighted composite contra thresholds (`evaluation-rubric-template.md:482-504`):

- **Aprovação estrita** (pagamento, alergia, dados pessoais): todos os gates limpos e score >= 90%.
- **Aprovação com revisão leve** (recomendações): gates limpos, score >= 80%, revisão entre 70-79%.
- **Retry automático**: critério não-crítico falhou, feedback estruturado ao Generator, uma tentativa.
- **Human review**: safety ou correctness falhou, sem retry cego.
- **Bloqueio de release**: mudança de prompt ou rubrica que reduz inter-rater reliability ou aumenta falsos positivos.

Para o arquiteto de sistemas, a implicação é dupla. Primeiro, **os gates precisam ser implementados como pré-condições que abortam a avaliação antes de consumir recursos nas outras dimensões.** Não faz sentido avaliar clareza de um output que recomenda um produto com alérgeno para um cliente alérgico. Segundo, **os thresholds não são constantes universais — são parâmetros de risco calibrados por domínio.** Um threshold de 90% para aprovação de pagamento é razoável; o mesmo threshold para uma saudação inicial seria overengineering.

No KODA, a arquitetura de avaliação operacionaliza isso com quatro níveis de decisão (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:119-125`):

- `APROVAR`: score alto, nenhum blocker, confidence suficiente.
- `APROVAR_COM_RESSALVAS`: pequenas imperfeições sem risco de negócio.
- `REJEITAR`: falha corrigível, feedback ao Generator, nova iteração.
- `REJEITAR_IMEDIATAMENTE`: risco médico, preço falso, violação de política — bloqueia envio e escala.

A diferença entre `REJEITAR` e `REJEITAR_IMEDIATAMENTE` é arquiteturalmente significativa: o primeiro mantém o agente no loop de geração; o segundo tira o agente do circuito e escala para um humano ou fluxo determinístico. O sistema precisa suportar ambos os caminhos.

---

## 5. Calibração Como Propriedade do Sistema, Não do Time

Uma rubrica não calibrada é pior do que intuição — porque produz scores com aparência de objetividade sem a substância. O template do long-running-agents dedica um guia completo de calibração (`evaluation-rubric-template.md:789-869`) que revela exigências arquiteturais frequentemente negligenciadas.

O processo tem dez passos, mas três deles têm implicações diretas de arquitetura:

**Inter-rater reliability**: dois humanos e um Evaluator aplicam a mesma rubrica aos mesmos exemplos, sem comunicação prévia. Critérios com divergência maior que 1 ponto (em escala de 5) estão ambíguos. O sistema precisa suportar avaliação paralela e independente com comparação automatizada de scores — algo que um harness baseado em arquivo ou API torna trivial, mas um harness puramente in-memory dificulta.

**Regression set com fixtures de produção**: a rubrica precisa ser testada contra outputs reais que já causaram incidentes. O template especifica que o regression set deve incluir "N+1 long-session fixtures: conversas 10+ turnos com compactação, 11o turno testa continuidade contextual" e "casos do Production Failure Regression Flywheel: reclamação de usuário, tool misuse, state persistence failure, scoring gap e escaped edge case" (`evaluation-rubric-template.md:821-823`). Isso exige que o sistema mantenha um repositório de fixtures versionadas, com estado inicial, output do Generator, e expected label (approve/reject).

**Correlação eval-produção**: a calibração não termina no laboratório. O score da rubrica precisa ser comparado com outcomes reais — devoluções, reclamações, recompra — para verificar se a rubrica está medindo o que importa. Isso exige um pipeline de métricas que conecte scores de avaliação com outcomes de negócio, algo que o padrão canônico Eval-to-Production Correlation Tracking (`docs/canonical/eval-to-production-correlation-tracking.md`) formaliza.

O modelo mental do repositório (`docs/analysis/2026-06-10-eval-maturity-phases/mental-model.md`) posiciona a calibração como propriedade de maturidade do sistema: sistemas imaturos calibram por opinião; sistemas maduros calibram por correlação com produção. A arquitetura determina em qual desses regimes o time opera.

A progressão de maturidade de evaluation (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md`) define cinco fases. A fase 1 é teste ad hoc — sem rubrica, sem reproducibilidade. A fase 2 introduz uma suíte de referência, mas a calibração ainda é manual. A fase 3 é onde a arquitetura começa a importar: PR-gated eval enforcement, que exige que toda mudança de prompt, modelo ou ferramenta seja acompanhada de evidência de que a rubrica continua funcionando. A fase 4 adiciona production-grounded sampling — os casos de teste não são mais inventados, são extraídos de interações reais de produção. A fase 5 fecha o ciclo com regression flywheel: incidentes de produção geram automaticamente novos casos de teste, e a correlação entre score de eval e outcome de produção é monitorada continuamente.

Cada transição de fase é um gate arquitetural. Você não passa da fase 3 para a fase 4 sem um pipeline que coleta, anonimiza e versiona interações de produção. Você não passa da fase 4 para a fase 5 sem um sistema que detecta incidentes, extrai o estado no momento da falha, e gera um caso de regressão que capture o comportamento esperado. Esses não são problemas de processo — são problemas de infraestrutura.

---

## 6. O Que Isso Implica para Quem Projeta Sistemas

O artigo começou com uma história de falha e termina com exigências de design. Para um arquiteto ou líder técnico que está projetando — ou evoluindo — um sistema de agentes com avaliação de qualidade, as implicações são seis:

**1. Separe Generator de Evaluator no nível de arquitetura, não de código.** O padrão Generator/Evaluator (`curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`) não é uma convenção de estilo — é uma separação de responsabilidades com consequências de infraestrutura. Generator e Evaluator devem poder evoluir independentemente, usar fontes de verdade potencialmente diferentes, e falhar sem contaminar um ao outro. No KODA, a arquitetura de avaliação (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:85-115`) mostra isso como um pipeline: contexto entra, Generator produz draft, Evaluator aplica rubrica, Decision Engine decide, e só então o output chega ao cliente.

**2. Cada dimensão da rubrica é um contrato de dados. Cumpra-o ou reduza a rubrica.** Se o sistema não consegue entregar ao Evaluator um price snapshot atualizado, a dimensão "correctness de preço" não pode ser medida — e incluí-la na rubrica produz scores falsos. Dimensões que o sistema não consegue sustentar com fontes de verdade devem ser removidas da rubrica ou movidas para um tier de avaliação separado (humano, assíncrono, amostral).

**3. Gates são pré-condições, não pós-condições.** Um gate violado deve abortar a avaliação antes de consumir recursos nas outras dimensões. Isso significa que o Decision Engine precisa suportar short-circuit evaluation: verificar gates primeiro, aplicar weighted composite depois. A arquitetura de coordenação (file-based, API-based, queue-based) precisa refletir essa ordem.

**4. O trace do Generator é input do Evaluator.** O Evaluator precisa saber quais dados o Generator consultou para produzir o output — não para confiar neles, mas para verificá-los. Sem trace auditável, o Evaluator está avaliando uma caixa-preta, e o score de correctness é uma aposta. O padrão canônico Deterministic Tool Dispatch (`docs/canonical/deterministic-tool-dispatch.md`) oferece um caminho: ferramentas produzem JSON determinístico, e esse JSON é o que o Evaluator confere.

**5. Calibração é infraestrutura, não processo manual.** Um sistema que exige que humanos comparem scores manualmente para calibrar rubrics não escala. A arquitetura precisa prover: fixtures versionadas, execução paralela de avaliações, comparação automatizada de scores, e correlação com outcomes de produção. Sem isso, a rubrica degrada com o tempo — porque os dados de produção mudam, os modelos mudam, e os thresholds calibrados há três meses viram ruído.

**6. A rubrica também precisa ser avaliada.** O template inclui uma seção de bias detection e uma checklist de qualidade para a própria rubrica (`evaluation-rubric-template.md:873-925`). Uma rubrica pode favorecer mensagens mais longas (viés de comprimento), tom mais formal (viés de registro), ou produtos de maior margem (viés de negócio). O sistema precisa expor essas métricas — distribuição de scores por dimensão, correlação com atributos do output, taxa de falsos positivos — para que o time possa detectar quando a régua está torta.

Para o arquiteto que está no momento de decisão — "por onde começo?" — o repositório oferece um guia implícito de progressão. A tabela abaixo sintetiza as decisões arquiteturais na ordem em que elas se tornam bloqueantes:

| Estágio | Decisão arquitetural | O que desbloqueia |
|---|---|---|
| **Inicial** | Separar Generator de Evaluator como componentes independentes | Permite que o Evaluator receba fontes de verdade diferentes das do Generator |
| **Básico** | Implementar coordenação file-based com locking e versionamento | Habilita trace auditável e avaliação assíncrona em conversas longas |
| **Intermediário** | Promover restrições críticas do plano da conversa para estado persistido | Safety e consistency deixam de depender da janela de contexto |
| **Avançado** | Criar pipeline de fixtures versionadas com N+1 long-session cases | Calibração deixa de ser manual e passa a ser reproduzível |
| **Maduro** | Fechar o ciclo eval-produção: incidentes geram casos de regressão automaticamente | A rubrica evolui com o sistema, não contra ele |

Cada estágio é um investimento arquitetural com retorno em confiabilidade. A armadilha é tentar pular estágios: implementar regression flywheel sem antes ter coordenação file-based é construir sobre areia. O repositório é explícito sobre isso: a maturidade de avaliação é progressiva, e cada fase depende da infraestrutura da fase anterior (`docs/analysis/2026-06-10-eval-maturity-phases/analysis.md:45-79`).

---

## Fechamento

Rubricas multidimensionais não são uma técnica de prompt engineering. São uma decisão de arquitetura. Cada dimensão que você adiciona a uma rubrica é uma exigência que você está fazendo ao seu sistema: "entregue este dado, neste formato, neste momento, para que o Evaluator possa medi-lo."

A pergunta que separa sistemas que funcionam em produção de sistemas que funcionam em demo não é "quantas dimensões nossa rubrica tem?" — é "para cada dimensão, qual fonte de verdade o sistema entrega, e o que acontece quando essa fonte falha?"

O repositório long-running-agents documenta a resposta em três camadas: os padrões canônicos que definem os contratos de arquitetura (`docs/canonical/`), o currículo que ensina a operacionalizá-los (`curriculum/`), e as análises que mostram o que acontece quando esses contratos não são cumpridos (`docs/analysis/`). O artigo que você leu é uma síntese dessas três camadas, focada na pergunta que arquitetos precisam responder antes de escrever a primeira linha de código do Evaluator.

---

*Este artigo foi produzido a partir do conteúdo do repositório [long-running-agents](https://github.com/futanbear/long-running-agents), um programa curricular e base de conhecimento para construção de sistemas de IA que operam de forma confiável por horas, dias ou pelo tempo que a tarefa exigir.*
