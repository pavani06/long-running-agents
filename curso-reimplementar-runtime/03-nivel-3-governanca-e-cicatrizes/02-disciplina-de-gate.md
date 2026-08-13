---
title: "Disciplina de gate: medir o disco, não ler a promessa"
type: curriculum-lesson
nivel: 3
aliases: ["disciplina de gate", "gate mede o disco", "mtime provenance", "placeholder pareado", "duas camadas do post-exec-gate"]
tags: [curriculo-conteudo, nivel-3, governanca, gate-design, mtime, md5, placeholder, post-exec-gate, garantia-estrutural]
relates-to:
  - "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Rule: Post-Exec Gate]]"
  - "[[vault:sisyphus-runtime/facts/_global/gate-mtime-provenance|Gate: mtime — proveniência, nunca integridade]]"
  - "[[vault:sisyphus-runtime/facts/_global/gate-placeholder-pareado|Gate: placeholder pareado]]"
  - "[[vault:sisyphus-runtime/facts/_global/incident-2026-07-22-recon-gate-reinterpretation|Incident: recon gate reinterpretation]]"
  - "[[vault:long-running-agents/docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]"
last_updated: 2026-08-13
---

# 📏 Disciplina de gate: medir o disco, não ler a promessa
## mtime é proveniência, hash é integridade, e o gate que se auto-arquiva sem se auto-reprovar

**Tempo Estimado:** 55 minutos
**Nível:** 3 — Governança e Cicatrizes
**Pré-requisito:** `01-a-familia-de-regras.md`
**Status:** 🔴 CRÍTICO — sem esta lição, os gates que você escrever vão medir a coisa errada
**Cicatriz de origem:** `incident-2026-07-22-recon-gate-reinterpretation` (o gate que se auto-disparava) + os adendos do `gate-mtime-provenance`

---

## 📖 Prólogo: o gate que reprovava a própria documentação

Um preflight tinha um check simples de higiene: *nenhum placeholder de operador pode
ficar em aberto no artefato final*. Placeholders eram marcados com um par de caracteres —
uma abertura e um fechamento. O gate contava as aberturas: se achasse alguma, reprovava.
`EXPECT 0`.

Um dia o gate disparou. Três hits. A sessão parou, escalou, gastou atenção — e a
investigação achou o culpado: os três hits eram o **próprio comando do gate**, citado na
documentação que descrevia o gate. O caractere de abertura aparecia ali, solto, dentro do
texto que *explicava* como o check funcionava.

Um placeholder de operador em aberto é sempre um **par**: abertura, conteúdo, fechamento.
Um caractere de abertura solto, dentro de um comando documentado, não é ato em aberto — é
documentação. Mas o gate contava o caractere solto, então não sabia distinguir os dois. E,
pior, **um relatório que arquivasse o comando do gate se auto-reprovava** — o que forçava
o operador a contornar o gate para poder documentá-lo, reabrindo exatamente o modo de
falha que o gate existia para fechar.

A correção foi um gate de forma **pareada** (só conta abertura *seguida de* fechamento),
**octal** e **`LC_ALL=C`** — de modo que o próprio comando do gate, contendo só escapes
octais e nenhum colchete literal, pudesse ser arquivado verbatim sem tropeçar em si mesmo.

> O gate deixou de depender de disciplina — de alguém *se lembrar* de não documentá-lo — e
> virou estrutura. É a mesma lição do T5c, num instrumento diferente: **garantia
> estrutural sobre processo compliance-dependente.**

A cicatriz completa vive no vault: `[[vault:sisyphus-runtime/facts/_global/incident-2026-07-22-recon-gate-reinterpretation]]`.

---

## 🧠 O conceito: um gate faz uma pergunta ao disco, e o disco responde sozinho

O `GLOSSARY` define o gate como *o ponto de verificação que mede o disco (não lê promessas)
para decidir se um artefato passa*. Toda a lição 02 desdobra essa frase. Um gate bem
projetado tem três propriedades, e a terceira é a que quase todo mundo esquece:

1. **Mede o estado verificável**, não a asserção do artefato sobre si mesmo.
2. **Falha fechado** — na ausência de sinal, trata como não-válido e retorna ao operador;
   nunca assume "passou" por default.
