<!--
  TEMPLATE — Incident (registro de cicatriz)
  =====================================================================
  Copie para facts/_global/incident-<AAAA-MM-DD>-<slug>.md, apague os comentários
  e preencha.

  O QUE É: o registro datado de uma falha. Classificação, o que aconteceu, o dano
  concreto, e a REGRA que a falha produziu.

  POR QUE IMPORTA: os incidents são o currículo. Cada um é uma cicatriz que, lida,
  evita uma re-quebra. Um incident bem escrito não descreve um bug — descreve a
  CLASSE de defeito, de modo que quem o lê não repita a classe em outra forma.

  DISCIPLINA: o dano concreto vai declarado com honestidade, inclusive "zero". Um
  incident com dano zero, pego pela detecção, é uma vitória do sistema — registrá-lo
  como grave mente; registrá-lo como trivial desperdiça a lição.
-->
---
# --- IDENTIDADE E CLASSIFICAÇÃO ---
id: incident.<AAAA-MM-DD>.<slug>
type: incident                      # LITERAL
severity: P2                        # P1 (grave) | P2 (minor) | P3 (trivial)
date: 2026-01-01                    # quando o incidente OCORREU
detected: 2026-01-01               # quando foi DETECTADO (pode diferir de `date`)
status: open                        # open | resolved | closed
actor: operator                     # quem cometeu: operator | agent | system
                                    #   (nomear o ator com honestidade é parte da cicatriz)

# --- PROVENIÊNCIA ---
repo: _global
session_detector: <id-da-sessao>    # a sessão que detectou (a prova de que foi pego)
source: <onde a evidência vive>     # sessão + artefato datado
evidence_verified: true             # a evidência foi medida por terceiro? (não afirmada)
concrete_damage: zero               # zero | minor | major — o DANO REAL, honesto

# --- A REGRA QUE ESTE INCIDENTE PRODUZIU OU VIOLOU ---
violated_rules:
  - <dispatch-rule-slug>            # a regra que foi quebrada (se já existia)
# produced_rule: <dispatch-rule-slug>   # a regra que este incidente FEZ NASCER (se houver)

tags:
  - incident
  - <classe-do-defeito>             # ex.: process-violation, gate-traversal, baseline-materiality
  - <minor|major>
related_incidents:
  - "[[facts/_global/incident-<AAAA-MM-DD>-<slug-irmao>]]"   # incidentes da mesma classe
---

# Incident: <título — o que aconteceu, em uma linha> (<data>, <severity>)

## Classification

- **Type**: <classe do defeito — a mesma linguagem dos irmãos, para agrupar>
- **Severity**: <P1|P2|P3> / <minor|major> (<justificativa: dano concreto x dano evitado>)
- **Actor**: <operator | agent | system> — nomeado sem eufemismo
- **Class**: <a classe abstrata; o que se repete entre este e outros incidentes>
- **Violated principle**: <dispatch-rule-slug> (§ ...)

## What happened

<!-- A narrativa factual, curta. O que foi feito, em que ordem, e onde a promessa
     divergiu do estado. Frases-âncora com localização (arquivo, §, mtime). -->

## Dano concreto

<!-- HONESTIDADE OBRIGATÓRIA. Separe:
     - Dano DIRETO: o que efetivamente quebrou (frequentemente "zero", se pego cedo).
     - Dano EVITADO por detecção: o que teria quebrado sem o pego. É aqui que a lição
       fica cara mesmo quando o dano direto é zero. -->

**Zero direto.** <por quê>
**Dano evitado por detecção.** <o que a detecção impediu>

## Resolução

<!-- O que fechou o incidente. Se `status: resolved`, qual dispatch/veredito o fechou,
     com proveniência. Se `open`, o que falta. -->

## Atenuantes e agravante

**Atenuantes:**
- <ex.: auto-detecção cooperativa; dano zero; diagnóstico completo>

**Agravante:**
- <ex.: a regra já existia e estava à vista; a classe já tinha 4 eventos>

## Action items

### Operador
- <o que muda no processo do operador>

### Agente
- <o que muda no comportamento do agente — ou "nenhuma ação", com justificativa>

## See also

- "[[facts/_global/<dispatch-rule-que-nasceu-daqui>]]"
- "[[facts/_global/incident-<irmão>]]" — incidente da mesma classe
- <id-da-sessão> — onde a evidência vive
