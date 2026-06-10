---
title: "Architecture Decision Record (ADR) Template"
type: curriculum-template
aliases: []
tags: [curriculo-conteudo, template]
last_updated: 2026-06-10
---
# 📋 Architecture Decision Record (ADR) Template
## Documentando Decisões Arquiteturais para Long-Running Agents

**Tempo Estimado:** 60 minutos (leitura + aplicação)  
**Nível:** Todos (fundamental para qualquer nível)  
**Pré-requisito:** Entendimento básico de arquitetura de agentes  
**Status:** 🟢 TEMPLATE - Use em todo projeto de long-running agents  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: Por Que Decisões Arquiteturais Precisam Ser Documentadas?

Três meses atrás, a equipe KODA enfrentava um dilema.

O sistema estava crescendo rápido. Novas features entravam toda semana. Novos engenheiros chegavam. O código evoluía. Mas havia um problema silencioso que ninguém conseguia nomear:

**"Por que escolhemos fazer assim?"**

Toda vez que alguém perguntava, a resposta era a mesma:

> "Foi o Fernando que decidiu. Acho que foi em março. Ou abril. Tem uma thread no Slack em algum lugar... deixa eu procurar."

E então começava a caça: 20 minutos vasculhando mensagens antigas, PRs fechados, documentos soltos no Google Drive. Às vezes achava. Às vezes não.

O pior não era a perda de tempo. Era o **custo das más decisões repetidas**.

Em junho, um novo engenheiro refatorou o módulo de busca de produtos. Ele implementou uma arquitetura baseada em **chamadas síncronas** para o catálogo. Funcionava bem nos testes. Em produção, travava o agente por 12 segundos em conversas de pico.

O que ele não sabia: há 4 meses, Fernando havia decidido usar **chamadas assíncronas com caching** exatamente para evitar esse problema. A decisão estava documentada... em algum lugar. Mas ninguém leu. Ninguém sabia que existia.

**O resultado:** 3 dias de debugging, um rollback apressado, e um cliente furioso que esperou 45 segundos por uma resposta.

---

### O Padrão que Toda Empresa de Tecnologia de Elite Usa

Naquele mês, Fernando descobriu o conceito de **Architecture Decision Records (ADRs)** — uma prática que a Amazon, Spotify, ThoughtWorks e Netflix usam há anos.

A ideia é simples e poderosa:

> **Toda decisão arquitetural significativa é registrada em um documento imutável, curto, que explica O QUE foi decidido, POR QUÊ, e quais as CONSEQUÊNCIAS.**

Quando o novo engenheiro chegou em junho, em vez de perguntar "por que o KODA faz assim?", ele poderia ter aberto a pasta `docs/decisions/` e lido:

```
adr-003-catalog-access-pattern.md:

Status: ACCEPTED
Decisão: Usar chamadas assíncronas com caching em TTL de 5 minutos
          para todas as consultas ao catálogo de produtos.

Motivo: Chamadas síncronas causam latência de 8-15 segundos em
        conversas de pico (10+ clientes simultâneos). Cache reduz
        para <200ms e evita degradação do agente.

Consequências:
- ✅ Latência caiu de 12s para 180ms
- ⚠️ Cache pode ficar stale por até 5 minutos
- ⚠️ Implementação adiciona complexidade no módulo de inventário
```

Em 30 segundos de leitura, ele entenderia **o que foi decidido, por quê, e o que evitar**. Zero caça ao tesouro. Zero más decisões repetidas.

Este template existe para que **você nunca precise explicar a mesma decisão duas vezes**.

---

### O Que Você Vai Aprender Neste Template

✅ O que é um ADR e por que ele é fundamental para projetos de long-running agents  
✅ A estrutura completa de um ADR: Título, Status, Contexto, Decisão, Consequências  
✅ Um exemplo real e preenchido — a decisão KODA de adotar o padrão Generator/Evaluator  
✅ Um guia prático de quando (e quando NÃO) criar um ADR  
✅ Um checklist de completude para validar seus ADRs antes de publicar  
✅ Como ADRs se relacionam com outros documentos do projeto (rubrics, sprint contracts, README)

---

## 🎯 O Que É um Architecture Decision Record (ADR)?

### Definição Formal

Um **Architecture Decision Record (ADR)** é um documento curto e imutável que captura:

1. **Uma decisão arquitetural significativa** — não qualquer decisão, mas aquelas que afetam estrutura, fluxo de dados, ou comportamento do sistema
2. **O contexto em que foi tomada** — o que estava acontecendo, quais eram as alternativas, quais eram as restrições
3. **As consequências** — boas e ruins. O que ganhamos e o que perdemos com essa decisão

### Características Fundamentais

