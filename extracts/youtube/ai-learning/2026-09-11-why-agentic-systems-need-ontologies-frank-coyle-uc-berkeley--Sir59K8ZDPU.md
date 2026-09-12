---
title: "Why Agentic Systems Need Ontologies — Frank Coyle, UC Berkeley"
type: "extract"
source: "youtube"
video_id: "Sir59K8ZDPU"
url: "https://www.youtube.com/watch?v=Sir59K8ZDPU"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-agentic-systems-need-ontologies-frank-coyle-uc-berkeley--Sir59K8ZDPU.txt]]"
tags: ["ontologia", "agents", "agent-loop", "arquitetura", "knowledge-management", "verification", "error-handling", "gate-design", "harness", "analise"]
thesis: "Ontologias (grafos de conhecimento formalizados com RDFS/OWL) podem servir como guard rails determinísticos e validadores de saída para agentes LLM probabilísticos, materializando a convergência da IA neurosimbólica."
concepts: ["Agentes de IA como sistemas que percebem, decidem e agem", "Ontologia como 'especificação formal de uma conceitualização compartilhada' (Gruber, 1993)", "IA neurosimbólica: convergência de LLMs probabilísticos com representações simbólicas", "Grafos de conhecimento vs. bancos de dados relacionais (flexibilidade de schema)", "Construção de ontologias top-down (especialistas) vs. bottom-up (dados de uso/clientes)", "RDFS domain/range para inferência de novos fatos", "OWL: propriedades funcionais, transitivas e disjuntas como restrições", "Loop de agente e completude de Turing (sequência, condicional, iteração — Böhm e Jacopini, 1966)", "Agent loop: tool use, stop reason e execução de ferramentas", "Validação de saídas de LLM via raciocinador ontológico", "Efeitos colaterais (side effects) em agentes e execução diferida", "Riscos de loops: iteração infinita, drift entre agentes e custo de tokens"]
tools: ["Claude (agente)", "Python", "Pydantic", "schema.org", "FOAF (Friend of a Friend)", "Dublin Core", "DBpedia / Wikipedia", "RDFS", "OWL (Web Ontology Language)", "Bancos de dados em grafo", "GPUs Nvidia"]
people: ["Frank Coyle", "UC Berkeley", "Sister Corita Kent", "John Cage", "John McCarthy", "Selfridge", "Marvin Minsky", "Aristóteles", "Willard van Orman Quine", "Thomas Gruber", "Böhm e Jacopini", "Alan Turing", "John Coltrane"]
claims: ["Use Pydantic para validar tipos na entrada da ferramenta e a ontologia para validar resultados — 'paid at the door, ontology at the ledger'", "Um raciocinador ontológico (RDFS/OWL) pode checar se a resposta do LLM é razoável antes de prosseguir, voltar ao LLM ou escalar para humano", "Agentes devem evitar efeitos colaterais (ex.: escrever em banco de dados) até que a saída passe pela validação ontológica", "Aproveite taxonomias existentes (schema.org, FOAF, Dublin Core, DBpedia) em vez de construir a ontologia do zero", "Propriedades disjuntas em OWL capturam erros de categoria, ex.: pagamento enviado ao suporte em vez do comprador", "Propriedades funcionais em OWL impõem unicidade e detectam duplicatas, ex.: segundo reembolso sobre o mesmo pedido", "Restrições de valor (enum: paid/shipped/refunded) capturam valores alucinados pelo LLM como 'probably shipped'", "RDFS domain/range permite inferir fatos implícitos: 'Bob teaches Scooter' + domain teacher/range student ⇒ Bob é professor e Scooter é aluno", "Loops completam a tríade de Turing (sequência, condicional, iteração) tornando agentes computacionalmente universais, mas sujeitos a loops infinitos, drift e custo crescente de tokens", "Grafos permitem anexar entidades, propriedades e relações sem reestruturar colunas como em bancos relacionais", "Hallucination é uma característica inerente (probabilística) dos LLMs, e a camada simbólica serve para contê-la, não eliminá-la"]
deep_dive: "medium"
deep_dive_reason: "Apresenta um padrão arquitetural acionável e relevante (ontologia como gate de validação no agent loop, combinada a Pydantic e execução sem side effects), mas o conteúdo é majoritariamente introdutório e histórico, com exemplos simplificados e baixa densidade técnica."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ontology-in-ai-the-hidden-skill-that-makes-architecture-and-your-career-work--J0hj0ms2ddo|Ontology in AI: The Hidden Skill That Makes Architecture and Your Career Work]]", "[[extracts/youtube/ai-learning/2026-09-11-ontology-vs-graph-db-why-use-them-together-talkit-global-191-infasis-pwc-consult--U_YyqxUBNiQ|Ontology vs. Graph DB: Why Use Them Together? [TalkIT Global 191, Infasis, PwC Consulting]]]", "[[extracts/youtube/ai-learning/2026-09-11-context-graphs-for-explainable-decision-aware-ai-agents-andreas-kollegger-zaid-z--abvQEhvRI_c|Context Graphs for Explainable, Decision-Aware AI Agents — Andreas Kollegger & Zaid Zaim, Neo4j]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-enterprise-tech-stack-isnt-ready-for-ai-agents-christopher-lovejoy-saul--mav15aW9lLM|Why Your Enterprise Tech Stack Isn’t Ready for AI Agents — Christopher Lovejoy & Saul Howard]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-agents-need-decision-traces-not-just-documents-zach-blumenfeld-neo4j--B9h9ovW5H9U|Why your agents need decision traces, not just documents — Zach Blumenfeld, Neo4j]]"]
theme: "Arquiteturas de Deep Agents"
---

