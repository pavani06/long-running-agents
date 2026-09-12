---
title: "26 Key Takeaways from Building 150+ Agents in 9 months"
type: "extract"
source: "youtube"
video_id: "jmeGqDu4tPU"
url: "https://www.youtube.com/watch?v=jmeGqDu4tPU"
channel: "Arseny Shatokhin"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-26-key-takeaways-from-building-150-agents-in-9-months--jmeGqDu4tPU.txt]]"
tags: ["agents", "agent-tooling", "multi-agent", "process", "evals", "verification", "error-handling", "gate-design", "model-selection", "decision-discipline", "production", "frameworks", "context-engineering"]
thesis: "Construir agentes de IA como serviço com sucesso exige mapear cada agente a um único SOP bem documentado, concentrar ~70% do esforço em ferramentas/integrações, validar valor e ROI antes de automatizar, e entregar incrementalmente com poucos agentes e poucas ferramentas por agente."
concepts: ["Agents as a Service", "SOPs (Standard Operating Procedures) - um agente por SOP em vez de por função", "Customer journey mapping como método de descoberta", "GIGO (garbage in, garbage out)", "Combinação de dados/conhecimento + ações de API", "Prompt engineering: exemplos, ordenação (recência), iteração testada", "Limite de 4-6 ferramentas por agente", "Fórmula de ROI: (taxa x horas - custos operacionais) / custo de desenvolvimento", "Divide and conquer / entrega incremental por departamento", "Evals para clientes enterprise vs. dispensáveis para PMEs", "Workflows agênticos (etapas fixas com passos agênticos) vs. agentes totalmente autônomos", "Feedback loop: ferramentas de leitura/verificação para autoconfirmar ações", "Human in the loop para ações irreversíveis", "Agentes verticais vs. horizontais (analogia com B2B SaaS vertical)", "Validação de entradas/saídas com Pydantic como solução de confiabilidade"]
tools: ["Pydantic", "Instructor", "Azure OpenAI", "OpenAI API (GPT-4o)", "Claude 3.5", "Figma", "Zendesk", "CrewAI", "Notion", "Upwork", "Facebook Marketing API", "Operator (OpenAI)", "Deep Research (OpenAI)", "RAG/File search (OpenAI)", "Framework próprio do autor (não nomeado)", "Plataforma própria de deploy do autor (não nomeada, waitlist)"]
people: ["Jason Liu (citado como 'Jason Leo')", "OpenAI", "Anthropic (Claude 3.5)", "DeepSeek (referido como 'DPS')", "Agência do autor (não nomeada, 150+ agentes em 9 meses)"]
claims: ["Projetar um agente por SOP em vez de por função: um funcionário cobre 5+ SOPs, um agente cobre bem apenas um.", "Começar sempre de processos já bem documentados (SOPs, materiais de onboarding) para simplificar o treinamento do agente.", "Em ~50% dos casos as ideias de agentes do cliente não são as mais valiosas; usar customer journey mapping para descobrir oportunidades melhores.", "Começar com o menor agente entregável e só adicionar mais agentes após deploy e validação pelo cliente; 20+ agentes aumentam complexidade, custo e latência.", "Combinar conhecimento (fontes internas e externas raspadas) com ações de API gera desempenho muito maior do que dados ou ações isolados.", "Colocar as instruções mais importantes no final do prompt (efeito de recência) e fornecer múltiplos exemplos, pois rearranjar o prompt pode levar de imprevisível a consistente.", "Nunca modificar prompt sem testar o impacto no desempenho; iterar e testar constantemente.", "Integrar o agente nas ferramentas que o cliente já usa diariamente (ex.: agente de suporte deve rodar dentro do Zendesk).", "Validar todas as entradas e saídas do agente com Pydantic para impedir ações catastróficas ('Pydantic is all you need').", "Direcionar ~70% do esforço de desenvolvimento para construir ações/ferramentas, pois é nelas que o agente gera valor.", "Limitar cada agente a 4-6 ferramentas; se o agente alucinar ou confundir ferramentas, dividi-lo em múltiplos agentes.", "Ignorar custo de modelo e focar em processos de alto ROI (ex.: US$300/3 dias manualmente → US$1-2/20 minutos).", "Usar Azure OpenAI para clientes com políticas rígidas de privacidade de dados; OpenAI permanece preferido pela developer experience.", "Validar o processo manualmente antes de automatizá-lo (ex.: contratar alguém no Upwork) em vez de automatizar um negócio que ainda não existe.", "Priorizar por ROI com a fórmula (taxa x horas - custos operacionais) / custo de desenvolvimento, não por use cases sugeridos pelo cliente.", "Testar múltiplas arquiteturas lado a lado (como em competições Kaggle) para determinar número de agentes, ferramentas e estrutura.", "Entregar incrementalmente e automatizar por departamento, o que permite combinar agentes do mesmo departamento depois.", "Pular evals no início para PMEs (baixo tráfego, ganhos incrementais só nos últimos 20%); implementá-los desde o início para clientes enterprise.", "Usar workflows agênticos quando a sequência de etapas é determinística mas cada passo requer capacidade agêntica (ex.: pesquisa de leads com prompts fixos).", "Adicionar ferramentas de leitura/verificação para que o agente confirme o efeito das próprias ações (ex.: ler o banco após gravar).", "Não arquitetar em torno de limitações atuais dos modelos (ex.: workarounds de contexto tornaram-se obsoletos com janela de 128k).", "Planejar que deploy/integração no processo do cliente leva tanto ou mais tempo que a construção do agente (2-3 dias para cada).", "Trabalhar em modelo de assinatura/ágil; projetos waterfall de 3 meses falham porque escopos agênticos evoluem constantemente.", "Incluir human-in-the-loop para ações irreversíveis ou mission-critical (ex.: revisar campanhas no Notion) e removê-lo após fine-tuning consistente.", "Construir agentes horizontais primeiro e verticalizar/productizar após identificar similaridades no setor; 2025 seria o ano dos agentes verticais.", "Evitar use cases óbvios e gerais (ex.: agente de desenvolvimento de software) que os labs provavelmente lançarão, tornando startups obsoletas."]
deep_dive: "medium"
deep_dive_reason: "Oferece densidade prática acionável de operação de agência (limite de ferramentas, validação Pydantic, fórmula de ROI, entrega incremental), mas a maioria dos insights já é amplamente difundida, com trechos promocionais e sem novidade arquitetural profunda em harness, evals ou ontologia que justificasse tier alto."
---