| Característica | Descrição |
|---|---|
| **Imutável** | Uma vez aceito, o ADR **não é editado**. Se a decisão mudar, crie um NOVO ADR que referencia e substitui o anterior |
| **Curto** | 1-2 páginas. Se precisa de mais, provavelmente é uma spec, não um ADR |
| **Contextual** | Explica o PORQUÊ, não apenas o QUÊ. O contexto é a parte mais valiosa |
| **Atemporal** | Alguém lendo daqui a 2 anos deve entender por que a decisão foi tomada |
| **Autocontido** | Não depende de links externos, threads do Slack, ou conhecimento tribal |

### O Que NÃO É um ADR

- ❌ **Documentação de API** — isso é spec técnica, não decisão arquitetural
- ❌ **README de módulo** — explica COMO usar, não POR QUE foi construído assim
- ❌ **Registro de reunião** — decisões de implementação tática não são ADRs
- ❌ **User story** — descreve o comportamento desejado, não a arquitetura
- ❌ **Post-mortem** — analisa o que deu errado, não captura uma decisão

### O Fluxo de Vida de um ADR

```
IDEA ou PROBLEMA surge
        │
        ▼
┌───────────────────────────┐
│ DISCUSSÃO entre time      │
│ (Issue, PR, reunião)      │
└──────────┬────────────────┘
           │
           ▼
┌───────────────────────────┐
│ PROPOSTA de ADR           │
│ Status: PROPOSED           │
└──────────┬────────────────┘
           │
           ▼
┌───────────────────────────┐
│ REVIEW pelo time          │
│ (2+ engenheiros aprovam)  │
└──────────┬────────────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
  ACEITO      REJEITADO
  Status:     Status:
  ACCEPTED    REJECTED
     │           │
     │           └─ Fim (documenta por que NÃO fazer)
     │
     ▼
┌───────────────────────────┐
│ IMPLEMENTAÇÃO             │
│ Decisão vira código       │
└──────────┬────────────────┘
           │
           ▼ (meses depois)
┌───────────────────────────┐
│ SUBSTITUÍDO ou DEPRECATED │
│ Novo ADR referencia este  │
│ Status: SUPERSEDED        │
└───────────────────────────┘
```

---

## 🏗️ A Estrutura do ADR

Cada ADR contém **6 seções obrigatórias** e **2 opcionais**. O template abaixo é o padrão que usamos em projetos de long-running agents.

### Template Base (copie e preencha)

```markdown
# ADR-NNN: Título da Decisão

**Status:** [PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED]  
**Data:** YYYY-MM-DD  
**Autor:** Nome ou @github  
**Decisores:** Lista de quem aprovou  
**Substitui:** ADR-NNN (se aplicável)  
**Substituído por:** ADR-NNN (se aplicável)

---

## Contexto

Descreva o problema ou a situação que motivou esta decisão. Inclua:

- O estado atual do sistema (como as coisas funcionam hoje)
- O problema ou limitação encontrada
- As forças em jogo (trade-offs, restrições, requisitos conflitantes)
- Por que uma decisão arquitetural é necessária AGORA

Use linguagem neutra. Não assuma que o leitor conhece o contexto.
Esta seção responde: "O que estava acontecendo que nos levou a decidir?"

Exemplo de forças:
- Restrições de latência (< 200ms para não degradar agente)
- Custo de infraestrutura (orçamento de R$ 500/mês para APIs)
- Escalabilidade (precisa suportar 10x mais conversas em 3 meses)
- Complexidade (time de 3 engenheiros, não podemos adotar arquitetura complexa)
- Segurança (dados de cliente não podem trafegar em texto plano)

---

## Eval Capability Impact (opcional)

Preencha quando a decisão altera prompt, model, tool, context, memory, rubric, evaluator, agent-loop ou capacidade de eval. Se não se aplica, escreva N/A.

| Campo | Valor |
|---|---|
| Pain signal | user complaint / manual bottleneck / score-feedback mismatch / escaped edge case / release-risk increase |
| Current eval capability | O que detecta regressão hoje |
| Chosen next capability | Menor capacidade nova que esta decisão exige |
| Deferred capabilities | O que foi deliberadamente deixado para depois |
| Owner | Pessoa ou squad responsável |
| Operating cost | Runtime, latência, custo financeiro ou revisão humana |
| Review date | Data para decidir KEEP, SIMPLIFY ou REMOVE |

---

## Decisão

Declare a decisão de forma clara e sem ambiguidade. Use uma frase direta:

> "Nós vamos [fazer X] usando [tecnologia/abordagem Y] para [resolver Z]."

Explique:

- **O que** exatamente foi decidido
- **Como** será implementado (alto nível, sem código)
- **Por que** esta opção foi escolhida sobre as alternativas

Inclua um diagrama ASCII se a decisão envolver fluxo de dados ou arquitetura.

---

## Alternativas Consideradas

Liste cada alternativa avaliada e por que foi rejeitada:

| Alternativa | Prós | Contras | Por que rejeitada |
|---|---|---|---|
| Opção A | ... | ... | ... |
| Opção B | ... | ... | ... |
| Opção C (escolhida) | ... | ... | Melhor trade-off |

Seja honesto sobre alternativas. Este registro existe para que futuros
leitores não tenham que reavaliar as mesmas opções.

---

## Consequências

Descreva o que muda após esta decisão ser implementada. Seja específico.

**Ganhos (positivo):**
- ✅ O que melhora?
- ✅ Quais problemas são resolvidos?
- ✅ Que novas capacidades surgem?

**Riscos e trade-offs (negativo):**
- ⚠️ O que piora ou fica mais complexo?
- ⚠️ Quais são os novos riscos?
- ⚠️ O que NÃO conseguimos fazer por causa desta decisão?

**Neutro (mudanças operacionais):**
- ℹ️ O que a equipe precisa fazer diferente?
- ℹ️ Novos processos, ferramentas, ou monitoramento?
- ℹ️ Impacto em outros times ou sistemas?

---

## Notas e Referências

(Opcional) Links para issues, PRs, documentos, threads de discussão que
fornecem mais contexto. Não coloque informações essenciais aqui — o ADR
deve ser autocontido.

- Issue: #NNN
- PR: #NNN
- Discussão: [link para thread]
- Documento relacionado: [link]
```

