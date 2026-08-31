---
name: agent-value-maturity-ladder
description: "Audita planos de deployment e roadmaps de produtos de agentes contra o modelo de quatro estagios de valor (1 falar com os dados, 2 automatizar workflows com revisao humana, 3 empoderar times a construir skills proprias, 4 hiper-personalizacao com contexto vivo). Detecta estagios pulados, ausencia de plano de proximo estagio, e a falta de listener de sinal de habituacao — a postura 'sempre que estao felizes, esteja paranoico' que converte o colapso do wow em proximos estagios planejados. Gera um staged audit report com classificacao de estagio atual, gap de cadencia, e custos de troca acumulados por estagio. Usar ao revisar roadmaps de produtos de agentes internos, ao planejar a proxima onda de funcionalidades, ou quando usuarios comparam o agente com outros produtos de IA. Dispara com: 'maturity ladder', 'escada de maturidade', 'estagios de valor', 'value stages', 'talk to your data', 'automate my workflows', 'team empowerment', 'hyper-personalization', 'wow collapse', 'colapso do wow', 'habituacao', 'habituation', 'switching cost', 'custo de troca', 'roadmap de agente', 'plano de deployment de agente', 'usuarios comparando com chatgpt', 'proximo estagio', 'paranoia quando felizes'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: audit
  priority: medium
  source: "GTM AI Agents: Lessons from Deploying to 6,000 Users (Sait Izmit, Snowflake, 2026)"
---

## What I Do

Eu audito um plano de deployment, roadmap, ou estado atual de um produto de agente contra o modelo de quatro estagios de valor, e devolvo um **staged audit report** com o que esta faltando para o valor nao estagnar. Meu trabalho nao e construir o proximo estagio -- e impedir as duas falhas que congelam deployments de agentes no primeiro estagio:

1. **Colapso do wow nao planejado** — o status de "rockstar" do launch decai em meses porque a capacidade vira habito e depois baseline; usuarios voltam com frustracoes e comparacoes com outros produtos de IA. Sem proximo estagio pronto, a queda e lida como decadencia do produto em vez de cronograma.
2. **Escada de custo de troca nao construida** — com switching costs proximos de zero, ficar parado em qualquer estagio significa disrupcao em 1-2 meses. Cada estagio sobe a dependencia do usuario na plataforma; pular estagios queima a confianca que a escada depende.

Meu output e um relatorio com: estagio atual classificado (1-4, com evidencia), o plano de proximo estagio existe ou nao (e com qual cadencia — a referencia e 1-2 meses por estagio), o listener de habituacao esta ou nao no lugar, e a auditoria de switching costs do estagio atual.

A regra central e simples: **valor entregue e funcao de estagio, nao de feature isolada** — e cada estagio deve estar comprando o direito de iterar no proximo.

## When to Use Me

Carregue esta skill quando:

- Um roadmap ou plano de deployment de agente interno chega para revisao e precisa ser auditado contra uma sequencia de valor
- O agente lancou ha meses no estagio 1 (Q&A / falar com os dados) e ninguem sabe qual e o estagio 2 ou quando ele chega
- Usuarios comecam a voltar com comparacoes ("o ChatGPT faz isso melhor") ou frustracoes — o sinal classico de habituacao comecando
- Um stakeholder pede "mais features" sem conexao com estagio — a auditoria mostra se a-feature-e-o-proximo-estagio ou ruido
- Alguem propoe pular direto para automacao total ou hiper-personalizacao sem os estagios intermediarios
- Um review periodico (tipo [[docs/canonical/garbage-collection-day-meta-loop|GC Day]]) quer incluir "o wow ainda esta de pe?" como item de agenda
- Voce esta planejando a proxima onda de shipping e precisa da structura estagio → sinal → cadencia

Nao use quando:

- O objeto e autonomia do agente (observe → assist → own) e nao valor de produto — para isso existe [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]; escadas diferentes, objetos diferentes
- O objeto e maturidade de evals ou lifecycle de componentes do harness — [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] e o system-of-record de evals cobrem; a ladder aqui e do valor percebido pelo usuario
- O deployment e um one-shot interno de uso unico sem usuarios recorrentes — sem habituacao, a ladder nao se aplica
- A tarefa e executar change management ou ativacao — roteie pelo [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]]; eu audito estagios, nao executo adocao
- O plano ja foi auditado contra a ladder recentemente e nada mudou — re-auditar sem novo sinal e cerimonial

## The Anti-Pattern

