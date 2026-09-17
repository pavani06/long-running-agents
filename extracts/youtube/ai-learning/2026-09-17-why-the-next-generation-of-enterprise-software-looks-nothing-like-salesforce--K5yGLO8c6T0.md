---
title: "Why the Next Generation of Enterprise Software Looks Nothing Like Salesforce"
type: "extract"
source: "youtube"
video_id: "K5yGLO8c6T0"
url: "https://www.youtube.com/watch?v=K5yGLO8c6T0"
channel: "a16z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-why-the-next-generation-of-enterprise-software-looks-nothing-like-salesforce--K5yGLO8c6T0.txt]]"
tags: ["agents", "context-engineering", "context-management", "data-platform", "arquitetura", "state", "harness", "process", "decision-discipline", "investimentos", "roadmap"]
thesis: "Keith Peiris argues that the durable AI-era company is not a workflow-executing CRM but a 'business world model' — a semi-structured, schemaless canonical activity log of customer reality from which agents derive updates, pricing tiers, and defensibility."
concepts: ["business world model", "canonical activity log as system primitive", "semi-structured storage (unstructured log + inferred causality)", "schemaless CRM / intelligence over schema", "greenfield vs brownfield go-to-market", "negative pricing as bootstrap tactic", "hybrid pricing (platform fee + seats + consumption)", "harness defensibility via MCP/CLI openness", "expansion-potential prioritization (3-year horizon)", "generalist org with no swim lanes and continuous planning", "network effects against rip-and-replace via free company-wide seats", "reference logos as marketing capture for crossing the chasm"]
tools: ["Lightfield", "Tome", "Salesforce", "HubSpot", "Sugar CRM", "GPT-3", "GPT-4", "GPT-6", "ChatGPT", "Figma", "Linear", "Slack", "Snowflake", "MCP", "CLI", "clinicaltrials.gov", "FDA data scraping", "Zendesk", "Bloomberg", "SAP", "IBM AS400"]
people: ["Keith Peiris (Lightfield CEO)", "Henry (Lightfield co-founder)", "Joe Schmidt (a16z)", "Alex Rampell (a16z)", "a16z", "Facebook/Instagram/Messenger", "OpenAI", "ElevenLabs", "Power (customer)", "Tesla"]
claims: ["Pivot from Tome was driven by the model lacking context about presenter, audience, and their relationship — no amount of general reasoning compensates for missing context", "Lightfield built the chronological activity log first as the canonical primitive; traditional CRM field/stage updates are triggered downstream from it", "Fully unstructured storage failed because queries were too slow (needle-in-haystack); a semi-structured approach storing unstructured data in the activity log lets the system infer causality and beat both extremes", "Schemaless onboarding works: connect email, call recorder, and data warehouse, relationships assemble in real time, and fields can be backfilled later by traversing the log — 'intelligence is greater than schema'", "Pricing split into four buckets: core CRM work (fixed platform fee/seat), pipeline generation (consumption, customers accept alpha pricing), workflow automations (pay per unit of real work), and intelligence/forecasting (charge for the alpha)", "Pure seat pricing failed because the head consumed 10,000x the tail; pure consumption pricing froze usage entirely; the hybrid platform-fee-plus-consumption model landed well", "Customers who build their own harness on top via MCP/CLI discover Lightfield's harness has better entity recognition, precision/recall, and speed — the harness itself is a moat", "Giving the product free to everyone in a company (engineering, finance, CS) creates internal network effects that neutralize incoming Salesforce-trained VPs of Sales", "Charging for outcomes is premature in sales because outcomes depend on the customer's own product-market fit; charge for the work instead", "Org design: no swim lanes, one company-wide standup, stack-ranked problems picked up by whoever is free, low bar to start a project and high bar to ship (company bug bashes)", "Use an internal Lightfield skill scoring each account's expansion potential over a 3-year horizon, prioritizing fastest-growing customers over average ones", "Greenfield-first (new startups) with the brownfield wedge being 'understand and steer your company' rather than 'do the work' like outbound emails Salesforce will commoditize", "AI lets anyone ramp on anything (Figma, Linear, customer context), making generalist-run projects feasible and pivots survivable"]
deep_dive: "medium"
deep_dive_reason: "Contains genuinely actionable architectural and GTM insights (activity-log primitive, semi-structured schemaless design, pricing taxonomy, harness moat via MCP/CLI) but they are diluted by founder narrative and promotional content, with no depth on evals, agent fleets, or governance."
---

