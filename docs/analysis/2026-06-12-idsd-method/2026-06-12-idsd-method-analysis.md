---
title: "Analise de Conhecimento Nao-Obvio: IDSD — Intent-Driven Software Development"
type: analysis
date: 2026-06-12
aliases: ["idsd analysis", "intent driven software development", "ICE framework", "IDSD method analysis", "Symphony trap", "agile specification driven development"]
tags: ["agentes-orquestracao", "governanca", "spec-driven-development", "agentic-coding", "harness-engineering", "decision-discipline", "context-engineering"]
last_updated: 2026-06-12
relates-to: ["[[docs/canonical/owner-of-no-role-design|Owner of No Role Design]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|SDD Trap Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|Mental Model IDSD Method]]"]
sources: ["https://medium.com/activated-thinker/the-method-that-replaces-spec-driven-development-idsd-66e921f6cdf7"]
---

# Analise de Conhecimento Nao-Obvio: IDSD — Intent-Driven Software Development

> Fonte: Kapil Viren Ahuja, "The Method That Replaces Spec-Driven Development — IDSD" (Medium/Activated Thinker, 2026-05-20)
> Extraido: 2026-06-12
> Regras: sem marketing, self-promotion, anedotas, historias pessoais, filler ou repeticao

---

## 1. Frameworks & Models

### 1.1 ICE Framework — Separacao de Crafts na Geracao Agentica

Decomposicao em tres partes que substitui a spec monolítica. Cada parte tem um dono diferente e um proposito distinto:

- **Intent (Intent)** — o primitivo de primeira classe. Cinco componentes obrigatorios: (1) descricao do que se quer, (2) constraints ao redor, (3) cenarios de falha, (4) cenarios de sucesso, (5) conexoes com outros intents que seriam afetados por uma mudanca aqui. Faltar qualquer um dos cinco devolve o controle ao agente para preencher a lacuna.
- **Expectations (Expectativas)** — o que o SDD chamava de spec, mas deliberadamente nao e uma spec. E a fronteira: cenarios de done, cenarios de failed, e limites que o resultado deve respeitar. Escrito em linguagem do usuario, nao em linguagem de implementacao.
- **Context (Contexto)** — o como: tecnologia, sistema existente, constraints do codebase. Deve vir do harness e ser alimentado progressivamente, nao despejado como uma parede no inicio.

A separacao de donos e o ponto arquitetonico central: o humano possui Intent e Expectations e nunca as abandona; o harness possui Context e o Loop e nunca e convidado a inventar o que o humano queria.

### 1.2 IDSD — Intent-Driven Software Development

IDSD inverte SDD ao recusar que um unico documento, escrito de um jeito por quem estiver com o teclado, sirva como intent, definicao de done, workflow e contexto simultaneamente — com os gaps entre eles delegados a discrecao do agente. Em IDSD, declarar outcomes e deixar a maquina determinar implementacao e o modo normal de trabalho, nao a aspiracao.

A sequencia conceitual: Intent + Expectations (humano) → alimentam o loop agentico (harness) → harness puxa Context, codifica, valida contra Expectations → se nao atende, itera → se atende, merge.

### 1.3 O Modelo de Colapso do SDD — Single-Document Failure

O argumento de falha: SDD colapsa porque pede que um documento carregue quatro responsabilidades distintas, e os gaps entre elas sao deixados para o agente preencher. Dois gaps humanos (nao de ferramenta):

1. Engenheiros nao dedicam tempo para aprender o que uma spec realmente e nesse contexto. Assume-se que sabemos porque escrevemos specs por 20 anos — mas nao escrevemos esse tipo.
2. Os metodos que viralizaram (spec-kit, Kiro, Tessl, BMAD, Agent OS) foram construidos para demos greenfield de 40 minutos no YouTube, nao para codebases enterprise com doze times, uma decada de decisoes e compliance reviewers.

### 1.4 Symphony Trap — A Spec Perfeita que Veio Depois, Nao Antes

OpenAI publicou Symphony em abril de 2026: um arquivo unico de spec com 2,169 linhas, dezoito secoes, linguagem formal must-and-should. Se alguem conseguisse escrever tudo isso upfront num SPEC.md, funcionaria. E a verdade literal.

A armadilha: a OpenAI passou ~6 meses construindo uma ferramenta interna sob uma regra — zero codigo humano, cada linha gerada pelo Codex. So DEPOIS que funcionou eles destilaram a spec do sistema rodando. Entao fizeram o Codex construir a implementacao de referencia em Elixir em um shot, e separadamente implementar a mesma spec em cinco linguagens (TypeScript, Go, Rust, Java, Python) para sacudir ambiguidades. A spec profunda, grau RFC, e documentacao retrospectiva de software que ja rodava.

