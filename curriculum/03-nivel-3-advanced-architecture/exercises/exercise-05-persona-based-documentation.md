---
title: "Exercício 5: Implementar Documentação Baseada em Personas"
type: curriculum-exercise
nivel: 3
aliases: ["persona-based documentation", "NFR por persona", "documentação persona", "revisor persona", "rubrica especializada", "multiplicação de conhecimento"]
tags: [curriculo-conteudo, nivel-3, exercicio, governanca, persona-based-docs, nfr-documents, reviewer-agents, knowledge-multiplication, domain-ownership, python, dataclass]
relates-to: ["[[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|Multi-Agent Systems]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[AGENTS|AGENTS.md]]"]
last_updated: 2026-06-11
---

# 🎭 Exercício 5: Implementar Documentação Baseada em Personas
## Nível 3 — Arquitetura Avançada

**Tempo Estimado:** 90-120 minutos
**Dificuldade:** ⭐⭐⭐⭐ (Avançado)
**Pré-requisito:** Ter completado `01-multi-agent-systems.md` + Exercícios 1-4 do Nível 3
**Objetivo:** Projetar um sistema onde cada especialista documenta seu conhecimento uma vez e todo agente herda esse conhecimento automaticamente, eliminando a dependência de um AGENTS.md universal

---

## 📖 Prólogo: O Conhecimento Que Morava na Cabeça da Camila

**Quinta-feira, 16h. Code review do PR #847.**

O PR era simples: adicionar um formulário de cadastro na página de checkout. Três campos, validação básica, nada complexo. O agente implementador gerou o código em 40 minutos. O review humano levou 2 horas.

```
═══════════════════════════════════════════════════════════════
         PR #847 — Formulário de Cadastro no Checkout
              Review por: Camila (Front-End Architect)
═══════════════════════════════════════════════════════════════

ENCONTRADO POR CAMILA EM 2 HORAS DE REVIEW:

❌ Input de e-mail sem autocomplete="email"
   → "Agente sempre esquece. Já é o 14º PR com esse problema."

❌ Mensagem de erro genérica "Campo inválido"
   → "Toda mensagem de erro precisa dizer COMO corrigir.
      Já documentei isso em... na verdade, nunca documentei."

❌ Tab order está errada (nome → CEP → e-mail)
   → "A ordem correta é nome → e-mail → CEP. O Guilherme (UX)
      definiu isso há 6 meses, mas ninguém documentou."

❌ Input de senha sem aria-describedby
   → "A Roberta (Security) quase teve um treco na última review
      que não tinha aria-describedby. Ela sempre cobra isso."

❌ Botão sem estado de loading
   → "State machine de formulário: idle → submitting → success/error.
      É um padrão que eu e o time de front definimos há 3 meses.
      Mas está na cabeça das pessoas, não no repositório."

❌ Sem teste de acessibilidade para teclado
   → "O QA já reportou 7 bugs de navegação por teclado esse mês.
      Padrão claríssimo, zero documentação."

RESULTADO:
  6 problemas encontrados. Nenhum era novo.
  Camila já tinha apontado CADA UM desses em PRs anteriores.
  Tempo total de review: 2h (80% apontando problemas recorrentes).
  Tempo que o agente levaria para corrigir SE soubesse: 20 min.
═══════════════════════════════════════════════════════════════
```

Na retrospectiva da sexta-feira, Camila explodiu:

```
Camila: "Eu passo 12 horas por semana revisando PRs. E 80% desse
        tempo é apontando os MESMOS problemas. Toda semana."

Roberta (Security): "Mesma coisa aqui. XSS em input, token em
        localStorage, CORS mal configurado. Os mesmos 5 problemas,
        toda review."

Guilherme (UX): "Ordem de tab, estados de loading, mensagens de erro
        que não ajudam. Eu poderia gravar um vídeo e dar play toda
        review."

Dev Senior: "Mas a gente tem o AGENTS.md. Ele tem regras."

Camila: "O AGENTS.md tem 16 regras genéricas. Ele diz 'siga padrões
        existentes'. Mas não diz QUAIS padrões. Não diz que input
        de e-mail precisa de autocomplete. Não diz que formulário
        tem 4 estados. O AGENTS.md é um ponto de partida, não um
        repositório de conhecimento."

Arquiteta: "Então o que vocês precisam?"

Camila: "Cada um de nós tem uma especialidade. Eu sei front-end.
        Roberta sabe segurança. Guilherme sabe UX. Essas especialidades
        são conhecimento DURÁVEL — não mudam a cada sprint. O que
        muda é o código que implementa esse conhecimento."

Roberta: "Se eu pudesse escrever UM documento com tudo que eu verifico
        em review de segurança, e todo agente lesse esse documento
        automaticamente..."

Guilherme: "E se, quando um PR toca em formulário, o revisor de UX
        carrega automaticamente minhas rubricas?"

Arquiteta: "Isso é persona-based documentation. Cada persona documenta
        sua especialidade uma vez. Os agentes herdam esse conhecimento.
        Reviewers carregam a persona certa para cada mudança."
```

Ela desenhou no quadro:

```
HOJE (AGENTS.md universal):
  ┌─────────────────────────────────┐
  │         AGENTS.md               │
  │  16 regras genéricas            │
  │  "siga padrões existentes"      │
  │  "mantenha código limpo"        │
  │  "não use any"                  │
  └─────────────────────────────────┘
           │
           ▼
  Todos os agentes recebem o mesmo.
  Reviewers verificam tudo manualmente.

PROPOSTA (Persona-Based):
  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ Frontend │ │ Security │ │    UX    │ │ Product  │
  │  Persona │ │ Persona  │ │ Persona  │ │ Persona  │
  │          │ │          │ │          │ │          │
  │ Camila   │ │ Roberta  │ │Guilherme │ │  Time de │
  │ escreve  │ │ escreve  │ │ escreve  │ │ Produto  │
  │ uma vez  │ │ uma vez  │ │ uma vez  │ │ escreve  │
  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
       │             │             │             │
       ▼             ▼             ▼             ▼
  ┌─────────────────────────────────────────────────────┐
  │              REVIEWER DISPATCH                       │
  │                                                     │
  │  PR toca em .tsx?     → Carrega Frontend Persona    │
  │  PR toca em auth?     → Carrega Security Persona     │
  │  PR toca em UI?       → Carrega UX Persona           │
  │  PR toca em regra?    → Carrega Product Persona      │
  └─────────────────────────────────────────────────────┘
```

```
Arquiteta: "O AGENTS.md continua existindo — ele tem as regras
        universais. Mas cada persona escreve seu conhecimento
        especializado EM UM ÚNICO LUGAR. E os revisores carregam
        a persona certa automaticamente."

Camila: "Então na próxima review, em vez de eu digitar 'input de
        e-mail precisa de autocomplete' pela 15ª vez..."

Arquiteta: "O agente implementador JÁ leu o Frontend Persona antes
        de codar. Ele JÁ sabe que input de e-mail precisa de
        autocomplete. Você só revisa o que é novo."

Roberta: "E se eu atualizar o Security Persona, todo agente que
        rodar amanhã já recebe as regras novas?"

Arquiteta: "Exato. Uma atualização, todos os agentes herdam.
        Isso é conhecimento que multiplica."
```

**Agora é a sua vez.**

Você é o arquiteto que vai implementar esse sistema de personas. Você vai definir 4 personas, escrever os NFR documents de cada uma, implementar o dispatch automático de revisores, e demonstrar que uma atualização em um persona doc melhora TODOS os agentes.

---

## 🎯 O Contexto