```
ANTI-PATTERN: Tratar o valor do launch como patrimonio, nao como deprecacao.

Cenario:
  1. O agente interno lancou no estagio 1: "falar com os dados".
     Sucesso imediato. Os usuarios chamam de rockstar. O time comemora.
  2. O roadmap seguinte e preenchido com features horizontais:
     mais uma fonte de dados, mais um filtro, mais um atalho.
     Nenhum item move de estagio.
  3. Quatro meses depois: a capacidade de perguntar aos dados virou
     habito, depois baseline. Ninguem comenta mais.
  4. Usuarios voltam com comparacoes: "o outro produto de IA faz
     isso e tambem escreve o email". O sinal e lido como ingratidao.
  5. Switching costs seguem proximos de zero: o dado ja esta la,
     a conversa e portatil, a lealdade nao existe.
  6. Em 1-2 meses, um produto concorrente interno ou externo
     absorve a funcao. O agente e descontinuado com a etiqueta
     "deu certo e depois sumiu".

Consequencia:
  - O wow decai sem sucessor planejado — decaindo e visto como
    falha do produto, quando era o cronograma natural da habituacao
  - Features horizontais nao constroem switching cost: nenhuma delas
    cria dependencia cumulativa
  - A confianca acumulada no estagio 1 nunca foi gasta comprando o
    direito ao estagio 2 — o ativo apreciava e foi consumido
```

O ponto de falha nao e a falta de features — havia roadmap cheio. A falha e estrutural: valor tratado como estoque ( conquistado no launch, preservado por inercia) em vez de escada (cada estagio levanta o custo de troca e financia o proximo).

## The Pattern

```
PATTERN: Roadmap como escada de estagios de valor com listener de habituacao.

  OS QUATRO ESTAGIOS (modelo observado, caso Snowflake GTM):

  ┌──────────────────────────────────────────────────────────────┐
  │ E1. FALAR COM OS DADOS                                        │
  │     Democratizacao: escapar de 1.000 dashboards e filas de    │
  │     2 semanas com analistas. Qualidade escopada (50 perguntas │
  │     a 95%, nao 100 a 70%) protege o primeiro contato.         │
  │                                                               │
  │ E2. AUTOMATIZAR MEUS WORKFLOWS                                │
  │     Orquestracao de sistemas externos com revisao humana no   │
  │     envio irreversivel (monitora inbox/Slack → rascunha →     │
  │     humano revisa → humano envia).                            │
  │                                                               │
  │ E3. EMPODERAR OS TIMES                                        │
  │     Times constroem proprias skills, dashboards, apps,        │
  │     automacoes, alertas — escapando do backlog de IT.         │
  │                                                               │
  │ E4. HIPER-PERSONALIZACAO                                     │
  │     Tudo personalizado por vendedor E por cliente, com        │
  │     contexto vivo de clientes e contatos.                     │
  └──────────────────────────────────────────────────────────────┘
        │                │                │               │
        └── confianca comprando o direito do proximo ─────┘

  AUDITORIA (o que eu executo sobre o plano/deployment):

  Entrada: plano de deployment, roadmap, ou estado atual
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. CLASSIFICAR ESTAGIO ATUAL                            │
  │    Evidencia exigida por estagio:                       │
  │    E1: Q&A sobre dados em producao com usuarios reais   │
  │    E2: ao menos um workflow ponta-a-ponta com gate      │
  │        humano no envio                                  │
  │    E3: artefato construido por UM TIME nao-engineering  │
  │        (skill, dashboard, app) rodando em producao      │
  │    E4: comportamento diferenciado por usuario E por     │
  │        cliente-alvo, com contexto vivo atualizado       │
  │    Classificar pelo MAIOR estagio com evidencia real —  │
  │    plano nao e evidencia.                               │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. AUDITAR O PLANO DE PROXIMO ESTAGIO                   │
  │    - Existe item de roadmap que MOVE de estagio?        │
  │    - Cadencia: 1-2 meses por proximo estagio (ref.)     │
  │    - Pulos: E1 → E4 direto e falha de confianca —       │
  │      estagios pressupoem os anteriores                  │
  │    - Features horizontais contam como manutencao do     │
  │      estagio atual, nao como progresso de ladder        │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. AUDITAR O LISTENER DE HABITUACAO                     │
  │    Sinais de que o estagio atual virou baseline:        │
  │    - Mencao/entusiasmo caindo (novidade → habito)       │
  │    - Usuarios voltando com comparacoes a outros         │
  │      produtos de IA                                     │
  │    - Frustracao com limites do estagio atual ("faz      │
  │      isso e nao escreve o email?")                      │
  │    Sem listener → o colapso do wow chega como surpresa. │
  │    Postura: sempre que estao felizes, esteja paranoico. │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. AUDITAR SWITCHING COSTS DO ESTAGIO ATUAL             │
  │    Por estagio, o que o usuario PERDERIA ao sair:       │
  │    E1: quase nada (a pergunta e portatil)               │
  │    E2: os workflows automatizados                       │
  │    E3: os artefatos que o proprio time construiu        │
  │    E4: o contexto vivo pessoal e por cliente            │
  │    Estagio sem switching cost acumulando =janela de    │
  │    disrupcao aberta (1-2 meses no caso-fonte).          │
  └─────────────────────────────────────────────────────────┘
       │
       ▼
  OUTPUT: staged audit report
  { estagio_atual, evidencia, proximo_estagio_planeado (s/n),
    cadencia_ok (s/n), pulos_detectados, listener_habituacao (s/n),
    switching_cost_acumulando (s/n), verdict }
  Verdicts: LADDER_SAUDAVEL | WOW_EXPONDO | ESTAGIO_PULADO |
            LADDER_CONGELADA
```