# 26 Key Takeaways from Building 150+ Agents in 9 months

## Tese
Construir agentes de IA como serviço com sucesso exige mapear cada agente a um único SOP bem documentado, concentrar ~70% do esforço em ferramentas/integrações, validar valor e ROI antes de automatizar, e entregar incrementalmente com poucos agentes e poucas ferramentas por agente.

## Conceitos-chave
- Agents as a Service
- SOPs (Standard Operating Procedures) - um agente por SOP em vez de por função
- Customer journey mapping como método de descoberta
- GIGO (garbage in, garbage out)
- Combinação de dados/conhecimento + ações de API
- Prompt engineering: exemplos, ordenação (recência), iteração testada
- Limite de 4-6 ferramentas por agente
- Fórmula de ROI: (taxa x horas - custos operacionais) / custo de desenvolvimento
- Divide and conquer / entrega incremental por departamento
- Evals para clientes enterprise vs. dispensáveis para PMEs
- Workflows agênticos (etapas fixas com passos agênticos) vs. agentes totalmente autônomos
- Feedback loop: ferramentas de leitura/verificação para autoconfirmar ações
- Human in the loop para ações irreversíveis
- Agentes verticais vs. horizontais (analogia com B2B SaaS vertical)
- Validação de entradas/saídas com Pydantic como solução de confiabilidade

## Ferramentas & pessoas
**Ferramentas:** Pydantic, Instructor, Azure OpenAI, OpenAI API (GPT-4o), Claude 3.5, Figma, Zendesk, CrewAI, Notion, Upwork, Facebook Marketing API, Operator (OpenAI), Deep Research (OpenAI), RAG/File search (OpenAI), Framework próprio do autor (não nomeado), Plataforma própria de deploy do autor (não nomeada, waitlist)

