---
title: "Exercicio 5: Aplicar o Manual Brake Question Gate a Features do KODA"
type: curriculum-exercise
nivel: 4
aliases: ["manual brake", "freio manual", "three brake questions", "tres perguntas de freio", "value gate KODA", "decisao de construir"]
tags: [curriculo-conteudo, nivel-4, exercicio, decision-discipline, governanca, value-gating, manual-brake, feature-prioritization, cost-proxy, refusal-ownership, spec-driven-development]
relates-to: ["[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake Skill]]", "[[curriculum/04-nivel-4-koda-specific/03-feature-design-patterns|Feature Design Patterns]]"]
last_updated: 2026-06-11
---
# 🛑 Exercicio 5: Aplicar o Manual Brake Question Gate a Features do KODA
## Nivel 4 -- KODA-Especifico

**Tempo Estimado:** 60-90 minutos
**Dificuldade:** ⭐⭐⭐ (Intermediario)
**Pre-requisito:** Ter lido `03-feature-design-patterns.md`, `docs/canonical/manual-brake-question-gate.md`
**Objetivo:** Aprender a aplicar as tres perguntas do Manual Brake (freio manual) a propostas reais de feature do KODA e classificar cada uma como build, experimento, adiar ou parar -- com dono nomeado e racional documentado.

---

## 📖 Prologo: A Segunda-Feira em Que o Backlog Explodiu

**Segunda-feira, 09h15. Sala de planejamento do KODA.**

O Product Manager abriu o board com um sorriso. "Boas noticias! O Claude 4.5 saiu e agora podemos fazer features que antes eram impossiveis. Tenho 14 ideias novas. Temos tokens suficientes para construir todas."

Voce olhou para a lista. Eram ideias legitimamente interessantes: recomendacao por video, gerador de NFT de treino, integracao com smartwatch, chatbot de nutricao com IA, classificador de intencao com embedding, sistema de recompensa gamificada, suporte a voz, dashboard do cliente em tempo real, ofertas de upsell baseadas em sentimento, e mais cinco que pareciam uteis mas que ninguem conseguia explicar para quem.

"Quanto custa construir tudo isso?" voce perguntou.

"Uns USD 80 em tokens. Duas tardes de agentes."

Oitenta dolares. Para 14 features. O preco real da geracao tinha removido o unico freio que existia.

Foi ai que voce se lembrou do **Manual Brake**: tres perguntas que artificialmente restauram o gate economico que o preco dos tokens removeu. Perguntas que existiam quando construir qualquer coisa custava uma semana de engenharia. Perguntas que o Spec-Driven Development fazia antes de colapsar.

Nao e um exercicio sobre codigo. E um exercicio sobre **decisao**. O tipo de decisao que define se o KODA acumula features que ninguem usa ou se cada build e justificada por valor real.

---

## 🎯 O Que Voce Precisa Fazer

Voce recebeu 7 propostas de feature para o KODA. Para cada uma, voce vai aplicar o Manual Brake de tres perguntas e classificar a proposta.

### As Tres Perguntas

1. **Quem precisa disso e o que quebra se nunca existir?** Se a resposta honesta e "ninguem", e um experimento -- trate como tal com criterios de sucesso e data de parada.
2. **Ainda construiriamos se custasse uma semana de engenharia em vez de uma tarde de tokens?** Esta e a pergunta de cost-proxy. Ela restaura o gate economico pedindo que o time precifique seu proprio trabalho em termos pre-agente.
3. **Quem e o dono de dizer nao a isso?** Uma decisao sem dono e uma armadilha. Nomeie a pessoa cujo trabalho inclui recusar. O trabalho dela tambem inclui fornecer intents alternativos quando o pedido original e rejeitado.

### As Classificacoes

- **Build** -- justificado por valor, com dono, aprovado.
- **Experimento** -- valor incerto, com criterios de sucesso e data de parada.
- **Adiar** -- potencialmente valioso mas sem urgencia ou sem dono.
- **Parar** -- nao justifica o custo de construcao em nenhum cenario.

---

## 📋 As 7 Propostas de Feature

### Feature A: "KODA Recomendacao por Video"

"O KODA envia um video curto (15-30s) gerado por IA mostrando o produto recomendado, explicando beneficios em video."

**Contexto adicional:** O time de marketing quer videos para aumentar engajamento. Nao ha dados sobre se clientes de WhatsApp assistem videos. O custo de geracao de video e 40x o custo de texto. A latencia de geracao e 2-4 minutos.

### Feature B: "Classificador de Intencao com Embedding"

"Substituir o classificador de intencao baseado em regex do KODA por um modelo de embedding semantico que entende mensagens ambiguas e classifica intencoes com maior precisao."

**Contexto adicional:** O regex atual tem 82% de precisao. O embedding promete 94%. A mudanca requer re-treinar todo o pipeline de jornada. O erro atual nao gera insatisfacao mensuravel (clientes resolvem com segunda mensagem).

### Feature C: "Integracao com Smartwatch"

"KODA se conecta a APIs de Apple Health e Google Fit para recomendar suplementos baseados em dados reais de treino do cliente."

**Contexto adicional:** 8% dos clientes KODA usam smartwatch. A integracao requer permissoes OAuth, compliance LGPD adicional para dados de saude, e manutencao continua contra mudancas de API. O desenvolvedor que construiu a integracao atual de pagamento disse que leva 3 meses so de compliance.

### Feature D: "Sistema de Recompensa Gamificada"

"Clientes acumulam pontos a cada compra e trocam por descontos. Ranking semanal. Badges por metas de treino."