# Why the Next Generation of Enterprise Software Looks Nothing Like Salesforce

## Tese
Keith Peiris argues that the durable AI-era company is not a workflow-executing CRM but a 'business world model' — a semi-structured, schemaless canonical activity log of customer reality from which agents derive updates, pricing tiers, and defensibility.

## Conceitos-chave
- business world model
- canonical activity log as system primitive
- semi-structured storage (unstructured log + inferred causality)
- schemaless CRM / intelligence over schema
- greenfield vs brownfield go-to-market
- negative pricing as bootstrap tactic
- hybrid pricing (platform fee + seats + consumption)
- harness defensibility via MCP/CLI openness
- expansion-potential prioritization (3-year horizon)
- generalist org with no swim lanes and continuous planning
- network effects against rip-and-replace via free company-wide seats
- reference logos as marketing capture for crossing the chasm

## Ferramentas & pessoas
**Ferramentas:** Lightfield, Tome, Salesforce, HubSpot, Sugar CRM, GPT-3, GPT-4, GPT-6, ChatGPT, Figma, Linear, Slack, Snowflake, MCP, CLI, clinicaltrials.gov, FDA data scraping, Zendesk, Bloomberg, SAP, IBM AS400

**Pessoas/orgs:** Keith Peiris (Lightfield CEO), Henry (Lightfield co-founder), Joe Schmidt (a16z), Alex Rampell (a16z), a16z, Facebook/Instagram/Messenger, OpenAI, ElevenLabs, Power (customer), Tesla

## Claims acionáveis
- Pivot from Tome was driven by the model lacking context about presenter, audience, and their relationship — no amount of general reasoning compensates for missing context
- Lightfield built the chronological activity log first as the canonical primitive; traditional CRM field/stage updates are triggered downstream from it
- Fully unstructured storage failed because queries were too slow (needle-in-haystack); a semi-structured approach storing unstructured data in the activity log lets the system infer causality and beat both extremes
- Schemaless onboarding works: connect email, call recorder, and data warehouse, relationships assemble in real time, and fields can be backfilled later by traversing the log — 'intelligence is greater than schema'
- Pricing split into four buckets: core CRM work (fixed platform fee/seat), pipeline generation (consumption, customers accept alpha pricing), workflow automations (pay per unit of real work), and intelligence/forecasting (charge for the alpha)
- Pure seat pricing failed because the head consumed 10,000x the tail; pure consumption pricing froze usage entirely; the hybrid platform-fee-plus-consumption model landed well
- Customers who build their own harness on top via MCP/CLI discover Lightfield's harness has better entity recognition, precision/recall, and speed — the harness itself is a moat
- Giving the product free to everyone in a company (engineering, finance, CS) creates internal network effects that neutralize incoming Salesforce-trained VPs of Sales
- Charging for outcomes is premature in sales because outcomes depend on the customer's own product-market fit; charge for the work instead
- Org design: no swim lanes, one company-wide standup, stack-ranked problems picked up by whoever is free, low bar to start a project and high bar to ship (company bug bashes)
- Use an internal Lightfield skill scoring each account's expansion potential over a 3-year horizon, prioritizing fastest-growing customers over average ones
- Greenfield-first (new startups) with the brownfield wedge being 'understand and steer your company' rather than 'do the work' like outbound emails Salesforce will commoditize
- AI lets anyone ramp on anything (Figma, Linear, customer context), making generalist-run projects feasible and pivots survivable

> **Deep dive:** `medium` — Contains genuinely actionable architectural and GTM insights (activity-log primitive, semi-structured schemaless design, pricing taxonomy, harness moat via MCP/CLI) but they are diluted by founder narrative and promotional content, with no depth on evals, agent fleets, or governance.
