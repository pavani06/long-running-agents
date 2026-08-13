# 🌳 Skeleton — a árvore mínima do vault numa máquina nova

> Esta é a **única pasta do curso feita para ser copiada**. Ela materializa o *núcleo
> reproduzível mínimo* da lição `04-nivel-4/01`: as pastas que precisam existir para o
> loop rodar. **Copie a árvore — nunca os fatos.** Os `facts/`, `state/` e `roles/` da
> sua máquina nascem do *seu* loop; importar os do vault de referência é importar
> memória alheia.

## Como usar

```bash
VAULT=$(mktemp -d)          # ou o diretório definitivo da sua máquina
cd "$VAULT"
mkdir -p facts/_global state/current sessions catalog meta roles dispatches traces
```

Depois, siga o bootstrap da lição `02-bootstrap-nova-maquina.md`, na ordem verificável:
esqueleto → charters → registry magro → primeiro dispatch → primeiro ciclo.

---

## A árvore mínima, comentada

```
<vault>/
├── facts/                  # 🟢 NÚCLEO — a memória durável do sistema
│   └── _global/            #    fatos que valem para todos os tópicos.
│                           #    Aqui vivem: durable-facts, incident-*, dispatch-rule-*,
│                           #    e o index.md (derivado, escrito por último).
│                           #    Fatos de um tópico específico vão em facts/<topico>/.
│
├── state/                  # 🟢 NÚCLEO — o estado corrente do sistema
│   └── current/            #    "onde estou agora": handoff vivo, mandato da sessão.
│                           #    Sem isto, o loop não sabe retomar. (Archive: state/archive/.)
│
├── roles/                  # 🟢 NÚCLEO — os charters dos papéis do loop
│                           #    Mínimo p/ um ciclo honesto: orchestrator, planner,
│                           #    momus, executor. Governança completa acrescenta
│                           #    meta, protocol, launch-convention.
│                           #    É onde vive o SPLIT-BRAIN. Escrever aqui aciona o
│                           #    gate mais duro: "governança se revisa".
│
├── dispatches/             # 🟢 NÚCLEO — as unidades de trabalho especificadas
│                           #    Cada dispatch é revisado ANTES de executar. Organize
│                           #    por tópico: dispatches/<topico>/dispatch-<slug>.md.
│                           #    Nada nasce fora daqui — não há porta lateral de escrita.
│
├── meta/                   # 🟡 NÚCLEO OPERACIONAL — o painel da meta-camada
│   └── registry.md         #    estado vivo: tópicos, autoria, inbox de escalação.
│                           #    DERIVADO e NÃO-AUTORITATIVO: abrigo, não autoridade.
│                           #    O DISCO VENCE — se o registry diverge dos arquivos,
│                           #    os arquivos são a verdade. Comece magro; cresça atrás
│                           #    dos fatos, nunca à frente deles.
│
├── sessions/               # 🟡 substrato — o rastro das sessões (handoffs por tópico)
│                           #    sessions/<topico>/ acumula o histórico de execução.
│
├── catalog/                # 🟡 ACESSÓRIO — catálogos e insumos de dispatches concretos
│                           #    nasce conforme os dispatches o criam; não é pré-condição.
│
└── traces/                 # 🟡 ACESSÓRIO — telemetria e forense
                            #    enriquece o sistema (medir), não o habilita (rodar).
                            #    É aqui que vive o schema versionado (ex.: telemetry.db,
                            #    schema_version) da lição 03. O loop fecha sem traces;
                            #    mas você não MEDE o sistema sem eles.
```

## Pastas que aparecem no vault real e são acessórias

O vault de referência tem mais pastas — `oracle-reviews/`, `recon/`, `evidence/`,
`reminders/`, `prompts/`. **Nenhuma é pré-condição para o loop fechar.** Elas nascem
do trabalho:

- `oracle-reviews/<topico>/` — onde os **vereditos do Momus** são escritos (o produto do
  gate Camada 2). Você vai criá-la no primeiro dispatch que exigir momus-saída — o que,
  pela regra, é qualquer escrita em `facts/` ou `roles/`.
- `recon/`, `evidence/` — insumos e provas de dispatches específicos.
- `reminders/`, `prompts/` — ergonomia operacional.

## A regra de leitura desta árvore

Um **acessório nunca vira pré-condição de um gate**. Se o seu gate depende de `traces/`
ou de `meta/registry.md` para decidir PASS/FAIL, você promoveu um acessório a autoridade
e reabriu o buraco do "disco vence". O que decide um gate é o **disco medido** — mtime,
hash, listagem das escritas nomeadas — nunca um resumo derivado.

## Confidencialidade

Este vault **nunca vira repositório git**. Ele é local-por-máquina e privado — contém
requests verbatim e decisões que não podem ser expostas. O que se compartilha é o
*procedimento* (este curso e os templates), jamais o conteúdo do vault.

---

**Próximo passo:** `04-nivel-4-reimplementar-e-evoluir/02-bootstrap-nova-maquina.md`.
