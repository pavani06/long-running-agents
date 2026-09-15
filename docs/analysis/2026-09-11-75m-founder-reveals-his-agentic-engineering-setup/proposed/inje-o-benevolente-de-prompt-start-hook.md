---
type: proposed-canonical-doc
status: proposed
created_by: analyze-and-improve F4 (creation != promotion)
source: 2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md
slug: 2026-09-11-75m-founder-reveals-his-agentic-engineering-setup
video_id: ''
pattern: Injeção benevolente de prompt (start hook)
phase3_verdict: Missing
intended_destination: docs/canonical/inje-o-benevolente-de-prompt-start-hook.md
evidence: []
---

# (PROPOSTA) Proposta: Injeção benevolente de prompt (start hook) para onboarding de agentes

> ⚠️ Proposta em quarentena — criada por análise, **não promovida**. Destino pretendido (se aprovada): `docs/canonical/inje-o-benevolente-de-prompt-start-hook.md`.

**Fonte:** `2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc.md` · **padrão:** Injeção benevolente de prompt (start hook) · **Fase-3:** Missing

---

## Problema

Cada sessão de agente (coding agent, assistente de CLI) começa sem memória do projeto. Sem um mecanismo de injeção, toda sessão exige re-onboarding manual: o operador cola contexto, aponta documentos ou repete convenções. Isso é custo recorrente, inconsistente entre sessões e propenso a omissões — o agente opera com menos contexto do que um engenheiro sênior do projeto teria.

## Mecanismo

1. **Pacote de contexto**: um artefato versionado no repositório (ex.: um documento canônico ou conjunto curto de documentos) contendo: propósito do projeto, decisões arquiteturais ativas, convenções de código e de commits, mapas de diretórios, restrições e armadilhas conhecidas.
2. **Start hook**: um hook de inicialização da ferramenta de agente (ex.: hooks de sessão suportados por CLIs de coding agents) que, ao abrir cada sessão, injeta esse pacote como prefixo do contexto do agente.
3. **Atualização**: o pacote é tratado como código — revisado em PRs quando decisões mudam, para que a injeção reflita o estado atual do repositório.

Resultado: o agente "acorda" em cada sessão já ambientado como um engenheiro sênior do projeto, com memória persistente entre sessões sem armazenamento externo.

## Trade-offs

- **Acoplamento a ferramentas**: só funciona em ferramentas de agente que suportam hooks de sessão; migração de ferramenta exige reescrever o hook (o pacote em si é portátil, o mecanismo de injeção não).
- **Custo de manutenção**: pacote desatualizado é pior que nenhum — o agente opera com confiança sobre contexto obsoleto. Exige disciplina de atualização junto a mudanças arquiteturais.
- **Orçamento de contexto**: injeção consome tokens de toda sessão; o pacote deve ser conciso e curado, não um dump de wikis.
- **Risco de prompt injection**: conteúdo injetado é confiável por construção (vem do repo), mas deve ser auditável como qualquer arquivo versionado.

## Como se aplicaria aqui

Este padrão está classificado como **ausente** neste repositório — a proposta abaixo é hipotética, não uma descrição do estado atual:

- Criar um pacote de contexto canônico único (seção Problema/Mecanismo/Trade-offs por tema, estilo dos docs deste acervo) descrevendo o projeto em ~1–2 telas.
- Adicionar um hook de sessão da ferramenta de agente em uso que injeta esse pacote no início de cada sessão.
- Tratar o pacote como código: atualização obrigatória em PRs que alterem decisões arquiteturais ou convenções; revisão humana como gate.
- Medir eficácia: redução de instruções de onboarding repetidas por sessão e consistência das respostas entre sessões distintas.

**Estado**: Proposta em quarentena — requer revisão humana antes de qualquer implementação ou afirmação de existência no repo.