### O Problema: Conhecimento Silosado em Pessoas

Em times que usam agentes de IA para implementação, o conhecimento de qualidade vive em três lugares:

1. **Na cabeça dos especialistas** (Camila sabe front-end, Roberta sabe segurança)
2. **Nos comentários de PR** (feedback repetido toda review)
3. **Em documentos genéricos** (AGENTS.md com regras universais)

Nenhum desses lugares escala. O especialista vira gargalo. Os comentários de PR somem depois do merge. O AGENTS.md é genérico demais para guiar decisões específicas.

### A Solução: Persona-Based Documentation

Cada especialista escreve **um documento** com todo o conhecimento da sua especialidade:

| Persona | Dono | Documento | Exemplos de Regras |
|---|---|---|---|
| **Frontend Architect** | Camila | `personas/frontend-architect.md` | autocomplete, aria attributes, state machines, CSS variables, bundle size |
| **Security Engineer** | Roberta | `personas/security-engineer.md` | XSS prevention, CSP headers, token storage, input sanitization, CORS |
| **UX Engineer** | Guilherme | `personas/ux-engineer.md` | tab order, error messages, loading states, empty states, keyboard nav |
| **Product Owner** | Time de Produto | `personas/product-owner.md` | feature flags, analytics events, error tracking, experiment isolation |

Estes documentos são:
- **Duráveis**: escritos uma vez, atualizados quando a especialidade evolui
- **Herança automática**: todo agente que implementa recebe as personas relevantes
- **Carregamento condicional**: o revisor carrega apenas as personas relevantes para o diff
- **Multiplicadores**: uma atualização no Security Persona melhora todos os PRs futuros

### O Que Você Vai Construir

Você vai implementar um sistema com três camadas:

1. **Persona Registry**: catálogo de personas com seus documentos NFR
2. **Agent Context Builder**: carrega as personas certas para o agente antes de implementar
3. **Reviewer Dispatch**: carrega as personas certas para o revisor baseado no diff

O domínio de exemplo é o mesmo KODA: um app React com formulários, autenticação e fluxos de usuário.

---

## 📋 Requisitos

### Funcionais

- [ ] Sistema define 4 personas: Frontend, Security, UX, Product
- [ ] Cada persona tem um `PersonaNFR` document com regras específicas
- [ ] Cada regra tem: id, descrição, severidade (BLOCKING/ADVISORY), exemplos
- [ ] `AgentContextBuilder` carrega personas baseado no tipo de tarefa
- [ ] `ReviewerDispatch` carrega personas baseado nos arquivos do diff
- [ ] Dispatch automático: PR tocando em `.tsx` carrega Frontend + UX
- [ ] Dispatch automático: PR tocando em `auth` carrega Security
- [ ] Uma atualização em um PersonaNFR afeta todos os agentes futuros
- [ ] O sistema detecta qual persona revisar com base no código, não em configuração manual

### Técnicos

- [ ] Python 3.9+ com type hints
- [ ] Usar `dataclasses` para os modelos
- [ ] `PersonaNFR` com regras categorizadas por severidade
- [ ] `DiffAnalyzer` que identifica tipos de arquivo no diff
- [ ] `ReviewReport` que agrega resultados de múltiplos revisores persona

### Validação

- [ ] Cenário 1: PR de formulário (`.tsx`) dispara Frontend + UX reviewers
- [ ] Cenário 2: PR de autenticação (`auth.ts`) dispara Security reviewer
- [ ] Cenário 3: atualizar Security Persona melhora próximo PR de auth
- [ ] Cenário 4: regras BLOCKING impedem merge; ADVISORY permitem com waiver
- [ ] Cenário 5: persona doc sobrevive a mudanças de modelo (conhecimento durável)
- [ ] Cenário 6: agente que lê Frontend Persona produz código que passa na review

---

## 🏗️ Arquitetura do Sistema

### Diagrama ASCII

```
┌──────────────────────────────────────────────────────────────────────┐
│                     PERSONA REGISTRY                                   │
│                                                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  ┌────────┐│
│  │ FrontendArchitect│  │SecurityEngineer │  │ UXEngineer │  │Product ││
│  │ Persona          │  │ Persona         │  │ Persona    │  │Owner   ││
│  │                  │  │                 │  │            │  │Persona ││
│  │ Dono: Camila     │  │ Dono: Roberta   │  │Dono:Guilher│  │Dono:PM ││
│  │ 12 regras        │  │ 8 regras        │  │ 10 regras  │  │6 regras││
│  └────────┬─────────┘  └────────┬────────┘  └─────┬──────┘  └───┬────┘│
│           │                     │                  │             │     │
└───────────┼─────────────────────┼──────────────────┼─────────────┼─────┘
            │                     │                  │             │
            ▼                     ▼                  ▼             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     AGENT CONTEXT BUILDER                              │
│                                                                        │
│  Task: "Adicionar formulário de checkout"                              │
│    → keywords: ["formulário", "checkout"]                              │
│    → personas relevantes: [Frontend, UX, Product]                      │
│    → NÃO carrega: [Security]  (não é task de auth)                     │
│                                                                        │
│  Output: contexto enriquecido com NFRs das personas selecionadas       │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     AGENTE IMPLEMENTADOR                               │
│                                                                        │
│  Recebe: task + NFRs de Frontend, UX, Product                          │
│  Implementa: formulário com autocomplete, aria, estados de loading     │
│  Output: PR #850 (diff com arquivos .tsx, .css)                        │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     REVIEWER DISPATCH                                  │
│                                                                        │
│  Analisa diff do PR #850:                                              │
│    src/components/CheckoutForm.tsx  → Frontend + UX                    │
│    src/styles/checkout.css          → Frontend                         │
│    src/hooks/useCheckout.ts         → Frontend                         │
│                                                                        │
│  NÃO analisa:                                                          │
│    (nenhum arquivo de auth)         → NÃO carrega Security             │
│    (nenhuma regra de negócio)      → NÃO carrega Product               │
│                                                                        │
│  Dispara: FrontendReviewer + UXReviewer                                │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│              FrontendReviewer                  UXReviewer              │
│                                                                        │
│  Verifica 12 regras:                     Verifica 10 regras:           │
│  ✅ autocomplete em inputs               ✅ tab order correta           │
│  ✅ aria attributes presentes            ❌ mensagem de erro genérica   │
│  ✅ CSS variables, não hex codes         ✅ loading state no botão      │
│  ✅ componente abaixo de 200 linhas      ✅ empty state tratado         │
│  ...                                     ...                           │
│                                                                        │
│  Resultado: 11/12 passou                 Resultado: 9/10 passou        │
│  1 BLOCKING: aria-describedby            1 BLOCKING: erro genérico     │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     AGGREGATED REVIEW REPORT                           │
│                                                                        │
│  PR #850:                                                              │
│    Frontend: 11/12 passou — 1 BLOCKING                                 │
│    UX:       9/10 passou — 1 BLOCKING                                  │
│    Veredito: REJECTED (2 BLOCKING findings)                            │
│                                                                        │
│  Agente recebe feedback e corrige.                                     │
│  Próximo PR similar: Frontend Persona JÁ foi carregado.                │
│  Agente JÁ sabe sobre autocomplete e aria.                             │
│  Camila NÃO precisa apontar de novo.                                   │
└──────────────────────────────────────────────────────────────────────┘
```

### Regras de Dispatch por Tipo de Arquivo

