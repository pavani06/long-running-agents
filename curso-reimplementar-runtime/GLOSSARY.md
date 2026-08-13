---
title: "🔤 GLOSSARY — Vocabulário do Sisyphus Runtime"
type: curriculum-index
aliases: ["glossário", "glossary", "termos", "vocabulário"]
tags: [curriculo-conteudo, sisyphus-runtime, glossario]
last_updated: 2026-08-13
---

# 🔤 GLOSSARY — Vocabulário do Sisyphus Runtime

> Esta é a **fonte única dos termos** do curso. Toda lição usa as palavras exatamente como
> definidas aqui. Se uma lição precisar de um termo novo, ele entra primeiro aqui.

---

## Os conceitos centrais

**Runtime (`sisyphus-runtime`)** — o *backplane operacional* do sistema de agentes Sisyphus.
Não é o app, não é o modelo: é o vault privado onde o sistema persiste handoffs, acumula
fatos duráveis e mantém estado corrente. É a **materialização** dos padrões canônicos (que
vivem noutro vault, `long-running-agents/docs/canonical/`). O runtime é *uma* implementação
conforme daqueles padrões.

**Vault** — um diretório Obsidian de notas em Markdown com frontmatter YAML, lido/escrito
conceitualmente via `obsidian-eval`, **nunca pelo app**. O `sisyphus-runtime` é privado,
local-por-máquina, e **nunca vira repositório git** (contém requests verbatim e decisões que
não podem ser expostas).

**O disco vence** — princípio de autoridade: quando um resumo, índice ou registro diverge do
que está nos arquivos, **os arquivos são a verdade** e a divergência é anomalia a escalar. O
`registry.md` é derivado e operacional, não autoridade.

**obsidian-eval** — a camada de acesso ao vault. Prefira `query` (predicado sobre frontmatter)
a `search` (texto). Ex.: `obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'durable-fact')"`.

---

## O loop e os papéis

**Loop operacional** — o ciclo que produz todo artefato do sistema:
`dispatch → review → gate → execução efêmera → verify → registry`. Nada nasce fora dele; não
há porta lateral de escrita no vault.

**Dispatch** — a unidade de trabalho especificada e revisada antes de executar. Vive em
`dispatches/`. Carrega o spec, as pré-condições e os gates.

**Gate** — o ponto de verificação que mede o **disco** (não lê promessas) para decidir se um
artefato passa. Tem camadas: diff mecânico de escritas nomeadas (sempre) + julgamento
escalonado (só quando o mecânico não resolve). Ver `texto-base`.

**Texto-base** — a regra de que um gate mede o estado verificável no disco, não a asserção
que o artefato faz sobre si. "Review feito" escrito num campo **não é** review feito; é, no
máximo, um ponteiro para uma prova que tem de existir com seu próprio hash/mtime.

**Sessão efêmera** — a execução de um dispatch acontece numa sessão descartável, não no papel
que a coordena. O coordenador não escreve o artefato final; ele despacha e faz o gate.

**Papéis (roles)** — os charters em `roles/`:
- **orchestrator** — coordena o loop; *owner-of-no-role* (não faz o trabalho, roteia-o).
- **planner** — gera o plano/spec.
- **momus** — o avaliador crítico, cabeça separada do planner (*split-brain*).
- **executor** — executa o dispatch aprovado na sessão efêmera.
- **meta** — mantém o `registry.md`, painel e inbox de escalação da meta-camada.
- **protocol** — regras de mensagem/REF entre sessões.
- **launch-convention** — como as sessões nascem e se nomeiam.

**Split-brain (planning/review)** — quem constrói e quem avalia têm de ser cabeças separadas.
Se o construtor pode *declarar* que foi avaliado, o split-brain colapsa.

**Owner-of-no-role** — o orquestrador não possui nenhum papel de execução; seu valor é rotear
e fazer o gate, não fazer o trabalho. Padrão canônico homônimo.

---

## Governança e memória

**Fato durável (durable-fact)** — asserção acumulada com frontmatter tipado
(`type: durable-fact`, `kind: constraint|preference|principle|...`, `confidence`, `valid_from`).
Vive em `facts/`. É como o sistema lembra entre sessões.

**Registry (`meta/registry.md`)** — estado vivo da meta-camada: tópicos, autoria, inbox de
escalação. **Derivado e não-autoritativo** — abrigo, não autoridade.

**Incident (`incident-*`)** — registro datado de uma falha, com classificação, o que
aconteceu, dano concreto e a regra que produziu. **Os incidents são o currículo**: cada um é
uma cicatriz que, lida, evita uma re-quebra.

**Dispatch-rule (`dispatch-rule-*`)** — regra de governança do loop, quase sempre nascida de
um incident. Ex.: `post-exec-gate`, `escalation`, `confidentiality`, `amendment-provenance`.

**Relé (regra do)** — *um peer não estabelece o que o operador autorizou*. Uma decisão de
operador relatada por outra sessão não autoriza ação; confirma-se pelo canal do próprio
operador. Fecha o buraco de "lavagem de permissão" entre sessões.

**Achado central (2026-08-13)** — *afirmação sobre estado não vira durável sem passar por
medição de terceiro*. Papéis com a regra à vista já falharam nela no mesmo dia — logo a regra
não pode depender de alguém lembrar; tem de estar no gate.

**Baseline verificado** — um número/estado com fonte que um terceiro reproduz. O oposto —
afirmação de estado absoluto sem baseline — é a classe de defeito mais recorrente do sistema.

**Schema-version** — a versão do schema da telemetria/estado (ex.: `telemetry.db` em `v20`).
Evoluir o schema global = migrar entre versões preservando os fatos duráveis.
