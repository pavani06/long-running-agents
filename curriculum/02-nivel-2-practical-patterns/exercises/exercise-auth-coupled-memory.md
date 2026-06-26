---
title: "Exercicio: Auth-Coupled Memory Architecture com Recuperacao por Nivel de Confianca"
type: exercise
level: "N2"
aliases: ["auth-coupled memory", "memoria acoplada a autenticacao", "memory sensitivity gating", "identity-gated memory", "auth confidence memory", "tiered memory access"]
tags: [curriculo-conteudo, nivel-2, exercicio, agentes-orquestracao, security, memory-architecture, auth-coupled, identity-resolution, sensitivity-gating, access-control]
duration: "60-75 min"
relates-to: ["[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-patterns|Sierra Patterns]]", "[[docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-classification|Classification]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]"]
last_updated: 2026-06-26
---
# Exercicio: Auth-Coupled Memory Architecture com Recuperacao por Nivel de Confianca
## Nivel 2 - Padroes Praticos

**Tempo Estimado:** 60-75 minutos
**Dificuldade:** Intermediario
**Pre-requisito:** Ter lido `02-sprint-contracts.md` (Nivel 2) + completado Exercicio 3
**Objetivo:** Construir um sistema de memoria que acopla recuperacao de memorias ao nivel de autenticacao do usuario, com thresholds de confianca diferentes para diferentes niveis de sensibilidade

---

## Prologo: O Agente Que Confundiu Dois Irmaos

### Segunda-feira, 10h15. Uma ligacao que expôs o design de memoria.

```
CLIENTE: "Oi, sou o Carlos. Quero comprar Whey de novo, o de sempre."
AGENTE:  "Claro, Carlos! Vejo que voce prefere Whey Isolado Baunilha.
          Seu ultimo pedido foi ha 15 dias. Tambem tenho aqui sua
          alergia a lactose documentada e os 3 enderecos de entrega.
          Ah, e vejo que sua mae ligou semana passada sobre a conta
          conjunta — posso ajudar com isso tambem?"
CLIENTE: "...Carlos e meu irmao. Eu sou o Andre. Como voce tem
          todas essas informacoes sem eu ter me identificado?"
```

O agente de atendimento da **FamilyTelco** tinha memoria, mas nao tinha acoplamento com autenticacao. Ele identificava o caller pelo numero de telefone (`+55 11 98765-4321`) e carregava TODAS as memorias associadas aquele numero. O problema: o telefone era da casa da familia. Mae, pai e dois irmaos compartilhavam a mesma linha.

Em uma unica ligacao, o agente expôs:
- Preferencias de compra do Carlos (baixa sensibilidade — "gosta de baunilha")
- Alergia a lactose (media sensibilidade — dado de saude)
- Enderecos de entrega (media sensibilidade — PII)
- Conversa da mae sobre conta financeira conjunta (alta sensibilidade)

**O que deveria ter acontecido:**

```
[identity] phone=+5511987654321 → auth_confidence=0.30 (linha compartilhada)
[memory] sensitivity=low → greeting OK: "Ola! Como posso ajudar?"
[memory] sensitivity=medium → blocked: requer auth_confidence >= 0.60
[memory] sensitivity=high → blocked: requer auth_confidence >= 0.85 + 2FA
```

**Sua missao:** Construir um `AuthCoupledMemory` que acopla a recuperacao de memorias ao nivel de autenticacao, com thresholds de confianca diferentes para memorias de baixa, media e alta sensibilidade.

---

## Cenario: Agente da FamilyTelco com Historico Familiar

### Contexto

A **FamilyTelco** e uma operadora de telecom que usa um agente de IA para atendimento ao cliente. O agente mantem memorias por cliente, mas o sistema de identificacao e fragil: o unico sinal de identidade e o numero de telefone.

O banco de memorias contem registros de 4 membros da familia Silva:

