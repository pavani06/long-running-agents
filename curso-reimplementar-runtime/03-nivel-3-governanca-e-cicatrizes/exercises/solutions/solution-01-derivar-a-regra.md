---
title: "Solução comentada: derivar a regra e escrever o gate que a pega"
type: curriculum-exercise
nivel: 3
aliases: ["solução derivar a regra", "solution regra e gate", "fecho datado"]
tags: [curriculo-conteudo, nivel-3, governanca, exercicio, solucao, gate-design, fecho, medicao-de-terceiro]
relates-to:
  - "[[vault:sisyphus-runtime/meta/registry.md|Registry — a nota sobre fechos]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Rule: Amendment Provenance]]"
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
last_updated: 2026-08-13
---

# 🗝️ Solução comentada: derivar a regra e escrever o gate que a pega
## Uma resposta correta — não a única — com os erros mais comuns anotados

**Status:** solução do `exercise-01-derivar-a-regra.md`. Leia só depois de ter tentado as
quatro partes. A solução vale pelo *contraste* com a sua, não como gabarito a copiar.

---

## Parte 1 — Classificação (uma resposta correta)

Este **não** é um caso de fato falso; é um **fecho que envelheceu**. A distinção é o núcleo,
e vem direto da nota do `registry.md` sobre fechos:

> **Uma lista datada é verdadeira para sempre. Uma lista sem data afirma um presente que não
> pode sustentar.** A data não valida o fecho — ela apenas o torna honesto: converte *"esta é
> a lista"* em *"esta era a lista às HH:MM"*.

*"Todos os 12 tópicos migrados para v20"* é uma afirmação sobre o **mundo**, e falsifica no
instante em que o mundo ganha um 13º tópico. *"Os 12 tópicos existentes em 2026-08-13 10:00
estavam em v20"* é uma afirmação sobre um **instante**, e é verdadeira para sempre.

Por que a distinção muda a correção: se fosse fato falso, a correção seria "meça melhor". Sendo
um fecho, nenhuma medição no instante da escrita conserta — a frase estava certa quando
escrita. O que falha é a frase **pretender completude sobre uma população que ainda vai
mudar**. Isto é o achado central da lição 04 na sua forma mais pura: *afirmação sobre estado
não vira durável sem passar por medição de terceiro* — e um fecho é o tipo de afirmação que só
uma **enumeração independente da população**, refeita no momento da leitura, pode validar.

**Erro comum na Parte 1:** classificar como "erro de contagem" ou "descuido". Não houve erro de
contagem — o 12 estava certo. Quem classifica assim vai escrever uma regra sobre *contar com
cuidado*, que não pega nada, porque a próxima contagem também estará certa no instante em que
for feita.

---

## Parte 2 — A regra (uma formulação correta)

### Dispatch Rule: Fechos se datam ou se enumeram — nunca se afirmam