| Extensão / Padrão | Personas Carregadas | Justificativa |
|---|---|---|
| `*.tsx`, `*.jsx` | Frontend, UX | Componentes React — padrões visuais e de acessibilidade |
| `*.css`, `*.scss` | Frontend | Estilização — design system, variáveis |
| `auth/*`, `*auth*`, `*session*` | Security | Autenticação e sessão — superfície de ataque |
| `*token*`, `*api*`, `*request*` | Security | Tokens, APIs — vulnerabilidades de rede |
| `*.test.tsx`, `*spec.tsx` | UX | Testes de comportamento — acessibilidade |
| `analytics*`, `*tracking*`, `*experiment*` | Product | Métricas e experimentos — isolamento |
| `feature-flags*`, `*config*` | Product | Configuração de produto — rollout seguro |

---

## 🚀 Starter Code

```python
"""
Exercício 5 — Implementar Documentação Baseada em Personas
Nível 3 — Arquitetura Avançada

Implemente um sistema onde cada especialista documenta seu conhecimento
uma vez e todo agente herda esse conhecimento automaticamente.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ============================================================================
# DATA MODELS
# ============================================================================

class Severity(Enum):
    """Severidade de uma regra de persona."""
    BLOCKING = "blocking"    # impede merge
    ADVISORY = "advisory"    # permite merge com waiver


class FindingStatus(Enum):
    """Status de um finding de review."""
    PASSED = "passed"
    FAILED = "failed"
    NOT_APPLICABLE = "not_applicable"


@dataclass
class PersonaRule:
    """
    Uma regra específica da especialidade de uma persona.

    Exemplos:
    - Frontend: "inputs de e-mail devem ter autocomplete='email'"
    - Security: "tokens nunca são armazenados em localStorage"
    - UX: "mensagens de erro devem ensinar COMO corrigir"
    """
    rule_id: str
    description: str
    severity: Severity
    examples: list[str] = field(default_factory=list)     # bons exemplos
    counter_examples: list[str] = field(default_factory=list)  # maus exemplos
    check_pattern: str = ""  # padrão para verificação automatizada (regex ou descrição)


@dataclass
class PersonaNFR:
    """
    Documento de Non-Functional Requirements de uma persona.

    Cada persona tem EXATAMENTE um PersonaNFR.
    Este documento é o ativo durável — escrito uma vez,
    atualizado quando a especialidade evolui, herdado
    por todos os agentes.

    O owner é a pessoa responsável por manter este documento.
    """
    persona_id: str
    persona_name: str           # ex: "Frontend Architect"
    owner_name: str             # ex: "Camila"
    owner_role: str             # ex: "Staff Frontend Engineer"
    description: str            # escopo da especialidade
    rules: list[PersonaRule] = field(default_factory=list)
    version: str = "1.0"
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DiffFile:
    """Um arquivo alterado em um PR."""
    filepath: str
    extension: str = ""
    content_summary: str = ""  # resumo do que foi mudado

    def __post_init__(self):
        if not self.extension:
            self.extension = self.filepath.split(".")[-1] if "." in self.filepath else ""


@dataclass
class PullRequest:
    """Representa um PR com seus arquivos alterados."""
    pr_id: str
    title: str
    description: str = ""
    changed_files: list[DiffFile] = field(default_factory=list)


@dataclass
class PersonaFinding:
    """Resultado da verificação de uma regra de persona."""
    rule_id: str
    rule_description: str
    severity: Severity
    status: FindingStatus
    evidence: str = ""
    filepath: str = ""
    line_hint: str = ""


@dataclass
class PersonaReviewResult:
    """Resultado da revisão de uma persona específica."""
    persona_id: str
    persona_name: str
    findings: list[PersonaFinding] = field(default_factory=list)

    @property
    def blocking_count(self) -> int:
        """Quantos findings BLOCKING falharam."""
        return sum(
            1 for f in self.findings
            if f.severity == Severity.BLOCKING and f.status == FindingStatus.FAILED
        )

    @property
    def advisory_count(self) -> int:
        """Quantos findings ADVISORY falharam."""
        return sum(
            1 for f in self.findings
            if f.severity == Severity.ADVISORY and f.status == FindingStatus.FAILED
        )

    @property
    def passed(self) -> bool:
        """A revisão passou? (nenhum BLOCKING falhou)."""
        return self.blocking_count == 0


@dataclass
class AggregatedReviewReport:
    """Relatório agregado de múltiplos revisores persona."""
    pr_id: str
    persona_results: list[PersonaReviewResult] = field(default_factory=list)
    reviewed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def overall_passed(self) -> bool:
        """O PR pode ser mergeado? (todos os reviewers passaram)."""
        return all(r.passed for r in self.persona_results)

    @property
    def total_blocking_failures(self) -> int:
        """Total de BLOCKING failures entre todos os revisores."""
        return sum(r.blocking_count for r in self.persona_results)


# ============================================================================
# PERSONA REGISTRY (Catálogo de Personas)
# ============================================================================

class PersonaRegistry:
    """
    Catálogo central de todas as personas e seus NFR documents.

    Responsabilidades:
    1. Armazenar PersonaNFR documents
    2. Permitir atualização de documentos (versionamento)
    3. Resolver quais personas são relevantes para um PR
    """

    def __init__(self):
        """Inicializa o registry vazio. Use register() para adicionar personas."""
        # TODO: Implementar inicialização
        # self._personas: dict[str, PersonaNFR] = {}
        pass

    def register(self, persona: PersonaNFR) -> None:
        """
        Registra (ou atualiza) uma persona no catálogo.

        Se a persona já existe, atualiza a versão.
        Se não existe, adiciona.

        Args:
            persona: Documento NFR da persona.
        """
        # TODO: Implementar registro de persona
        pass

    def get(self, persona_id: str) -> PersonaNFR | None:
        """
        Recupera uma persona por ID.

        Args:
            persona_id: Identificador da persona.

        Returns:
            PersonaNFR ou None se não encontrada.
        """
        # TODO: Implementar consulta
        pass

    def list_all(self) -> list[PersonaNFR]:
        """Retorna todas as personas registradas."""
        # TODO: Implementar listagem
        pass


# ============================================================================
# AGENT CONTEXT BUILDER
# ============================================================================

class AgentContextBuilder:
    """
    Constrói o contexto do agente implementador com as personas relevantes.

    Antes de um agente começar a implementar, ele recebe as NFRs
    das personas relevantes para a tarefa. Isso garante que o agente
    JÁ SAIBA das regras antes de escrever a primeira linha.

    Responsabilidades:
    1. Analisar a descrição da tarefa
    2. Identificar quais personas são relevantes
    3. Carregar as regras dessas personas
    4. Construir o contexto enriquecido para o agente
    """

    def __init__(self, registry: PersonaRegistry):
        """
        Args:
            registry: Catálogo de personas.
        """
        # TODO: Implementar inicialização
        pass

    def resolve_personas_for_task(self, task_description: str) -> list[PersonaNFR]:
        """
        Identifica quais personas são relevantes para uma tarefa.

        Usa palavras-chave na descrição da tarefa para decidir:
        - "formulário", "componente", "UI", "página" → Frontend, UX
        - "auth", "login", "token", "sessão" → Security
        - "experimento", "métrica", "tracking" → Product

        Args:
            task_description: Descrição da tarefa a ser implementada.

        Returns:
            Lista de PersonaNFR relevantes.
        """
        # TODO: Implementar resolução de personas por tarefa
        #
        # Algoritmo sugerido:
        # 1. Criar mapping de keywords → persona_ids:
        #    frontend_keywords = ["formulário", "componente", "ui", "react",
        #                         "página", "css", "estilo", "layout"]
        #    security_keywords = ["auth", "login", "token", "sessão", "senha",
        #                        "autenticação", "autorização"]
        #    ux_keywords = ["ux", "acessibilidade", "loading", "erro", "estado",
        #                  "formulário", "mensagem", "feedback"]
        #    product_keywords = ["experimento", "métrica", "tracking", "analytics",
        #                       "feature flag", "config"]
        #
        # 2. Para cada persona, verificar se task_description (lowercased)
        #    contém alguma keyword
        # 3. Retornar personas que deram match
        pass

    def build_context(self, task_description: str) -> dict[str, Any]:
        """
        Constrói o contexto completo para o agente implementador.

        O contexto inclui:
        - Descrição da tarefa
        - Lista de personas relevantes
        - Regras de cada persona (agrupadas por severidade)

        Args:
            task_description: Descrição da tarefa.

        Returns:
            Dicionário com o contexto estruturado.
        """
        # TODO: Implementar construção de contexto
        #
        # Formato esperado do output:
        # {
        #     "task": task_description,
        #     "personas_loaded": ["frontend-architect", "ux-engineer"],
        #     "blocking_rules": [
        #         {"persona": "frontend-architect", "rule": "autocomplete em inputs"},
        #         ...
        #     ],
        #     "advisory_rules": [...],
        # }
        pass


# ============================================================================
# REVIEWER DISPATCH
# ============================================================================

class ReviewerDispatch:
    """
    Dispatcher que decide quais personas revisam um PR.

    Baseado nos arquivos alterados no diff, carrega os revisores
    persona corretos. Isso é automático — ninguém precisa manualmente
    escolher quais personas revisar.

    Responsabilidades:
    1. Analisar os arquivos do PR
    2. Mapear extensões/paths para personas
    3. Executar revisão com cada persona relevante
    4. Agregar resultados em ReviewReport
    """

    # Mapping de padrões de arquivo → Persona IDs
    FILE_TO_PERSONA_MAP: dict[str, list[str]] = {
        ".tsx": ["frontend-architect", "ux-engineer"],
        ".jsx": ["frontend-architect", "ux-engineer"],
        ".css": ["frontend-architect"],
        ".scss": ["frontend-architect"],
        "auth": ["security-engineer"],
        "token": ["security-engineer"],
        "session": ["security-engineer"],
        "api": ["security-engineer"],
        "cors": ["security-engineer"],
        "analytics": ["product-owner"],
        "tracking": ["product-owner"],
        "experiment": ["product-owner"],
        "feature-flag": ["product-owner"],
        "config": ["product-owner"],
    }

    def __init__(self, registry: PersonaRegistry):
        """
        Args:
            registry: Catálogo de personas.
        """
        # TODO: Implementar inicialização
        pass

    def resolve_reviewers(self, pr: PullRequest) -> list[PersonaNFR]:
        """
        Decide quais personas devem revisar este PR.

        Analisa cada arquivo no diff e determina quais personas
        são relevantes. Remove duplicatas (uma persona só revisa
        uma vez, mesmo que múltiplos arquivos a acionem).

        Args:
            pr: Pull request com os arquivos alterados.

        Returns:
            Lista de PersonaNFR que devem revisar.
        """
        # TODO: Implementar resolução de revisores
        #
        # Algoritmo sugerido:
        # 1. Coletar todos os persona_ids relevantes:
        #    persona_ids = set()
        #    for file in pr.changed_files:
        #        for pattern, personas in FILE_TO_PERSONA_MAP.items():
        #            if pattern in file.filepath.lower():
        #                persona_ids.update(personas)
        #
        # 2. Resolver cada persona_id para PersonaNFR via registry
        # 3. Retornar lista (sem duplicatas)
        pass

    def review_pr(self, pr: PullRequest) -> AggregatedReviewReport:
        """
        Executa a revisão completa do PR com todas as personas relevantes.

        Para cada persona relevante:
        1. Carrega as regras da persona
        2. Verifica cada regra contra os arquivos do PR
        3. Coleta findings

        Args:
            pr: Pull request a ser revisado.

        Returns:
            AggregatedReviewReport com resultados de todos os revisores.
        """
        # TODO: Implementar revisão completa
        #
        # Algoritmo sugerido:
        # 1. Resolver revisores (resolve_reviewers)
        # 2. Para cada persona:
        #    a. Criar PersonaReviewResult
        #    b. Para cada regra da persona:
        #       - Verificar se a regra se aplica aos arquivos do PR
        #       - Criar PersonaFinding com status
        #    c. Adicionar ao report
        # 3. Retornar AggregatedReviewReport
        pass

    def check_rule_against_files(
        self, rule: PersonaRule, files: list[DiffFile]
    ) -> PersonaFinding:
        """
        Verifica uma regra de persona contra os arquivos do PR.

        Simula a verificação automatizada de uma regra.
        Em produção, isso seria um lint rule, um test, ou um check estático.

        Args:
            rule: A regra a verificar.
            files: Arquivos do PR.

        Returns:
            PersonaFinding com o resultado da verificação.
        """
        # TODO: Implementar verificação de regra
        #
        # Para simular, use o check_pattern da regra como uma substring
        # a procurar (ou ausência a detectar) nos arquivos.
        #
        # Exemplo:
        # - Rule "inputs de e-mail devem ter autocomplete='email'"
        #   → procurar por 'type="email"' nos .tsx
        #   → verificar se 'autocomplete' está próximo
        #
        # - Rule "tokens nunca em localStorage"
        #   → procurar por 'localStorage' nos arquivos
        #   → se encontrado, FAILED
        pass


# ============================================================================
# PERSONA NFR DOCUMENTS (Conteúdo de exemplo)
# ============================================================================

def build_frontend_persona() -> PersonaNFR:
    """
    Constrói o PersonaNFR da Frontend Architect (Camila).

    Regras que todo componente React deve seguir.
    """
    return PersonaNFR(
        persona_id="frontend-architect",
        persona_name="Frontend Architect",
        owner_name="Camila",
        owner_role="Staff Frontend Engineer",
        description=(
            "Padrões de qualidade para componentes React: acessibilidade, "
            "performance, design system, e estrutura de código."
        ),
        rules=[
            PersonaRule(
                rule_id="fe-001",
                description="Inputs de e-mail devem ter autocomplete='email'",
                severity=Severity.BLOCKING,
                examples=['<input type="email" autocomplete="email" />'],
                counter_examples=['<input type="email" />'],
                check_pattern='autocomplete="email"',
            ),
            PersonaRule(
                rule_id="fe-002",
                description="Inputs de senha devem ter aria-describedby apontando para requisitos",
                severity=Severity.BLOCKING,
                examples=['<input type="password" aria-describedby="password-requirements" />'],
                counter_examples=['<input type="password" />'],
                check_pattern='aria-describedby',
            ),
            PersonaRule(
                rule_id="fe-003",
                description="Cores devem usar CSS variables, não hex codes hardcoded",
                severity=Severity.BLOCKING,
                examples=['color: var(--color-primary)'],
                counter_examples=['color: #3B82F6'],
                check_pattern='var(--',
            ),
            PersonaRule(
                rule_id="fe-004",
                description="Componentes não devem exceder 200 linhas",
                severity=Severity.ADVISORY,
                examples=["Componente CheckoutForm: 145 linhas — ok"],
                counter_examples=["Componente ProductPage: 340 linhas — refatorar"],
                check_pattern="",  # verificação manual
            ),
            PersonaRule(
                rule_id="fe-005",
                description="Formulários devem usar estado explícito: idle → submitting → success/error",
                severity=Severity.BLOCKING,
                examples=["const [status, setStatus] = useState('idle')"],
                counter_examples=["// sem estado de formulário"],
                check_pattern="useState.*idle|useState.*submitting|useState.*loading",
            ),
            PersonaRule(
                rule_id="fe-006",
                description="Botões devem ter estado disabled durante submissão",
                severity=Severity.BLOCKING,
                examples=['<button disabled={isSubmitting}>Enviar</button>'],
                counter_examples=['<button onClick={handleSubmit}>Enviar</button>'],
                check_pattern="disabled=",
            ),
        ],
    )


def build_security_persona() -> PersonaNFR:
    """
    Constrói o PersonaNFR da Security Engineer (Roberta).

    Regras que toda superfície de autenticação e API deve seguir.
    """
    return PersonaNFR(
        persona_id="security-engineer",
        persona_name="Security Engineer",
        owner_name="Roberta",
        owner_role="Application Security Engineer",
        description=(
            "Requisitos de segurança para auth, tokens, input sanitization, "
            "CORS, CSP headers, e prevenção de vulnerabilidades comuns."
        ),
        rules=[
            PersonaRule(
                rule_id="sec-001",
                description="Tokens NUNCA são armazenados em localStorage",
                severity=Severity.BLOCKING,
                examples=["// usando httpOnly cookie para token"],
                counter_examples=['localStorage.setItem("token", jwt)'],
                check_pattern="localStorage",
            ),
            PersonaRule(
                rule_id="sec-002",
                description="Inputs de usuário são sanitizados antes de renderizar",
                severity=Severity.BLOCKING,
                examples=["import DOMPurify from 'dompurify'"],
                counter_examples=['<div>{userInput}</div>'],
                check_pattern="DOMPurify|sanitize|escapeHtml",
            ),
            PersonaRule(
                rule_id="sec-003",
                description="CORS headers são configurados explicitamente (não wildcard)",
                severity=Severity.BLOCKING,
                examples=["Access-Control-Allow-Origin: https://koda.app"],
                counter_examples=["Access-Control-Allow-Origin: *"],
                check_pattern="Access-Control-Allow-Origin",
            ),
            PersonaRule(
                rule_id="sec-004",
                description="CSP headers incluem script-src e style-src restritivos",
                severity=Severity.BLOCKING,
                examples=["Content-Security-Policy: default-src 'self'"],
                counter_examples=["// sem CSP configurado"],
                check_pattern="Content-Security-Policy",
            ),
            PersonaRule(
                rule_id="sec-005",
                description="Senhas NUNCA são logadas ou incluídas em traces",
                severity=Severity.BLOCKING,
                examples=["logger.info('Login attempt', { email })  // sem senha"],
                counter_examples=['logger.info("Login", { email, password })'],
                check_pattern="",  # difícil verificar estaticamente
            ),
        ],
    )


def build_ux_persona() -> PersonaNFR:
    """
    Constrói o PersonaNFR do UX Engineer (Guilherme).

    Regras de acessibilidade e experiência do usuário.
    """
    return PersonaNFR(
        persona_id="ux-engineer",
        persona_name="UX Engineer",
        owner_name="Guilherme",
        owner_role="Senior UX Engineer",
        description=(
            "Padrões de UX e acessibilidade: navegação por teclado, "
            "screen readers, mensagens de erro, estados de loading, "
            "e feedback ao usuário."
        ),
        rules=[
            PersonaRule(
                rule_id="ux-001",
                description="Ordem de tab segue fluxo lógico: nome → email → campos restantes → submit",
                severity=Severity.BLOCKING,
                examples=["<input tabIndex={1} ... />"],
                counter_examples=["// tabIndex aleatório ou ausente"],
                check_pattern="tabIndex",
            ),
            PersonaRule(
                rule_id="ux-002",
                description="Mensagens de erro ensinam COMO corrigir, não apenas que está errado",
                severity=Severity.BLOCKING,
                examples=['"Digite um e-mail no formato nome@exemplo.com"'],
                counter_examples=['"Campo inválido"', '"Erro"'],
                check_pattern="",
            ),
            PersonaRule(
                rule_id="ux-003",
                description="Estados vazios têm mensagem amigável e call-to-action",
                severity=Severity.ADVISORY,
                examples=['"Nenhum produto no carrinho. Que tal começar pelas ofertas?"'],
                counter_examples=["// array vazio, sem mensagem"],
                check_pattern="",
            ),
            PersonaRule(
                rule_id="ux-004",
                description="Todo elemento interativo é acessível por teclado (tabIndex >= 0 ou elemento nativo)",
                severity=Severity.BLOCKING,
                examples=["<button>, <input>, <a href> — nativamente acessíveis por teclado"],
                counter_examples=['<div onClick={handler}>  // sem role, sem tabIndex'],
                check_pattern="role=|tabIndex",
            ),
        ],
    )


def build_product_persona() -> PersonaNFR:
    """
    Constrói o PersonaNFR do Product Owner (Time de Produto).

    Regras de produto: analytics, experimentos, feature flags.
    """
    return PersonaNFR(
        persona_id="product-owner",
        persona_name="Product Owner",
        owner_name="Time de Produto",
        owner_role="Product Management",
        description=(
            "Requisitos de produto: analytics events, feature flags, "
            "tracking de conversão, isolamento de experimentos."
        ),
        rules=[
            PersonaRule(
                rule_id="prod-001",
                description="Features novas usam feature flags para rollout gradual",
                severity=Severity.BLOCKING,
                examples=["if (featureFlags.newCheckout) { return <NewCheckout /> }"],
                counter_examples=["// feature nova implementada sem flag"],
                check_pattern="featureFlag|feature_flag",
            ),
            PersonaRule(
                rule_id="prod-002",
                description="Eventos de analytics têm nome padronizado: snake_case, domínio claro",
                severity=Severity.ADVISORY,
                examples=['analytics.track("checkout_form_submitted", {...})'],
                counter_examples=['analytics.track("btn1", {...})'],
                check_pattern="analytics.track",
            ),
            PersonaRule(
                rule_id="prod-003",
                description="Experimentos A/B são isolados — usuário não vê duas variantes na mesma sessão",
                severity=Severity.BLOCKING,
                examples=["// experiment assignment persiste na sessão"],
                counter_examples=["// re-atribui experimento a cada render"],
                check_pattern="experiment|variant",
            ),
        ],
    )


def build_default_registry() -> PersonaRegistry:
    """
    Constrói um PersonaRegistry com as 4 personas padrão do KODA.
    """
    registry = PersonaRegistry()
    registry.register(build_frontend_persona())
    registry.register(build_security_persona())
    registry.register(build_ux_persona())
    registry.register(build_product_persona())
    return registry


# ============================================================================
# TESTS / EXEMPLOS DE USO
# ============================================================================

def test_registry_register_and_retrieve():
    """Cenário 1: Registrar e recuperar personas do catálogo."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: Registry — Registrar e Recuperar Personas")
    print("=" * 60)

    registry = build_default_registry()

    # Verificar que todas as 4 personas foram registradas
    personas = registry.list_all()
    assert len(personas) == 4, f"Esperado 4 personas, encontrado {len(personas)}"

    # Verificar recuperação individual
    frontend = registry.get("frontend-architect")
    assert frontend is not None, "Frontend Architect deve existir"
    assert frontend.owner_name == "Camila"
    assert len(frontend.rules) == 6, f"Esperado 6 regras, encontrado {len(frontend.rules)}"

    security = registry.get("security-engineer")
    assert security is not None, "Security Engineer deve existir"
    assert security.owner_name == "Roberta"
    assert len(security.rules) == 5

    print(f"   Personas registradas: {[p.persona_id for p in personas]}")
    print(f"   Frontend: {len(frontend.rules)} regras, owner={frontend.owner_name}")
    print(f"   Security: {len(security.rules)} regras, owner={security.owner_name}")
    print("✅ Teste 1 concluído!")


def test_context_builder_resolves_personas():
    """Cenário 2: AgentContextBuilder carrega personas corretas por tarefa."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: ContextBuilder — Resolver Personas por Tarefa")
    print("=" * 60)

    registry = build_default_registry()
    builder = AgentContextBuilder(registry)

    # Tarefa de formulário → Frontend + UX
    task_form = "Adicionar formulário de checkout com validação de e-mail e senha"
    personas_form = builder.resolve_personas_for_task(task_form)
    persona_ids_form = {p.persona_id for p in personas_form}
    assert "frontend-architect" in persona_ids_form, (
        "Tarefa de formulário deve carregar Frontend"
    )
    assert "ux-engineer" in persona_ids_form, (
        "Tarefa de formulário deve carregar UX"
    )
    print(f"   Task: '{task_form}'")
    print(f"   Personas: {sorted(persona_ids_form)}")

    # Tarefa de auth → Security
    task_auth = "Implementar renovação de token JWT no middleware de autenticação"
    personas_auth = builder.resolve_personas_for_task(task_auth)
    persona_ids_auth = {p.persona_id for p in personas_auth}
    assert "security-engineer" in persona_ids_auth, (
        "Tarefa de auth deve carregar Security"
    )
    print(f"   Task: '{task_auth}'")
    print(f"   Personas: {sorted(persona_ids_auth)}")

    # Tarefa de experimento → Product
    task_exp = "Adicionar experimento A/B para nova página de checkout"
    personas_exp = builder.resolve_personas_for_task(task_exp)
    persona_ids_exp = {p.persona_id for p in personas_exp}
    assert "product-owner" in persona_ids_exp, (
        "Tarefa de experimento deve carregar Product"
    )
    print(f"   Task: '{task_exp}'")
    print(f"   Personas: {sorted(persona_ids_exp)}")

    print("✅ Teste 2 concluído!")


def test_context_builder_output_structure():
    """Cenário 3: ContextBuilder produz contexto estruturado."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: ContextBuilder — Estrutura do Contexto")
    print("=" * 60)

    registry = build_default_registry()
    builder = AgentContextBuilder(registry)

    task = "Criar componente de formulário de cadastro com validação"
    context = builder.build_context(task)

    # Verificar estrutura esperada
    assert "task" in context, "Contexto deve ter 'task'"
    assert "personas_loaded" in context, "Contexto deve ter 'personas_loaded'"
    assert "blocking_rules" in context, "Contexto deve ter 'blocking_rules'"

    assert context["task"] == task
    assert len(context["personas_loaded"]) >= 2, (
        "Formulário deve carregar pelo menos Frontend + UX"
    )
    assert len(context["blocking_rules"]) > 0, (
        "Deve haver regras BLOCKING"
    )

    print(f"   Personas loaded: {context['personas_loaded']}")
    print(f"   Blocking rules: {len(context['blocking_rules'])}")
    print(f"   Advisory rules: {len(context.get('advisory_rules', []))}")
    print("✅ Teste 3 concluído!")


def test_reviewer_dispatch_form_pr():
    """Cenário 4: PR de formulário dispara Frontend + UX reviewers."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: Dispatch — PR de Formulário → Frontend + UX")
    print("=" * 60)

    registry = build_default_registry()
    dispatch = ReviewerDispatch(registry)

    # PR que só mexe em componentes React
    pr = PullRequest(
        pr_id="PR-850",
        title="Adicionar formulário de checkout",
        changed_files=[
            DiffFile(filepath="src/components/CheckoutForm.tsx"),
            DiffFile(filepath="src/components/CheckoutButton.tsx"),
            DiffFile(filepath="src/styles/checkout.css"),
        ],
    )

    reviewers = dispatch.resolve_reviewers(pr)
    reviewer_ids = {r.persona_id for r in reviewers}

    assert "frontend-architect" in reviewer_ids, (
        "PR com .tsx deve carregar Frontend"
    )
    assert "ux-engineer" in reviewer_ids, (
        "PR com .tsx deve carregar UX"
    )
    assert "security-engineer" not in reviewer_ids, (
        "PR sem auth não deve carregar Security"
    )

    print(f"   PR: {pr.pr_id} — {pr.title}")
    print(f"   Arquivos: {[f.filepath for f in pr.changed_files]}")
    print(f"   Reviewers: {sorted(reviewer_ids)}")
    print("✅ Teste 4 concluído!")


def test_reviewer_dispatch_auth_pr():
    """Cenário 5: PR de autenticação dispara Security reviewer."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: Dispatch — PR de Auth → Security")
    print("=" * 60)

    registry = build_default_registry()
    dispatch = ReviewerDispatch(registry)

    pr = PullRequest(
        pr_id="PR-851",
        title="Refatorar middleware de autenticação",
        changed_files=[
            DiffFile(filepath="src/auth/session.ts"),
            DiffFile(filepath="src/middleware/auth-middleware.ts"),
        ],
    )

    reviewers = dispatch.resolve_reviewers(pr)
    reviewer_ids = {r.persona_id for r in reviewers}

    assert "security-engineer" in reviewer_ids, (
        "PR com auth deve carregar Security"
    )

    print(f"   PR: {pr.pr_id} — {pr.title}")
    print(f"   Arquivos: {[f.filepath for f in pr.changed_files]}")
    print(f"   Reviewers: {sorted(reviewer_ids)}")
    print("✅ Teste 5 concluído!")


def test_persona_update_affects_future_agents():
    """Cenário 6: Atualizar PersonaNFR melhora agentes futuros."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 6: Atualização de Persona → Agentes Futuros Melhoram")
    print("=" * 60)

    registry = build_default_registry()

    # Cenário: Roberta descobre um novo padrão de vulnerabilidade
    # e adiciona uma nova regra ao Security Persona

    security_before = registry.get("security-engineer")
    rules_before = len(security_before.rules)
    print(f"   Regras Security antes: {rules_before}")

    # Roberta adiciona nova regra
    new_rule = PersonaRule(
        rule_id="sec-006",
        description="Headers de segurança (X-Content-Type-Options, X-Frame-Options) são configurados",
        severity=Severity.BLOCKING,
        examples=["X-Content-Type-Options: nosniff"],
        counter_examples=["// sem headers de segurança"],
        check_pattern="X-Content-Type-Options|X-Frame-Options",
    )

    # Registrar persona atualizada
    updated_security = PersonaNFR(
        persona_id=security_before.persona_id,
        persona_name=security_before.persona_name,
        owner_name=security_before.owner_name,
        owner_role=security_before.owner_role,
        description=security_before.description,
        rules=security_before.rules + [new_rule],
        version="1.1",
    )
    registry.register(updated_security)

    # Verificar que a atualização está disponível
    security_after = registry.get("security-engineer")
    rules_after = len(security_after.rules)
    assert rules_after == rules_before + 1, (
        f"Esperado {rules_before + 1} regras, encontrado {rules_after}"
    )
    assert security_after.version == "1.1", "Versão deve ser atualizada"

    # Agora, qualquer agente futuro que carregar Security Persona
    # receberá as 6 regras (não mais as 5 antigas)
    builder = AgentContextBuilder(registry)
    personas = builder.resolve_personas_for_task("implementar autenticação JWT")
    security_persona = next(p for p in personas if p.persona_id == "security-engineer")
    assert len(security_persona.rules) == 6, (
        "Agente futuro deve receber a versão atualizada"
    )

    print(f"   Regras Security depois: {rules_after}")
    print(f"   Nova regra: {new_rule.rule_id} — {new_rule.description}")
    print("   ✅ Agentes futuros herdam automaticamente a atualização")

    print("✅ Teste 6 concluído!")


def test_blocking_vs_advisory_severity():
    """Cenário 7: Regras BLOCKING impedem merge; ADVISORY permitem com waiver."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 7: Severidade — BLOCKING vs ADVISORY")
    print("=" * 60)

    registry = build_default_registry()

    # Criar um PR que passa nas regras ADVISORY mas falha em BLOCKING
    frontend = registry.get("frontend-architect")
    blocking_rules = [r for r in frontend.rules if r.severity == Severity.BLOCKING]
    advisory_rules = [r for r in frontend.rules if r.severity == Severity.ADVISORY]

    print(f"   Frontend: {len(blocking_rules)} BLOCKING, {len(advisory_rules)} ADVISORY")

    # Simular um review result com 1 BLOCKING failure
    result = PersonaReviewResult(
        persona_id="frontend-architect",
        persona_name="Frontend Architect",
        findings=[
            PersonaFinding(
                rule_id="fe-001", rule_description="autocomplete em inputs",
                severity=Severity.BLOCKING, status=FindingStatus.FAILED,
                evidence="input type=email sem autocomplete",
            ),
            PersonaFinding(
                rule_id="fe-004", rule_description="componente <= 200 linhas",
                severity=Severity.ADVISORY, status=FindingStatus.FAILED,
                evidence="CheckoutForm.tsx: 245 linhas",
            ),
        ],
    )

    # Verificar contagem
    assert result.blocking_count == 1, "1 BLOCKING failure"
    assert result.advisory_count == 1, "1 ADVISORY failure"
    assert not result.passed, "Não deve passar (tem BLOCKING failure)"

    # Simular um review que só tem ADVISORY failures
    result_advisory_only = PersonaReviewResult(
        persona_id="frontend-architect",
        persona_name="Frontend Architect",
        findings=[
            PersonaFinding(
                rule_id="fe-004", rule_description="componente <= 200 linhas",
                severity=Severity.ADVISORY, status=FindingStatus.FAILED,
                evidence="CheckoutForm.tsx: 245 linhas",
            ),
        ],
    )
    assert result_advisory_only.blocking_count == 0, "0 BLOCKING failures"
    assert result_advisory_only.passed, (
        "Deve passar (apenas ADVISORY, permite merge com waiver)"
    )

    print(f"   Com BLOCKING failure: passed={result.passed}")
    print(f"   Apenas ADVISORY: passed={result_advisory_only.passed}")
    print("✅ Teste 7 concluído!")


def test_persona_knowledge_is_durable():
    """Cenário 8: Persona doc sobrevive a mudanças de modelo (conhecimento durável)."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 8: Conhecimento de Persona é Durável")
    print("=" * 60)

    registry = build_default_registry()

    # As regras de persona NÃO dependem de qual modelo está gerando código.
    # "Input de e-mail precisa de autocomplete" é verdade com GPT-4, Claude 4, etc.
    # "Token não vai em localStorage" é verdade com qualquer backend.

    # Simular: trocar o modelo NÃO altera as regras
    frontend = registry.get("frontend-architect")
    security = registry.get("security-engineer")

    # "Trocar" o modelo — mas as regras permanecem idênticas
    model_name = "claude-4"  # poderia ser qualquer um
    assert len(frontend.rules) == 6, (
        f"Regras Frontend não mudam com modelo {model_name}"
    )
    assert len(security.rules) == 5, (
        f"Regras Security não mudam com modelo {model_name}"
    )

    # O que MUDA com o modelo é a qualidade do código gerado,
    # não as constraints que ele deve satisfazer
    print(f"   Modelo: {model_name}")
    print(f"   Frontend rules: {len(frontend.rules)} (inalteradas)")
    print(f"   Security rules: {len(security.rules)} (inalteradas)")
    print("   ✅ Conhecimento de persona independe do modelo de LLM")

    print("✅ Teste 8 concluído!")


def test_aggregated_report():
    """Cenário 9: AggregatedReviewReport agrega múltiplos revisores."""
    print("\n" + "=" * 60)
    print("🧪 TESTE 9: Relatório Agregado de Múltiplos Revisores")
    print("=" * 60)

    # Simular um PR que foi revisado por Frontend (passou) e UX (falhou)
    report = AggregatedReviewReport(
        pr_id="PR-850",
        persona_results=[
            PersonaReviewResult(
                persona_id="frontend-architect",
                persona_name="Frontend Architect",
                findings=[
                    PersonaFinding(
                        rule_id="fe-001", rule_description="autocomplete",
                        severity=Severity.BLOCKING, status=FindingStatus.PASSED,
                        evidence="autocomplete='email' presente",
                    ),
                ],
            ),
            PersonaReviewResult(
                persona_id="ux-engineer",
                persona_name="UX Engineer",
                findings=[
                    PersonaFinding(
                        rule_id="ux-002", rule_description="mensagem de erro específica",
                        severity=Severity.BLOCKING, status=FindingStatus.FAILED,
                        evidence='mensagem "Erro" sem instrução de correção',
                    ),
                ],
            ),
        ],
    )

    print(f"   PR: {report.pr_id}")
    print(f"   Revisores: {len(report.persona_results)}")
    for pr_result in report.persona_results:
        print(f"      - {pr_result.persona_name}: {pr_result.blocking_count} BLOCKING failures")

    assert not report.overall_passed, "PR não deve passar (UX tem BLOCKING)"
    assert report.total_blocking_failures == 1, "1 BLOCKING failure total"

    print(f"   Overall: {'PASSED' if report.overall_passed else 'REJECTED'}")
    print(f"   Total BLOCKING failures: {report.total_blocking_failures}")
    print("✅ Teste 9 concluído!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCÍCIO 5: DOCUMENTAÇÃO BASEADA EM PERSONAS")
    print("=" * 60)

    # Quando implementado, descomente para testar:
    # test_registry_register_and_retrieve()
    # test_context_builder_resolves_personas()
    # test_context_builder_output_structure()
    # test_reviewer_dispatch_form_pr()
    # test_reviewer_dispatch_auth_pr()
    # test_persona_update_affects_future_agents()
    # test_blocking_vs_advisory_severity()
    # test_persona_knowledge_is_durable()
    # test_aggregated_report()

    print("\n📝 TODO: Implemente as classes acima!")
    print("   1. PersonaRegistry — register(), get(), list_all()")
    print("   2. AgentContextBuilder — resolve_personas_for_task(), build_context()")
    print("   3. ReviewerDispatch — resolve_reviewers(), review_pr(), check_rule_against_files()")
    print("   Após implementar, descomente os testes em main()")
```