### Tabela de verdicts

| Condicao detectada | Verdict | Significado |
|---|---|---|
| Estagio com evidencia + proximo planeado com cadencia + listener ativo | LADDER_SAUDAVEL | Confianca sendo convertida em proximo estagio no ritmo da habituacao |
| Estagio atual virando baseline e sem sucessor planeado | WOW_EXPONDO | O relogio de 1-2 meses comecou; planejar o proximo showing agora |
| Roadmap pula estagios (ex: E1 → E4) | ESTAGIO_PULADO | A confianca que a escada depende ainda nao foi construida; re-sequenciar |
| Features horizontais ha N ciclos sem item que mova de estagio | LADDER_CONGELADA | O plano preserva o estagio em vez de subi-lo; switching cost estagnado |

## Implementation Rules

1. **Classifique por evidencia de producao, nao por intencao de plano.** Um roadmap que promete automacao nao move o deployment para E2; um workflow com gate humano rodando move. A auditoria le o que existe, e o maior estagio com evidencia real e o estagio atual.

2. **Pulos sao falha estrutural, nao otimismo.** Cada estagio pressupoe a confianca do anterior (E4 sem E2/E3 e personalizacao sem workflows nem artefatos que personalizar). Auditoria que encontra E1 → E4 retorna ESTAGIO_PULADO com a recomendacao de re-sequenciar, nao de "tentar".

3. **Features horizontais sao manutencao de estagio.** Mais uma fonte de dados em E1, mais um filtro, mais um atalho: nada disso levanta switching cost nem responde a habituacao. Conte-as separadamente do progresso de ladder — e um plano so de features horizontais por mais de 1-2 ciclos e LADDER_CONGELADA.

4. **O listener de habituacao e obrigatoria e barata.** Os sinais (mencao caindo, comparacoes a outros produtos de IA, frustracao com limites do estagio) sao qualitativos e ja circulam em canais existentes; a auditoria so exige que alguem os escute com proposito. Sem listener, o colapso do wow e sempre uma surpresa tardia.

5. **Cadencia de 1-2 meses por estagio e a referencia, nao lei.** O caso-fonte shipping um estagio por 1-2 meses. Contextos menores podem ser mais rapido; o que nao muda e a relacao: o proximo estagio chega antes de o atual terminar de virar baseline. A auditoria checa a relacao, nao o numero absoluto.

6. **Switching cost e o placar da ladder.** A pergunta por estagio e simples: "o usuario perderia o que ao sair amanha?". Se a resposta e "quase nada" por dois estagios seguidos, a escada nao esta sendo construida — o produto e substituivel por definicao, independente do quao bom ele e.

7. **A auditoria informa, o operador decide.** O staged audit report e insumo para a decisao de roadmap (do dono do produto), nao um gate que bloqueia. Wow expondo com stakeholders exigindo features horizontais e uma decisao de trade-off — meu trabalho e garantir que ela seja tomada sabendo que o relogio existe.

## Integration with Existing Repo Infrastructure

A ladder entra como instrumento de auditoria do eixo valor/adocao, ao lado das escadas existentes para outros objetos:

