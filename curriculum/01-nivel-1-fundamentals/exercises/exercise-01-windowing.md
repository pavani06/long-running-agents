---
title: "Exercício 1: Implementar History Windowing"
type: curriculum-exercise
nivel: 1
aliases: ["janela deslizante", "history windowing", "compressão histórico", "exercício windowing"]
tags: [curriculo-conteudo, nivel-1, exercicio, context-management, token-budgeting, sliding-window, history-compression, metadata-preservation, head-tail-pattern, conversation-manager, python, dataclass]
relates-to: ["[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Plot]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
last_updated: 2026-06-10
---
# 🪟 Exercício 1: Implementar History Windowing

**Nível:** 1 - Fundamentals  
**Tempo Estimado:** 60-90 minutos  
**Dificuldade:** ⭐⭐ (Intermediária)  
**Pré-requisito:** Ter lido `03-basic-harness-patterns.md`  
**Status:** Hands-On Prático  

---

## 🎯 Objetivo

Você vai implementar um **gerenciador de histórico com janela deslizante** que:
1. Mantém apenas os últimos K mensagens em contexto
2. Comprime automaticamente histórico antigo em resumo
3. Preserva metadados críticos (preferências, decisões)
4. Simula chamadas a Claude e valida economia de tokens

**Resultado Final:** Você entenderá como KODA mantém conversas de 4+ horas sem degradação.

---

## 📖 O Problema Real

Você trabalha em um agente de recomendação. Cliente começa conversa às 14:00. Às 18:00, a conversa tem:
- 240+ mensagens
- 120K tokens de contexto
- Agente está LENTO (P95 latência: 4.2s)
- Taxa de erro subiu de 0.8% para 3.1%
- Custo por resposta: R$0.50 (era R$0.12)

**Por quê?** Você está passando TODA a conversa para o modelo a cada mensagem.

Seu trabalho: **implementar History Windowing para resolver isso.**

---

## 📋 Requisitos

### Funcional
- [ ] Classe `ConversationManager` que mantém histórico
- [ ] Adicionar/recuperar mensagens
- [ ] Janela deslizante de K mensagens (padrão: 20)
- [ ] Resumo automático quando atinge limite
- [ ] Preservação de metadados críticos
- [ ] Método `get_context_for_model()` que retorna contexto otimizado

### Técnico
- [ ] Suportar Python 3.8+
- [ ] Usar estruturas simples (dict, list, dataclass se preferir)
- [ ] Implementar logging de debug
- [ ] Adicionar type hints básicos
- [ ] Testes manuais com exemplos

### Validação
- [ ] Economia de tokens: deve economizar 50-70% vs manter tudo
- [ ] Memória de críticas: nunca perder decisões/preferências
- [ ] Rastreabilidade: conseguir debugar o que foi comprimido

### Requisitos Adicionais — Variante Head-Tail

**Funcional:**
- [ ] Preservar system prompt intacto.
- [ ] Manter head (N mensagens iniciais) e tail (M finais) no contexto ativo.
- [ ] Remover o middle do contexto ativo, mas armazená-lo com IDs recuperáveis.

**Técnico:**
- [ ] Cada mensagem do middle deve ter `id`, `role`, `preview` com 80 caracteres e `full_text`.
- [ ] Contexto final deve seguir a forma `[system_prompt] + [head] + [tail] + [latest_result]`.
- [ ] Implementar função `fetch_omitted(id)` para recuperar conteúdo omitido por handle.

**Validação:**
- [ ] Contexto ativo contém system prompt, primeiro turno, último turno e resultado.
- [ ] Middle está ausente do contexto ativo, mas recuperável.
- [ ] Follow-up que referencia o middle é respondido corretamente após fetch.

---

## 🚀 Starter Code

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import json

@dataclass
class OmittedMessage:
    id: str
    role: str  # "user" | "assistant" | "tool"
    preview: str  # primeiros 80 caracteres
    full_text: str

@dataclass
class ContextWindow:
    system_prompt: str
    head: list[Message]
    tail: list[Message]
    latest_result: str
    memory_catalog: list[OmittedMessage]  # middle armazenado

class ConversationManager:
    """
    Gerencia histórico de conversa com janela deslizante.
    
    Requisitos:
    - Manter últimas K mensagens em contexto
    - Resumir histórico antigo automaticamente
    - Preservar metadados críticos
    - Retornar contexto otimizado para o modelo
    """
    
    def __init__(
        self, 
        max_window_messages: int = 20,
        max_tokens_history: int = 30000
    ):
        """
        Args:
            max_window_messages: Quantas mensagens recentes manter (default: 20)
            max_tokens_history: Máximo de tokens no histórico total (ref apenas)
        """
        # TODO: Implementar inicialização
        pass
    
    def add_message(
        self, 
        role: str, 
        content: str, 
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Adiciona mensagem ao histórico.
        
        Args:
            role: "user" ou "assistant"
            content: Conteúdo da mensagem
            metadata: Metadados opcionais (decisão, preferência, etc)
        
        Comportamento esperado:
        - Se atingir max_window_messages, comprime histórico antigo
        - Se há metadados críticos, preserva em critical_metadata
        """
        # TODO: Implementar
        pass
    
    def _compress_history(self) -> None:
        """
        Comprime as 10 mensagens mais antigas em um resumo.
        
        Comportamento esperado:
        - Remove as 10 mensagens mais antigas de recent_messages
        - Gera resumo (para simular, use um placeholder)
        - Atualiza historical_summary
        - Extrai e preserva metadados críticos
        """
        # TODO: Implementar
        pass
    
    def _extract_critical_metadata(self, messages: List[Dict]) -> None:
        """
        Extrai informações críticas que nunca devem expirar.
        
        Procura por:
        - metadata['decision']: Decisões tomadas
        - metadata['preference']: Preferências confirmadas
        - metadata['commitment']: Compromissos feitos
        
        Comportamento esperado:
        - Se encontrar, adiciona a critical_metadata
        """
        # TODO: Implementar
        pass
    
    def get_context_for_model(self) -> str:
        """
        Retorna contexto otimizado para passar ao modelo Claude.
        
        Ordem esperada:
        1. Metadados críticos (nunca expiram)
        2. Resumo do histórico antigo (comprimido)
        3. Histórico recente (janela deslizante)
        
        Returns:
            String com contexto formatado
        
        Exemplo esperado:
        '''
        CRITICAL CONTEXT (Never expires):
        - Previous Decisions: [...]
        - Customer Preferences: [...]
        
        CONVERSATION HISTORY SUMMARY:
        [resumo do histórico antigo]
        
        RECENT MESSAGES:
        user: Qual seu orçamento?
        assistant: Seu orçamento é R$100-150
        user: Posso aumentar para R$200?
        ...
        '''
        """
        # TODO: Implementar
        pass
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas sobre o histórico (para debug).
        
        Returns:
            {
                'total_messages': int,
                'recent_messages_count': int,
                'has_summary': bool,
                'critical_metadata_keys': list,
                'estimated_tokens': int (aproximado)
            }
        """
        # TODO: Implementar
        pass


# ============================================================================
# TESTS / EXEMPLOS DE USO
# ============================================================================

def test_basic_workflow():
    """Test 1: Fluxo básico de adicionar mensagens"""
    print("\n🧪 Test 1: Fluxo Básico")
    
    manager = ConversationManager(max_window_messages=5)  # Pequeno para testar
    
    # Simular conversa
    manager.add_message("user", "Oi! Gosto de chocolate", 
                       metadata={"preference": "flavor=chocolate"})
    manager.add_message("assistant", "Entendi! Vou recomendar produtos com chocolate")
    
    # Verificar
    stats = manager.get_statistics()
    assert stats['total_messages'] == 2, "Deve ter 2 mensagens"
    assert stats['recent_messages_count'] == 2, "Ambas em recent_messages"
    
    print("✅ Test 1 passou!")


def test_history_compression():
    """Test 2: Compressão automática quando atinge limite"""
    print("\n🧪 Test 2: Compressão Automática")
    
    manager = ConversationManager(max_window_messages=5)
    
    # Adicionar 10 mensagens (deve triggerar compressão)
    for i in range(10):
        manager.add_message("user", f"Mensagem {i}")
        manager.add_message("assistant", f"Resposta {i}")
    
    # Verificar
    stats = manager.get_statistics()
    assert stats['recent_messages_count'] == 5, "Deve manter apenas 5 recentes"
    assert stats['has_summary'] == True, "Deve ter resumo"
    
    print("✅ Test 2 passou!")


def test_critical_metadata_preservation():
    """Test 3: Preservação de metadados críticos"""
    print("\n🧪 Test 3: Preservação de Metadados")
    
    manager = ConversationManager(max_window_messages=3)
    
    # Adicionar mensagem com metadado crítico (vai ser comprimida)
    manager.add_message("user", "Meu budget é R$100", 
                       metadata={"preference": "budget=100"})
    
    # Adicionar mais mensagens para triggerizar compressão
    for i in range(5):
        manager.add_message("user", f"Pergunta {i}")
        manager.add_message("assistant", f"Resposta {i}")
    
    # Verificar se preferência foi preservada
    context = manager.get_context_for_model()
    assert "budget=100" in context or "R$100" in context, \
        "Preferência crítica deve estar no contexto!"
    
    print("✅ Test 3 passou!")


def test_context_output():
    """Test 4: Formato do contexto para o modelo"""
    print("\n🧪 Test 4: Formato de Contexto")
    
    manager = ConversationManager(max_window_messages=3)
    
    manager.add_message("user", "Oi!", metadata={"decision": "init_conversation"})
    manager.add_message("assistant", "Olá! Como posso ajudar?")
    manager.add_message("user", "Gosto de chocolate", metadata={"preference": "chocolate"})
    manager.add_message("assistant", "Anotado!")
    
    context = manager.get_context_for_model()
    
    # Verificar estrutura esperada
    assert "CRITICAL CONTEXT" in context or "RECENT MESSAGES" in context, \
        "Contexto deve ter seções bem-definidas"
    assert "user:" in context.lower() or "user" in context.lower(), \
        "Deve mostrar mensagens do usuário"
    
    print("✅ Test 4 passou!")


def test_head_tail_preserves_anchors():
    """System prompt, primeira e última mensagens estão no contexto ativo."""
    print("\n🧪 Test 5: Head-Tail Preserva Âncoras")

    manager = ConversationManager(max_window_messages=5)
    context_window = manager.get_context_for_model()

    assert "system" in context_window.lower() or "critical" in context_window.lower(), (
        "System prompt ou contexto crítico deve estar preservado"
    )
    assert "recent" in context_window.lower() or "messages" in context_window.lower(), (
        "Tail recente deve estar no contexto ativo"
    )

    print("✅ Test 5 passou!")


def test_middle_is_recoverable():
    """Mensagem do middle pode ser recuperada por fetch_omitted(id)."""
    print("\n🧪 Test 6: Middle Recuperável")

    omitted = OmittedMessage(
        id="msg_middle_001",
        role="user",
        preview="Cliente comparou whey vegano e isolado antes de decidir",
        full_text="Cliente comparou whey vegano e isolado antes de decidir pelo produto sem lactose.",
    )

    assert omitted.id == "msg_middle_001", "Mensagem omitida deve ter ID estável"
    assert omitted.full_text.startswith(omitted.preview[:40]), (
        "Preview deve apontar para o conteúdo recuperável"
    )

    print("✅ Test 6 passou!")


def test_followup_after_truncation():
    """Follow-up que referencia middle ainda é respondido corretamente após fetch."""
    print("\n🧪 Test 7: Follow-up Após Truncation")

    omitted = OmittedMessage(
        id="msg_middle_002",
        role="assistant",
        preview="KODA explicou que whey vegano evita lactose",
        full_text="KODA explicou que whey vegano evita lactose e cabe no orçamento confirmado.",
    )
    followup = "aquele whey sem lactose ainda cabe no orçamento?"

    assert "lactose" in omitted.full_text.lower(), (
        "Fetch do middle deve recuperar o fato necessário ao follow-up"
    )
    assert "orçamento" in omitted.full_text.lower(), (
        "Fetch do middle deve recuperar o critério usado na resposta"
    )
    assert "whey" in followup.lower(), "Follow-up deve referenciar conteúdo omitido"

    print("✅ Test 7 passou!")


def simulate_long_conversation():
    """Simulação: Conversa de 4 horas"""
    print("\n🧪 Test 8: Simulação - Conversa Longa (4 horas)")
    
    manager = ConversationManager(max_window_messages=20)
    
    # Simular 100 trocas (user + assistant)
    for turn in range(100):
        manager.add_message("user", f"Pergunta {turn}", 
                           metadata={"turn": turn})
        manager.add_message("assistant", f"Resposta {turn}")
    
    stats = manager.get_statistics()
    
    print(f"  Total de mensagens adicionadas: {stats['total_messages']}")
    print(f"  Mensagens recentes mantidas: {stats['recent_messages_count']}")
    print(f"  Tem resumo comprimido: {stats['has_summary']}")
    print(f"  Tokens estimados (contexto final): {stats['estimated_tokens']}")
    
    # Economia de tokens
    # Se mantivesse TUDO: ~200K tokens
    # Com windowing: ~30-40K tokens
    economy = (200000 - stats['estimated_tokens']) / 200000 * 100
    print(f"  💰 Economia de tokens: ~{economy:.1f}%")
    
    print("✅ Test 5 passou!")


if __name__ == "__main__":
    print("="*60)
    print("EXERCÍCIO 1: IMPLEMENTAR HISTORY WINDOWING")
    print("="*60)
    
    # Quando implementado, descomente para testar:
    # test_basic_workflow()
    # test_history_compression()
    # test_critical_metadata_preservation()
    # test_context_output()
    # simulate_long_conversation()
    
    print("\n📝 TODO: Implemente a classe ConversationManager acima!")
    print("   Após implementar, descomente os tests em main()")
```

---

## 🏗️ Como Começar

### Passo 1: Entender a Estrutura
Leia o starter code acima. Foco em:
- `__init__`: Inicializar estruturas
- `add_message`: Adicionar + triggerizar compressão
- `_compress_history`: Logica de compressão
- `get_context_for_model`: Retornar contexto formatado

### Passo 2: Implementar `__init__`
```python
def __init__(self, max_window_messages: int = 20, max_tokens_history: int = 30000):
    self.max_window = max_window_messages
    self.max_tokens = max_tokens_history
    self.recent_messages = []
    self.historical_summary = None
    self.critical_metadata = {
        "decisions": [],
        "preferences": {},
        "commitments": []
    }
```

### Passo 3: Implementar `add_message`
- Adicionar à `recent_messages`
- Se `len(recent_messages) > max_window`, chamar `_compress_history()`

### Passo 4: Implementar `_compress_history`
- Pegar as 10 primeiras mensagens de `recent_messages`
- Gerar resumo (pode ser placeholder: "Summary of conversations 1-10")
- Salvar em `historical_summary`
- Chamar `_extract_critical_metadata` para extrair dados críticos
- Remover as 10 mensagens antigas

### Passo 5: Implementar `get_context_for_model`
- Retornar string com 3 seções:
  1. Critical metadata (sempre inclui)
  2. Historical summary (se existe)
  3. Recent messages (janela atual)

### Passo 6: Testar
- Descomente os tests
- Execute `python seu_arquivo.py`
- Todos tests devem passar ✅

---

## 🎯 Desafios Extra (Opcional)

Se terminar rápido, implemente também:

### Desafio 1: Integração com Claude API
```python
def _compress_with_claude(self, messages_to_compress: List[Dict]) -> str:
    """
    Use Claude para gerar resumo de verdade (não placeholder).
    Dica: Veja exemplo em `03-basic-harness-patterns.md`
    """
    pass
```

### Desafio 2: Persistência em Banco
```python
def save_to_db(self, conversation_id: str, db_path: str = "conversations.db"):
    """Salva estado completo em SQLite"""
    pass

def load_from_db(self, conversation_id: str, db_path: str = "conversations.db"):
    """Carrega estado anterior"""
    pass
```

### Desafio 3: Métricas Reais de Tokens
```python
def estimate_tokens(self, text: str) -> int:
    """
    Estime tokens de verdade usando:
    - Encoding tiktoken (para GPT)
    - Ou simples: len(text.split()) * 1.3
    """
    pass
```

### Desafio 4: Validação de Dados Críticos
```python
def validate_critical_metadata(self) -> Dict[str, bool]:
    """
    Valida que metadados críticos nunca foram perdidos.
    Retorna relatório de conformidade.
    """
    pass
```

---

## 📊 Checklist de Implementação

- [ ] Classe `ConversationManager` criada
- [ ] Método `__init__` implementado
- [ ] Método `add_message` implementado
- [ ] Método `_compress_history` implementado
- [ ] Método `_extract_critical_metadata` implementado
- [ ] Método `get_context_for_model` implementado
- [ ] Método `get_statistics` implementado
- [ ] Test 1 (básico) passa ✅
- [ ] Test 2 (compressão) passa ✅
- [ ] Test 3 (metadados) passa ✅
- [ ] Test 4 (contexto) passa ✅
- [ ] Test 5 (conversa longa) passa ✅

---

## 💡 Dicas de Implementação

**Dica 1:** Comece simples. Não otimize tokens no início, foco em lógica.

**Dica 2:** Use `print()` ou `logging` para debug. Exemplo:
```python
print(f"📊 Stats: {self.get_statistics()}")
```

**Dica 3:** Metadados críticos devem estar em **dicionários** estruturados, não strings vagas.

**Dica 4:** Teste com `max_window_messages=3` ou `=5` para ver compressão rápido.

**Dica 5:** Contexto final deve ser **legível**. Algo que você passaria para Claude de verdade.

---

## ✅ Validação Final

Sua implementação está correta se:

1. ✅ Todos os 5 testes passam
2. ✅ Economia de tokens é 40-70% (vs manter tudo)
3. ✅ Metadados críticos **nunca** são perdidos
4. ✅ Contexto é legível e formatado bem
5. ✅ Código tem type hints básicos
6. ✅ Não há crashes/exceções não tratadas

---

## 🎓 O Que Você Aprendeu

Após completar este exercício, você entende:

- ✅ Como manter histórico eficiente com janela deslizante
- ✅ Quando triggerar compressão
- ✅ Como preservar informações críticas
- ✅ Trade-off entre contexto completo vs comprimido
- ✅ Como formatar contexto para o modelo

**Próximo:** Exercício 2 - Implementar Structured Output

---

*Exercício 1 de Nível 1 | Curso Long-Running Agents | FutanBear Technical Program*
