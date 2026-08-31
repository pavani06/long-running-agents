---
title: "Centralized Data Plane with Inherited RBAC"
type: canonical
tags: ["agentes-orquestracao", "governanca", "production"]
Status: Active
Source: "AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 5-6 conexões MCP)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-30
aliases: ["inherited rbac", "unified data plane", "zero-code agent deployment", "platform-level rbac"]
relates-to:
  - "[[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]]"
  - "[[docs/canonical/regulated-data-boundary|Regulated Data Boundary]]"
  - "[[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]]"
  - "[[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|GTM AI Agents Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification|GTM AI Agents Classification]]"
---

# Centralized Data Plane with Inherited RBAC

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Sait Izmit, Snowflake (GTM assistant: 6.000 usuários, 5-6 conexões MCP, deployment zero-code)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Dados first-party e third-party (Salesforce, transcripts de calls) silados em ferramentas SaaS tornam a governança de acesso de dados por agente **inviável por integração** (`docs/analysis/...-patterns.md:183-186`). Cada conector novo traz seu próprio modelo de autenticação; com N fontes e M agentes, o controle de acesso vira N×M decisões manuais — cada agente nova é um projeto de segurança do zero.

A forma de falha concreta: um time quer spawnar um agente para um novo workflow. Antes de qualquer valor, ele decide como este agente autentica em cada fonte, quais linhas/colunas pode ver, e como isso fica auditável. O gargalo de engenharia mata agentes na origem; ou pior — o agente nasce com acesso genérico demais porque per-agente estava caro demais.

## Solução

Uma arquitetura de **consolidação e herança**: governança definida uma vez no data plane e herdada automaticamente por todo agente deployado sobre ele (`docs/analysis/...-patterns.md:186-212`).

| Componente | Função |
|---|---|
| Plataforma unificada de dados | Consolida first-party + third-party em um único plano |
| Camada RBAC no plano | Controles de acesso baseados em papel definidos **uma vez**, no nível da plataforma |
| Superfície de deployment zero-code | Agentes spawnados sem código sobre o plano |
| Guardrails e curadoria de plataforma | UI de chat out-of-the-box, guardrails e curadoria para cada agente deployado |

Fluxo (`docs/analysis/...-patterns.md:207-212`): consolidar dados first/third-party em uma plataforma → definir RBAC no nível da plataforma → deployar agentes com zero código → agentes herdam controles de acesso automaticamente → governar e curar centralizadamente.

Propriedades resultantes (`docs/analysis/...-patterns.md:193-197`): governança definida uma vez e herdada por toda a frota; nenhum código de autenticação por agente; postura de segurança consistente na frota; zero-code remove o gargalo de engenharia para spawnar agentes novos.

## Implementação neste repositório

### O que já existe

Governança de dados de agente existe em três docs canônicas — cada uma cobrindo um mecanismo isolado (classification:148-182):

- **Acesso keyed por identidade:** [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] — "An auth-coupled memory architecture where memory storage, retrieval, and sensitivity gating are all keyed by identity" (`docs/canonical/auth-coupled-memory-architecture.md:32`); "Identity resolution as memory key: Every memory item is stored with an identity key" (`:36`) — confiança de identidade com tiers de sensibilidade.
- **Isolamento estrutural:** [[docs/canonical/regulated-data-boundary|Regulated Data Boundary]] — "A regulated data boundary is an architectural isolation pattern: a separate infrastructure tier handling regulated operations that is physically isolated from LLM compute" (`docs/canonical/regulated-data-boundary.md:32`).
- **Tagging de PII no catálogo:** [[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]] — "Agents access enterprise data catalogs containing PII (SSN, phone, address, credit card numbers, customer names) but the model has no awareness of which fields are sensitive" (`docs/canonical/governance-context-injection-pii-prevention.md:22`).
- **Adjacência no nível análise:** a camada no-code e compilação determinística como mudança de persona (`docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-analysis.md:186`).

### O que falta

(classification:172-182) — busca da classificação: `RBAC|role-based|data plane|zero-code` em `docs/canonical/` — matches apenas no pacote-fonte GTM, em aliases de documentação role-based (`persona-based-documentation.md:5`, não equivalente) e na análise simpler-than-you-think; `MCP` — zero matches em `docs/canonical/` (2026-08-30):

1. **A arquitetura de consolidação-e-herança** — plataforma unificada first+third-party como pré-requisito; as docs existentes assumem fontes já acessíveis.
2. **RBAC definido uma vez no plano** — controle de acesso herdado automaticamente; as docs existentes tratam identidade (auth-coupled), isolamento (boundary) e rotulagem (PII), nunca herança por deployment.
3. **Deployment zero-code herdando controles** — a superfície de spawn sem código; o repo não tem noção de deployment de agente como ato de plataforma.
4. **Postura de segurança consistente na frota** como propriedade de primeira classe.
5. Papel de **canonical unificadora**: conectar as três docs de governança existentes sob uma arquitetura comum (classification:180-182).

## Tradeoffs

| Benefício | Custo |
|---|---|
| Governança definida uma vez no data plane e herdada por todo agente | Acoplamento estratégico à plataforma — o builder é também customer zero |
| Sem código de autenticação por agente; postura de segurança consistente na frota | Consolidação de dados é projeto pré-requisito com custo próprio |
| Zero-code deployment remove o gargalo de engenharia para novos agentes | Plataformas no-code têm teto para comportamento profundamente customizado |
| Unifica as três docs de governança existentes sob uma arquitetura | Guardrails de plataforma uniformes podem frustrar casos-limite que exigem override |

## Relação com outros padrões

- **Unifica:** [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] (identidade como chave por item), [[docs/canonical/regulated-data-boundary|Regulated Data Boundary]] (isolamento estrutural por tier), [[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]] (tagging no catálogo) — cada mecanismo vira uma política definida no plano e herdada, em vez de reimplementada por agente.
- **Habilita:** [[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]] — o plano consolidado é a fonte natural dos logs de perguntas unificados que a taxonomia classifica.

## Referências

- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md:183-212` — padrão extraído: silos SaaS, plataforma unificada, RBAC no plano, zero-code, guardrails.
- `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-classification.yaml:148-182` — classificação Partial Coverage (Medium) com NOT_FOUND de RBAC/data plane/MCP.
- `docs/canonical/auth-coupled-memory-architecture.md:32, :36` — identidade como chave de memória.
- `docs/canonical/regulated-data-boundary.md:32` — tier isolado de dados regulados.
- `docs/canonical/governance-context-injection-pii-prevention.md:22` — catálogo de dados com tagging PII.
- `docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-analysis.md:186` — adjacência no-code (nível análise).