| Componente Existente | Como o Agent Value Maturity Ladder complementa |
|---|---|
| [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder (canonical)]] | O doc canonico define o modelo de quatro estagios, a tese de switching costs e as regras operacionais. Esta skill e a rotina de auditoria executavel em cima dele: classificar estagio por evidencia, auditar plano de proximo estagio, listener de habituacao e switching costs, devolver verdict. |
| [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] | A escada mais proxima com objeto errado: observe → assist → own governa QUANTO o agente pode fazer sozinho; a value ladder governa QUANTO o produto vale para o usuario. Complementares: E2 (automatizar workflows) tipicamente coincide com a transicao assist → own, com o gate humano do envio. |
| [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] | Lifecycle mede a evolucao dos componentes do harness; a ladder mede a evolucao do valor percebido. Juntas respondem: "a plataforma amadureceu E o usuario depende mais dela?" — uma sem a outra e melhoria invisivel ou adocao sem fundacao. |
| [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] | Confianca e a moeda: o escopo de qualidade (50 a 95%) protege o primeiro contato que compra o direito ao estagio seguinte. A auditoria de ladder assume que os brakes existem — pulo de estagio com qualidade baixa queima a escada inteira. |
| [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] | O gate decide qual capacidade construir proxima por dor observada; a ladder audita se o resultado dessas decisoes forma uma escada de valor. Dor que aponta para o proximo estagio tem prioridade estrutural sobre dor horizontal. |
| [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver Skillify Capability Pipeline]] | Mecanica do estagio 3: times constroem skills proprias com resolver metadata e gates. Empoderamento (E3) sem essa pipeline e pedido de baixo-code sem entrega — a auditoria de E3 exige artefato real de time nao-engineering. |
| [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] | Cadencia periodica onde o listener de habituacao mora naturalmente: cada ciclo pergunta "o wow ainda esta de pe? qual o proximo showing?". A ladder fornece o rubrico, o GC Day o ritmo. |
| [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] + padroes do mesmo pacote-fonte ([[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]) | Quality-Over-Coverage (padrao 2) arma o E1; Human-Review Staged Workflow Automation (padrao 8) e a mecanica do E2; Skill Library (padrao 7) alimenta o E3; o Owner-Led Activation Blitz cuida da ativacao que cada estagio recruta — o blitz enche o funil, a escada converte uso em retencao. |

## Quality Gates

Antes de declarar um staged audit report como valido, verifique:

- [ ] O estagio atual foi classificado pelo maior estagio com evidencia de producao real (artefato rodando, nao item de plano)
- [ ] A evidencia de classificacao esta citada (onde o auditor a encontrou) — sem evidencia, e palpite
- [ ] O plano de proximo estagio foi distinguido das features horizontais de manutencao do estagio atual
- [ ] Pulos de estagio foram verificados explicitamente (E1→E3, E1→E4, E2→E4) e sinalizados
- [ ] A cadencia verificada e a relacao (proximo estagio antes do atual virar baseline), com o numero absoluto declarado como referencia de contexto
- [ ] O listener de habituacao foi auditado: quem escuta mencao caindo, comparacoes a outros produtos, frustracao com limites do estagio
- [ ] A pergunta de switching cost foi respondida por estagio: "o usuario perderia o que ao sair amanha?"
- [ ] O verdict (LADDER_SAUDAVEL | WOW_EXPONDO | ESTAGIO_PULADO | LADDER_CONGELADA) e consistente com os achados acima
- [ ] O relatorio foi entregue ao dono do produto como insumo de decisao — nao executado como gate automatico

## References

- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]:62-67 — o modelo de quatro estagios (talk to your data → automate workflows → team empowerment → hyper-personalization)
- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]:57-60 — colapso do wow, postura paranoica, switching costs proximos de zero
- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]:136 — rockstar decai em frustracao em ~4-6 meses conforme capacidade vira baseline
- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]:407-440 — Pattern 13: Agent Value Maturity Ladder (estagios, sinais, cadencia, limitacoes)
- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]:348-369 — classificacao como Missing (Medium value)
- [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]] — doc canonico do modelo (spec desta rotina de auditoria)
- [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] — ativacao que cada estagio da escada recruta
- [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — escada vizinha com objeto diferente (autonomia do agente, nao valor de produto)
- [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — confianca como moeda que cada estagio gasta e recarrega
- [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver Skillify Capability Pipeline]] — mecanica do estagio 3 (times constroem skills proprias)

---

*Created: 2026-08-30 | Source: GTM AI Agents — Pattern 13 (Missing, Medium value)*
