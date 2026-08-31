---
name: trial-retention-attribution-split
description: "Diagnostica numeros baixos de uso pos-launch separando duas populacoes que exigem donos diferentes: quem tentou e nao voltou (problema de produto) vs. quem nunca tentou (problema de change management). Rotula cada usuario com um trial flag, mede retorno (weekly-active), aplica a regra de atribuicao de duas ramas e roteia o achado para o dono que pode agir — em vez de deixar o alarme de gestao virar rollback cego do produto. Usar quando numeros de adocao baixos sao lidos como falha de produto, ao instrumentar telemetria de ativacao, ou em reviews pos-launch de agentes internos. Dispara com: 'ativacao vs retencao', 'activation vs retention', 'trial retention split', 'tentou e nao voltou', 'ninguem tentou', 'nunca tentou', 'baixa adocao', 'uso baixo pos launch', 'misattributing activation', 'problema de change management', 'roll back do agente', 'gestao alarmada com numeros', 'trial flag', 'quem ja usou o agente', 'adoption diagnostic', 'diagnostico de adocao', 'so 20 por cento usaram'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: diagnostic
  priority: medium
  source: "GTM AI Agents: Lessons from Deploying to 6,000 Users (Sait Izmit, Snowflake, 2026)"
---

## What I Do

Eu transformo "o uso esta baixo" em um diagnostico com duas ramas e dois donos. Meu trabalho nao e defender o produto nem confirmar o alarme -- e impedir que uma falha de ativacao seja atribuida a qualidade do produto (ou vice-versa) sem evidencia.

Eu produzco quatro artefatos:

1. **Auditoria de instrumentacao** — verifico se a telemetria consegue responder as duas perguntas do split: (a) existe um trial flag por usuario (quem ja interagiu ao menos uma vez com o agente)? (b) existe uma metrica de retorno (ex: weekly-active) sobre a populacao que experimentou?
2. **O split em si** — sobre uma janela de medidacao estavel, calculo: taxa de trial (experimentou / populacao elegivel) e taxa de retorno (voltou / quem experimentou).
3. **Atribuicao de duas ramas** — aplico a regra: tentou-e-nao-voltou → problema de produto (dono: time de produto); nunca-tentou → problema de change management (dono: trabalho de ativacao).
4. **Roteamento de propriedade** — o achado sai de mim como dois itens roteados, um por rama, cada um com dono nomeado e acao correta; nunca como um veredito unico ("o produto falhou").

A regra central e simples: **uso agregado e um numero; atribuicao e uma decisao de roteamento**. No caso-fonte, duas semanas apos o GA apenas 20% da organizacao havia sequer experimentado o produto — o numero baixo era ativacao, nao retencao, e a resposta correta era mudanca de gestao, nao retrabalho de produto.

## When to Use Me

Carregue esta skill quando:

