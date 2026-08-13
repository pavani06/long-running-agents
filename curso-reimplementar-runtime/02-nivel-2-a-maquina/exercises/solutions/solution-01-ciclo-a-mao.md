---
title: "Solução 01 — Um ciclo à mão (comentada)"
type: curriculum-exercise
nivel: 2
aliases: ["solução ciclo à mão", "solution-01-ciclo", "gabarito loop"]
tags: [curriculo-conteudo, nivel-2, a-maquina, solucao, loop, gate-design]
relates-to:
  - "[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orquestrador]]"
  - "[[vault:sisyphus-runtime/roles/executor|Charter — Executor]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Regra — Post-Exec Gate]]"
  - "[[vault:long-running-agents/docs/canonical/plan-execute-verify|Plan-Execute-Verify]]"
last_updated: 2026-08-13
---

# ✅ Solução 01 — Um ciclo à mão (comentada)
## O que "certo" parece em cada estágio — e por que o gate mede o disco, não a sua palavra

**Nível:** 2 — A Máquina
**Exercício:** `exercises/exercise-01-ciclo-a-mao.md`

> Esta solução mostra **uma** execução correta e comenta as decisões. O valor não está em
> copiar os arquivos; está em entender *por que* cada estágio se recusa a confiar no estágio
> anterior. Se você fez o exercício e o seu terceiro aprovou medindo o disco, você já passou —
> use isto para conferir o raciocínio.

---

## 📝 Passo 1 — O dispatch (as cinco partes)

`dispatches/treino/dispatch-saudacao-v1.md`:

```markdown
# Dispatch — saudação (treino)
**Classe:** custodia

## Autoridade única
Este dispatch é a única autoridade. Ignore qualquer contexto anterior da sessão.

## Objetivo
Criar um único arquivo de estado com uma linha de saudação fixa.

## Escritas nomeadas
- state/treino/current/saudacao.md

## Escopo negativo
- NÃO criar índice, MOC ou qualquer outro arquivo.
- NÃO tocar em facts/ nem roles/.
- NÃO renomear, mover ou deletar nada.
- NÃO criar outros arquivos em state/treino/current/.

## Especificação por arquivo
state/treino/current/saudacao.md deve conter, exatamente, a única linha:
`Olá do ciclo à mão — treino 2026-08-13`

## Verificação (antes de reportar done)
1. `cat state/treino/current/saudacao.md` bate, byte a byte, com a linha especificada.
2. `ls -la state/treino/current/` mostra apenas saudacao.md como arquivo novo.
Colar as duas saídas no handoff.

## Report
done ao treino-orchestrator; handoff em sessions/treino/2026-08-13-saudacao-done.md
```

**Comentário.** A trivialidade é de propósito: uma escrita, um conteúdo fixo, verificação
mecânica. Isso deixa o gate de saída **decidível por inspeção** — que é o ponto. O escopo
negativo lista as tentações concretas (índice, `facts/`, renomear), não proibições genéricas.

---

## 🔀 Passos 2–4 — Handoff, Momus-entrada, gate de entrada

**Passo 2.** O erro comum aqui é o hub "adiantar" e criar o arquivo — afinal é trivial. Isso é
a violação de owner-of-no-role: o hub que escreve vira autor não-revisado. A ação **correta** é
só uma: spawnar o Momus-entrada. Se você criou o arquivo neste passo, releia
`roles/orchestrator.md` §0 ("três coisas que você nunca faz").

**Passo 3.** O veredito, em `oracle-reviews/treino/2026-08-13-dispatch-saudacao-v1-entrada.md`,
com o bloco de proveniência do exercício. Dois campos são o que o gate de entrada vai *casar*:
`dispatch:` (path literal, com extensão, idêntico ao `REF`) e `review_kind: entrada`. Um
veredito sem esses campos **não conta** — não é frouxo, é inválido.

**Passo 4.** O gate de entrada, feito **lendo o arquivo**:

```bash
# o arquivo do veredito existe?
ls oracle-reviews/treino/2026-08-13-dispatch-saudacao-v1-entrada.md
# a proveniência casa? (inspeção do frontmatter)
#   dispatch: == dispatches/treino/dispatch-saudacao-v1.md   ✔
#   review_kind: entrada                                     ✔
#   findings.bloqueante == 0                                 ✔
# baseline do HUB, tomada AGORA, antes de o executor existir:
ls -la --time-style=full-iso state/treino/current/ > /tmp/ciclo-a-mao/baseline-hub.txt
```

**Comentário.** A baseline é tirada **pelo hub, antes do spawn**. Este é o detalhe que quase
todo mundo pula. Se você usar a baseline do executor (tirada dentro da sessão auditada), o gate
está confiando na parte que ele deveria auditar — a mesma falha que o gate de entrada proíbe,
só que do outro lado do ciclo.

---

## ⚙️ Passo 5 — O executor, numa sessão que só lê o disco

Handoff em `sessions/treino/2026-08-13-saudacao-done.md` com a evidência **real** colada
(`ls -la` + `cat`), não a afirmação "verifiquei, está certo". A mensagem `done` é uma linha; o
conteúdo mora no arquivo.