A industria esta vendendo o output como se fosse o metodo. Nao se pode escrever a spec upfront. A unica organizacao que produziu uma spec tao boa a produziu por ultimo, fazendo engenharia reversa de software que ja estava vivo.

### 1.5 Drift e Ausencia — O Reframe

O autor chama de "drift" o fenomeno de o agente se desviar mesmo com uma spec boa. Depois corrige: nao e drift. Drift e a palavra que se alcanca quando nao se quer dizer que saiu. O agente preencheu partes que o humano nao tinha pensado porque o humano saiu do loop. Uma spec boa nao se sustenta sozinha; ela se sustenta porque alguem permanece no loop enquanto ela roda.

### 1.6 Distincao Harness vs. Method

spec-kit, BMAD, Kiro, Tessl, Agent OS sao harnesses — uteis, mas apenas harnesses. ICE e o metodo que decide o que e o trabalho antes que o harness o manipule. Adotar o harness sem o metodo (o default hoje, porque o harness e a parte com botao de download) produz a mesma falha que o autor pagou com tres dias de retrabalho, so que em escala e com nome de cliente.

---

## 2. Patterns & Architectures

### 2.1 Intent como Primitivo de Cinco Partes

**Problema**: specs tradicionais nao capturam o que o agente precisa para decidir corretamente nos gaps.

**Mecanica**: cinco elementos que juntos fazem algo ser um intent. Exemplo concreto — "um usuario quer comprar um tenis vermelho por menos de $90":
- Descricao: um tenis vermelho que o comprador possa de fato comprar por menos de $90
- Constraints: tamanho do comprador, em estoque, entregavel para ele
- Cenarios de falha: retorna um tenis de $140, um tenis fora de estoque, ou um tenis nao-vermelho
- Cenario de sucesso: comprador adiciona um tenis vermelho acessivel ao carrinho e faz checkout
- Conexoes: qualquer coisa que toque preco, inventario ou checkout, porque uma mudanca la muda isso aqui

**Implicacao**: conexoes criam rastreabilidade de impacto — uma mudanca em um intent e rastreavel a tudo que toca.

### 2.2 Practical First Move — Uma Hora, Nao um Rollout Metodologico

**Problema**: times nao adotarao uma metodologia completa de imediato. Ira (lead consultant, 18 anos): "Isso esta dois degraus acima de onde os times realmente estao."

**Mecanica**: pegue um unico outcome real que voce vai shipar esta semana. Escreva as cinco partes so para ele. Entregue para alguem que nao estava na sua cabeca e pergunte onde o agente ainda teria que adivinhar. Cada lugar apontado e um buraco que voce estava prestes a deixar preencher. Feche esses, nao o sistema inteiro. Custa uma hora, nao um rollout metodologico.

### 2.3 Expectations como Craft Separavel

**Problema**: o momento em que a definicao de done se afasta da pessoa que queria o outcome, o agente comeca a decidir "done" por ela.

**Mecanica**: Expectations e um artefato separado, escrito pela mesma pessoa que escreveu o Intent, em linguagem do usuario. E a fronteira: cenarios de done, cenarios de failed, limites. Nao e uma spec — e o craft do que significa terminado.

### 2.4 Progressive Context Disclosure via Harness

**Problema**: contexto despejado como uma parede no inicio sobrecarrega o agente com informacao irrelevante e dilui o que realmente importa.

**Mecanica**: Context (o como — tech, sistema existente, constraints do codebase) deve vir do harness e ser alimentado progressivamente conforme necessario, nao como um unico dump upfront. O harness possui o Context e o entrega sob demanda.

### 2.5 Presence-in-the-Loop (nao Approval-at-the-Gate)

**Problema**: o humano aparece no final para abencoar um diff ja grande demais para realmente ler.

**Mecanica**: metrica central e presenca no loop, nao aprovacao no gate. O humano e parte do time enquanto o trabalho acontece. Nyra (membro do time): "O risco nao e que os times nao estejam prontos. O risco e o dia em que um agente escreve dez mil linhas que parecem certas, e ninguem possui a parte que explica o que 'certo' significa."

### 2.6 The ICE Loop

**Fluxo**: humano fornece Intent + Expectations → harness puxa Context → harness codifica → harness valida contra Expectations → se nao atende, itera → se atende, merge.

**Propriedade**: o humano possui Intent e Expectations e nunca as abandona; o harness possui o Loop e nunca e convidado a inventar o que o humano queria. Tudo o mais (modelo, prompting, orquestracao, harness usado para rodar o loop) e mecanica.