---

## 🏗️ Como Começar

### Passo 1: Implementar PersonaRegistry (15 min)

É a camada mais simples. Um dicionário interno `_personas: dict[str, PersonaNFR]`. O método `register()` é upsert (atualiza se existe, insere se não). O `get()` é lookup simples. O `list_all()` retorna os valores.

### Passo 2: Implementar AgentContextBuilder (25 min)

**resolve_personas_for_task:** Analisa a descrição da tarefa e mapeia para personas. Use palavras-chave:

```python
def resolve_personas_for_task(self, task_description: str) -> list[PersonaNFR]:
    task_lower = task_description.lower()
    persona_ids = set()

    keyword_map = {
        "frontend-architect": [
            "formulário", "componente", "ui", "react", "página",
            "css", "estilo", "layout", "input", "botão", "modal",
        ],
        "security-engineer": [
            "auth", "login", "token", "sessão", "senha",
            "autenticação", "autorização", "jwt", "oauth",
        ],
        "ux-engineer": [
            "ux", "acessibilidade", "loading", "erro", "estado",
            "formulário", "mensagem", "feedback", "tab", "teclado",
        ],
        "product-owner": [
            "experimento", "métrica", "tracking", "analytics",
            "feature flag", "config", "a/b",
        ],
    }

    for persona_id, keywords in keyword_map.items():
        if any(kw in task_lower for kw in keywords):
            persona_ids.add(persona_id)

    return [self.registry.get(pid) for pid in persona_ids if self.registry.get(pid)]
```