---

### Explicação Detalhada de Cada Seção

#### 1. Cabeçalho (ADR-NNN: Título)

O título deve ser descritivo o suficiente para que alguém lendo apenas o índice entenda a decisão.

**Formato:** `ADR-NNN: Verbo no presente + objeto da decisão`

| ✅ Bom Título | ❌ Título Ruim |
|---|---|
| ADR-001: Usar PostgreSQL para persistência de estado | ADR-001: Banco de dados |
| ADR-002: Adotar padrão Generator/Evaluator para recomendações | ADR-002: Melhorar recomendações |
| ADR-003: Implementar file-based coordination entre agentes | ADR-003: Coordenação |
| ADR-004: Migrar de REST para GraphQL no módulo de catálogo | ADR-004: GraphQL |

**Numeração:** Sequencial (001, 002, 003...). Nunca reuse números. Se um ADR é substituído, o novo ganha um número novo.

#### 2. Status

Use **apenas um** destes status:

| Status | Significado | Quando usar |
|---|---|---|
| `PROPOSED` | Decisão proposta, ainda em discussão | Durante review da proposta |
| `ACCEPTED` | Decisão aceita e em vigor | Após aprovação pelo time |
| `REJECTED` | Decisão rejeitada | Documenta por que NÃO fazer algo (útil para evitar repetição) |
| `DEPRECATED` | Decisão não é mais relevante (mas não foi substituída) | Sistema evoluiu além desta decisão |
| `SUPERSEDED` | Substituída por outro ADR | Nova decisão torna esta obsoleta. Referenciar ADR substituto |

> ⚠️ **Regra de Imutabilidade:** Nunca mude o status de `ACCEPTED` para `REJECTED` editando o ADR. Crie um novo ADR com status `SUPERSEDED` e referencie o original.

#### 3. Contexto

Esta é a **seção mais importante** para leitores futuros. Sem contexto, a decisão parece arbitrária.

**Perguntas que o contexto deve responder:**
- Qual era o problema que estávamos tentando resolver?
- O que tínhamos tentado antes? O que funcionou? O que falhou?
- Quais eram as restrições (tempo, budget, equipe, tecnologia)?
- Quais eram as forças conflitantes (ex: velocidade vs qualidade, custo vs performance)?
- Por que esta decisão era necessária AGORA e não podia esperar?

**Anti-padrões de contexto:**
- "Precisávamos escalar" — muito vago. Escalar de quanto para quanto? Em quanto tempo?
- "O time decidiu" — quem? Quais eram as opções?
- "A arquitetura atual não serve" — por que especificamente?

#### 4. Decisão

A decisão em si. Uma frase clara, seguida de explicação.

**Template de frase:**
> "Nós vamos **[verbo de ação]** usando **[tecnologia/abordagem]** para **[resultado esperado]**."

**Exemplos:**
- "Nós vamos **persistir estado do cliente em JSON flat files** usando **sistema de arquivos do worker** para **evitar dependência de banco de dados externo e latência de rede**."
- "Nós vamos **separar geração de avaliação em dois agentes independentes** usando **o padrão Generator/Evaluator com comunicação via JSON state files** para **eliminar sycophancy e aumentar precisão de 75% para 98%**."