```python
FAMILY_SILVA_MEMORIES = [
    # Carlos (filho, 22 anos)
    {"id": "MEM-001", "owner": "carlos_silva", "sensitivity": "low",
     "content": "Prefere Whey Isolado sabor baunilha. Compra a cada 30 dias."},
    {"id": "MEM-002", "owner": "carlos_silva", "sensitivity": "low",
     "content": "Ultimo pedido: #88214 em 2026-06-11. Whey Isolado 1kg + Creatina 300g."},

    # Andre (filho, 19 anos)
    {"id": "MEM-003", "owner": "andre_silva", "sensitivity": "low",
     "content": "Prefere Whey Concentrado sabor chocolate. Compra a cada 45 dias."},

    # Mae (Dona Lucia)
    {"id": "MEM-004", "owner": "lucia_silva", "sensitivity": "high",
     "content": "Titular da conta conjunta #4567-8. Limite: R$ 5.000. Vencimento: dia 15."},
    {"id": "MEM-005", "owner": "lucia_silva", "sensitivity": "medium",
     "content": "Endereco: Rua das Flores, 450, Sao Paulo-SP, 01234-567."},

    # Familia (compartilhado)
    {"id": "MEM-006", "owner": "familia_silva", "sensitivity": "low",
     "content": "Plano familia com 4 linhas. 50GB. Renovacao em 2026-12-01."},
    {"id": "MEM-007", "owner": "familia_silva", "sensitivity": "medium",
     "content": "Endereco alternativo: Av. Brasil, 1200, apto 302, Sao Paulo-SP."},
    {"id": "MEM-008", "owner": "lucia_silva", "sensitivity": "high",
     "content": "Senha de acesso ao portal: S!lva2026 (alterada em 2026-04)."},
]
```

Cada identidade tem um metodo de autenticacao com confianca diferente:

```python
IDENTITY_RESOLUTION = {
    "phone_shared": {
        "method": "phone_number", "number": "+55 11 98765-4321",
        "auth_confidence": 0.30,
        "possible_owners": ["carlos_silva", "andre_silva", "lucia_silva"],
    },
    "carlos_pin": {
        "method": "pin_code", "auth_confidence": 0.65,
        "confirmed_owner": "carlos_silva",
    },
    "andre_2fa": {
        "method": "sms_2fa", "auth_confidence": 0.85,
        "confirmed_owner": "andre_silva",
    },
    "lucia_biometric": {
        "method": "voice_biometric", "auth_confidence": 0.95,
        "confirmed_owner": "lucia_silva",
    },
}
```

### Dados de Entrada

O agente recebe um `AccessRequest`:

```json
{
  "session_id": "SES-5521",
  "identity_method": "phone_shared",
  "auth_confidence": 0.30,
  "possible_owners": ["carlos_silva", "andre_silva", "lucia_silva"]
}
```

---

## Requisitos

### Requisitos Funcionais

1. **RF1 - Sensitivity thresholds:** Memorias sao classificadas em 3 niveis com thresholds diferentes: `low` → 0.20, `medium` → 0.60, `high` → 0.85
2. **RF2 - Owner-filtered retrieval:** So retorna memorias cujo owner corresponde aos `possible_owners` OU e compartilhado (`familia_silva`)
3. **RF3 - Progressive disclosure:** Memorias sao reveladas progressivamente conforme a confianca aumenta
4. **RF4 - Re-authentication escalation:** Quando precisa de memoria de sensibilidade mais alta, agente solicita escalacao
5. **RF5 - Auth audit trail:** Cada acesso registra: session_id, memory_id, sensitivity, auth_confidence, timestamp
6. **RF6 - Confidence upgrade:** Durante a sessao, usuario pode fazer upgrade de phone_shared → PIN → 2FA

### Requisitos Tecnicos

