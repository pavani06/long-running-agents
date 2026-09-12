---
title: "Beyond the Prompt: \"Goodbye slop; welcome determinism\" David Khourshid"
type: "extract"
source: "youtube"
video_id: "uMvTAF280so"
url: "https://www.youtube.com/watch?v=uMvTAF280so"
channel: "AG Grid"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-beyond-the-prompt-goodbye-slop-welcome-determinism-david-khourshid--uMvTAF280so.txt]]"
tags: ["agents", "agentic-coding", "agent-loop", "arquitetura", "state", "spec-driven-development", "frameworks", "process", "decision-discipline", "gate-design", "context-engineering", "production"]
thesis: "Aplicações com IA devem inverter o padrão de 'LLMs que chamam programas' para 'programas determinísticos que chamam LLMs', mantendo um núcleo lógico explícito e estruturado (modelável p.ex. com máquinas de estados) e confinando a não-determinismo às bordas, eliminando o 'slop' gerado pela delegação não estruturada."
concepts: ["determinismo vs. não-determinismo", "DFAs vs. NFAs (autômatos finitos determinísticos e não-determinísticos)", "explosão de estados e transições", "statecharts / máquinas de estados", "delegação não estruturada (unstructured delegation)", "slop code (código sem modelo confiável)", "modelo explícito como fonte de verdade (intenção + execução)", "markdown vs. código como fonte de verdade ruidosa", "given-when-then (estados, eventos, transições)", "deterministic core / agentic shell", "functional core, imperative shell", "oneshotting como anti-padrão", "controle de fluxo em prosa (skills/prompts)", "agentes como sistema / multi-agentes sem restrição", "emaranhado de concerns vs. separação de concerns", "slop composto por suposições erradas amplificadas", "janelas de contexto maiores não geram mais estrutura", "metáfora da planta baixa (blueprint) para o codebase", "iteração com humano no loop", "domain-driven design e modelagem de dados"]
tools: ["XState", "XState v6", "XState Store v4", "Stately.ai (editor Stately)", "visualizador de máquinas de estados stately.scetch.ai", "TanStack", "Claude", "Codex", "Cursor", "CLAUDE.md", "AGENTS.md", "Skills", "React (useState)", "Gherkin/Cucumber", "Bun (mencionado na piada da PR em Rust)"]
people: ["David Khourshid (David Kpiano)", "Stately.ai", "Ken Wheeler", "Gary Bernhardt (transcrito como 'Carrie Bernard')", "Matt (palestrante posterior, transcrito como 'Matt PCO')", "TanStack"]
claims: ["Inverta a arquitetura: escreva programas determinísticos que chamam LLMs nas bordas, em vez de deixar o LLM orquestrar todo o fluxo.", "Escolha um fluxo confuso de uma aplicação existente e modele-o explicitamente (estados, eventos, transições) antes de delegar ao agente.", "Não represente controle de fluxo em linguagem natural (skills, prompts, planos em markdown); codifique-o em um modelo formal verificável.", "Use invariantes da máquina de estados para tornar impossíveis ações fora de ordem — ex.: impossível enviar um e-mail sem draft aprovado, ou redigir sem requisitos satisfeitos.", "Ao modelar, pergunte: o que pode ser determinístico, onde a iteração com humano no loop agrega valor, e onde a lógica pode ser separada da UI.", "Mais contexto não significa mais estrutura; encher o contexto de instruções obrigatórias só adiciona ruído e degrada desempenho.", "Modele apenas as partes confusas do sistema — modelagem substitui confusão, não é cerimônia — e comece com modelos grosseiros refinando por iteração.", "Mantenha separação de concerns explícita: agentes seguem os padrões já existentes no codebase, então suposições erradas são amplificadas se não houver estrutura.", "LLMs foram treinados em todo o código (não só no bom), então forneça um modelo explícito como entendimento compartilhado entre humano, time e agentes.", "Refine iterando sobre o modelo (artefato limpo) e referencie-o no código, em vez de fazer o agente iterar diretamente no código ruidoso."]
deep_dive: "medium"
deep_dive_reason: "A palestra oferece uma diretriz arquitetural clara e acionável (núcleo determinístico com LLMs nas bordas via modelos explícitos), mas é introdutória e parcialmente promocional do ecossistema Stately/XState, sem aprofundar tecnicamente em harness, evals ou implementação."
---

