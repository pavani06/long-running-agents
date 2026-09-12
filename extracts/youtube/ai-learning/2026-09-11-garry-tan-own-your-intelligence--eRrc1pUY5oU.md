---
title: "Garry Tan: Own Your Intelligence"
type: "extract"
source: "youtube"
video_id: "eRrc1pUY5oU"
url: "https://www.youtube.com/watch?v=eRrc1pUY5oU"
channel: "Y Combinator"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-garry-tan-own-your-intelligence--eRrc1pUY5oU.txt]]"
tags: ["agents", "harness", "harness-engineering", "context-engineering", "context-management", "memory-architecture", "knowledge-management", "agent-tooling", "agent-fleets", "cross-session", "governanca", "stack-tooling", "process", "production"]
thesis: "AGI não chega como evento singular, mas difuso na forma de 'AGI pessoal' — um agente rodando na sua infraestrutura, alimentado por contexto/memória que você possui e por um harness de skill files em markdown — e a posse desse contexto e dessas habilidades determina se você compõe capital cognitivo ou tem sua cognição extraída por outros."
concepts: ["AGI pessoal (inteligência geral para uma pessoa, não para todos de uma vez)", "Conatus / poder de agir (Spinoza) como métrica de alegria e tristeza", "Skill files: markdown executável como código, com o modelo de linguagem como compilador", "Fat skills, thin harness", "Biblioteca + bibliotecário (memória pessoal curada de ~220k páginas markdown)", "Limite de memória de trabalho humana (7±2 itens) vs janela de contexto de ~1M tokens", "Divisão de computação: espaço latente (gosto, juízo) vs espaço determinístico (aritmética, SQL, scripts)", "Higiene de memória: proveniência por fato, checagem de contradições, poda pelo bibliotecário", "Skillify: converter trabalho one-off em skill reutilizável em vez de descartar contexto", "Posse de skill files: carreira que compõe vs extração de julgamento pelo empregador", "Custódia como modelo de segurança: infra própria, chaves próprias", "Contexto próprio como diferenciador quando pesos do modelo viram commodity", "Agente como força de trabalho: skill file como funcionário, resolver como organograma", "Compendium skill: deep research pessoal sobre fontes múltiplas com cronologia, discordâncias entre fontes e citações", "Software de audiência-de-um construído em um fim de semana"]
tools: ["OpenClaw", "Hermes Agent", "Claude Code", "Codex", "GBrain (gbrain.io)", "GStack", "Circle Back", "Bookface", "Postgres (mencionado como analogia)", "SQL (mencionado)"]
people: ["Baruch Spinoza", "Albert Einstein", "Vannevar Bush", "Marshall McLuhan", "Steve Jobs", "Paul Graham", "Gottfried Leibniz", "Y Combinator (YC)", "Nadler, Goldstein e Stewart (biógrafos de Spinoza)", "Emergent (batch YC S24)", "Retail (batch YC W24)", "Universidade de Heidelberg (oferta de cátedra a Spinoza, 1673)"]
claims: ["Equação da década: modelo de fronteira (alugado e commoditizado) + seu contexto (possuído e único) + um harness que os conecta = agente que age como uma versão muito rápida de você", "Regra de autoria de skill: se um estagiário inteligente conseguiria seguir a instrução escrita, um agente consegue executá-la", "Separe os espaços de computação: gosto e interpretação de pedidos vagos ficam no espaço latente dirigidos por markdown; aritmética, queries SQL e alocação em escala ficam em código determinístico chamado pelos arquivos markdown", "Plano de adoção em 5 passos: (1) rodar um harness na própria máquina hoje; (2) começar a biblioteca com uma pasta de markdown no fim de semana, uma página por projeto e por pessoa; (3) escrever o primeiro skill file para a tarefa semanal mais odiada; (4) agendar como job recorrente; (5) nunca fazer trabalho one-off — skillificar tudo ao final de cada tarefa", "Memória sem curadoria é lixeira com boa busca: exija proveniência em cada fato, sinalize contradições sem sobrescrever (flag, não override) e mantenha um bibliotecário cujo trabalho é podar", "Curva esperada de 90 dias: semana 1 é um brinquedo, semana 4 o flywheel engata, semana 12 a biblioteca responde antes de você terminar a pergunta", "Mantenha os skill files em um repo que você controla desde o dia 1, antes de qualquer plataforma ou adquirente ter opinião; caso contrário seu julgamento executa para sempre na empresa sem seu nome no histórico de commits", "Custódia é o modelo de segurança: consolidar o próprio contexto em infra e chaves próprias assume o risco em vez de criá-lo, em contraste com a vida espalhada por dez clouds de terceiros", "Modelos melhores aumentam o valor da sua biblioteca: quando todos têm o mesmo motor, a corrida é decidida pelo contexto que só você possui", "Retrieval é o primitivo, não o produto — o difícil é o que é escrito, enriquecido, promovido a hot memory vs cold reference e quem arbitra quando dois fatos colidem", "Números citados: ~400x de aumento de output pessoal desde 2013 (piso defendido de 8x); 25% do batch W25 com codebases 95% gerados por IA; Emergent com 9 dígitos de receita em 8 meses com ~15 pessoas; Retail com US$60M anualizados e ~40 pessoas", "A liberdade estratégica está em recusar o equivalente moderno dos mil florins: qualquer arranjo confortável em que seu julgamento compõe no repo de outra pessoa"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de insight arquitetural e acionável (skill files, fat skills/thin harness, divisão latente-determinístico, higiene de memória com proveniência e poda, loop de skillificação, plano de 5 passos) somada a um enquadramento relativamente novo de governança e posse cognitiva, com relevância direta a harness, context-engineering, memory-architecture e fleets de agentes."
---

# Garry Tan: Own Your Intelligence

## Tese
AGI não chega como evento singular, mas difuso na forma de 'AGI pessoal' — um agente rodando na sua infraestrutura, alimentado por contexto/memória que você possui e por um harness de skill files em markdown — e a posse desse contexto e dessas habilidades determina se você compõe capital cognitivo ou tem sua cognição extraída por outros.

## Conceitos-chave
- AGI pessoal (inteligência geral para uma pessoa, não para todos de uma vez)
- Conatus / poder de agir (Spinoza) como métrica de alegria e tristeza
- Skill files: markdown executável como código, com o modelo de linguagem como compilador
- Fat skills, thin harness
- Biblioteca + bibliotecário (memória pessoal curada de ~220k páginas markdown)
- Limite de memória de trabalho humana (7±2 itens) vs janela de contexto de ~1M tokens
- Divisão de computação: espaço latente (gosto, juízo) vs espaço determinístico (aritmética, SQL, scripts)
- Higiene de memória: proveniência por fato, checagem de contradições, poda pelo bibliotecário
- Skillify: converter trabalho one-off em skill reutilizável em vez de descartar contexto
- Posse de skill files: carreira que compõe vs extração de julgamento pelo empregador
- Custódia como modelo de segurança: infra própria, chaves próprias
- Contexto próprio como diferenciador quando pesos do modelo viram commodity
- Agente como força de trabalho: skill file como funcionário, resolver como organograma
- Compendium skill: deep research pessoal sobre fontes múltiplas com cronologia, discordâncias entre fontes e citações
- Software de audiência-de-um construído em um fim de semana

## Ferramentas & pessoas
**Ferramentas:** OpenClaw, Hermes Agent, Claude Code, Codex, GBrain (gbrain.io), GStack, Circle Back, Bookface, Postgres (mencionado como analogia), SQL (mencionado)

**Pessoas/orgs:** Baruch Spinoza, Albert Einstein, Vannevar Bush, Marshall McLuhan, Steve Jobs, Paul Graham, Gottfried Leibniz, Y Combinator (YC), Nadler, Goldstein e Stewart (biógrafos de Spinoza), Emergent (batch YC S24), Retail (batch YC W24), Universidade de Heidelberg (oferta de cátedra a Spinoza, 1673)

## Claims acionáveis
- Equação da década: modelo de fronteira (alugado e commoditizado) + seu contexto (possuído e único) + um harness que os conecta = agente que age como uma versão muito rápida de você
- Regra de autoria de skill: se um estagiário inteligente conseguiria seguir a instrução escrita, um agente consegue executá-la
- Separe os espaços de computação: gosto e interpretação de pedidos vagos ficam no espaço latente dirigidos por markdown; aritmética, queries SQL e alocação em escala ficam em código determinístico chamado pelos arquivos markdown
- Plano de adoção em 5 passos: (1) rodar um harness na própria máquina hoje; (2) começar a biblioteca com uma pasta de markdown no fim de semana, uma página por projeto e por pessoa; (3) escrever o primeiro skill file para a tarefa semanal mais odiada; (4) agendar como job recorrente; (5) nunca fazer trabalho one-off — skillificar tudo ao final de cada tarefa
- Memória sem curadoria é lixeira com boa busca: exija proveniência em cada fato, sinalize contradições sem sobrescrever (flag, não override) e mantenha um bibliotecário cujo trabalho é podar
- Curva esperada de 90 dias: semana 1 é um brinquedo, semana 4 o flywheel engata, semana 12 a biblioteca responde antes de você terminar a pergunta
- Mantenha os skill files em um repo que você controla desde o dia 1, antes de qualquer plataforma ou adquirente ter opinião; caso contrário seu julgamento executa para sempre na empresa sem seu nome no histórico de commits
- Custódia é o modelo de segurança: consolidar o próprio contexto em infra e chaves próprias assume o risco em vez de criá-lo, em contraste com a vida espalhada por dez clouds de terceiros
- Modelos melhores aumentam o valor da sua biblioteca: quando todos têm o mesmo motor, a corrida é decidida pelo contexto que só você possui
- Retrieval é o primitivo, não o produto — o difícil é o que é escrito, enriquecido, promovido a hot memory vs cold reference e quem arbitra quando dois fatos colidem
- Números citados: ~400x de aumento de output pessoal desde 2013 (piso defendido de 8x); 25% do batch W25 com codebases 95% gerados por IA; Emergent com 9 dígitos de receita em 8 meses com ~15 pessoas; Retail com US$60M anualizados e ~40 pessoas
- A liberdade estratégica está em recusar o equivalente moderno dos mil florins: qualquer arranjo confortável em que seu julgamento compõe no repo de outra pessoa

> **Deep dive:** `high` — Densidade alta de insight arquitetural e acionável (skill files, fat skills/thin harness, divisão latente-determinístico, higiene de memória com proveniência e poda, loop de skillificação, plano de 5 passos) somada a um enquadramento relativamente novo de governança e posse cognitiva, com relevância direta a harness, context-engineering, memory-architecture e fleets de agentes.
