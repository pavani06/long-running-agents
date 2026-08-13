---
title: "🔁 Curso: Reimplementar o Sisyphus Runtime"
type: curriculum-index
aliases: ["reimplementar runtime", "runtime reimplementation course", "continuidade runtime", "overview"]
tags: [curriculo-conteudo, sisyphus-runtime, reimplementacao, continuidade]
relates-to: ["[[QUICK_START|Quick Start]]", "[[INDEX|Índice]]", "[[GLOSSARY|Glossário]]"]
last_updated: 2026-08-13
---

# 🔁 Curso: Reimplementar o Sisyphus Runtime

> Pegar um humano que nunca viu este sistema e deixá-lo capaz de **reconstruir o
> `sisyphus-runtime` do zero em outra máquina** — e de evoluir o schema global depois.

**Público:** um engenheiro humano · **Objetivo duplo:** seguro de continuidade + base para evoluir o schema · **Formato:** curso por etapas, no molde de `long-running-agents/curriculum`

---

## 🎯 A tese do curso

O `sisyphus-runtime` não é um conjunto de arquivos — é um **procedimento** que se materializou
em arquivos. Copiar o vault não reimplementa o sistema. Reimplementar é reconstruir o **loop**
(`dispatch → review → gate → execução efêmera → verify → registry`), os **papéis** que o rodam,
e a **disciplina de gate** que impede o sistema de mentir para si mesmo.

**O que torna este curso diferente do currículo do KODA:** lá, os prólogos eram histórias
semi-ficcionais. Aqui, **cada prólogo é uma cicatriz real** — um `incident-*` datado do próprio
vault. As cicatrizes é que se transmitem; um reimplementador que lê os incidents não re-quebra o
que o sistema já aprendeu a caro.

## 🔀 Modelo híbrido (público + privado)

Este curso é **híbrido**, por design:

- **A matéria — arquitetura e procedimento — é compartilhável** e pode viver em repo público
  junto do `curriculum/`. Os prólogos são **sanitizados**: ensinam a cicatriz sem os requests
  verbatim privados.
- **As cicatrizes completas ficam no vault privado** e são acessadas por **wikilink**
  (`[[vault:sisyphus-runtime/...]]`), que só resolve para quem tem o vault. Quem tem a máquina
  lê o incident inteiro; quem tem só o repo aprende a lição sem o verbatim.

Regra de ouro, herdada do vault: **o curso aponta, não copia.** A única pasta feita para ser
copiada é `08-tools-templates/`.

---

## 🚀 Comece Aqui

| Se você… | Vá para |
|---|---|
| 🆕 nunca viu o Sisyphus | `Nível 0`, na ordem |
| 🔧 vai reconstruir numa máquina nova | `Nível 0 → 1 → 2`, depois `Nível 4` |
| 🧬 vai **evoluir o schema global** | `Nível 3` (governança) → `Nível 4 · lição 03` |
| 🚑 precisa retomar um sistema em pé | `QUICK_START.md`, caminho "retomada" |
| 🔤 travou num termo | `GLOSSARY.md` |

---

## 🗺️ Os cinco níveis

| Nível | Nome | O que você sai sabendo | Tempo |
|---|---|---|---|
| **0** | Orientação | O que é o runtime e o loop numa tela | ~30 min |
| **1** | O substrato | A camada de dados: vault, fatos duráveis, estado, `obsidian-eval` | 3–4 h |
| **2** | A máquina | Os papéis e o loop `dispatch → gate` rodando | 4–5 h |
| **3** | Governança e cicatrizes | Por que cada regra existe — via incidents reais | 5–6 h |
| **4** | Reimplementar e evoluir | Reconstruir do zero + evoluir o schema global | 6–8 h |

O **Nível 3 é o coração**: é onde a memória de cicatriz se transmite. O **Nível 4 é o objetivo**:
reimplementação + o seu segundo alvo, evoluir o schema.

---

## 📁 Estrutura

Ver `INDEX.md` para o mapa completo com dependências entre lições. Esqueleto:

```
curso-reimplementar-runtime/
├── README.md · QUICK_START.md · GLOSSARY.md · INDEX.md
├── 00-nivel-0-orientacao/
├── 01-nivel-1-substrato/         (+ exercises/)
├── 02-nivel-2-a-maquina/         (+ exercises/)
├── 03-nivel-3-governanca-e-cicatrizes/  (+ case-studies/ + exercises/)
├── 04-nivel-4-reimplementar-e-evoluir/  (+ case-studies/ + real-world-exercises/)
└── 08-tools-templates/           (templates/ + skeleton/ — feito para copiar)
```

---

## ✅ Como o curso se auto-verifica

Coerente com o achado central do próprio sistema — *afirmação sobre estado não vira durável
sem medição de terceiro* — os exercícios **não são auto-aprovados**. Cada exercício-chave só
"passa" quando outra pessoa (ou outra sessão) roda o seu resultado contra o caso de teste e
confirma. Você não aprova o próprio trabalho; esse é o ponto pedagógico inteiro.