# Beyond the Prompt: "Goodbye slop; welcome determinism" David Khourshid

## Tese
Aplicações com IA devem inverter o padrão de 'LLMs que chamam programas' para 'programas determinísticos que chamam LLMs', mantendo um núcleo lógico explícito e estruturado (modelável p.ex. com máquinas de estados) e confinando a não-determinismo às bordas, eliminando o 'slop' gerado pela delegação não estruturada.

## Conceitos-chave
- determinismo vs. não-determinismo
- DFAs vs. NFAs (autômatos finitos determinísticos e não-determinísticos)
- explosão de estados e transições
- statecharts / máquinas de estados
- delegação não estruturada (unstructured delegation)
- slop code (código sem modelo confiável)
- modelo explícito como fonte de verdade (intenção + execução)
- markdown vs. código como fonte de verdade ruidosa
- given-when-then (estados, eventos, transições)
- deterministic core / agentic shell
- functional core, imperative shell
- oneshotting como anti-padrão
- controle de fluxo em prosa (skills/prompts)
- agentes como sistema / multi-agentes sem restrição
- emaranhado de concerns vs. separação de concerns
- slop composto por suposições erradas amplificadas
- janelas de contexto maiores não geram mais estrutura
- metáfora da planta baixa (blueprint) para o codebase
- iteração com humano no loop
- domain-driven design e modelagem de dados

## Ferramentas & pessoas
**Ferramentas:** XState, XState v6, XState Store v4, Stately.ai (editor Stately), visualizador de máquinas de estados stately.scetch.ai, TanStack, Claude, Codex, Cursor, CLAUDE.md, AGENTS.md, Skills, React (useState), Gherkin/Cucumber, Bun (mencionado na piada da PR em Rust)

**Pessoas/orgs:** David Khourshid (David Kpiano), Stately.ai, Ken Wheeler, Gary Bernhardt (transcrito como 'Carrie Bernard'), Matt (palestrante posterior, transcrito como 'Matt PCO'), TanStack

## Claims acionáveis
- Inverta a arquitetura: escreva programas determinísticos que chamam LLMs nas bordas, em vez de deixar o LLM orquestrar todo o fluxo.
- Escolha um fluxo confuso de uma aplicação existente e modele-o explicitamente (estados, eventos, transições) antes de delegar ao agente.
- Não represente controle de fluxo em linguagem natural (skills, prompts, planos em markdown); codifique-o em um modelo formal verificável.
- Use invariantes da máquina de estados para tornar impossíveis ações fora de ordem — ex.: impossível enviar um e-mail sem draft aprovado, ou redigir sem requisitos satisfeitos.
- Ao modelar, pergunte: o que pode ser determinístico, onde a iteração com humano no loop agrega valor, e onde a lógica pode ser separada da UI.
- Mais contexto não significa mais estrutura; encher o contexto de instruções obrigatórias só adiciona ruído e degrada desempenho.
- Modele apenas as partes confusas do sistema — modelagem substitui confusão, não é cerimônia — e comece com modelos grosseiros refinando por iteração.
- Mantenha separação de concerns explícita: agentes seguem os padrões já existentes no codebase, então suposições erradas são amplificadas se não houver estrutura.
- LLMs foram treinados em todo o código (não só no bom), então forneça um modelo explícito como entendimento compartilhado entre humano, time e agentes.
- Refine iterando sobre o modelo (artefato limpo) e referencie-o no código, em vez de fazer o agente iterar diretamente no código ruidoso.

> **Deep dive:** `medium` — A palestra oferece uma diretriz arquitetural clara e acionável (núcleo determinístico com LLMs nas bordas via modelos explícitos), mas é introdutória e parcialmente promocional do ecossistema Stately/XState, sem aprofundar tecnicamente em harness, evals ou implementação.