---

## 3. Operational Lessons

### 3.1 Voce Nao Consegue Escrever a Spec Upfront — a Prova do Symphony

O caso Symphony demonstra que mesmo a melhor spec agentica ja produzida foi gerada por ultimo, extraida de um sistema que ja funcionava. A industria vende o artefato como processo. Isso nao e um acidente — e uma inversao que beneficia quem vende harnesses, nao quem constroi software.

### 3.2 Uma Spec Boa Nao se Sustenta Sozinha

O autor tinha uma spec boa e ainda assim o agente derivou. O custo: tres dias de retrabalho, ~$985 em tokens (150-200M tokens/dia a precos Opus), dinheiro real gasto para criar o problema e depois pagar de novo para desfaze-lo. A spec ser boa e exatamente o ponto: uma spec boa nao segura sozinha; segura porque alguem fica no loop.

### 3.3 Estar Errado Enquanto se Sente Rapido — METR 2025

O estudo controlado do METR: desenvolvedores experientes foram mensuravelmente mais lentos com AI e sairam certos de que ela os tornou mais rapidos. Estar errado enquanto se sente rapido e a falha inteira em uma frase.

### 3.4 Paradoxo Economico dos Tokens

O preco por token continua caindo, mas o custo total por outcome terminado sobe. Nao porque tokens ficaram caros — porque um agente deixado para preencher gaps queima muito mais tokens por resultado. Um numero surpreendente desses tokens vai para estar confiantemente errado antes que alguem perceba. SDD quebrado infla o custo de construir software, e essa inflacao nao e absorvida pelo vendor ou pelo influencer — desce a linha ate o cliente.

### 3.5 O Flywheel Exige a Primeira Volta

O time do autor esta migrando de SDD para IDSD: intents e expectations escritos com disciplina real, contexto mantido exatamente no necessario, agentes fazem o trabalho. Principio: dogfooding — rode seu proprio metodo em si mesmo antes que ele chegue na conta de um cliente. O flywheel so compoe se girar, e so gira se alguem tomar a primeira volta.

### 3.6 Presenca no Loop como Metrica, Nao Aprovacao no Gate

A resposta genuina ao problema: estar envolvido em cada passo. Parte do time enquanto o trabalho acontece, nao o revisor que chega no fim para abencoar um diff grande demais para realmente ler.

### 3.7 O SDD nao e Novo — a Falha e Repetir sem Aprender

Larman e Basili documentaram no IEEE Computer (2003) que desenvolvimento iterativo remonta aos anos 1950. Ostroff, Makalsky e Paige na XP 2004 defenderam "Agile Specification-Driven Development" — uma spec "completa" e um ideal falho; a spec deve emergir como testes e contratos. A falha do vibe coding fez o SDD ir para o mainstream. O padrao se repete.

---

## 4. Tradeoffs

| Decisao | Beneficio | Custo |
|---|---|---|
| Spec monolítica (SDD) vs. crafts separados (ICE) | Um documento unico e simples de gerenciar | Gaps entre Intent, Done, Workflow e Context sao preenchidos pelo agente; colapso sob pressao |
| Escrever spec upfront vs. extrair spec do sistema rodando | Ilusao de controle antecipado | Spec tem buracos que o agente preenche; a unica spec boa ja produzida foi retrospectiva |
| Harness sem metodo (spec-kit, BMAD, etc.) vs. harness com metodo (ICE) | Adocao rapida (download button) | Mesma falha de tres dias de retrabalho, em escala e com nome de cliente |
| Contexto despejado upfront vs. contexto progressivo | Simplicidade de implementacao do harness | Diluicao do que importa; agente toma decisoes com base em ruido |
| Revisor-no-gate vs. presente-no-loop | Custo de atencao humana menor (so no final) | Diff grande demais para ler; agente decide "done" pelo humano |
| Rollout metodologico completo vs. one-hour practical start | Cobertura sistematica | Times nao estao prontos (dois degraus acima); o risco real e ninguem possuir "certo" |
| Escrever codigo manualmente vs. delegar a agentes com gaps | Agentic: rapido para author | Agentic com gaps: caro para rodar; tokens queimados em estar confiantemente errado |
| Focar no formato do documento vs. focar em quem possui cada craft | Formatos sao faceis de padronizar | O formato nunca foi o problema; o que mudou e o que cada arquivo e e quem o possui |

---

## 5. Failure Patterns

