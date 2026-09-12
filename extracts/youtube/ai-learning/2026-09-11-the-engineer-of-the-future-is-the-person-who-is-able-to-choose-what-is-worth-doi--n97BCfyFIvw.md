---
title: "\"The engineer of the future is the person who is able to choose what is worth doing.\" — Addy Osmani"
type: "extract"
source: "youtube"
video_id: "n97BCfyFIvw"
url: "https://www.youtube.com/watch?v=n97BCfyFIvw"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-engineer-of-the-future-is-the-person-who-is-able-to-choose-what-is-worth-doi--n97BCfyFIvw.txt]]"
tags: ["agent-loop", "harness", "code-review", "verification", "governanca", "decision-discipline", "escalation", "agent-fleets", "production", "process"]
thesis: "À medida que agentes executam cada vez mais o loop interno de engenharia, o diferencial humano se desloca para o loop externo — posse de vereditos de produção respaldados por evidência, pois execução e responsabilidade são coisas distintas."
concepts: ["answerability/veredito de produção (ship, block, redirect, accept risk)", "harness engineering (modelo + harness: contexto, ferramentas, filesystem, git)", "loop engineering e software factories", "loop interno (capacidade do agente) vs loop externo (agência humana: decidir, verificar, aprovar, possuir)", "alpha e decay como matemática de carreira (meia-vida de uma vantagem ≈ um release de modelo)", "gosto/taste como julgamento qualitativo sem métrica objetiva (Hashimoto) e sua decay lenta", "divida cognitiva (cognitive debt) e delegation depth", "rendição cognitiva (cognitive surrender) e confiança emprestada", "taxa de orquestração (orchestration tax): largura de banda cognitiva não paraleliza", "assinatura (signature) com meia-vida maior que skills", "escada de agência: flag → execute → diagnose → propose → recommend → resolve → discernment", "fronteira evidência-e-responsabilidade em vez de humano-olha-saída-do-IA", "regra operacional: explique ou não entregue", "taxonomia de modos de engenharia: prototype, build, sweep, grow, maintain", "stewardship de brownfield e demanda latente ao baixar custo de geração"]
tools: ["Sonar (pesquisas/estudos citados)", "git", "filesystem"]
people: ["Boris Cherny", "Paul Graham", "Mitchell Hashimoto", "Wharton (estudo sobre confiança emprestada)", "Sonar"]
claims: ["Quando o código assistido por IA vira código normal, answerability deixa de ser filosofia e vira requisito de engenharia", "Segurança vem de tornar verificação mais barata, mais clara e mais difícil de pular — há risco de desconfiança sem banda (96% céticos, só ~metade sempre verifica antes do commit)", "Código limpo tem pass rates similares aos de repositórios bagunçados, mas consome menos tokens e causa menos revisitas (pesquisa Sonar)", "Baratear geração não barateia revisão; revisão/validação viram gargalo quando governança não acompanha a adoção", "Tarefas de longo horizonte (horas/dias) em paralelo exigem que review deixe de ser um olhar final e vire um sistema de controle", "Delegação exige evidência suficiente para julgamento; rendição é adotar a resposta da IA antes de formar opinião própria (estudo Wharton: 73% seguiram respostas erradas com mais confiança)", "Mais agentes rodando não aumenta sua banda cognitiva: projete sua atenção como sistema (onde entra, o que exige, o que reusa)", "A pergunta estratégica não é 'o que o agente consegue fazer', mas 'pelo que só um humano pode ser responsabilizado'", "O agente pode seguir o runbook mas não herda as consequências; alguém deve possuir o blast radius", "Operacionalize posse como um owners file de codebase: quem responde por cada parte da arquitetura", "Automação sobe o piso e move o gargalo de 'conseguimos construir' para 'isso deveria existir e conseguimos responder por isso'"]
deep_dive: "medium"
deep_dive_reason: "Oferece frameworks acionáveis e anti-padrões relevantes a governança e verificação de agentes, mas é majoritariamente um discurso de evolução de papéis/carreira com pouca densidade arquitetural ou novidade técnica."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ryan-lopopolo-harness-engineering-how-to-build-software-when-humans-steer-and-ag--c8bE0cj7vHY|Ryan Lopopolo - Harness Engineering: How to Build Software When Humans Steer and Agents Execute]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-frontrunners-say-coding-is-solved-but-engineering-is-not--Q7l8YGiMgUw|Why the Frontrunners Say Coding Is Solved BUT Engineering is Not]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo|Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary]]", "[[extracts/youtube/ai-learning/2026-09-11-the-era-of-compound-engineering-kieran-klaassen-every-cora--_ehJyfHg1Vk|The Era of Compound Engineering — Kieran Klaassen, Every/Cora]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-best-software-engineers-focus-on-system-design--LeUUxLRdvho|Why The Best Software Engineers Focus On System Design]]", "[[extracts/youtube/ai-learning/2026-09-11-the-pipeline-is-dead-iris-ten-teije-sky-valley-ambient-computing--bRnoEpoK5m4|The Pipeline Is Dead - Iris ten Teije, Sky Valley Ambient Computing]]", "[[extracts/youtube/ai-learning/2026-09-11-is-this-the-only-skill-left--7zCsfe57tpU|Is this the only skill left?]]", "[[extracts/youtube/ai-learning/2026-09-11-google-aws-veteran-what-top-tier-software-architects-do-differently--F8X9_Dp3ZUk|Google & AWS Veteran: What Top Tier Software Architects Do Differently]]"]
theme: "Processo de Engenharia Agêntica"
---