1. **RT1 - Python puro:** stdlib + dataclasses
2. **RT2 - Determinismo:** Mesmo AccessRequest → mesmas memorias
3. **RT3 - Sem vazamento:** Agente nunca revela que existem memorias bloqueadas de nivel superior

---

## Sua Tarefa

### Parte 1: Diagnosticar o Vazamento de Memoria (10 min)

```python
# TAREFA: Responda no codigo como comentario
#
# 1. No cenario do prologo, quando Andre ligou e o agente carregou
#    TODAS as memorias do telefone, quais foram reveladas indevidamente?
#    Classifique por sensibilidade e explique o dano.
#
# 2. Com Auth-Coupled Memory e auth_confidence=0.30 (phone_shared):
#    Quais memorias seriam reveladas? Quais estariam bloqueadas?
#
# 3. Por que "memory startups haven't broken out" segundo Wedeen?
#    Qual a relacao com auth-coupled memory?
#
# 4. Proponha uma politica para telefone publico (auth_confidence=0.05).
```

---

### Parte 2: Implementar o AuthCoupledMemory (45 min)

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class SensitivityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AuthMethod(Enum):
    PHONE_SHARED = "phone_shared"
    PIN_CODE = "pin_code"
    SMS_2FA = "sms_2fa"
    VOICE_BIOMETRIC = "voice_biometric"


SENSITIVITY_THRESHOLDS = {
    SensitivityLevel.LOW: 0.20,
    SensitivityLevel.MEDIUM: 0.60,
    SensitivityLevel.HIGH: 0.85,
}

AUTH_METHOD_CONFIDENCE = {
    AuthMethod.PHONE_SHARED: 0.30,
    AuthMethod.PIN_CODE: 0.65,
    AuthMethod.SMS_2FA: 0.85,
    AuthMethod.VOICE_BIOMETRIC: 0.95,
}


@dataclass
class Memory:
    memory_id: str
    owner: str
    sensitivity: SensitivityLevel
    content: str


@dataclass
class AccessRequest:
    session_id: str
    identity_method: AuthMethod
    auth_confidence: float
    possible_owners: list[str] = field(default_factory=list)
    confirmed_owner: Optional[str] = None


@dataclass
class MemoryAccessResult:
    memory: Memory
    granted: bool
    reason: str


@dataclass
class AuditRecord:
    session_id: str
    memory_id: str
    sensitivity: SensitivityLevel
    auth_confidence: float
    granted: bool
    timestamp: str


@dataclass
class AuthCoupledMemory:
    memories: list[Memory] = field(default_factory=list)
    audit_log: list[AuditRecord] = field(default_factory=list)

    def is_owner_match(self, memory: Memory, request: AccessRequest) -> bool:
        """
        Verifica se a memoria pertence a um dos possible_owners
        ou se e compartilhada (owner com prefixo 'familia_').
        Se confirmed_owner definido, apenas esse owner (ou compartilhada).
        """
        # SEU CODIGO AQUI
        pass

    def can_access(self, memory: Memory, request: AccessRequest) -> MemoryAccessResult:
        """
        Verifica se o request tem confianca suficiente para acessar a memoria.

        Regras:
        1. Owner mismatch → negar
        2. Comparar auth_confidence com SENSITIVITY_THRESHOLDS[sensitivity]
        3. Se >= threshold: conceder; senao: negar
        4. Registrar no audit_log
        """
        # SEU CODIGO AQUI
        pass

    def retrieve_accessible(self, request: AccessRequest) -> list[Memory]:
        """
        Retorna todas as memorias acessiveis no nivel de autenticacao atual.
        Filtra por owner e sensitivity threshold.
        Ordena por sensitivity (LOW primeiro) e depois por memory_id.
        """
        # SEU CODIGO AQUI
        pass

    def get_blocked_memory_count(self, request: AccessRequest) -> dict[str, int]:
        """
        Contagem de memorias bloqueadas por nivel.
        Returns: {"low": 0, "medium": 3, "high": 5}
        """
        # SEU CODIGO AQUI
        pass

    def escalate_authentication(
        self, request: AccessRequest, new_method: AuthMethod, confirmed_owner: str
    ) -> AccessRequest:
        """
        Escala autenticacao para metodo mais seguro.
        Atualiza auth_confidence e define confirmed_owner.
        """
        # SEU CODIGO AQUI
        pass

    def build_greeting(self, request: AccessRequest) -> str:
        """
        Constroi saudacao segura baseada nas memorias acessiveis.
        NUNCA revela dados MEDIUM/HIGH nem menciona memorias bloqueadas.
        """
        # SEU CODIGO AQUI
        pass