**build_context:** Estrutura o contexto. Separe regras BLOCKING de ADVISORY. Inclua exemplos bons e maus.

### Passo 3: Implementar ReviewerDispatch (30 min)

**resolve_reviewers:** Para cada arquivo no PR, verifique patterns. Use `FILE_TO_PERSONA_MAP`:

```python
def resolve_reviewers(self, pr: PullRequest) -> list[PersonaNFR]:
    persona_ids = set()
    for file in pr.changed_files:
        filepath_lower = file.filepath.lower()
        for pattern, pids in self.FILE_TO_PERSONA_MAP.items():
            if pattern in filepath_lower:
                persona_ids.update(pids)
    return [self.registry.get(pid) for pid in persona_ids if self.registry.get(pid)]
```

**check_rule_against_files:** Simula verificação. Se `rule.check_pattern` é uma substring, procure nos arquivos. Se deve estar presente e não está → FAILED. Se é algo que NÃO deve estar (ex: "localStorage") e está presente → FAILED.

**review_pr:** Orquestra tudo. Para cada persona → para cada regra → chama `check_rule_against_files` → coleta findings → agrega.

### Passo 4: Testar (10 min)

Descomente os testes. Execute. Todos os 9 devem passar.

---

## 🎯 Desafios Extra (Opcional)