#### 5. Alternativas Consideradas

Esta seção é **prova de que você não decidiu por impulso**. Ela documenta que outras opções foram avaliadas racionalmente.

**Para cada alternativa, documente:**
- Nome e descrição breve
- Prós (por que consideramos)
- Contras (por que não escolhemos)
- Custo estimado (se relevante)
- Quem defendeu esta opção (opcional, para rastreabilidade)

**A alternativa escolhida também deve aparecer na tabela**, com justificativa de por que foi a melhor.

#### 6. Consequências

Esta seção é o **"contrato" da decisão**. Ela diz ao time o que esperar depois que a decisão for implementada.

**Use linguagem concreta, não aspiracional:**
- ❌ "O sistema ficará mais rápido"
- ✅ "Latência de resposta do agente deve cair de 12s para <200ms em 90% das consultas ao catálogo"

**Inclua consequências negativas honestamente:**
- ⚠️ "Cache pode servir dados stale por até 5 minutos — cliente pode ver preço desatualizado brevemente"
- ⚠️ "Complexidade adicional de manter dois agentes em vez de um — custo de manutenção sobe ~20%"

**Anti-padrão:** Listar apenas benefícios. Toda decisão arquitetural tem trade-offs.

---

## 📊 Quando Criar (e Quando NÃO Criar) um ADR

### Regra de Ouro

> **Crie um ADR quando a decisão afeta MAIS de uma pessoa e sua justificativa NÃO é óbvia lendo o código.**

Se alguém novo no time, lendo apenas o código, consegue entender POR QUE foi feito assim, provavelmente não precisa de ADR. Se a decisão envolveu trade-offs não visíveis no código, precisa.

### Matriz de Decisão

| Tipo de Decisão | Criar ADR? | Justificativa |
|---|---|---|
| Escolha de linguagem de programação | ✅ SIM | Afeta contratação, ferramental, ecossistema inteiro. Difícil reverter |
| Escolha de framework/biblioteca core | ✅ SIM | Afeta arquitetura, performance, manutenção de longo prazo |
| Padrão de arquitetura (ex: Generator/Evaluator) | ✅ SIM | Decisão estrutural que afeta todo o design do sistema |
| Estratégia de persistência (DB, arquivos, cache) | ✅ SIM | Afeta performance, confiabilidade, custo |
| Protocolo de comunicação entre serviços | ✅ SIM | Afeta latência, acoplamento, debugabilidade |
| Estrutura de diretórios do projeto | ⚠️ TALVEZ | Se for óbvia (convenção da linguagem), não. Se for não-óbvia, sim |
| Nome de variável ou função | ❌ NÃO | Code review resolve |
| Configuração de ESLint/Prettier | ❌ NÃO | Documente no README ou CONTRIBUTING.md |
| Escolha de cor ou espaçamento no CSS | ❌ NÃO | Design system documenta |
| Implementação de uma rota específica | ❌ NÃO | A própria rota + testes documentam |
| Bug fix ou melhoria incremental | ❌ NÃO | PR description + changelog bastam |

### Gatilhos Comuns para Criar um ADR

Você **provavelmente precisa de um ADR** quando ouvir frases como:

- "Temos duas abordagens possíveis, ambas parecem boas..."
- "Se escolhermos X, ganhamos A mas perdemos B..."
- "Isso vai afetar como outros módulos funcionam..."
- "Daqui a 6 meses, alguém vai olhar para este código e perguntar por que..."
- "O time está dividido entre duas soluções..."
- "É uma decisão difícil de reverter depois de implementada..."
- "Afeta segurança, performance, ou confiabilidade do sistema..."

### Quando NÃO Criar um ADR

- A decisão é trivial ou de senso comum
- A decisão pode ser facilmente revertida (ex: mudar uma flag de configuração)
- O código + testes + PR description já documentam suficientemente
- É uma decisão tática/operacional, não arquitetural
- O custo de documentar > benefício de documentar

---

## 💼 Exemplo Preenchido: ADR-002 — Generator/Evaluator no KODA

Abaixo está um ADR **real e completo** documentando uma das decisões arquiteturais mais impactantes do KODA. Use como referência para preencher seus próprios ADRs.

---

# ADR-002: Adotar padrão Generator/Evaluator para recomendações de produto

**Status:** ACCEPTED  
**Data:** 2026-03-15  
**Autor:** Fernando (tech lead)  
**Decisores:** Fernando, Carla (backend), Ricardo (ML), Juliana (produto)  
**Substitui:** Nenhum  
**Substituído por:** Nenhum

---

## Contexto

O KODA processa ~500 recomendações de produto por dia. A precisão atual é de **75%** — ou seja, 1 em cada 4 recomendações tem algum problema: produto fora de estoque, preço desatualizado, ou alergia do cliente ignorada.

