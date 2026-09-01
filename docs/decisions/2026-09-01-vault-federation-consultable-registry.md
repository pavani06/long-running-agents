---
title: "Vault Federation — Registro Consultável e Roteamento por Domínio"
type: adr
status: accepted
date: 2026-09-01
deciders: ["pavan"]
tags: ["governanca", "agentes-orquestracao", "vault-federation", "harness"]
aliases: ["vault federation ADR", "federacao multi-vault ADR", "wikillm federation", "ADR federacao vaults"]
last_updated: 2026-09-01
relates-to:
  - "[[../canonical/addressable-memory-catalog|Addressable Memory Catalog]]"
  - "[[../canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"
  - "[[../canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[../system-of-record|System of Record]]"
  - "[[vault:sisyphus-runtime/facts/_global/vault-source-of-truth|Vault Source of Truth (runtime)]]"
sources:
  - "[[../../.omo/plans/2026-09-01-wikillm-federacao-multi-vault|Plano de Federação Multi-Vault]]"
  - "https://github.com/pavani06/sisyphus-runtime/issues/44"
---

# ADR: Vault Federation — Registro Consultável e Roteamento por Domínio

## Contexto

O operador mantém múltiplos vaults Obsidian que funcionam como um wikillm (knowledge base legível por humanos e agentes). Antes de 2026-09-01, a descoberta de qual vault cobre qual domínio era memória tribal: nenhum artefato consultável respondia "onde procuro X?". Três problemas concretos:

1. O registry do `obsidian-eval` apontava 4 de 5 vaults para mounts Windows (`/mnt/c/Users/pavan/`) com cópias divergentes dos vaults do home Linux (`long-running-agents`: 613 vs 1227 .md); `raw-knowledge` e `mhc-knowledge-base` não existiam no home.
2. O skill `canonical-context` consultava apenas 2 vaults hardcoded (`sisyphus-runtime` e `long-running-agents`).
3. A DSL de query do `obsidian-eval` é deliberadamente restrita (igualdade, `tags.includes`, `path.startsWith`), o que impede roteamento por termo livre no nível da ferramenta.