- Numeros de uso pos-launch estao baixos e alguem (gestao, stakeholder, revisor) esta lendo isso como falha do produto
- Um rollout em fases ([[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]; padrao Retention-Gated Phased Rollout do mesmo pacote-fonte) chegou ao GA ou ao beta e o gate de retencao precisa ser diagnosticado
- Voce esta instrumentando telemetria de adocao para um agente interno e precisa definir quais eventos capturar (trial, retorno, recorrencia)
- Um periodo pos-intervencao chegou e o split precisa ser re-medido para verificar se a intervencao moveu a rama certa
- Um stakeholder pede "rollback" ou "rework" do agente baseado apenas em numeros agregados de uso
- Voce esta montando um dashboard de adocao e precisa decidir quais cortes ele deve expor (trial vs. retorno, por time)

Nao use quando:

- O sistema ainda esta em piloto fechado com coorte recrutada de proposito — a populacao "nunca tentou" nao existe como falha; o piloto e seleto por design
- Nao ha telemetria alguma e nao ha como instala-la — o split exige o trial flag; sem ele, a entrega e "instrumente primeiro", nao um palpite de atribuicao
- A janela pos-launch e curta demais e o ruido domina (novidade, ferias, ciclo de venda) — registre a limitacao e marque a data de re-medida; nao diagnostique em janela instavel
- A pergunta e sobre qualidade de resposta do agente e nao sobre adocao — para isso existem evals ([[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]])
- O produto e externo e o funil (aquisicao → ativacao → retencao) ja e tratado por analytics dedicada — esta skill espelha aquele funil para agentes internos, onde o "marketing" e change management

## The Anti-Pattern

```
ANTI-PATTERN: Ler uso agregado como veredito de produto e reagir com retrabalho.

Cenario:
  1. O agente interno passa pelo GA apos o gate de retencao do beta.
  2. Duas semanas depois, o dashboard mostra uso baixo: poucas sessoes,
     poucos usuarios ativos na semana.
  3. Gestao le o numero: "o produto nao presta". Sprint de produto e
     redirecionada para retrabalho de qualidade e cobertura.
  4. Ninguem pergunta: desses 6.000 usuarios, quantos JÁ abriram o
     agente uma unica vez?
  5. A resposta (caso-fonte): 20%. Oito em cada dez nunca tentaram.
     O retrabalho de produto nao moveria o numero — o produto nao era
     o gargalo.
  6. Resultado: semanas de ciclo de produto queimadas na rama errada,
     enquanto a rama certa (ativacao: demos, dashboards por time,
     patrocinio de lideranca) fica sem dono.

Consequencia:
  - Falha de ativacao tratada como falha de qualidade
  - O time de produto paga por um problema que nao e dele
  - A intervencao que resolveria (change management) nao acontece
  - O alarme de gestao se reforca porque o numero nao se move
```

O ponto de falha nao e o numero baixo — ele era real. A falha e diagnostica: uso agregado mistura duas populacoes com donos diferentes, e sem o split a atribuicao vira chute politico.

## The Pattern

```
PATTERN: Split trial/retention com atribuicao de duas ramas e roteamento de dono.

Fluxo:

  Alarme de uso baixo (ou review pos-launch agendado)
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 1. AUDITORIA DE INSTRUMENTACAO                          │
  │                                                         │
  │ Verificar, nesta ordem:                                 │
  │ - Trial flag por usuario existe? (evento persistente    │
  │   de primeira interacao real, nao click em banner)      │
  │ - Metrica de retorno existe? (weekly-active sobre quem  │
  │   experimentou, consistente com o gate de retencao)     │
  │ - Populacao elegivel definida? (todos os usuarios com    │
  │   acesso liberado no GA, nao so os voluntarios)         │
  │                                                         │
  │ Qualquer "nao" → entrega e "instrumente primeiro".      │
  │ Palpite de atribuicao sem telemetria e proibido.        │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. O SPLIT (janela estavel)                             │
  │                                                         │
  │   Populacao elegivel ──┬── nunca tentou   (taxa NT)     │
  │                        └── experimentou ──┬── voltou     │
  │                                           └── nao voltou│
  │                                                         │
  │   Taxa de trial    = experimentou / elegivel            │
  │   Taxa de retorno  = voltou / experimentou              │
  │                                                         │
  │ Janela: suficiente para absorver novidade e ruido       │
  │ (caso-fonte: duas semanas pos-GA ja revelou os 20%).    │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. ATRIBUICAO (duas ramas, dois donos)                  │
  │                                                         │
  │  Rama A: experimentaram E nao voltaram                  │
  │          → PROBLEMA DE PRODUTO                          │
  │          → dono: time de produto                        │
  │          → acao: diagnosticar QUALIDADE na ponta        │
  │            (evals, radar de gaps, spot-checks)          │
  │                                                         │
  │  Rama B: nunca experimentaram                           │
  │          → PROBLEMA DE CHANGE MANAGEMENT                │
  │          → dono: trabalho de ativacao                   │
  │          → acao: demos ao vivo, visibilidade por time,  │
  │            patrocinio de lideranca                      │
  │          → NAO e culpa do produto                       │
  └─────────────────────────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. ROTEAMENTO E RE-CHECK                                │
  │                                                         │
  │ - Dois itens roteados (um por rama), cada um com dono   │
  │   nomeado — nunca um veredito unico                     │
  │ - Intervencao acontece NA rama; depois, re-medir o      │
  │   split completo (a rama tratada deve mover; a outra    │
  │   valida que o diagnostico estava certo)                │
  │ - Registrar cada rodada: janela, taxas, acao, dono,     │
  │   resultado — historico que desarma o proximo alarme    │
  └─────────────────────────────────────────────────────────┘
```

### Tabela de decisao

| Leitura do split | Atribuicao | Dono | Acao tipica |
|---|---|---|---|
| Trial alto, retorno baixo | Produto nao sustenta o retorno | Time de produto | Diagnose de qualidade: evals contra a zona de uso real, gap radar, spot-checks |
| Trial baixo (dominante) | Ativacao falhou | Change management / ativacao | Demos ao vivo, dashboards por time, patrocinio de lideranca |
| Ambos baixos | Duas falhas independentes | Dois donos, duas frentes | Nao serializar: uma rama nao espera a outra |
| Trial baixo, retorno alto | Produto bom, alcance curto | Change management | Escalar ativacao preservando a qualidade que segura o retorno |
| Ambos altos | Sem problema de adocao | — | Alarme era ruido de janela; registrar e seguir |

### Limite da skill

O split e **diagnostico, nao cura**. Ele nao corrige qualidade nem executa ativacao — ele impede a intervencao errada e nomeia quem age. A rama de produto se arma com os evals do repositorio; a rama de change management e trabalho organizacional ([[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] cobre o como, fora de escopo desta skill).

## Implementation Rules

1. **Trial flag e evento persistente, nao metrica derivada.** "Experimentou" precisa sobreviver a limpeza de sessao e a troca de dispositivo: um flag por usuario (primeira interacao real com o agente), gravado no perfil, nao recomputado de logs volateis. Sem isso o split degrada silenciosamente.

2. **Retorno se mede sobre quem experimentou, nunca sobre a populacao total.** Taxa de retorno com denominador errado (populacao toda) re-contamina o split que a metrica existe para separar. O denominador da rama de produto e o conjunto que deu ao produto uma chance.

3. **Defina "tentou" e "voltou" antes de medir.** Uma interacao real (pergunta enviada, tarefa disparada) — nao abrir a UI, nao click em tutorial. Ambiguidade aqui vira disputa de interpretacao quando o numero for politicamente desconfortavel.

4. **Janela estavel ou nenhuma janela.** Early noise domina: lancamento, novidade, ferias, ciclo comercial. Se a janela ainda e ruidosa, o output e "re-medir em <data>", nao uma atribuicao. Declarar a janela usada em toda rodada.

5. **Duas ramas, dois itens roteados — sempre.** Mesmo quando uma rama domina (os 80% nunca-tentaram), a outra rama existe e vai roteada com dono. O caso-fonte mostra o custo de nao fazer isso: retrabalho de produto por falha de ativacao.

6. **O split e a resposta ao alarme, nao um argumento.** Quando gestao le numero baixo como falha, a entrega e o mecanismo: dois numeros, dois donos, uma tabela de decisao. Isso desarma o alarme com metodo — desde que a telemetria exista (regra 1), o que torna a instrumentacao parte do trabalho de launch, nao um retrofit.

7. **Re-check apos cada intervencao e parte do padrao.** A rama tratada deve mover; a outra serve de controle. Se a rama tratada nao move, o diagnostico estava errado ou a intervencao foi fraca — registrar qual, e reabrir.

## Integration with Existing Repo Infrastructure

O split entra no ciclo de vida de rollout e diagnostico do repositorio como instrumento de atribuicao do eixo populacional:

| Componente Existente | Como o Trial-Retention Attribution Split complementa |
|---|---|
| [[docs/canonical/trial-retention-attribution-split|Trial-Retention Attribution Split (canonical)]] | O doc canonico define o padrao (problema, regra de duas ramas, tradeoffs). Esta skill e a rotina executavel em cima dele: auditoria de instrumentacao, calculo do split, tabela de decisao e roteamento. Quando o canonical e a spec, a skill e o como-executar. |
| [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] | O correlacao-tracking disciplina a misatribuicao eval-vs-producao (score bom, outcome ruim). O split e o analogo no eixo de adocao: separa ativacao de retencao quando o numero agregado mente. Juntos: tres fontes de falso sinal (eval, producao, adocao) com regra de atribuicao propria. |
| [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] | Precedente de roteamento de propriedade: captura, tria, converte em item com dono. O split aplica o mesmo principio a diagnostico de ativacao: o achado (rama A ou B) vira item roteado, nao veredito solto. |
| [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] | Define shadow/canary/rollback e metricas de producao para infra. O split opera o eixo que falta: populacao de usuarios. Quando o gate de retencao de um rollout em fases falha, o split diz qual rama (e qual dono) responde. |
| [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard as Primary Detection Surface]] | O dashboard torna sinais de dor visiveis. Os cortes de trial/retorno pertencem a essa superficie: o split define quais numeros o dashboard precisa expor para que o alarme chegue ja atribuido. |
| [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] | Evals sao o freio que da confianca para nao desacelerar. O split e o freio analogo do rollback: existencia de diagnostico com dono evita a reacao lenta-e-errada (retrabalho cego de produto). |
| [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] | Cadencia periodica de revisao. Rodadas de re-check do split se agendam no mesmo ritmo: cada ciclo revisa se as intervencoes moveram as ramas certas. |
| [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] + padrao Retention-Gated Phased Rollout ([[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]) | O Retention-Gated Phased Rollout fornece o gate (>70% weekly-active) cuja falha o split diagnostica; o Owner-Led Activation Blitz e o manual de execucao da rama B (nunca-tentou). Esta skill cobre o diagnostico e o roteamento entre eles. |

## Quality Gates

Antes de declarar um diagnostico de split como valido, verifique:

- [ ] O trial flag existe como evento persistente por usuario e captura interacao real (nao abertura de UI)
- [ ] A taxa de retorno usa como denominador quem experimentou, nao a populacao total
- [ ] A populacao elegivel esta definida (todos com acesso no GA) e declarada na rodada
- [ ] A janela de medidacao e estavel o suficiente para o ruido de novidade, e esta registrada
- [ ] O output sao duas ramas com dono nomeado cada — nao um veredito unico de "produto falhou/nem tanto"
- [ ] Nenhuma intervencao foi serializada: as duas ramas quando presentes recebem frentes independentes
- [ ] A rama de produto roteia para instrumentos de qualidade existentes (evals, gap radar), nao para retrabalho generico
- [ ] A rodada ficou registrada (janela, taxas, acoes, donos) para o re-check pos-intervencao
- [ ] O re-check esta agendado e a rama nao-tratada sera usada como controle
- [ ] Nenhum palpite de atribuicao foi entregue onde a telemetria nao sustenta o split

## References

- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]:48-51 — o split: 20% tentaram; tentou-e-nao-voltou → produto; nunca-tentou → change management
- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]:132 — management leu baixo uso como falha de produto ate o split ser mostrado
- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]:120-148 — Pattern 4: Trial-Retention Attribution Split (componentes, fluxo, limitacoes)
- [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]:99-123 — classificacao como Missing (Medium value)
- [[docs/canonical/trial-retention-attribution-split|Trial-Retention Attribution Split]] — doc canonico do padrao (spec desta rotina executavel)
- [[docs/canonical/owner-led-activation-blitz|Owner-Led Activation Blitz]] — execucao da rama never-tried (change management)
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — disciplina de anti-misatribuicao no eixo eval-vs-producao (o split e o analogo de adocao)
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] — precedente de roteamento de achados com dono
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — rollout em fases cujo gate de retencao o split diagnostica

---

*Created: 2026-08-30 | Source: GTM AI Agents — Pattern 4 (Missing, Medium value)*