### Desafio 1: Versionamento de PersonaNFR com changelog

```python
@dataclass
class PersonaVersion:
    version: str
    changes: str  # descrição do que mudou
    changed_by: str
    changed_at: str

class VersionedPersonaRegistry:
    """Registry que mantém histórico de versões de cada persona."""
    def get_version(self, persona_id: str, version: str) -> PersonaNFR | None: ...
    def get_changelog(self, persona_id: str) -> list[PersonaVersion]: ...
```

### Desafio 2: Conflict Resolution entre Personas

```python
def resolve_persona_conflicts(report: AggregatedReviewReport) -> list[str]:
    """
    O que acontece quando duas personas têm regras conflitantes?
    Ex: UX diz "botão grande e visível", Frontend diz "componente <= 200 linhas".
    Implemente uma política de resolução de conflitos.
    """
    pass
```

### Desafio 3: Persona Effectiveness Metrics

```python
@dataclass
class PersonaMetrics:
    persona_id: str
    times_loaded: int           # quantas vezes a persona foi carregada
    blocking_findings_caught: int  # quantos BLOCKING foram detectados
    false_positives: int         # quantas vezes a regra apontou algo correto
    rules_never_triggered: list[str]  # regras que nunca detectaram nada

def calculate_persona_roi(metrics: PersonaMetrics) -> float:
    """
    Assim como componentes de harness têm ROI, personas também têm.
    Se uma regra nunca dispara, talvez seja desnecessária.
    """
    pass
```