**Contexto adicional:** O fundador pediu esta feature pessoalmente depois de ver um concorrente fazendo. Nao ha estudo de retencao. Ninguem no time usa gamificacao em apps proprios. O escopo completo estimado em 4 semanas de agente + 2 semanas de teste.

### Feature E: "Notificacao de Reposicao Inteligente"

"KODA calcula quando o produto do cliente vai acabar (baseado em dose diaria declarada) e envia mensagem proativa de reposicao 3 dias antes."

**Contexto adicional:** 40% dos clientes compram o mesmo produto todo mes. O churn ocorre quando o cliente esquece de repor e compra em outro lugar. A logica e simples (dose x dias = data de reposicao). Custo de implementacao estimado em 4 horas de agente. Impacto financeiro projetado: +15% em receita recorrente.

### Feature F: "Analise de Sentimento em Tempo Real"

"KODA monitora o sentimento do cliente durante a conversa e adapta o tom. Se detecta frustracao, escala para humano."

**Contexto adicional:** O time de suporte diz que e a feature mais urgente. Clientes frustrados sao mal atendidos por tom uniforme. Mas o modelo de analise de sentimento para portugues brasileiro informal tem 71% de precisao. Falsos positivos escalariam clientes felizes para suporte humano desnecessariamente.

### Feature G: "Gerador de NFT de Treino"

"KODA gera um NFT comemorativo quando o cliente atinge meta de treino (ex.: '100 dias de whey'). Colecionaveis com arte gerada por IA."

**Contexto adicional:** Ideia do estagiario de growth. Zero estudo de mercado. Custo de minting em blockchain + gas fees. Publico do KODA (praticantes de musculacao) nunca demonstrou interesse em NFTs em nenhuma pesquisa.

---

## 📝 Entregaveis

Para cada uma das 7 features, produza:

### 1. Analise Individual

| Pergunta | Sua Resposta |
|---|---|
| Quem precisa disso e o que quebra se nunca existir? | [resposta] |
| Ainda construiriamos se custasse uma semana de engenharia? | [sim/nao e por que] |
| Quem e o dono de dizer nao a isso? | [nome do papel ou pessoa] |
| **Classificacao** | [build / experimento / adiar / parar] |
| **Racional da decisao** | [2-4 frases] |

### 2. Matriz Consolidada

Crie uma tabela unica com as 7 features ranqueadas por urgencia de build (1 = construir primeiro):

| Prioridade | Feature | Classificacao | Dono | Criterio de Sucesso (se build/experimento) |
|---|---|---|---|---|
| 1 | [nome] | [build/experimento] | [dono] | [criterio] |
| ... | ... | ... | ... | ... |
| 7 | [nome] | [parar] | -- | -- |

### 3. Refusal Audit

Para cada feature classificada como **parar** ou **adiar**:

- Qual foi o motivo principal da recusa? (valor, custo, risco, timing, ownership)
- Que intent alternativo voce ofereceria em vez dessa feature?
- Sob quais condicoes essa feature seria reconsiderada?

### 4. Reflexao Final (2-3 paragrafos)

Responda:
- Qual foi a decisao mais dificil e por que?
- O que mudou na sua percepcao depois de precificar features com "uma semana de engenharia" em vez de "uma tarde de tokens"?
- Se o KODA nao tivesse um Owner-of-No, qual dessas features teria sido construida sem justificativa?

---

## 🎯 Rubrica de Avaliacao

| Criterio | Peso | Insuficiente | Satisfatorio | Excelente |
|---|---|---|---|---|
| **Precisao da analise** | 30% | Respostas genericas, sem engajamento com o contexto | Respostas usam o contexto fornecido, com raciocinio visivel | Respostas desafiam o contexto quando ele e insuficiente, buscam dados faltantes |
| **Consistencia da classificacao** | 25% | Classificacoes arbitrarias sem relacao com as respostas | Classificacoes alinhadas com as respostas dadas | Classificacoes demonstram criterios consistentes e hierarquia de tradeoffs |
| **Qualidade da recusa** | 20% | Recusas sem alternativa ou racional | Recusas com racional documentado | Recusas com intents alternativos concretos e condicoes de reconsideracao |
| **Matriz consolidada** | 15% | Ordem arbitraria, sem criterios de sucesso | Ordem justificada, com criterios de sucesso para builds | Ordem considera tradeoffs entre features (nao apenas cada uma isoladamente) |
| **Reflexao final** | 10% | Generica, nao demonstra aprendizado | Conecta a experiencia com os conceitos do Manual Brake | Identifica padroes nas proprias decisoes e questiona os limites do metodo |

---

## 🔧 Habilidades Praticadas

- **Decision discipline** -- Separar o que e barato de construir do que merece ser construido.
- **Cost-proxy reasoning** -- Usar precificacao artificial para revelar valor real.
- **Refusal ownership** -- Nomear quem diz nao como ato de design organizacional.
- **Intent articulation** -- Substituir "constroi X" por "resolva o problema Y para a pessoa Z".
- **Feature portfolio management** -- Ver o backlog como portifolio de apostas, nao como lista de tarefas.

---

## 📚 Material de Referencia

- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] -- Canonical doc com as tres perguntas e fluxo completo.
- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]] -- O papel cujo trabalho e recusar.
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]] -- O gate de valor no loop de controle.
- [[.opencode/skills/manual-brake-question-gate/SKILL|Manual Brake Skill]] -- Skill que operacionaliza as tres perguntas.
- `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns.md` -- Pattern 1 (Manual Brake Question Gate) e Pattern 2 (Value-Gated Agent Control Loop).

---
**Criado para o curriculo Long-Running Agents | v1.0 | Junho 2026**