O módulo de recomendação atual é um **agente único** que:
1. Recebe a pergunta do cliente
2. Busca produtos no catálogo
3. Gera uma recomendação
4. Auto-avalia se a recomendação é boa
5. Envia ao cliente

O problema está no passo 4. Quando o agente tenta avaliar seu próprio trabalho, ele sofre de **sycophancy** — viés confirmatório que o faz sempre aprovar sua própria resposta. Isso explica os 25% de erro.

**Forças em jogo:**

| Força | Direção | Peso |
|---|---|---|
| Precisão das recomendações | ↑ Aumentar (75% → 95%+) | CRÍTICO |
| Latência de resposta | ↔ Manter < 3 segundos | ALTO |
| Custo de API (tokens) | ↓ Manter ou reduzir | MÉDIO |
| Complexidade do código | ↔ Não explodir | MÉDIO |
| Tempo de implementação | ↔ Máximo 2 sprints | ALTO |
| Confiabilidade (menos devoluções) | ↑ Aumentar | CRÍTICO |

**Restrições:**
- Orçamento mensal de API: R$ 2.000
- Time de 3 engenheiros backend
- Não podemos trocar de modelo LLM (contrato com Anthropic até 2027)
- Stack atual: Node.js + TypeScript + Claude API

**Tentativa anterior:**
Em fevereiro, tentamos melhorar o prompt do agente único pedindo para ele "ser mais crítico". Resultado: precisão subiu de 75% para 78%. Insuficiente.

---

## Decisão

> **Nós vamos separar a geração de recomendação da avaliação usando o padrão Generator/Evaluator com dois agentes independentes comunicando-se via JSON state files, para eliminar o viés de auto-avaliação (sycophancy) e aumentar a precisão de 75% para 98%.**

**Como funciona:**