# ============================================================
# TESTES RAPIDOS
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO AUTH-COUPLED MEMORY")
    print("=" * 60)

    # Construir banco de memorias
    memories = []
    for raw in FAMILY_SILVA_MEMORIES:
        memories.append(Memory(
            memory_id=raw["id"], owner=raw["owner"],
            sensitivity=SensitivityLevel(raw["sensitivity"]),
            content=raw["content"],
        ))
    acm = AuthCoupledMemory(memories=memories)

    # Teste 1: Phone shared (confidence=0.30) — apenas LOW
    req = AccessRequest("SES-5521", AuthMethod.PHONE_SHARED, 0.30,
                        possible_owners=["carlos_silva", "andre_silva", "lucia_silva"])
    accessible = acm.retrieve_accessible(req)
    print(f"Teste 1: Phone shared — {len(accessible)} memorias acessiveis")
    assert all(m.sensitivity == SensitivityLevel.LOW for m in accessible), \
        "Apenas LOW deve ser acessivel com confidence 0.30"
    print("  OK: apenas memorias LOW acessiveis")

    # Teste 2: Memorias bloqueadas
    blocked = acm.get_blocked_memory_count(req)
    print(f"Teste 2: Bloqueadas — LOW={blocked.get('low',0)}, MEDIUM={blocked.get('medium',0)}, HIGH={blocked.get('high',0)}")
    assert blocked.get("medium", 0) >= 1, "Deve haver MEDIUM bloqueadas"
    assert blocked.get("high", 0) >= 1, "Deve haver HIGH bloqueadas"
    print("  OK: MEDIUM e HIGH bloqueadas")

    # Teste 3: Escalar para PIN (Carlos)
    req_pin = acm.escalate_authentication(req, AuthMethod.PIN_CODE, "carlos_silva")
    acc_pin = acm.retrieve_accessible(req_pin)
    high_pin = [m for m in acc_pin if m.sensitivity == SensitivityLevel.HIGH]
    assert len(high_pin) == 0, "HIGH ainda bloqueado com confidence 0.65"
    print(f"Teste 3: PIN (Carlos) — {len(acc_pin)} memorias, HIGH bloqueadas OK")

    # Teste 4: Escalar para 2FA (Andre)
    req_2fa = acm.escalate_authentication(req_pin, AuthMethod.SMS_2FA, "andre_silva")
    acc_2fa = acm.retrieve_accessible(req_2fa)
    for m in acc_2fa:
        assert m.owner in ["andre_silva", "familia_silva"], \
            f"Andre nao deve ver memorias de {m.owner}"
    print(f"Teste 4: 2FA (Andre) — {len(acc_2fa)} memorias, isolamento OK")

    # Teste 5: Lucia com biometria
    req_lucia = AccessRequest("SES-9901", AuthMethod.VOICE_BIOMETRIC, 0.95,
                              confirmed_owner="lucia_silva")
    acc_lucia = acm.retrieve_accessible(req_lucia)
    high_lucia = [m for m in acc_lucia if m.sensitivity == SensitivityLevel.HIGH]
    assert len(high_lucia) >= 2, f"Lucia deve acessar HIGH, obtido {len(high_lucia)}"
    print(f"Teste 5: Biometria (Lucia) — {len(acc_lucia)} memorias, {len(high_lucia)} HIGH OK")

    # Teste 6: Greeting seguro
    g = acm.build_greeting(req)
    assert "senha" not in g.lower(), "Greeting nao deve revelar senha"
    assert "conta" not in g.lower(), "Greeting nao deve revelar dados financeiros"
    print(f"Teste 6: Greeting — \"{g}\" OK")

    # Teste 7: Audit trail
    print(f"Teste 7: Audit — {len(acm.audit_log)} registros OK")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES DO AUTH-COUPLED MEMORY PASSARAM")
    print("=" * 60)
