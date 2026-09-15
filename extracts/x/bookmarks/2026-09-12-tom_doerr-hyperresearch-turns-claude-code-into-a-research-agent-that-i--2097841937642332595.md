---
title: "Agente de pesquisa profunda para Claude Code"
type: "extract"
source: "x"
status_id: "2097841937642332595"
handle: "tom_doerr"
url: "https://x.com/tom_doerr/status/2097841937642332595"
created_at: "2026-09-10T00:17:48.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-tom_doerr-hyperresearch-turns-claude-code-into-a-research-agent-that-i--2097841937642332595.json]]"
tags: ["agents", "multi-agent", "harness-engineering", "verification", "knowledge-management", "cross-session", "context-management", "gate-design", "memory-architecture", "evals", "model-selection"]
topic: "Agente de pesquisa profunda para Claude Code"
summary: "Hyperresearch transforma o Claude Code em agente de deep research com pipeline tier-adaptive de 16 passos, verificação de citações, críticos adversariais e vault persistente de fontes reutilizável entre sessões; lidera (internamente, validação externa pendente) o DeepResearch-Bench RACE. Vale salvar como referência de arquitetura de harness multi-agente com verificação e memória cross-session."
key_points: ["Pipeline de 16 passos com roteamento por tier: light (~30-40 min, 5 passos), full (~1.5-2.5 h, todos os passos + cite-check) e dissertation opt-in (4-8 h, 300-450 fontes, 25K-80K palavras em capítulos); 'gears' configuráveis em config.toml ajustam alvos de fontes, profundidade e modelos por agente.", "Verificação como gate rígido: cite-checker cético audita se cada fonte citada sustenta a frase correspondente (citações alucinadas e retratações não reconhecidas bloqueiam o ship); auditoria de independência agrupa cópias derivativas para que 5 reprints contem como 1 fonte.", "Padrão 'patch, never regenerate': 4 críticos adversariais atacam o rascunho em paralelo e o patcher é tool-locked em [Read, Edit] no allowlist do Claude Code — mecanicamente incapaz de reescrever o relatório; findings grandes demais escalam como problemas estruturais.", "Vault persistente markdown+SQLite: toda fonte lida fica indexada e buscável para sessões futuras (texto completo de paywalls via Unpaywall/Europe PMC/CORE, substituições divulgadas); 'markdown is truth, SQLite is cache' com índice reconstruível; runs crashados resumem do passo exato via manifest.", "Context engineering explícito: skill de entrada é um router fino que invoca um step skill por fase, carregando o procedimento só quando o passo roda (evita queda silenciosa de passos por 'context rot'); 8 fontes acadêmicas (OpenAlex, Crossref, CORE, DOAB, ClinicalTrials.gov, SEC EDGAR, FRED) via um cliente só, dedup por DOI/título."]
entities: ["Hyperresearch", "Claude Code", "DeepResearch-Bench", "OpenAlex", "Crossref", "CORE", "DOAB", "ClinicalTrials.gov", "SEC EDGAR", "FRED", "Unpaywall", "Europe PMC", "SQLite", "crawl4ai", "pymupdf", "Claude-in-Chrome", "Sonnet", "Opus", "Haiku", "@tom_doerr"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/jordan-gibbs/hyperresearch"]
media: ["https://pbs.twimg.com/media/HR0IIByWcAQqg6J.jpg"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-14-ryrenz-claude-code-alphaxiv-openresearch-openresearch-6-github-1000--2098577841944207463|OpenResearch: agente de pesquisa científica]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420|Arquitetura de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-also-see-our-open-source-reference-implementation-this-inclu--2095233747562180849|implementação de referência de agentes de comércio]]", "[[extracts/x/bookmarks/2026-09-12-0xdeliriumm-boris-cherny-lead-of-claude-code-at-anthropic-published-a-pi--2081050632727793775|pipeline de code review com agentes]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-read-the-full-announcement-https-t-co-cdudn3gvhd--2095233748719817153|Blueprint de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-polydao-claude-obsidian-loop-engineering-a-vault-that-runs-itself-th--2098288931620184216|Claude + Obsidian vault como estado do agente]]", "[[extracts/x/bookmarks/2026-09-12-milesdeutscher-this-is-the-one-github-repo-that-everyone-needs-to-save-the--2079048927593275868|Vault Obsidian de Claude Skills]]", "[[extracts/x/bookmarks/2026-09-12-svpino-i-ve-been-trying-codex-to-analyze-a-dataset-and-honestly-i-v--2098489252707541305|Codex para análise de dados]]", "[[extracts/x/bookmarks/2026-09-12-anthropicai-we-re-publishing-our-most-detailed-threat-intelligence-repor--2098097512544444447|Relatório de ameaças sobre misuse de Claude]]", "[[extracts/x/bookmarks/2026-09-12-askalphaxiv-introducing-deepseek-v4-1-flash-for-understanding-research-p--2098309348858704095|alphaXiv AI paper Q&A]]"]
theme: "Tooling e arquitetura de agentes"
---

# Agente de pesquisa profunda para Claude Code

**@tom_doerr** · [2097841937642332595](https://x.com/tom_doerr/status/2097841937642332595) · `tool`

## Resumo
Hyperresearch transforma o Claude Code em agente de deep research com pipeline tier-adaptive de 16 passos, verificação de citações, críticos adversariais e vault persistente de fontes reutilizável entre sessões; lidera (internamente, validação externa pendente) o DeepResearch-Bench RACE. Vale salvar como referência de arquitetura de harness multi-agente com verificação e memória cross-session.

## Pontos-chave
- Pipeline de 16 passos com roteamento por tier: light (~30-40 min, 5 passos), full (~1.5-2.5 h, todos os passos + cite-check) e dissertation opt-in (4-8 h, 300-450 fontes, 25K-80K palavras em capítulos); 'gears' configuráveis em config.toml ajustam alvos de fontes, profundidade e modelos por agente.
- Verificação como gate rígido: cite-checker cético audita se cada fonte citada sustenta a frase correspondente (citações alucinadas e retratações não reconhecidas bloqueiam o ship); auditoria de independência agrupa cópias derivativas para que 5 reprints contem como 1 fonte.
- Padrão 'patch, never regenerate': 4 críticos adversariais atacam o rascunho em paralelo e o patcher é tool-locked em [Read, Edit] no allowlist do Claude Code — mecanicamente incapaz de reescrever o relatório; findings grandes demais escalam como problemas estruturais.
- Vault persistente markdown+SQLite: toda fonte lida fica indexada e buscável para sessões futuras (texto completo de paywalls via Unpaywall/Europe PMC/CORE, substituições divulgadas); 'markdown is truth, SQLite is cache' com índice reconstruível; runs crashados resumem do passo exato via manifest.
- Context engineering explícito: skill de entrada é um router fino que invoca um step skill por fase, carregando o procedimento só quando o passo roda (evita queda silenciosa de passos por 'context rot'); 8 fontes acadêmicas (OpenAlex, Crossref, CORE, DOAB, ClinicalTrials.gov, SEC EDGAR, FRED) via um cliente só, dedup por DOI/título.

## Links
- https://github.com/jordan-gibbs/hyperresearch

## Entidades
Hyperresearch, Claude Code, DeepResearch-Bench, OpenAlex, Crossref, CORE, DOAB, ClinicalTrials.gov, SEC EDGAR, FRED, Unpaywall, Europe PMC, SQLite, crawl4ai, pymupdf, Claude-in-Chrome, Sonnet, Opus, Haiku, @tom_doerr

> **Revisit:** `high` · **fonte:** `article`