```
┌─────────────────────────────────────────────────────────┐
│                FLUXO GENERATOR/EVALUATOR                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  INPUT: Cliente pergunta + perfil + restrições           │
│      │                                                  │
│      ▼                                                  │
│  ┌──────────────────────────────────────┐               │
│  │ GENERATOR (Agente 1)                 │               │
│  │ • Temperature: 0.7 (criatividade)    │               │
│  │ • Gera 3-5 opções de produtos        │               │
│  │ • NÃO se auto-avalia                 │               │
│  │ • Output → generator_draft.json      │               │
│  └──────────────┬───────────────────────┘               │
│                 │                                       │
│                 ▼                                       │
│  ┌──────────────────────────────────────┐               │
│  │ EVALUATOR (Agente 2)                 │               │
│  │ • Temperature: 0.3 (rigor)           │               │
│  │ • Verifica contra rubrica rígida     │               │
│  │ • Checa: estoque real, lactose,      │               │
│  │   preço atual, alergias, budget      │               │
│  │ • Output → evaluator_verdict.json    │               │
│  └──────────────┬───────────────────────┘               │
│                 │                                       │
│         ┌───────┴───────┐                               │
│         │               │                               │
│    SCORE ≥ 7.0    SCORE < 7.0                           │
│         │               │                               │
│         ▼               ▼                               │
│    ✅ APROVA     ❌ REJEITA                              │
│    → Cliente     → Feedback.json                        │
│                  → Generator tenta de novo              │
│                  → Máx 3 iterações                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**State files (comunicação entre agentes):**

| Arquivo | Criado por | Lido por | Conteúdo |
|---|---|---|---|
| `customer_context.json` | Sistema (imutável) | Generator, Evaluator | Perfil, restrições, histórico |
| `generator_draft.json` | Generator | Evaluator | Recomendação candidata |
| `evaluator_verdict.json` | Evaluator | Sistema | Score + aprovação/rejeição |
| `feedback.json` | Evaluator (se rejeitado) | Generator | Issues específicas a corrigir |
| `audit_log.jsonl` | Sistema | Debugging/auditoria | Timeline de eventos |

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Por que rejeitada |
|---|---|---|---|
| **A: Melhorar prompt do agente único** | Zero mudança de arquitetura. Rápido (1 dia) | Melhoria marginal (+3%). Sycophancy persiste | Resultado insuficiente. Já tentamos (fevereiro, 75→78%) |
| **B: Fine-tuning do modelo** | Potencialmente mais preciso | Custo alto (~R$ 15.000). Tempo (4-6 semanas). Sem garantia. Dependência de dados de treino | Fora do orçamento e prazo. Risco alto |
| **C: Human-in-the-loop (revisão manual)** | 100% de precisão nas revisões | Não escala (500/dia). Custo operacional (R$ 8.000/mês). Latência (5-30 min) | Inviável para escala do KODA. Contraria visão de autonomia |
| **D: Generator/Evaluator (ESCOLHIDA)** | Precisão projetada 95%+. Sem sycophancy. Auditável. Escalável | Duas chamadas API por recomendação (custo 2x). Latência adicional (~1s). Complexidade extra | Melhor trade-off custo/precisão/escala |

---

## Consequências

### ✅ Ganhos

- **Precisão de recomendações:** 75% → 98% (projetado). Menos devoluções, menos reclamações
- **Auditabilidade:** Cada recomendação deixa rastro completo (draft → evaluation → verdict). Debugging passa de horas para minutos
- **Confiança do cliente:** Recomendações consideram alergias, preferências e histórico de forma verificável
- **Satisfação (NPS):** Projetado subir de 70 para 88
- **Taxa de devolução:** Projetado cair de 15% para 6%
- **Escalabilidade da precisão:** Quanto mais complexa a recomendação, MAIOR a vantagem do padrão sobre agente único

### ⚠️ Riscos e Trade-offs

- **Custo de API:** Sobe ~2x (duas chamadas em vez de uma). De R$ 400/mês para ~R$ 800/mês. Ainda dentro do orçamento (R$ 2.000)
- **Latência adicional:** +800ms a +1.2s por recomendação (chamada extra + I/O de arquivos). Tempo total ~2.5s — dentro do target de <3s
- **Complexidade de manutenção:** Dois agentes para manter, testar e debugar. Curva de aprendizado para novos engenheiros
- **Falha em cascata:** Se o Evaluator falhar, recomendação não é entregue. Precisa de fallback (após 3 iterações, escala para humano)
- **Consistência entre ambientes:** State files precisam ser sincronizados entre dev/staging/prod

### ℹ️ Mudanças Operacionais

- **Novo diretório:** `state/{customer_id}/` para state files. Precisa de política de limpeza (TTL 7 dias)
- **Monitoramento:** Adicionar métricas de latência do Evaluator, taxa de rejeição, número de iterações
- **Onboarding:** Todo novo engenheiro precisa ler este ADR + módulo de Generator/Evaluator no currículo
- **Code review:** PRs que alteram lógica de recomendação precisam incluir testes do Evaluator

---

## Notas e Referências

- Currículo relacionado: `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` — explica o padrão em profundidade com 5 casos de estudo KODA
- Case study relacionado: `curriculum/09-case-studies/koda-product-discovery.md` — dados reais do ganho de precisão com Generator/Evaluator
- Evidência de suporte: análise de 1000 recomendações pré e pós-adoção do padrão mostrou melhoria de 75% para 98% de precisão (documentado internamente)
- Impacto medido: taxa de devolução caiu de 15% para 6%, satisfação do cliente subiu de 70% para 88% (métricas do dashboard KODA, Q1 2026)

---

> **Fim do ADR-002.** Este documento não será editado. Se a decisão mudar, um novo ADR será criado com status `SUPERSEDED`.

---

### Checklist Aplicado ao ADR-002

| Critério | Status | Evidência |
|---|---|---|
| Título descritivo | ✅ | "Adotar padrão Generator/Evaluator para recomendações de produto" |
| Status claro | ✅ | ACCEPTED |
| Contexto explica o problema | ✅ | Detalha 25% de erro, sycophancy, tentativa anterior |
| Decisão é uma frase clara | ✅ | "Nós vamos separar geração de avaliação..." |
| Alternativas documentadas | ✅ | 4 alternativas com prós/contras/rejeição |
| Consequências positivas | ✅ | 5 ganhos mensuráveis |
| Consequências negativas | ✅ | 4 riscos honestamente documentados |
| Diagrama de arquitetura | ✅ | Fluxo Generator/Evaluator em ASCII |
| Forças/trade-offs explícitos | ✅ | Tabela de forças com pesos |
| Autocontido | ✅ | Não depende de links externos |

---

## ✅ Checklist de Completude do ADR

Use este checklist antes de submeter seu ADR para review. Um ADR só está pronto quando **todos os itens obrigatórios** estão marcados.

### Checklist Obrigatório (todos devem passar)

- [ ] **Título:** Descritivo, segue formato "ADR-NNN: Verbo + Objeto"
- [ ] **Status:** Um dos 5 status válidos (PROPOSED, ACCEPTED, REJECTED, DEPRECATED, SUPERSEDED)
- [ ] **Contexto:** Explica o problema E as forças em jogo (restrições, trade-offs)
- [ ] **Decisão:** Uma frase clara que alguém novo entende em 10 segundos
- [ ] **Alternativas:** Pelo menos 2 alternativas documentadas com prós/contras/razão de rejeição
- [ ] **Consequências positivas:** Lista concreta do que melhora (com métricas se possível)
- [ ] **Consequências negativas:** Lista honesta de trade-offs, riscos, e complexidade adicional
- [ ] **Eval Capability Impact:** Preenchido ou marcado como N/A quando a decisão toca prompt, model, tool, context, memory, rubric, evaluator ou agent-loop
- [ ] **Autocontido:** Alguém lendo daqui a 2 anos entende sem precisar de links externos
- [ ] **Linguagem neutra:** Não tem tom de "eu acho", "talvez", "provavelmente"
- [ ] **Decisores listados:** Quem aprovou (2+ pessoas para decisões significativas)
- [ ] **Numeração única:** Número não conflita com ADRs existentes

### Checklist de Qualidade (desejável)

- [ ] **Diagrama:** Decisões que envolvem fluxo de dados ou arquitetura têm diagrama ASCII
- [ ] **Métricas:** Consequências incluem números sempre que possível (ex: "latência de 12s para 200ms")
- [ ] **Referências:** Links para issues, PRs, discussões relevantes (opcional, na seção Notas)
- [ ] **Substituição:** Se este ADR substitui outro, o campo "Substitui" está preenchido
- [ ] **Tamanho:** 1-2 páginas (se precisa de mais, considere dividir em múltiplos ADRs ou criar uma spec)
- [ ] **Revisão cruzada:** Pelo menos 1 pessoa que NÃO participou da decisão leu e entendeu

### Anti-padrões (se marcou algum, revise)

- [ ] ADR tem mais de 3 páginas (provável que seja spec, não ADR)
- [ ] Contexto contém apenas 1-2 frases vagas ("precisávamos melhorar performance")
- [ ] Seção "Alternativas" está vazia ou contém apenas a opção escolhida
- [ ] Seção "Consequências" só lista benefícios (sem trade-offs negativos)
- [ ] Decisão usa linguagem vaga ("devemos considerar", "talvez implementar")
- [ ] ADR referencia "thread do Slack" ou "documento do Google Drive" sem resumir o conteúdo
- [ ] Decisão é auto-evidente lendo o código (provavelmente não precisava de ADR)

---

## 🔗 Relação com Outros Documentos do Projeto

ADRs não existem no vácuo. Eles fazem parte de um ecossistema de documentação.

### Documentos que ADRs Alimentam

```
ADR-001 (Persistência)      ADR-002 (Generator/Evaluator)
        │                            │
        └──────────┬─────────────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ SPECS TÉCNICAS      │
        │ (detalhes de impl)  │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ CÓDIGO + TESTES     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ README / GUIDES     │
        │ (onboarding)        │
        └─────────────────────┘
