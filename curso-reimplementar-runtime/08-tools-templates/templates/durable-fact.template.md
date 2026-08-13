<!--
  TEMPLATE — Fato durável (durable-fact)
  =====================================================================
  Esta pasta (08-tools-templates/) é a ÚNICA do curso feita para ser COPIADA.
  Copie este arquivo para facts/_global/<slug>.md (ou facts/<topico>/<slug>.md),
  apague os comentários <!-- ... --> e preencha.

  O QUE É: a unidade de memória do sistema. Uma asserção acumulada, tipada por
  frontmatter, que sobrevive entre sessões. Vive em facts/. É como o runtime
  lembra do que aprendeu.

  REGRA DE OURO: um fato durável descreve estado VERIFICADO. Se a asserção é
  sobre estado que ninguém mediu ("a latência é 40ms"), ela precisa de uma fonte
  que um terceiro reproduza — senão é afirmação, não fato. (Ver o achado central:
  afirmação sobre estado não vira durável sem medição de terceiro.)
-->
---
# --- IDENTIDADE ---
id: fact.<area>.<slug>              # id estável e único. Ex.: fact.constraints.global
title: <Título legível do fato>     # uma linha, humana
type: durable-fact                  # LITERAL — o tipo que o obsidian-eval filtra
kind: constraint                    # constraint | preference | principle | index | ...
                                    #   constraint = regra dura ("nunca usar `as any`")
                                    #   preference = escolha default, mais fraca
                                    #   principle  = heurística acumulada com evidência
                                    #   index      = nota que só agrega links a outros fatos

# --- ESCOPO E CONFIANÇA ---
repo: _global                       # _global, ou o tópico dono do fato
confidence: high                    # high | medium | low — quão firme é esta asserção
valid_from: 2026-01-01              # desde quando o fato vale (data ISO)
# valid_until:                      # OPCIONAL — quando o fato deixa de valer (fatos expiram)
last_updated: 2026-01-01            # última edição deste arquivo

# --- FRONTEIRA DE SCHEMA (só em fatos novos; ver lição 03) ---
# schema: v2                        # marca a versão do schema deste fato. Ausência = legado.
#                                   # NÃO adicione a fatos antigos — legado se lê, não se converte.
# evidence_verified: true           # se o schema exigir prova de terceiro, aponte-a aqui

# --- LIGAÇÕES ---
tags:
  - runtime-state
  - <tag-de-area>
relates-to:
  - "[[facts/_global/index|Facts Index — Global]]"
  # Aponte para o padrão canônico que este fato materializa, quando houver:
  # - "[[vault:long-running-agents/docs/canonical/<slug>|<Nome do padrão>]]"
---

## <área do fato em minúsculas>

<!--
  O CORPO. Para fatos do tipo constraint/preference/principle, o padrão do vault
  é uma LISTA de asserções, cada uma com sua fonte entre parênteses. A fonte é o
  que torna o fato auditável: quem lê sabe de onde a asserção veio e pode contestá-la.
-->

- "<asserção, em uma frase>" (source: <origem verificável — sessão, dispatch, doc>)
- "<outra asserção>" (confidence: high, evidence: <o que a sustenta>)

<!--
  Para um fato do tipo `index`, o corpo é uma lista de wikilinks a outros fatos,
  agrupados por seção (## Restrições, ## Preferências, ## Incidentes, ...).

  LEMBRE: o index é derivado. Atualize-o DEPOIS que o fato indexado existe e passou
  pelo gate — nunca antes. O disco vence; o índice segue o disco.
-->
