---
title: "Why AI is going vertical (again) | Dianne Penn (Anthropic)"
type: "extract"
source: "youtube"
video_id: "tivaWTTVRhY"
url: "https://www.youtube.com/watch?v=tivaWTTVRhY"
channel: "Lenny's Podcast"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-ai-is-going-vertical-again-dianne-penn-anthropic--tivaWTTVRhY.txt]]"
tags: ["evals", "agent-tooling", "agentic-coding", "token-budgeting", "decision-discipline", "process", "roadmap", "harness", "model-selection", "error-handling"]
thesis: "Na Anthropic, o product management de IA migrou de PRDs e pixels para evals e leitura de tokens/transcripts como forma primária de capturar dor de usuário e dirigi-la ao treinamento de modelos, sob a tese de que 'produtos frontier são necessários para que modelos frontier sejam sentidos' (caso Opus 4.5 + Claude Code)."
concepts: ["evals são os novos PRDs", "suar os tokens tanto quanto os pixels (ler transcripts de falha)", "taxonomia de falhas: erro de tool use vs. busca/síntese de conhecimento vs. alinhamento", "construção de eval sets a partir de feedback de usuário (30–40 exemplos iniciais, checar distribuição e contra-exemplos)", "capacidades emergentes descontínuas nas scaling laws", "product overhang e user overhang", "forward compatibility: 'e se o Claude 8 chegasse amanhã?'", "frontier models precisam de frontier products (modelo + veículo)", "labs como apostas descontínuas: convicção forte no tema, flexível no protótipo", "retomar teses falhas após 1–2 gerações de modelo", "experimentação comunal / trabalhar em público internamente", "fallback UX e model safeguards package", "token maxing como input; experimentação como outcome", "first principles thinking em vez de pattern matching para PMs", "PMs e gestores devem fazer shipping hands-on para manter theory of mind"]
tools: ["Claude", "Claude Code", "Opus 3", "Opus 4.5", "Opus 4", "Opus 5.5", "Fable / Mythos", "MCP", "Skills", "Claude Design", "claude.ai", "Golden Gate Claude", "GPT-4", "Codex / app Codeex (OpenAI)", "Slack"]
people: ["Diane Penn", "Lenny (host)", "Gary Tan", "Dario Amodei", "Ben Mann", "Mike Krieger", "Andrew (OpenAI, Codeex)", "Anthropic", "OpenAI", "Y Combinator"]
claims: ["Substitua o PRD por evals quando o problema é definido: derive o eval de feedback real consentido, verifique se reproduz a dor consistentemente e se a distribuição inclui casos em que o modelo NÃO deve falhar", "Comece eval sets pequenos (30–40 exemplos prompt+resposta com golden answer) e expanda a partir daí — assim foi resolvido o problema de schema/JSON do Claude 2, que respondia por ~80% do feedback 'não segue instruções'", "Leia transcripts completos e classifique a trajetória de falha (tool use, busca/síntese, alinhamento) antes de levar feedback a pesquisadores — 'fixe a alucinação' não é acionável", "Sue os tokens tanto quanto os pixels: a dor do usuário está na trajetória de tokens, não só na UI", "Projete para forward compatibility: pergunte 'o que muda no comportamento do usuário quando o próximo modelo chegar?' e ajuste o que constrói hoje", "Trate gasto de tokens como input e experimentação como métrica de outcome, não como fim em si", "Experimente em público dentro da organização (canais compartilhados): variações sobre ideias alheias geram casos de uso emergentes em ~10 requests", "Em labs/incubação, mantenha convicção forte no tema e fraca no protótipo; desligue apostas que não funcionam e reavalie-as 1–2 gerações de modelo depois", "Equipes pequenas e autodirigidas superam times grandes em apostas ambíguas de zero-para-um", "Construa fallback UX (ex.: degradação para Opus 4) como parte do pacote de safeguards para manter experiência em modelos mais restritos", "PRDs seguem úteis em dois casos: alinhar grupos grandes em fonte de verdade única por release de modelo, e explorar apostas ambíguas pré-produto (ex.: computer use)", "Gestores e PMs seniores de IA devem reservar tempo para shipping hands-on end-to-end; sem isso não conseguem avaliar o que é um bom produto de IA", "Aposte em diferenciação por treinamento focado em casos de uso subexplorados (ex.: código long-form no Opus 3) — mudanças pequenas de training podem gerar vantagem competitiva grande"]
deep_dive: "medium"
deep_dive_reason: "Contém prática acionável densa sobre evals-como-PRDs, taxonomia de falhas e fallback UX com relevância direta a evals e harness, mas é diluída por narrativa histórica da Anthropic e leituras promocionais de patrocinadores, sem novidade arquitetural profunda."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-openais-cpo-on-how-ai-changes-must-have-skills-moats-coding-startup-playbooks-mo--scsW6_2SPC4|OpenAI’s CPO on how AI changes must-have skills, moats, coding, startup playbooks, more | Kevin Weil]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-cpo-mike-krieger-building-ai-products-from-the-bottom-up--Js1gU6L1Zi8|Anthropic CPO Mike Krieger: Building AI Products From the Bottom Up]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-nikhyl-singhal-from-skip-on-product-management-i--BQrJ4lHAjhc|Stanford CS153 Frontier Systems | Nikhyl Singhal from Skip on Product Management in the AI Era]]", "[[extracts/youtube/ai-learning/2026-09-11-o-treinamento-secreto-da-ia-que-vai-mudar-tudo-vetto-ai--Z4BXg02i8sI|O treinamento secreto da IA que vai mudar tudo | Vetto AI]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s|Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-the-ai-product-going-viral-with-doctors-openevidence-with-ceo-daniel-nadler--huR0Oa2odxA|The AI Product Going Viral With Doctors: OpenEvidence, with CEO Daniel Nadler]]"]
---