1. **Single-document collapse**: um documento deve servir como intent, definicao de done, workflow e contexto. Os gaps entre essas quatro funcoes sao preenchidos pelo agente. Causa: SDD nao separa crafts. Mitigacao: decompor em Intent (5 partes) + Expectations + Context, com donos distintos.

2. **Symphony trap — selling output as method**: a spec mais impressionante ja produzida foi gerada por ultimo, extraida de codigo que ja rodava. A industria vende o artefato como se fosse o processo. Causa: incentivo comercial de quem vende harnesses. Mitigacao: reconhecer que specs de qualidade emergem de sistemas vivos; nao tentar escreve-las upfront.

3. **Agent drift is actually human absence**: o agente derivou porque o humano saiu do loop, nao porque a spec era ruim. Usa-se a palavra "drift" para evitar admitir a ausencia. Causa: ilusao de que uma spec boa e suficiente sem presenca continua. Mitigacao: metrica de presenca no loop, nao aprovacao no gate.

4. **Harness without method at scale**: adotar spec-kit/BMAD (harness) sem ICE (metodo) reproduz a falha de tres dias de retrabalho, so que em escala enterprise com nome de cliente. Causa: harness tem botao de download; metodo nao tem. Mitigacao: metodo antes do harness — defina o que e o trabalho antes de entrega-lo ao harness.

5. **Being wrong while feeling fast** (METR 2025): desenvolvedores experientes foram mensuravelmente mais lentos com AI e sairam certos de que estavam mais rapidos. Causa: vies de percepcao — a velocidade de geracao mascara a baixa qualidade do resultado. Mitigacao: medir outcomes, nao velocidade percebida.

6. **Done definition drift**: a definicao de done se afasta da pessoa que queria o outcome, e o agente comeca a decidir "done" por ela. Causa: Expectations nao sao um craft separado com dono explicito. Mitigacao: Expectations escritas pela mesma pessoa que escreveu o Intent, em linguagem do usuario.

7. **Context wall at start**: contexto despejado como uma parede no inicio sobrecarrega o agente. Causa: harness nao implementa progressive disclosure. Mitigacao: Context alimentado pelo harness progressivamente, sob demanda.

8. **Monolithic context fed to fill gaps**: agentes queimam tokens sendo confiantemente errados porque preenchem buracos que o humano deixou. O custo por outcome sobe enquanto o preco por token cai. Causa: gaps nos cinco componentes do Intent. Mitigacao: fechar os cinco antes de entregar ao agente; validar com alguem que nao estava na sua cabeca.

---

## 6. Synthesis

O insight unificador e que o SDD colapsa por uma falha de decomposicao, nao de formato. Pedir que um documento carregue simultaneamente Intent, Expectations, Workflow e Context e um erro de arquitetura da decisao — os gaps entre essas funcoes sao exatamente onde os agentes tomam decisoes ruins. A resposta nao e uma spec melhor ou um formato melhor; e separar os crafts e atribuir donos distintos a cada um.

Tres implicacoes estruturais que o autor nomeia mas nao desenvolve completamente:

- **A arquitetura da decisao e o verdadeiro problema de engenharia nao resolvido**: o problema nao e que agentes constroem mal — e que constroem coisas que nao deveriam existir, porque ninguem definiu o que "deveria existir" com rigor suficiente. O design do fluxo de decisao (quem define o intent, com que granularidade, quem valida expectations, quem fecha os gaps) e mais impactante que o design do codigo produzido.

- **O output do Symphony e a prova de que o metodo e o inverso do que se vende**: a unica spec de qualidade RFC ja produzida para agentes foi documentacao retrospectiva de um sistema que ja rodava. Isso nao e um detalhe — e a evidencia de que specs uteis emergem de sistemas vivos, nao de especulacao upfront. O processo real foi: construir → extrair spec do que funciona → usar spec para rebuild multi-linguagem. A industria vende: escrever spec → construir. A inversao esconde que o primeiro passo e o mais caro e o mais incerto.

- **ICE e uma arquitetura de control plane para agentes**: Intent + Expectations como contrato de valor, Context como configuracao ambiental, Loop como motor de execucao. O humano e o control plane; o harness e o data plane. Essa separacao ecoa diretamente padroes como `application-owned-agent-control-plane` e `value-gated-agent-control-loop` no repositorio.

Para o contexto de agentes long-running, a implicacao e que o harness deve incorporar um componente de Intent-gating antes do ciclo de construcao: validar que os cinco componentes do intent estao presentes, que expectations sao verificaveis, e que o contexto e progressivo. Sem esse gate, o harness e um motor sem volante — eficiente em produzir codigo, cego em relacao ao que deveria ou nao ser produzido.
