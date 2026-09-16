---
title: "Agente de negociação de gastos SaaS"
type: "extract"
source: "x"
status_id: "2099876435737325724"
handle: "grok"
url: "https://x.com/grok/status/2099876435737325724"
created_at: "2026-09-15T15:02:10.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-grok-haggle-bot-audited-125-vendor-contracts-reached-out-to-the-v--2099876435737325724.json]]"
tags: ["agents", "permissions", "governanca", "decision-discipline", "memory-architecture", "process", "startups"]
topic: "Agente de negociação de gastos SaaS"
summary: "Haggle Bot é um agente que inventaria gastos de SaaS a partir do Ramp, identifica poupanças com evidências (assentos não usados, duplicatas, alternativas mais baratas) e redata contrapropostas a fornecedores — teria auditado ~125 contratos e gerado mais de US$100K em economia. Vale salvar como exemplo raro de spec completa de agente com permissões rígidas, fonte da verdade de dados e barra de evidência quantitativa."
key_points: ["Permissões como anti-jobs: nunca gastar, assinar, enviar PO nem qualquer e-mail/Slack (inclusive DM interno) sem 'go' explícito do operador para aquele envio específico; na dúvida, não é go. Enviar rascunho até para outro agente conta como envio.", "Barra de oportunidade em 3 partes: $ rastreado a dados vivos de despesa/ERP com a matemática, mecanismo específico de economia e 'por que agora' (janela de renovação de 120 dias, uso ou cotação); faltando um item, vira LEAD; waste exige evidência de utilização.", "Fonte da verdade hierárquica: acordos e faturas do sistema de despesas (Ramp/ERP tipo NetSuite) prevalecem sobre planilhas de fornecedor; Notion e Slack só preenchem donos e uso, e apenas sem contradizer os dados de despesa.", "Base de fornecedores em Google Sheets com coluna Focus (Switch/Renegotiate/Waste/Sticky) que exige um 'Why' de uma linha com mecanismo e $ vivo — tag sem tese não vale; maioria das linhas fica em branco de propósito.", "Padrões de saída e pesquisa: 3+ alternativas nomeadas por linha com preço de lista + benchmark de compradores (Vendr, Tropic, Spendflo), números citados e datados, nunca inventar contagens de assentos; e-mails externos saem como o operador, sem fingerprint do agente."]
entities: ["Haggle Bot", "Daniel Gartshein", "Ramp", "NetSuite", "Google Sheets", "Notion", "Slack", "Vendr", "Tropic", "Spendflo"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://x.ai/bot/marketplace/bots/haggle-bot"]
media: ["https://pbs.twimg.com/media/HSRBomnWMAAX2To.jpg"]
---

# Agente de negociação de gastos SaaS

**@grok** · [2099876435737325724](https://x.com/grok/status/2099876435737325724) · `tool`

## Resumo
Haggle Bot é um agente que inventaria gastos de SaaS a partir do Ramp, identifica poupanças com evidências (assentos não usados, duplicatas, alternativas mais baratas) e redata contrapropostas a fornecedores — teria auditado ~125 contratos e gerado mais de US$100K em economia. Vale salvar como exemplo raro de spec completa de agente com permissões rígidas, fonte da verdade de dados e barra de evidência quantitativa.

## Pontos-chave
- Permissões como anti-jobs: nunca gastar, assinar, enviar PO nem qualquer e-mail/Slack (inclusive DM interno) sem 'go' explícito do operador para aquele envio específico; na dúvida, não é go. Enviar rascunho até para outro agente conta como envio.
- Barra de oportunidade em 3 partes: $ rastreado a dados vivos de despesa/ERP com a matemática, mecanismo específico de economia e 'por que agora' (janela de renovação de 120 dias, uso ou cotação); faltando um item, vira LEAD; waste exige evidência de utilização.
- Fonte da verdade hierárquica: acordos e faturas do sistema de despesas (Ramp/ERP tipo NetSuite) prevalecem sobre planilhas de fornecedor; Notion e Slack só preenchem donos e uso, e apenas sem contradizer os dados de despesa.
- Base de fornecedores em Google Sheets com coluna Focus (Switch/Renegotiate/Waste/Sticky) que exige um 'Why' de uma linha com mecanismo e $ vivo — tag sem tese não vale; maioria das linhas fica em branco de propósito.
- Padrões de saída e pesquisa: 3+ alternativas nomeadas por linha com preço de lista + benchmark de compradores (Vendr, Tropic, Spendflo), números citados e datados, nunca inventar contagens de assentos; e-mails externos saem como o operador, sem fingerprint do agente.

## Links
- https://x.ai/bot/marketplace/bots/haggle-bot

## Entidades
Haggle Bot, Daniel Gartshein, Ramp, NetSuite, Google Sheets, Notion, Slack, Vendr, Tropic, Spendflo

> **Revisit:** `high` · **fonte:** `article`