# Why AI is going vertical (again) | Dianne Penn (Anthropic)

## Tese
Na Anthropic, o product management de IA migrou de PRDs e pixels para evals e leitura de tokens/transcripts como forma primária de capturar dor de usuário e dirigi-la ao treinamento de modelos, sob a tese de que 'produtos frontier são necessários para que modelos frontier sejam sentidos' (caso Opus 4.5 + Claude Code).

## Conceitos-chave
- evals são os novos PRDs
- suar os tokens tanto quanto os pixels (ler transcripts de falha)
- taxonomia de falhas: erro de tool use vs. busca/síntese de conhecimento vs. alinhamento
- construção de eval sets a partir de feedback de usuário (30–40 exemplos iniciais, checar distribuição e contra-exemplos)
- capacidades emergentes descontínuas nas scaling laws
- product overhang e user overhang
- forward compatibility: 'e se o Claude 8 chegasse amanhã?'
- frontier models precisam de frontier products (modelo + veículo)
- labs como apostas descontínuas: convicção forte no tema, flexível no protótipo
- retomar teses falhas após 1–2 gerações de modelo
- experimentação comunal / trabalhar em público internamente
- fallback UX e model safeguards package
- token maxing como input; experimentação como outcome
- first principles thinking em vez de pattern matching para PMs
- PMs e gestores devem fazer shipping hands-on para manter theory of mind

## Ferramentas & pessoas
**Ferramentas:** Claude, Claude Code, Opus 3, Opus 4.5, Opus 4, Opus 5.5, Fable / Mythos, MCP, Skills, Claude Design, claude.ai, Golden Gate Claude, GPT-4, Codex / app Codeex (OpenAI), Slack

**Pessoas/orgs:** Diane Penn, Lenny (host), Gary Tan, Dario Amodei, Ben Mann, Mike Krieger, Andrew (OpenAI, Codeex), Anthropic, OpenAI, Y Combinator

## Claims acionáveis
- Substitua o PRD por evals quando o problema é definido: derive o eval de feedback real consentido, verifique se reproduz a dor consistentemente e se a distribuição inclui casos em que o modelo NÃO deve falhar
- Comece eval sets pequenos (30–40 exemplos prompt+resposta com golden answer) e expanda a partir daí — assim foi resolvido o problema de schema/JSON do Claude 2, que respondia por ~80% do feedback 'não segue instruções'
- Leia transcripts completos e classifique a trajetória de falha (tool use, busca/síntese, alinhamento) antes de levar feedback a pesquisadores — 'fixe a alucinação' não é acionável
- Sue os tokens tanto quanto os pixels: a dor do usuário está na trajetória de tokens, não só na UI
- Projete para forward compatibility: pergunte 'o que muda no comportamento do usuário quando o próximo modelo chegar?' e ajuste o que constrói hoje
- Trate gasto de tokens como input e experimentação como métrica de outcome, não como fim em si
- Experimente em público dentro da organização (canais compartilhados): variações sobre ideias alheias geram casos de uso emergentes em ~10 requests
- Em labs/incubação, mantenha convicção forte no tema e fraca no protótipo; desligue apostas que não funcionam e reavalie-as 1–2 gerações de modelo depois
- Equipes pequenas e autodirigidas superam times grandes em apostas ambíguas de zero-para-um
- Construa fallback UX (ex.: degradação para Opus 4) como parte do pacote de safeguards para manter experiência em modelos mais restritos
- PRDs seguem úteis em dois casos: alinhar grupos grandes em fonte de verdade única por release de modelo, e explorar apostas ambíguas pré-produto (ex.: computer use)
- Gestores e PMs seniores de IA devem reservar tempo para shipping hands-on end-to-end; sem isso não conseguem avaliar o que é um bom produto de IA
- Aposte em diferenciação por treinamento focado em casos de uso subexplorados (ex.: código long-form no Opus 3) — mudanças pequenas de training podem gerar vantagem competitiva grande

> **Deep dive:** `medium` — Contém prática acionável densa sobre evals-como-PRDs, taxonomia de falhas e fallback UX com relevância direta a evals e harness, mas é diluída por narrativa histórica da Anthropic e leituras promocionais de patrocinadores, sem novidade arquitetural profunda.