**Rule.** Toda afirmação de **completude ou totalidade** num artefato durável ("todos", "os N",
"completo", "migração encerrada") **declara sua data e a fonte independente pela qual a
população referente é enumerável** — ou é reescrita como um recorte datado ("os N existentes em
`<data/mtime>`"). Um fecho absoluto sem data e sem fonte de enumeração é defeito de proveniência
e é bloqueado na saída. *Justificativa ou boa-fé não o salvam; a data ou a fonte, sim.*

**Rationale.** Um fecho é a única parte de um artefato que **não se verifica olhando para o
artefato** — porque fala do que *não* está ali (os itens que faltariam). Verdadeiro quando
escrito, ele envelhece sozinho quando a população cresce, sem que ninguém o edite. Datá-lo não
o completa: **troca um fecho por um recorte** — de uma afirmação sobre o mundo (que falsifica)
para uma sobre um instante (que não). Quando a população é enumerável por fonte independente
(um `query` no disco), o leitor pode **revalidar o fecho no momento da leitura** em vez de
herdar a confiança de quem o escreveu.

**What qualifies (fecho que precisa de data/fonte).**
- "Todos os N itens em estado X."
- "Migração/varredura/cobertura completa."
- Qualquer contagem apresentada como totalidade de uma população que pode crescer.

**What does NOT qualify.**
- Recorte já datado: "os 12 tópicos existentes em 2026-08-13 estavam em v20".
- Afirmação sobre um item singular e imutável ("o tópico `ciot` está em v20") — não é fecho.
- Enumeração acompanhada do comando que a produz ("`query ... → 12/12`, rodado em ...").

**Enforcement `both`.** *Agent:* ao escrever um fecho num artefato durável, ou o data, ou anexa
a fonte de enumeração, ou o reescreve como recorte. *Operator:* ao ler um fecho sem data numa
decisão, pede a fonte antes de agir sobre ele.

**Comentário.** Note a forma **estrutural**, não exortativa. A regra não diz "cuidado com
resumos"; ela remove a *opção* de escrever um fecho absoluto — ou você data, ou você enumera,
ou você recorta. As três alternativas são verificáveis; "ter cuidado" não é.

**Erro comum na Parte 2:** escrever uma regra que manda *re-verificar o índice periodicamente*.
Isso reintroduz a dependência de alguém lembrar — a exata falha da lição 04. A regra tem de
mudar a **forma da afirmação** (datada/enumerável), não agendar vigilância humana sobre ela.

---

## Parte 3 — O gate (uma implementação correta)

O gate **não lê o índice**. Ele enumera a população pelo disco e compara. Suponha que cada
tópico tenha seu `schema-version` no frontmatter de `state/<topico>/current/schema.md` (ou
equivalente no seu runtime). O gate pergunta ao disco *quantos tópicos existem* e *quantos estão
em v20* — e derruba a afirmação de completude se os dois números não casarem.

```bash
#!/usr/bin/env bash
# Gate: fecho de migração v20. EXPECT: exit 0 (todos os tópicos em v20).
# Mede a população pelo disco; NÃO lê a frase do índice.
set -euo pipefail

STATE_DIR="${1:?uso: gate-fecho-v20.sh <state_dir>}"

# Fonte independente: enumera todo state/<topico>/current/schema.md existente AGORA.
mapfile -t schemas < <(find "$STATE_DIR" -type f -path '*/current/schema.md' | sort)

# Fail-closed: sem população enumerável, NÃO conclua "completo".
if [ "${#schemas[@]}" -eq 0 ]; then
  echo "GATE-INDETERMINADO: nenhum schema.md encontrado sob $STATE_DIR — retornar ao operador" >&2
  exit 2
fi

total=0; em_v20=0; atrasados=()
for f in "${schemas[@]}"; do
  total=$((total+1))
  # extrai o campo schema_version do frontmatter, locale-independente
  v="$(LC_ALL=C grep -m1 -E '^schema_version:' "$f" | LC_ALL=C sed 's/^schema_version:[[:space:]]*//')"
  if [ "$v" = "v20" ]; then
    em_v20=$((em_v20+1))
  else
    atrasados+=("$f => ${v:-<ausente>}")
  fi
done

echo "populacao medida no disco: $total | em v20: $em_v20 | data: $(date -u +%FT%TZ)"

if [ "$em_v20" -ne "$total" ]; then
  echo "GATE-FAIL: fecho de completude falso — $((total-em_v20)) tópico(s) fora de v20:" >&2
  printf '  %s\n' "${atrasados[@]}" >&2
  exit 1
fi
echo "GATE-PASS: $em_v20/$total em v20 (recorte válido nesta medição)"
```

Por que este gate satisfaz os três requisitos:

1. **Enumera por fonte independente.** A população vem de `find ... schema.md` — o disco *agora*
   — não do "12" que o índice declara. Um 13º tópico novo entra na contagem automaticamente,
   então o fecho "todos os 12" não sobrevive a ele.
2. **Falha fechado.** Sem nenhum `schema.md`, o gate sai com código `2` (indeterminado) e manda
   ao operador — não assume "completo por vacuidade". Um erro clássico é `[ "$em_v20" -eq "$total" ]`
   com `total=0` retornar sucesso: `0 -eq 0` é verdadeiro, e o gate aprovaria um estado vazio.
   O guard `-eq 0` fecha isso.
3. **Auto-arquivável.** O comando não contém o texto do fecho que procura; ele mede um campo de
   frontmatter. Pode ser colado num relatório sem se auto-disparar (lição 02). Usa `LC_ALL=C`
   para não depender de locale.

Observe o `echo` da linha de PASS: ele reporta *"recorte válido nesta medição"*, com a data —
o gate não emite um fecho absoluto sobre si mesmo. Ele produz exatamente o recorte datado que a
regra da Parte 2 exige.

**Erros comuns na Parte 3:**
- **Ler o índice.** `grep "Todos os 12" index.md` mede a promessa, não o disco. É o defeito que
  o exercício inteiro existe para expor.
- **Confiar na contagem declarada.** Comparar contra um `12` hardcoded (ou lido do índice) em
  vez de derivar o total do `find`. Se o total vem do artefato, um 13º item invisível ao gate
  passa despercebido — exatamente a quebra do incidente.
- **Fail-open.** Tratar "não achei schemas" como "nada a migrar, logo completo".

---

## Parte 4 — Vira gatilho de escalação?

**Não é preciso um gatilho novo, e reconhecer isso é a resposta certa.** A violação já cai na
**Camada 1 do `post-exec-gate`** se o gate acima for parte da rotina de saída de dispatches que
tocam `state/`, e sua reprovação encaminha ao **gatilho 6** (diff/medição mecânica de saída
falhou) da lista existente. Não há ponto de parada novo: há uma nova *medição mecânica* plugada
numa camada que já existe.

Se você propôs um gatilho novo, verifique se ele não é redundante — a lição da manutenção da
`dispatch-rule-escalation` é que **um gatilho que sempre resolve em "pode seguir" é ruído que
treina o operador a aprovar sem ler.** Só se justifica um gatilho novo quando a parada exige
**decisão humana** que a medição mecânica não resolve; aqui, a medição resolve sozinha (o disco
diz se todos estão em v20), então ela pertence à Camada 1, não à lista de escalação.

---

## 🧷 Sobre o critério de aprovação (por que ele fecha o círculo)

O exercício se recusa a ser auto-aprovado de propósito. Se você rodou o próprio gate contra o
próprio caso e disse "passou", você fez exatamente o que os papéis da lição 04 fizeram:
verificou fidelidade ("meu gate roda?") em vez de verdade ("meu gate pega um fecho falso que
*outra pessoa* plantou?"). Só a medição de terceiro — o revisor acrescentando um 13º tópico
`v19` e um índice que ainda diz "12" — prova que o gate mede o disco e não a promessa. **É a
lição inteira do Nível 3, aplicada à sua própria prova.**

---

## 🔗 Para ir fundo

- A nota do registry sobre fechos, datados × censo implícito (privada): `[[vault:sisyphus-runtime/meta/registry.md]]`
- "Gates são texto-base": `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance]]`
- As duas camadas e o gatilho 6: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate]]`
- Enunciado do exercício: `../exercise-01-derivar-a-regra.md`