```

### Tabela de Decisão: Qual Documento Usar?

| Situação | Documento | Exemplo |
|---|---|---|
| Decisão arquitetural com trade-offs | **ADR** | "Usar JSON files em vez de PostgreSQL" |
| Como implementar algo específico | **Spec técnica** | "API de catálogo: endpoints, schemas, erros" |
| Como usar um módulo | **README** | "README do módulo de busca" |
| Processo ou convenção do time | **Guia / CONTRIBUTING** | "Guia de code review" |
| Análise de problema ou investigação | **Doc de análise** | "Análise de latência nas conversas de pico" |
| Lição aprendida com incidente | **Post-mortem** | "Incidente #42: Cache stale causou preço errado" |
| Avaliação de qualidade de output | **Rubric** | "Rubric de qualidade de recomendação" |
| Próxima capacidade de eval por dor observada | **ADR + eval gate** | "Adicionar corpus production-sampled porque score não prevê tickets" |
| Contrato entre módulos | **Sprint Contract** | "Contrato do módulo SEARCH → RANKING" |

### O Fluxo: De ADR a Código

1. **ADR criado** → Decisão arquitetural documentada
2. **Spec técnica** → Detalhamento de implementação (se necessário)
3. **Sprint Contracts** → Se a decisão afeta comunicação entre módulos
4. **Código + Testes** → Implementação
5. **Rubric** → Se a decisão afeta qualidade de output
6. **README atualizado** → Para onboarding de novos engenheiros

---

## 📁 Onde Armazenar ADRs

### Estrutura de Diretórios Recomendada

```
docs/
└── decisions/
    ├── README.md             # Índice de todos os ADRs
    ├── TEMPLATE.md           # Este template
    ├── adr-001-postgresql-state-persistence.md
    ├── adr-002-generator-evaluator-koda.md
    ├── adr-003-file-based-coordination.md
    └── ...
```

### README.md de Índice (exemplo)

```markdown
# Architecture Decision Records

Este diretório contém todas as decisões arquiteturais significativas do projeto.

