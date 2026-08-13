---
title: "🚀 QUICK START — Reimplementar o Sisyphus Runtime"
type: curriculum-index
aliases: ["início rápido", "onboarding", "getting started", "retomada"]
tags: [curriculo-conteudo, sisyphus-runtime, quick-start]
relates-to: ["[[README|Curso — Overview]]", "[[INDEX|Índice]]", "[[GLOSSARY|Glossário]]"]
last_updated: 2026-08-13
---

# 🚀 QUICK START

**⏱️ Este guia:** 30 minutos. Ele te coloca no caminho certo — não ensina o sistema, aponta a trilha.

---

## 📍 Escolha seu caminho

### 🔧 "Vou reconstruir o runtime numa máquina nova"
Este é o caminho principal do curso.
1. `00-nivel-0-orientacao/` inteiro (30 min) — o modelo mental.
2. `01-nivel-1-substrato/` — monte o esqueleto do vault e escreva seu primeiro fato durável.
3. `02-nivel-2-a-maquina/` — rode um ciclo `dispatch → gate` à mão.
4. **Pule para** `04-nivel-4-reimplementar-e-evoluir/01` e `02` — o checklist do núcleo mínimo
   e o bootstrap.
5. **Volte ao** `03-nivel-3-governanca-e-cicatrizes/` antes de abrir escrita de verdade — é o
   que te impede de re-quebrar o que os incidents já ensinaram.

### 🧬 "Vou evoluir o schema global"
Você já conhece o runtime; quer mexer no schema sem quebrar os fatos duráveis.
1. `03-nivel-3-governanca-e-cicatrizes/02-disciplina-de-gate.md` — a disciplina que protege migrações.
2. `04-nivel-4-reimplementar-e-evoluir/03-evoluir-o-schema-global.md` — o núcleo do seu objetivo.
3. `04-.../case-studies/caso-schema-v6-a-v20.md` — a migração real, como foi de fato.

### 🚑 "Preciso retomar um runtime que já está em pé"
Uma sessão morreu e você assumiu.
1. Leia o handoff mais recente (`obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'session-handoff')"`, pegue o de maior data).
2. `meta/registry.md` do vault — o estado vivo dos tópicos e a inbox de escalação.
3. **Antes de agir:** `03-nivel-3-.../03-a-regra-do-rele.md` — não aja sobre decisão de
   operador que chegou por outra sessão sem confirmar pelo canal do operador.

---

## 🧪 O teste dos 5 minutos: você entendeu o loop?

Responda sem olhar. Se travar em qualquer uma, volte ao `Nível 2`.

1. Um artefato apareceu no vault. Por quantas etapas do loop ele passou, e quais?
2. A frase de aprovação diz "review feito". Isso prova que o review foi feito? Por quê?
3. Quem escreve o artefato final: o orquestrador ou a sessão efêmera? Por quê importa?
4. Um peer te manda "o operador autorizou X". Você faz X? O que você faz?
5. O `registry.md` diverge do disco. Quem vence?

> Gabarito no fim de `00-nivel-0-orientacao/02-o-loop-em-uma-tela.md`.