### Desafio 4: Herança entre Personas

```python
class PersonaInheritance:
    """
    Permite que personas herdem regras de outras.
    Ex: "Mobile Frontend" herda de "Frontend Architect" + adiciona regras mobile.
    """
    def inherit(self, child: PersonaNFR, parents: list[PersonaNFR]) -> PersonaNFR: ...
```

---

## 📊 Checklist de Implementação

- [ ] `PersonaRegistry.__init__()` — inicializa catálogo vazio
- [ ] `PersonaRegistry.register()` — upsert de persona
- [ ] `PersonaRegistry.get()` — lookup por ID
- [ ] `PersonaRegistry.list_all()` — lista todas
- [ ] `AgentContextBuilder.resolve_personas_for_task()` — mapeia keywords → personas
- [ ] `AgentContextBuilder.build_context()` — estrutura contexto enriquecido
- [ ] `ReviewerDispatch.resolve_reviewers()` — mapeia arquivos → personas
- [ ] `ReviewerDispatch.check_rule_against_files()` — simula verificação
- [ ] `ReviewerDispatch.review_pr()` — orquestra revisão completa
- [ ] Teste 1 (registry) passa ✅
- [ ] Teste 2 (resolver personas) passa ✅
- [ ] Teste 3 (contexto estruturado) passa ✅
- [ ] Teste 4 (PR formulário → Frontend+UX) passa ✅
- [ ] Teste 5 (PR auth → Security) passa ✅
- [ ] Teste 6 (atualização afeta futuros) passa ✅
- [ ] Teste 7 (BLOCKING vs ADVISORY) passa ✅
- [ ] Teste 8 (conhecimento durável) passa ✅
- [ ] Teste 9 (relatório agregado) passa ✅