**Pessoas/orgs:** Jason Liu (citado como 'Jason Leo'), OpenAI, Anthropic (Claude 3.5), DeepSeek (referido como 'DPS'), Agência do autor (não nomeada, 150+ agentes em 9 meses)

## Claims acionáveis
- Projetar um agente por SOP em vez de por função: um funcionário cobre 5+ SOPs, um agente cobre bem apenas um.
- Começar sempre de processos já bem documentados (SOPs, materiais de onboarding) para simplificar o treinamento do agente.
- Em ~50% dos casos as ideias de agentes do cliente não são as mais valiosas; usar customer journey mapping para descobrir oportunidades melhores.
- Começar com o menor agente entregável e só adicionar mais agentes após deploy e validação pelo cliente; 20+ agentes aumentam complexidade, custo e latência.
- Combinar conhecimento (fontes internas e externas raspadas) com ações de API gera desempenho muito maior do que dados ou ações isolados.
- Colocar as instruções mais importantes no final do prompt (efeito de recência) e fornecer múltiplos exemplos, pois rearranjar o prompt pode levar de imprevisível a consistente.
- Nunca modificar prompt sem testar o impacto no desempenho; iterar e testar constantemente.
- Integrar o agente nas ferramentas que o cliente já usa diariamente (ex.: agente de suporte deve rodar dentro do Zendesk).
- Validar todas as entradas e saídas do agente com Pydantic para impedir ações catastróficas ('Pydantic is all you need').
- Direcionar ~70% do esforço de desenvolvimento para construir ações/ferramentas, pois é nelas que o agente gera valor.
- Limitar cada agente a 4-6 ferramentas; se o agente alucinar ou confundir ferramentas, dividi-lo em múltiplos agentes.
- Ignorar custo de modelo e focar em processos de alto ROI (ex.: US$300/3 dias manualmente → US$1-2/20 minutos).
- Usar Azure OpenAI para clientes com políticas rígidas de privacidade de dados; OpenAI permanece preferido pela developer experience.
- Validar o processo manualmente antes de automatizá-lo (ex.: contratar alguém no Upwork) em vez de automatizar um negócio que ainda não existe.
- Priorizar por ROI com a fórmula (taxa x horas - custos operacionais) / custo de desenvolvimento, não por use cases sugeridos pelo cliente.
- Testar múltiplas arquiteturas lado a lado (como em competições Kaggle) para determinar número de agentes, ferramentas e estrutura.
- Entregar incrementalmente e automatizar por departamento, o que permite combinar agentes do mesmo departamento depois.
- Pular evals no início para PMEs (baixo tráfego, ganhos incrementais só nos últimos 20%); implementá-los desde o início para clientes enterprise.
- Usar workflows agênticos quando a sequência de etapas é determinística mas cada passo requer capacidade agêntica (ex.: pesquisa de leads com prompts fixos).
- Adicionar ferramentas de leitura/verificação para que o agente confirme o efeito das próprias ações (ex.: ler o banco após gravar).
- Não arquitetar em torno de limitações atuais dos modelos (ex.: workarounds de contexto tornaram-se obsoletos com janela de 128k).
- Planejar que deploy/integração no processo do cliente leva tanto ou mais tempo que a construção do agente (2-3 dias para cada).
- Trabalhar em modelo de assinatura/ágil; projetos waterfall de 3 meses falham porque escopos agênticos evoluem constantemente.
- Incluir human-in-the-loop para ações irreversíveis ou mission-critical (ex.: revisar campanhas no Notion) e removê-lo após fine-tuning consistente.
- Construir agentes horizontais primeiro e verticalizar/productizar após identificar similaridades no setor; 2025 seria o ano dos agentes verticais.
- Evitar use cases óbvios e gerais (ex.: agente de desenvolvimento de software) que os labs provavelmente lançarão, tornando startups obsoletas.

> **Deep dive:** `medium` — Oferece densidade prática acionável de operação de agência (limite de ferramentas, validação Pydantic, fórmula de ROI, entrega incremental), mas a maioria dos insights já é amplamente difundida, com trechos promocionais e sem novidade arquitetural profunda em harness, evals ou ontologia que justificasse tier alto.