```

---

### Parte 3: Simulacao de Sessao com Escalacao Progressiva (20 min)

```python
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SIMULACAO: SESSAO FAMILYTELCO — ESCALACAO PROGRESSIVA")
    print("=" * 60)

    acm = AuthCoupledMemory(memories=memories)

    # Fase 1: Telefone compartilhado
    req = AccessRequest("SES-7701", AuthMethod.PHONE_SHARED, 0.30,
                        possible_owners=["carlos_silva", "andre_silva", "lucia_silva"])
    p1 = acm.retrieve_accessible(req)
    print(f"FASE 1 (phone, auth=0.30): {len(p1)} memorias")
    print(f"  Greeting: \"{acm.build_greeting(req)}\"")

    blocked = acm.get_blocked_memory_count(req)
    if blocked.get("medium", 0) + blocked.get("high", 0) > 0:
        print("  Agente: 'Confirme seu PIN de 4 digitos para acessar seu historico.'")

    # Fase 2: PIN (Carlos)
    req = acm.escalate_authentication(req, AuthMethod.PIN_CODE, "carlos_silva")
    p2 = acm.retrieve_accessible(req)
    print(f"FASE 2 (PIN, auth=0.65, Carlos): {len(p2)} memorias")

    # Fase 3: 2FA
    blocked2 = acm.get_blocked_memory_count(req)
    if blocked2.get("high", 0) > 0:
        print("  Agente: 'Enviamos um codigo SMS para confirmar sua identidade.'")
    req = acm.escalate_authentication(req, AuthMethod.SMS_2FA, "carlos_silva")
    p3 = acm.retrieve_accessible(req)
    print(f"FASE 3 (2FA, auth=0.85): {len(p3)} memorias")

    high_carlos = [m for m in p3 if m.sensitivity == SensitivityLevel.HIGH]
    if not high_carlos:
        print("  (Carlos nao tem memorias HIGH — pertencem a Lucia)")

    print(f"\nRESUMO: {len(p1)} → {len(p2)} → {len(p3)} memorias reveladas")
    print(f"  Audit: {len(acm.audit_log)} registros")
    print(f"  Zero vazamentos entre owners confirmado")