---

## 💡 Dicas de Implementação

**Dica 1:** O coração do exercício é o dispatch. O mapping de arquivos para personas é a decisão de design mais importante. Pense em extensões, paths e padrões de nome.

**Dica 2:** `check_rule_against_files` é simulado. Em produção, cada regra seria um lint rule, um test case, ou uma verificação estática. Aqui, usar `check_pattern` como substring é suficiente.

**Dica 3:** `PersonaRule.severity` define o contrato: BLOCKING = não pode mergear, ADVISORY = pode mergear com anotação. Isso é idêntico ao que o `issue-review` skill faz com BLOCKING/ADVISORY findings.

**Dica 4:** O exercício é sobre o MODELO, não sobre implementação de lint rules reais. O valor está em entender que separar conhecimento por persona multiplica o impacto de cada especialista.

**Dica 5:** As funções `build_*_persona()` já fornecem dados realistas. Use-as como ponto de partida. Se quiser, adicione mais regras — o sistema deve comportar.

---

## ✅ Validação Final

Sua implementação está correta se:

1. ✅ Todos os 9 testes passam
2. ✅ `PersonaRegistry` suporta atualização de documentos (não apenas criação)
3. ✅ `AgentContextBuilder` carrega personas diferentes para tarefas diferentes
4. ✅ `ReviewerDispatch` carrega personas diferentes para arquivos diferentes
5. ✅ Atualizar um `PersonaNFR` afeta imediatamente agentes futuros
6. ✅ Regras BLOCKING impedem merge; ADVISORY permitem
7. ✅ O sistema funciona com as 4 personas built-in E com personas adicionais

---

## 🎓 O Que Você Aprendeu

Após completar este exercício, você internalizou:

- ✅ O padrão Persona-Based Documentation: cada especialista documenta uma vez, todos os agentes herdam
- ✅ A diferença entre AGENTS.md universal e persona-specific NFR documents
- ✅ Como implementar dispatch automático de revisores baseado em diffs
- ✅ Como separar regras BLOCKING (impedem merge) de ADVISORY (permitem com waiver)
- ✅ Que conhecimento de persona é durável — independe de modelo de LLM
- ✅ O poder multiplicador: uma atualização de persona melhora todos os agentes futuros

**Próximo:** Nível 4 — Aplicação Específica ao KODA

---

*Exercício 5 de Nível 3 | Curso Long-Running Agents | Programa Técnico FutanBear*