# Why Agentic Systems Need Ontologies — Frank Coyle, UC Berkeley

## Tese
Ontologias (grafos de conhecimento formalizados com RDFS/OWL) podem servir como guard rails determinísticos e validadores de saída para agentes LLM probabilísticos, materializando a convergência da IA neurosimbólica.

## Conceitos-chave
- Agentes de IA como sistemas que percebem, decidem e agem
- Ontologia como 'especificação formal de uma conceitualização compartilhada' (Gruber, 1993)
- IA neurosimbólica: convergência de LLMs probabilísticos com representações simbólicas
- Grafos de conhecimento vs. bancos de dados relacionais (flexibilidade de schema)
- Construção de ontologias top-down (especialistas) vs. bottom-up (dados de uso/clientes)
- RDFS domain/range para inferência de novos fatos
- OWL: propriedades funcionais, transitivas e disjuntas como restrições
- Loop de agente e completude de Turing (sequência, condicional, iteração — Böhm e Jacopini, 1966)
- Agent loop: tool use, stop reason e execução de ferramentas
- Validação de saídas de LLM via raciocinador ontológico
- Efeitos colaterais (side effects) em agentes e execução diferida
- Riscos de loops: iteração infinita, drift entre agentes e custo de tokens

## Ferramentas & pessoas
**Ferramentas:** Claude (agente), Python, Pydantic, schema.org, FOAF (Friend of a Friend), Dublin Core, DBpedia / Wikipedia, RDFS, OWL (Web Ontology Language), Bancos de dados em grafo, GPUs Nvidia

**Pessoas/orgs:** Frank Coyle, UC Berkeley, Sister Corita Kent, John Cage, John McCarthy, Selfridge, Marvin Minsky, Aristóteles, Willard van Orman Quine, Thomas Gruber, Böhm e Jacopini, Alan Turing, John Coltrane

## Claims acionáveis
- Use Pydantic para validar tipos na entrada da ferramenta e a ontologia para validar resultados — 'paid at the door, ontology at the ledger'
- Um raciocinador ontológico (RDFS/OWL) pode checar se a resposta do LLM é razoável antes de prosseguir, voltar ao LLM ou escalar para humano
- Agentes devem evitar efeitos colaterais (ex.: escrever em banco de dados) até que a saída passe pela validação ontológica
- Aproveite taxonomias existentes (schema.org, FOAF, Dublin Core, DBpedia) em vez de construir a ontologia do zero
- Propriedades disjuntas em OWL capturam erros de categoria, ex.: pagamento enviado ao suporte em vez do comprador
- Propriedades funcionais em OWL impõem unicidade e detectam duplicatas, ex.: segundo reembolso sobre o mesmo pedido
- Restrições de valor (enum: paid/shipped/refunded) capturam valores alucinados pelo LLM como 'probably shipped'
- RDFS domain/range permite inferir fatos implícitos: 'Bob teaches Scooter' + domain teacher/range student ⇒ Bob é professor e Scooter é aluno
- Loops completam a tríade de Turing (sequência, condicional, iteração) tornando agentes computacionalmente universais, mas sujeitos a loops infinitos, drift e custo crescente de tokens
- Grafos permitem anexar entidades, propriedades e relações sem reestruturar colunas como em bancos relacionais
- Hallucination é uma característica inerente (probabilística) dos LLMs, e a camada simbólica serve para contê-la, não eliminá-la

> **Deep dive:** `medium` — Apresenta um padrão arquitetural acionável e relevante (ontologia como gate de validação no agent loop, combinada a Pydantic e execução sem side effects), mas o conteúdo é majoritariamente introdutório e histórico, com exemplos simplificados e baixa densidade técnica.
