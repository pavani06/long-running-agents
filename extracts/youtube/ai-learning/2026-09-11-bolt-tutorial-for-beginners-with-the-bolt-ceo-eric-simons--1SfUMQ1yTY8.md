---
title: "Bolt tutorial for beginners with the Bolt CEO Eric Simons"
type: "extract"
source: "youtube"
video_id: "1SfUMQ1yTY8"
url: "https://www.youtube.com/watch?v=1SfUMQ1yTY8"
channel: "Greg Isenberg"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-bolt-tutorial-for-beginners-with-the-bolt-ceo-eric-simons--1SfUMQ1yTY8.txt]]"
tags: ["agentic-coding", "agent-tooling", "agent-loop", "stack-tooling", "process", "error-handling", "production", "state", "permissions"]
thesis: "Em uma demonstração ao vivo, o fundador da StackBlitz mostra que o Bolt permite a não-desenvolvedores ir de ideia a apps web em produção (diretório SEO com gamificação e chat em tempo real) sem escrever código, desde que se use prompts incrementais com captura de 'vibe', checkpoints de rollback e um loop de correção alimentado por erros colados no chat."
concepts: ["Vibe-driven prompting (capturar estética/essência em texto ou screenshot)", "Prompts incrementais e focados por bloco de trabalho", "Checkpoints e undo/rollback para reverter a última geração", "Loop de correção colando mensagens de erro no chat do agente", "Gamificação via framework Octalysis (leaderboards, upvotes, ranking)", "Diretório SEO como negócio evoluível para micro-SaaS com afiliados", "Escopo funcional mínimo primeiro, depois incrementos um-a-um", "Deploy in-browser direto para produção sem setup local", "Provedores recomendados vs provedores arbitrários (Firebase/Supabase)", "Modo teste vs permissões reais do banco em produção", "Prompt enhancer para expandir prompts curtos em especificações determinísticas", "Arbitragem de adoção de LLMs por empreendedores vs engenheiros", "File locking futuro para impedir o LLM de modificar certos arquivos (ex.: .env)"]
tools: ["Bolt (bolt.new)", "StackBlitz (web IDE)", "Cursor", "Firebase (Realtime Database e Firestore)", "Supabase", "Netlify", "Unsplash", "v0", "GitHub Copilot", "Claude/Anthropic (Sonnet)", "Perplexity", "Octalysis", "Upwork", "Arc Browser", "Product Hunt", "Google Analytics"]
people: ["Eric (fundador da StackBlitz/Bolt)", "Greg (host do Startup Ideas Podcast)", "Pitch (criadora do ViralHooks, Tailândia)", "Tomac (devrel da StackBlitz, tutorial de Firebase)", "Paul (fundador de CRM construído com Bolt)", "Anthropic", "Y Combinator (startups citadas)"]
claims: ["Inclua no primeiro prompt tanto o 'vibe'/público-alvo quanto requisitos funcionais concretos: isso melhora não só o design mas o copy de marketing e CTAs gerados", "Divida o trabalho em prompts pequenos e focados: se o agente faz muitas coisas e erra uma, o rollback descartaria tudo e você teria que corrigir código manualmente", "Cole erros de execução diretamente no chat para o agente corrigir (ex.: aspa não escapada quebrando a compilação)", "Peça funcionalidade mínima primeiro, verifique funcionando, e só então adicione incrementos (ex.: 'chat simples' antes de 'experiência tipo Discord')", "Use o botão undo/checkpoint para reverter à última versão que funcionava em vez de reprometer às cegas", "Se a primeira geração sair muito longe do desejado, volte à home e comece um prompt novo em vez de remendar", "Prefira Firebase ou Supabase como backend no Bolt (auth e realtime integrados); provedores obscuros podem falhar", "Em prototipagem, use test mode do Firebase para velocidade, mas configure permissões do banco antes de ir a produção", "Se o preview não sobe, o LLM pode ter esquecido de reiniciar o dev server — peça explicitamente 'restart the dev server' (npm run dev)", "Fique atento ao LLM movendo segredos para .env durante deploy (comportamento 'correto' mas inesperado); file locking está no roadmap para travar arquivos", "Use o prompt enhancer para expandir prompts curtos em especificações detalhadas e tornar a saída mais determinística", "Screenshot de um site de referência + 'capture the vibe/cores' funciona para transferir identidade visual ao agente", "Mecânicas de gamificação (ranking numerado, upvotes ilimitados) dão sensação de atividade/vitalidade a diretórios", "O botão deploy faz o build no navegador e publica no Netlify sem setup local, permitindo domínio próprio e indexação SEO", "Para estimar valor: caso citado de app cotado a US$3-5K/2 meses por contratados foi entregue em ~2 semanas com plano de US$50/mês no Bolt"]
deep_dive: "low"
deep_dive_reason: "É essencialmente uma demo promocional de produto com boas práticas de prompting já difundidas (prompts pequenos, rollback, colar erros), sem densidade arquitetural, novidade ou cobertura de harness, evals, context-engineering ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-i-built-a-4589-website-in-minutes-with-bolt-new-and-cursor-ai--KqiQ4kC8OJI|I Built a $4589 Website in Minutes with Bolt.new and Cursor AI!]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-perfect-looking-apps-with-bolt-new-easy-hack--gZKLPNhWXxE|How to Build PERFECT Looking Apps With Bolt.new (Easy Hack)]]", "[[extracts/youtube/ai-learning/2026-09-11-i-tested-bolt-and-lovable-here-s-what-s-best-for-your-project--_PgBDk_GhPo|I Tested Bolt and Lovable Here's What's Best for Your Project]]", "[[extracts/youtube/ai-learning/2026-09-11-bolt-vs-lovable-which-ai-app-builder-comes-out-on-top--yHDvCGNjIqk|Bolt vs Lovable: which AI app builder comes out on top?]]", "[[extracts/youtube/ai-learning/2026-09-11-is-this-the-best-vibe-coding-platform-lovable-ai--3eDrAHjSqXo|Is this the Best Vibe Coding Platform? (Lovable AI)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-new-100k-month-a-i-saas-with-me-in-20-minutes-no-code-is-insane--6GBFiseyDnk|Build a NEW $100K/Month A.I SaaS WITH ME in 20 minutes (No-code Is INSANE)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-cursor-agent-for-beginners--2gBcO3ht0ws|How to use Cursor Agent for beginners]]"]
theme: "Agentes de IA No-Code"
---