A federação foi planejada (plano validado por verificação adversarial, epic pavani06/sisyphus-runtime#44) e executada em 2026-09-01. Este ADR registra a decisão de desenho central.

## Decisão

A federação multi-vault usa um **registro consultável de notas** (`vault-entry`) no vault de runtime + **roteamento por domínio no skill consumidor**, com estas escolhas:

1. **Fonte de verdade única**: home Linux (`/home/pavanpavan/`) para todos os vaults; mounts Windows são backup, nunca fonte de consulta (fato durável `vault:sisyphus-runtime/facts/_global/vault-source-of-truth`).
2. **Registro federativo**: uma nota `type: vault-entry` por vault em `vault:sisyphus-runtime/facts/_global/vaults/`, com frontmatter `domain`, `vault`, `vault-path`, `role` (uma nota por vault porque a DSL filtra nós individuais — uma nota única produziria 1 resultado, não 7).
3. **Roteamento por domínio**: o `canonical-context` carrega um mapa termo→domínio e resolve o vault alvo com igualdade exata (`filter(n => n.frontmatter.type === 'vault-entry' && n.frontmatter.domain === '<domínio>')`), usando o `vault-path` retornado. Queries hardcoded antigas permanecem como fallback retrocompatível.
4. **Índice raiz**: o MOC do runtime (`_moc-runtime.md`) lista os 7 vaults federados (vault → domínio → papel → path).
5. **Grafo federado opcional**: `knowledge-graph.json` mesclados com prefixo de id `vault:<nome>:<id>` (evita colisão de dedup), instalado em `sisyphus-runtime/.understand-anything/federated-graph.json`, não versionado (`.understand-anything/` é gitignore do repo).

## Opções Consideradas

| Opção | Complexidade | Custo | Escalabilidade | Pros | Contras |
|-------|-------------|-------|---------------|------|---------|
| **A (adotada): registro consultável + roteamento no skill** | Baixa | Zero de código de ferramenta | Alta (nova vault = 1 nota) | Notas são observáveis, editáveis e consultáveis pela DSL existente; zero acoplamento CLI↔federação | Mapa termo→domínio duplicado no SKILL.md (staleness possível) |
| B: busca única multi-vault no CLI (`KnowledgeRuntime` multi-driver) | Média | Mudança de código + testes no obsidian-eval | Alta | Uma query busca em todos os vaults | Acopla a federação à ferramenta; API multi-fonte existe mas não é usada por nenhum skill; adiciona superfície de manutenção sem demanda real |
| C: grafo unificado como única interface de descoberta | Alta | Pipeline understand por vault + merge | Baixa | Visualização rica | Grafo é derivado e pesado; só 2/4 vaults de conhecimento passam no detector Karpathy; não serve a consulta determinística de um agente |
| D: convenção de domínio no frontmatter sem registro central | Muito baixa | Zero | Baixa | Zero artefato novo | Descoberta exige scan de cada vault (impraticável no mount remoto); nenhum lugar único responde "quais vaults existem?" |

## Análise de Trade-offs

- **Dimensão decisiva:** a consulta de descoberta é determinística e estruturada (qual vault, qual path), não semântica (qual conteúdo). Para isso, notas de frontmatter + igualdade exata resolvem sem código novo; busca semântica multi-vault (B) resolveria um problema que não foi o gargalo.
- **Risco aceito (A):** staleness do mapa termo→domínio no SKILL.md. Mitigação: o registro (`vault-entry`) é a fonte; o mapa é derivado, e a seção "Vaults disponiveis" aponta para ele. Convenção: mudar o domínio primeiro no registro, depois no mapa.
- **Risco aceito (membros em mount):** `a-casa-conta` vive em mount remoto; full-scan do vault impraticável (>5min). Mitigação: roteamento usa a vault-entry do runtime (scan local); o vault alvo é lido por path, nunca escaneado inteiro.
- **Custo de reverter:** baixo. Remover o Passo 0 do SKILL.md e as notas restaura o comportamento anterior; nada no CLI depende da federação.

## Consequências

**Fica mais fácil:**
- Um agente sem contexto descobrir qual vault consultar (MOC + registro + obsidian-eval; QA 5/5 com agente fresco)
- Adicionar um vault à federação: 1 nota `vault-entry` + campo `domain` na nota de topo + linha no mapa do canonical-context
- Auditar a federação: `obsidian-eval ~/sisyphus-runtime query "filter(n => n.frontmatter.type === 'vault-entry')"` retorna o estado completo

**Fica mais difícil:**
- Mover um vault de lugar: exige atualizar symlink do registry + `vault-path` da nota (duas fontes de path, mitigadas pelo fato durável de fonte de verdade)
- Renomear um domínio: toque em nota + mapa do SKILL.md + MOC

**Revisitar quando:**
- **A vs B:** quando um skill real precisar de busca semântica cross-vault frequente, avaliar ativar o `KnowledgeRuntime` multi-driver no CLI
- **Grafo 2/4:** quando `obsidian-eval` e `hop-ecosystem-atlas` ganharem nota de topo no padrão Karpathy (index.md com `type: index`), regenerar o grafo federado
- **mhc-knowledge-base:** se o domínio ecommerce MHC/KODA voltar a ser ativo, criar a 8ª `vault-entry` e a linha no mapa

## Ações

- [x] Tarefa 0: fonte de verdade home Linux; registry com 8 nomes; symlinks; fato durável (obsidian-eval `6dd8959`)
- [x] T1: 7 notas `vault-entry` + MANIFEST + índice (runtime `83bcb83`)
- [x] T2: campo `domain` nas 7 notas de topo (5 repos)
- [x] T3: índice federado no MOC raiz (runtime `bf636be`)
- [x] T4: Passo 0 de roteamento no `canonical-context` + auditoria Core Triad sem breaks (opencode-config `2021b92`)
- [x] T5: grafo federado com prefixo de id (2023 nodes, 8814 edges, 0 dangling)
- [x] T6: verificação transversal (6/6 checks PASS, QA de roteamento 5/5)
- [ ] Incluir `mhc-knowledge-base` como 8ª vault-entry quando o domínio for reativado
- [ ] Regenerar grafo federado quando obsidian-eval e hop-ecosystem-atlas ganharem index no padrão Karpathy