| ADR | Título | Status | Data | Substituído por |
|-----|--------|--------|------|-----------------|
| 001 | Usar PostgreSQL para persistência de estado | ACCEPTED | 2026-01-10 | - |
| 002 | Adotar Generator/Evaluator para recomendações | ACCEPTED | 2026-03-15 | - |
| 003 | Implementar file-based coordination | PROPOSED | 2026-05-20 | - |

## Convenções

- ADRs são **imutáveis** após ACCEPTED
- Para mudar uma decisão, crie um NOVO ADR com status SUPERSEDED
- Use o template em `TEMPLATE.md`
```

---

## 🎓 O Que Você Aprendeu

### Conceitos Fundamentais

1. **ADR é o "porquê" documentado.** Código mostra o "como". ADR mostra "por que assim e não de outro jeito". Sem ADR, decisões se perdem no tempo.

2. **Imutabilidade é a feature mais importante.** Um ADR aceito nunca é editado — apenas substituído por um novo. Isso cria um histórico auditável de evolução arquitetural.

3. **Contexto é mais valioso que a decisão em si.** Daqui a 2 anos, saber O QUE foi decidido é fácil (está no código). Saber POR QUE — com restrições, alternativas, forças em jogo — é o ouro.

4. **Trade-offs devem ser documentados com honestidade.** Toda decisão arquitetural tem custos. Se seu ADR só lista benefícios, ele não é um ADR — é marketing.

5. **ADR é barato. Re-decidir é caro.** Escrever um ADR leva 30-60 minutos. Redescobrir uma decisão perdida leva horas. Reverter uma decisão mal documentada leva dias.

### Quando Usar Este Template

| Cenário | Ação |
|---|---|
| Começando um novo projeto | Crie ADRs para as 3-5 decisões arquiteturais iniciais (linguagem, DB, padrão de arquitetura) |
| Durante uma discussão de design | Use o template para estruturar a proposta (status: PROPOSED) |
| Fazendo onboarding de alguém | Apresente a pasta `docs/decisions/` como primeiro passo |
| Revisando um PR grande | Se o PR introduz um novo padrão, pergunte: "Isso precisa de um ADR?" |
| Planejando refatoração | Leia os ADRs existentes ANTES de refatorar |
| Herdando um sistema legado | Crie ADRs retrospectivos para documentar decisões implícitas |
| Encerrando um projeto | ADRs documentam o racional para o próximo time que herdar o código |

### O Anti-Padrão Mais Comum

> "Vou documentar essa decisão depois, quando o código estiver pronto."

Este é o erro #1. Depois que o código está pronto, o contexto da decisão já se perdeu. Você não lembra mais por que rejeitou a alternativa B. Você já se convenceu de que a decisão foi "óbvia".

**Escreva o ADR durante a decisão, não depois.** Use status `PROPOSED` como documento vivo de discussão. Após aprovação, mude para `ACCEPTED` e não edite mais.

---

## 🚀 Próximos Passos

1. **Copie o template base** (seção "🏗️ A Estrutura do ADR") para um novo arquivo em `docs/decisions/adr-NNN-seu-titulo.md`
2. **Preencha com sua decisão real** seguindo o checklist de completude
3. **Submeta para review** com pelo menos 2 engenheiros que NÃO participaram da decisão
4. **Atualize o README.md de índice** com o novo ADR
5. **Referencie o ADR** em specs, PRs, e documentos relacionados

---

## 📚 Referências

### Dentro deste Currículo
- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` — ADR-002 em ação
- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` — Outro exemplo de decisão arquitetural
- `curriculum/08-tools-templates/sprint-contract-template.md` — Complemento para contratos entre módulos

### Externo
- **ThoughtWorks Technology Radar** — ADRs como prática recomendada desde 2017
- **Michael Nygard, "Documenting Architecture Decisions"** (2011) — artigo que popularizou ADRs
- **Spotify Engineering Culture** — Uso de ADRs em times ágeis
- **ADR GitHub Organization** (adr.github.io) — Comunidade e ferramentas

---

## 📋 Metadata

| Campo | Valor |
|---|---|
| **Arquivo** | architecture-decision-record-template.md |
| **Nível** | Todos (template transversal) |
| **Tempo** | 60 minutos (leitura) / 30-60 minutos (preenchimento) |
| **Status** | ✅ Template completo |
| **Formato** | ADR (Architecture Decision Record) |
| **Linguagem** | Português (Brasil) com termos técnicos em inglês |
| **Atualizado** | Maio 2026 |

---

> *"In a world of agile and continuous delivery, architecture decisions are made continuously. Documenting them is not optional — it's the difference between a system that evolves with clarity and one that decays into mystery."*

*Escrito com foco em aplicabilidade prática imediata. Use este template hoje.*