# Bolt tutorial for beginners with the Bolt CEO Eric Simons

## Tese
Em uma demonstração ao vivo, o fundador da StackBlitz mostra que o Bolt permite a não-desenvolvedores ir de ideia a apps web em produção (diretório SEO com gamificação e chat em tempo real) sem escrever código, desde que se use prompts incrementais com captura de 'vibe', checkpoints de rollback e um loop de correção alimentado por erros colados no chat.

## Conceitos-chave
- Vibe-driven prompting (capturar estética/essência em texto ou screenshot)
- Prompts incrementais e focados por bloco de trabalho
- Checkpoints e undo/rollback para reverter a última geração
- Loop de correção colando mensagens de erro no chat do agente
- Gamificação via framework Octalysis (leaderboards, upvotes, ranking)
- Diretório SEO como negócio evoluível para micro-SaaS com afiliados
- Escopo funcional mínimo primeiro, depois incrementos um-a-um
- Deploy in-browser direto para produção sem setup local
- Provedores recomendados vs provedores arbitrários (Firebase/Supabase)
- Modo teste vs permissões reais do banco em produção
- Prompt enhancer para expandir prompts curtos em especificações determinísticas
- Arbitragem de adoção de LLMs por empreendedores vs engenheiros
- File locking futuro para impedir o LLM de modificar certos arquivos (ex.: .env)

## Ferramentas & pessoas
**Ferramentas:** Bolt (bolt.new), StackBlitz (web IDE), Cursor, Firebase (Realtime Database e Firestore), Supabase, Netlify, Unsplash, v0, GitHub Copilot, Claude/Anthropic (Sonnet), Perplexity, Octalysis, Upwork, Arc Browser, Product Hunt, Google Analytics

**Pessoas/orgs:** Eric (fundador da StackBlitz/Bolt), Greg (host do Startup Ideas Podcast), Pitch (criadora do ViralHooks, Tailândia), Tomac (devrel da StackBlitz, tutorial de Firebase), Paul (fundador de CRM construído com Bolt), Anthropic, Y Combinator (startups citadas)

## Claims acionáveis
- Inclua no primeiro prompt tanto o 'vibe'/público-alvo quanto requisitos funcionais concretos: isso melhora não só o design mas o copy de marketing e CTAs gerados
- Divida o trabalho em prompts pequenos e focados: se o agente faz muitas coisas e erra uma, o rollback descartaria tudo e você teria que corrigir código manualmente
- Cole erros de execução diretamente no chat para o agente corrigir (ex.: aspa não escapada quebrando a compilação)
- Peça funcionalidade mínima primeiro, verifique funcionando, e só então adicione incrementos (ex.: 'chat simples' antes de 'experiência tipo Discord')
- Use o botão undo/checkpoint para reverter à última versão que funcionava em vez de reprometer às cegas
- Se a primeira geração sair muito longe do desejado, volte à home e comece um prompt novo em vez de remendar
- Prefira Firebase ou Supabase como backend no Bolt (auth e realtime integrados); provedores obscuros podem falhar
- Em prototipagem, use test mode do Firebase para velocidade, mas configure permissões do banco antes de ir a produção
- Se o preview não sobe, o LLM pode ter esquecido de reiniciar o dev server — peça explicitamente 'restart the dev server' (npm run dev)
- Fique atento ao LLM movendo segredos para .env durante deploy (comportamento 'correto' mas inesperado); file locking está no roadmap para travar arquivos
- Use o prompt enhancer para expandir prompts curtos em especificações detalhadas e tornar a saída mais determinística
- Screenshot de um site de referência + 'capture the vibe/cores' funciona para transferir identidade visual ao agente
- Mecânicas de gamificação (ranking numerado, upvotes ilimitados) dão sensação de atividade/vitalidade a diretórios
- O botão deploy faz o build no navegador e publica no Netlify sem setup local, permitindo domínio próprio e indexação SEO
- Para estimar valor: caso citado de app cotado a US$3-5K/2 meses por contratados foi entregue em ~2 semanas com plano de US$50/mês no Bolt

> **Deep dive:** `low` — É essencialmente uma demo promocional de produto com boas práticas de prompting já difundidas (prompts pequenos, rollback, colar erros), sem densidade arquitetural, novidade ou cobertura de harness, evals, context-engineering ou governança.