3. **Não se corrompe ao ser documentado** — pode ser citado verbatim num relatório sem se
   auto-disparar.

Os dois gates canônicos do runtime — `mtime` e `placeholder-pareado` — existem para ensinar
onde essa disciplina escorrega.

---

## ⏱️ Camada de fatos: mtime é proveniência, hash é integridade

O gate `mtime` responde a **uma** pergunta, e apenas uma:

```
mtime > T_ref   →  este arquivo é DESTA execução   (sujeito ao gate)
mtime ≤ T_ref   →  este arquivo é pré-existente     (fora do gate)
```

onde `T_ref` é capturado **uma vez, no início da execução, antes da primeira escrita**
(canonicamente `date +%s` ou o mtime de um arquivo-sentinela do preflight), e é **imutável**
durante a execução. A fronteira de empate (`mtime == T_ref`) conta como **pré-existente** —
inclusiva no lado `≤`, para não haver corrida entre a captura de `T_ref` e a criação do
sentinela.

O erro que este gate existe para prevenir é confundir **proveniência** com **integridade**:

| A pergunta | A ferramenta | A propriedade |
|---|---|---|
| "este arquivo é desta execução?" | **mtime** | mutável, barata, suficiente para *triagem de proveniência* |
| "este arquivo tem o conteúdo esperado?" | **hash** (sha256/md5) | imutável, cara, necessária para *integridade* |

Confiar em mtime para integridade dá **falso positivo** — um `touch -r` preserva o mtime de
um arquivo editado. Confiar em hash para proveniência é caro e desnecessário. O gate usa o
barato para triagem e o caro só quando integridade é o requisito. E ele **falha fechado**:
se o mtime está ausente ou ilegível, o gate não chuta — trata como não-válido e devolve ao
operador o que observou.

> **A regra de ouro do `gate-mtime-provenance`: mtime nunca é garantia de integridade de
> conteúdo. Se você precisa saber que o conteúdo é o esperado, hash. Se precisa só saber de
> onde o arquivo veio, mtime.** Confundir os dois é o modo de falha.

---

## 🔤 O gate que não se auto-reprova

O `gate-placeholder-pareado` é a lição do prólogo cristalizada. As três propriedades que a
forma final (octal, `LC_ALL=C`, pareada) garante:

1. **Distingue par de solto.** Só conta abertura *seguida de fechamento*. O caractere solto
   da documentação é ignorado — teria evitado o incidente inteiro.
2. **Locale-independente.** `LC_ALL=C` torna a busca byte-orientada; funciona em qualquer
   shell, não só UTF-8. A variante que dependia de codepoint PCRE quebrava em locale POSIX.
3. **Auto-arquivável — o ponto estrutural.** O comando não contém colchete literal, só
   escapes octais. Um relatório arquiva o comando verbatim sem se auto-reprovar. As formas
   antigas se auto-disparavam quando documentadas — e um gate que força seu documentador a
   contorná-lo *não é mais um gate*.

O gate se aplica a **templates** (specs com placeholders a preencher) e a **saídas de
execução** (rede de segurança de vazamento — deve ser 0 por construção). Não se aplica a
facts que *discutem* a sintaxe do placeholder — a documentação da convenção fica fora do
escopo do gate. **O gate mede templates e saídas, não a documentação de si mesmo.**

`[[vault:sisyphus-runtime/facts/_global/gate-placeholder-pareado|Gate: placeholder pareado]]`

---

## 🧱 As duas camadas do post-exec-gate

Toda essa disciplina de medição se organiza no gate de saída, que tem **duas camadas com
regimes diferentes** (`dispatch-rule-post-exec-gate`):

### Camada 1 — diff mecânico de escritas nomeadas: SEMPRE

Incondicional. Todo dispatch executado — sem exceção de tamanho, trivialidade ou confiança —
tem o conjunto de arquivos tocados comparado contra a lista de **escritas nomeadas** do
dispatch. Como o vault não tem git, a evidência é **mtime + listagem** contra uma baseline
tomada *antes* da execução (o executor toma essa baseline como primeiro ato).