# "The engineer of the future is the person who is able to choose what is worth doing." — Addy Osmani

## Tese
À medida que agentes executam cada vez mais o loop interno de engenharia, o diferencial humano se desloca para o loop externo — posse de vereditos de produção respaldados por evidência, pois execução e responsabilidade são coisas distintas.

## Conceitos-chave
- answerability/veredito de produção (ship, block, redirect, accept risk)
- harness engineering (modelo + harness: contexto, ferramentas, filesystem, git)
- loop engineering e software factories
- loop interno (capacidade do agente) vs loop externo (agência humana: decidir, verificar, aprovar, possuir)
- alpha e decay como matemática de carreira (meia-vida de uma vantagem ≈ um release de modelo)
- gosto/taste como julgamento qualitativo sem métrica objetiva (Hashimoto) e sua decay lenta
- divida cognitiva (cognitive debt) e delegation depth
- rendição cognitiva (cognitive surrender) e confiança emprestada
- taxa de orquestração (orchestration tax): largura de banda cognitiva não paraleliza
- assinatura (signature) com meia-vida maior que skills
- escada de agência: flag → execute → diagnose → propose → recommend → resolve → discernment
- fronteira evidência-e-responsabilidade em vez de humano-olha-saída-do-IA
- regra operacional: explique ou não entregue
- taxonomia de modos de engenharia: prototype, build, sweep, grow, maintain
- stewardship de brownfield e demanda latente ao baixar custo de geração

## Ferramentas & pessoas
**Ferramentas:** Sonar (pesquisas/estudos citados), git, filesystem

**Pessoas/orgs:** Boris Cherny, Paul Graham, Mitchell Hashimoto, Wharton (estudo sobre confiança emprestada), Sonar

## Claims acionáveis
- Quando o código assistido por IA vira código normal, answerability deixa de ser filosofia e vira requisito de engenharia
- Segurança vem de tornar verificação mais barata, mais clara e mais difícil de pular — há risco de desconfiança sem banda (96% céticos, só ~metade sempre verifica antes do commit)
- Código limpo tem pass rates similares aos de repositórios bagunçados, mas consome menos tokens e causa menos revisitas (pesquisa Sonar)
- Baratear geração não barateia revisão; revisão/validação viram gargalo quando governança não acompanha a adoção
- Tarefas de longo horizonte (horas/dias) em paralelo exigem que review deixe de ser um olhar final e vire um sistema de controle
- Delegação exige evidência suficiente para julgamento; rendição é adotar a resposta da IA antes de formar opinião própria (estudo Wharton: 73% seguiram respostas erradas com mais confiança)
- Mais agentes rodando não aumenta sua banda cognitiva: projete sua atenção como sistema (onde entra, o que exige, o que reusa)
- A pergunta estratégica não é 'o que o agente consegue fazer', mas 'pelo que só um humano pode ser responsabilizado'
- O agente pode seguir o runbook mas não herda as consequências; alguém deve possuir o blast radius
- Operacionalize posse como um owners file de codebase: quem responde por cada parte da arquitetura
- Automação sobe o piso e move o gargalo de 'conseguimos construir' para 'isso deveria existir e conseguimos responder por isso'

> **Deep dive:** `medium` — Oferece frameworks acionáveis e anti-padrões relevantes a governança e verificação de agentes, mas é majoritariamente um discurso de evolução de papéis/carreira com pouca densidade arquitetural ou novidade técnica.