```

---

## Validacao: Criterios de Aceitacao

### Criterio 1: Diagnostico (Parte 1)

- [ ] Classificou memorias vazadas por sensibilidade com dano documentado
- [ ] Explicou por que "memory startups haven't broken out"
- [ ] Propos politica para auth_confidence=0.05

### Criterio 2: Sensitivity thresholds

- [ ] LOW acessivel com auth >= 0.20
- [ ] MEDIUM requer auth >= 0.60
- [ ] HIGH requer auth >= 0.85
- [ ] auth=0.30 acessa APENAS LOW

### Criterio 3: Owner filtering

- [ ] `is_owner_match()` funciona para confirmed_owner e compartilhadas
- [ ] Andre nao ve memorias da Lucia
- [ ] Carlos nao ve memorias da Lucia

### Criterio 4: Escalation

- [ ] `escalate_authentication()` atualiza confianca corretamente
- [ ] phone → PIN desbloqueia MEDIUM
- [ ] PIN → 2FA desbloqueia HIGH

### Criterio 5: Audit + Greeting

- [ ] Audit log registra cada acesso
- [ ] `build_greeting()` nunca revela MEDIUM/HIGH
- [ ] `build_greeting()` nunca menciona memorias bloqueadas

---

## Rubrica de Avaliacao

| Criterio | Peso | Insuficiente (0-3) | Basico (4-6) | Proficiente (7-8) | Excelente (9-10) |
|---|---|---|---|---|---|
| **Diagnostico (Parte 1)** | 15% | Nao identificou o vazamento | Identificou sem classificar sensibilidade | Classificacao completa com dano | Politica para todos os niveis de auth |
| **Thresholds + Owner (Parte 2)** | 35% | Nao implementado | Thresholds funcionam, owner filter falha | Thresholds + owner filter corretos | Edge cases: telefone publico, owner removido |
| **Escalation (Partes 2+3)** | 30% | Nao implementado | Basico sem confirmed_owner | Completo com upgrade progressivo | Simulacao com zero vazamentos |
| **Testes + Audit** | 20% | Nenhum passa | 3 criterios | 4 criterios | Todos os 5 criterios |

**Nota final:** Media ponderada. **Aprovacao:** >= 7.0

---

## Dicas para Implementacao

1. **Thresholds sao dominios-especificos.** 0.20/0.60/0.85 sao para e-commerce. Um banco usaria 0.40/0.75/0.95. Ajuste conforme o dominio.

2. **O greeting e a superficie mais perigosa.** E facil vazar informacao na saudacao ("Ola Carlos! Vejo que sua alergia a lactose..."). O greeting so pode usar memorias LOW. Qualquer mention de dado MEDIUM ou HIGH e um vazamento.

3. **"Sem vazamento de sensibilidade" inclui implicito.** Dizer "Para ver seus dados financeiros, confirme 2FA" revela que existem dados financeiros. O agente deve dizer "Para continuar, confirme sua identidade" — sem especificar o que sera revelado.

4. **Owner filtering e tao importante quanto sensitivity.** Mesmo com auth_confidence=0.95, a Lucia nao deve ver memorias do Carlos (e vice-versa). O confirmed_owner restringe o escopo de owner, nao apenas de sensitivity.

---

## Duvidas Comuns

**P: Por que nao usar o telefone como identificador unico?**
R: Porque telefones sao compartilhados (familias, empresas, hoteis). Um numero de telefone identifica um ponto de contato, nao uma pessoa. A autenticacao resolve a ambiguidade: "este telefone tem 4 usuarios possiveis; qual deles esta falando agora?"

**P: Isso nao torna o agente menos util?**
R: Torna o agente menos perigoso. Um agente que revela dados financeiros da mae para o filho e "util" de forma errada. O Auth-Coupled Memory troca "utilidade maxima em qualquer cenario" por "utilidade proporcional a confianca de identidade". E um trade-off de seguranca, nao de funcionalidade.

**P: Como isso se relaciona com Addressable Memory Catalog?**
R: O Addressable Memory Catalog (`docs/canonical/addressable-memory-catalog.md`) define COMO armazenar e recuperar memorias. O Auth-Coupled Memory define QUEM pode acessar quais memorias. Sao camadas complementares: o catalogo gerencia a recuperacao tecnica; o auth-coupled memory gerencia a autorizacao de acesso.

---

## Proximo Passo

Depois de completar este exercicio:
1. Leia `[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]` para entender a camada de armazenamento
2. Leia `[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]` para entender grafos de memoria cross-session
3. (Opcional) Estenda com `AuthDecay`: auth_confidence diminui com inatividade (30 min sem interacao reduz 0.10)

---

*Exercicio Auth-Coupled Memory | Nivel 2 - Padroes Praticos*

**Memoria sem autenticacao e um banco de dados sem controle de acesso. Nao importa o quao boa e a recuperacao — se a autorizacao e fraca, o sistema e perigoso.**