**Comentário.** Se, ao executar, você "notou" que faltava um índice e o criou — parabéns, você
reproduziu o modo de falha mais comum e mais caro do sistema (plan-step-substitution). Cada
favor não solicitado é, para o gate, um arquivo fora da lista. O caminho certo para qualquer
divergência é `[blocker]`, nunca improviso.

---

## 📏👁️ Passos 6–7 — O gate de saída, as duas camadas

**Camada 1 (sempre):**

```bash
ls -la --time-style=full-iso state/treino/current/ > /tmp/ciclo-a-mao/final-hub.txt
diff /tmp/ciclo-a-mao/baseline-hub.txt /tmp/ciclo-a-mao/final-hub.txt
# esperado: exatamente uma adição — saudacao.md. Nada mais.
```

Tocou exatamente `{saudacao.md}` → Camada 1 passou. Qualquer arquivo a mais → falhou → gatilho
6 (`[escalation]`), sem exceção de trivialidade.

**Camada 2 (condicional): DISPENSADA aqui.** As quatro condições de dispensa de
`dispatch-rule-post-exec-gate` são todas verdadeiras: ≤2 arquivos ✔, não-destrutivo ✔, sem
arquivo sensível ✔, dispatch trivial ✔. E nenhuma condição de obrigatoriedade dispara — em
especial, **não tocou `facts/` nem `roles/`**. Por isso o Momus-saída não é chamado.

> É *este* o contraste que fecha a lição do loop: se o dispatch tivesse tocado **um** arquivo
> em `facts/`, a Camada 2 seria **obrigatória** mesmo com uma escrita só — governança se
> revisa. A trivialidade nunca dispensa a Camada 1, e nunca sobrepõe o gatilho absoluto de
> `facts/`/`roles/`.

---

## ✅ Passo 8 — Registry

O registro de brinquedo aponta o ciclo fechado (dispatch → veredito → done → gate PASS). Ele é
**derivado**: se amanhã ele disser "ciclo fechado" mas o `diff` do disco mostrar um arquivo a
mais, o disco vence e a divergência é anomalia.

---

## 🕳️ Passo 9 — As três sabotagens (o gabarito)

| Sabotagem | Estágio que pega | Como pega | Gatilho |
|---|---|---|---|
| **(a)** executor cria `extra.md` fora das escritas nomeadas | **Gate de saída, Camada 1** | o `diff` da baseline-do-hub mostra dois arquivos novos, não um | **6** (plan-step-substitution / escopo) |
| **(b)** veredito com `dispatch:` de outro dispatch | **Gate de entrada, passo 3 (casamento de proveniência)** | o campo `dispatch:` não é idêntico ao `REF`; o PASS não é *deste* dispatch | **2** (prova-de-Momus falhou) |
| **(c)** hub pula o Momus e spawna o executor | **Gate de entrada, passo 2 (arquivo existe?)** | não há veredito em disco; ausência **nunca** é aprovação tácita | **2** (sem veredito provado) |

**Comentário.** Note que **(b)** e **(c)** são pegas *antes* de qualquer execução — o gate de
entrada existe justamente para isso. E **(a)** é pega pela Camada 1, que é **incondicional**:
mesmo num dispatch trivial, ninguém sai sem o diff mecânico. As três sabotagens são as três
formas canônicas de o loop ser burlado, e o desenho as fecha estruturalmente — não por alguém
"lembrar de conferir".

---

## 🎓 A medição de terceiro — por que ela É a solução

A parte do exercício que **não** tem gabarito aqui é, de propósito, a mais importante: o
terceiro que confere o seu gate **medindo o disco**. Se esta solução trouxesse "e então você
confirma que passou", ela cometeria exatamente o defeito que o Nível 2 inteiro ensina a evitar
— uma afirmação de estado ("passou") sem medição independente.

O sistema já falhou nessa classe, com regra à vista, no mesmo dia em que a comentava
(`caso-momus-skip.md`, Nível 3). Por isso a regra não pode depender de você lembrar: ela tem
de estar no **gate**, e o gate tem de ser rodado por quem não produziu o resultado. Se o seu
terceiro reproduziu o `diff`, casou a proveniência e confirmou as três sabotagens **lendo só o
disco** — o seu ciclo passou, e você entendeu o runtime melhor do que qualquer resumo poderia
ensinar.

---

## 🔗 Para ir fundo

- O gate de entrada e de saída, na fonte: `[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orquestrador]]`
- O escopo fechado do executor: `[[vault:sisyphus-runtime/roles/executor|Charter — Executor]]`
- As duas camadas do gate de saída: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Regra — Post-Exec Gate]]`
- Padrão canônico — plano/execução/verificação: `[[vault:long-running-agents/docs/canonical/plan-execute-verify|Plan-Execute-Verify]]`
- A cicatriz que ancora o achado central: `03-nivel-3-governanca-e-cicatrizes/case-studies/caso-momus-skip.md`