- Tocou **exatamente** as escritas nomeadas → passou.
- Tocou **algo fora** → falhou → escala (gatilho 6, suspeita de plan-step-substitution).
- **Faltou** uma escrita nomeada, sem `blocker` → falhou → escala.

É barata e mecânica. É o que torna "dispatch trivial" uma categoria *segura* de existir:
mesmo dispensando o Momus-saída, ninguém sai sem o diff. Note que a Camada 1 é exatamente o
gate `mtime` aplicado: proveniência ("o que esta execução tocou?"), não integridade.

### Camada 2 — Momus-saída: condicional

Dispensada **só** se **TODAS** forem verdadeiras: ≤ 2 arquivos, não-destrutivo, nenhum
arquivo sensível, dispatch trivial. Obrigatória se **QUALQUER** for verdadeira: toca código,
config ou regra; fase destrutiva ou sensível; mais de 2 escritas substantivas; aprovado com
reservas na entrada; **qualquer escrita em `facts/` ou `roles/`** (governança se revisa). As
conjunções são literais — dispensa exige *todas*, obrigatoriedade basta *uma*. Na dúvida:
**obrigatório**, porque o custo é assimétrico.

> **Por que a Camada 1 nunca desce.** Ela responde a uma pergunta binária e barata — "o
> executor saiu do escopo?" — que é a assinatura do modo de falha mais caro do sistema. Um
> gate que às vezes não roda não detecta o caso em que mais importaria, e a economia de
> rodá-lo é aproximadamente zero.

`[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Post-Exec Gate]]`

---

## 🔎 O elo com a lição anterior — e a próxima

A lição 01 disse que *garantia estrutural vence obediência*. A lição 02 mostra a mecânica:
uma garantia estrutural é um **gate que mede o disco** de um jeito que não dá para narrar em
volta. mtime não acredita numa promessa de proveniência — ele lê o carimbo. O diff da Camada
1 não acredita em "só toquei o que devia" — ele lista e compara. O placeholder pareado não
acredita em "limpei os placeholders" — ele conta os pares.

A lição 04 vai fechar o argumento: mostrar o dia em que três sessões, todas com a regra à
vista, afirmaram estados que o disco não sustentava — prova empírica de que a medição tem de
estar **no gate**, nunca na memória de quem escreve.

---

## 🧪 Exercício

**Contexto.** Você está escrevendo os gates do seu runtime reimplementado.

1. **Separe as duas perguntas.** Pegue um gate seu que hoje use mtime. Ele está perguntando
   *proveniência* ("é desta execução?") ou *integridade* ("o conteúdo está certo?")? Se for
   o segundo, ele tem um falso positivo esperando: demonstre-o com `touch -r`.
2. **Auto-arquive.** Escreva um gate de higiene (ex.: "nenhum placeholder em aberto") e
   depois cole o comando dele dentro do próprio relatório de execução. O gate reprova o
   relatório? Se sim, reescreva-o para a forma auto-arquivável (dica: escapes octais,
   `LC_ALL=C`, forma pareada) e prove que agora ele ignora a própria citação.
3. **Falhe fechado.** Force o sinal a sumir (arquivo ausente, permissão negada). Seu gate
   assume "passou", assume "reprovou", ou retorna ao operador com o observado? Só a terceira
   está correta.

**Critério de aprovação (medição de terceiro):** outra pessoa roda seus três gates — inclusive
o caso `touch -r` do passo 1 e a auto-citação do passo 2 — e confirma que (a) o gate de mtime
não é enganado por conteúdo editado com carimbo preservado, e (b) o gate de higiene não se
auto-reprova ao ser documentado.

---

## 🔗 Para ir fundo

- Cicatriz do gate que se auto-disparava (privada): `[[vault:sisyphus-runtime/facts/_global/incident-2026-07-22-recon-gate-reinterpretation]]`
- mtime como proveniência: `[[vault:sisyphus-runtime/facts/_global/gate-mtime-provenance]]`
- Placeholder pareado: `[[vault:sisyphus-runtime/facts/_global/gate-placeholder-pareado]]`
- As duas camadas: `[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate]]`
- Próxima lição: `03-a-regra-do-rele.md`
