---
title: "Coordenacao Baseada em Arquivos para Agentes Confiaveis"
type: curriculum-lesson
nivel: 3
aliases: []
tags: [curriculo-conteudo, nivel-3, arquitetura-avancada, coordenacao-baseada-em-arquivos, arquivos-de-lock, arquivos-de-status, protocolo-json, controle-de-concorrencia, condicao-de-corrida, manifest-auditavel, idempotencia, escrita-atomica, rastreamento-auditavel]
relates-to: ["[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[curriculum/05-core-concepts/05-state-persistence|State Persistence Concept]]"]
last_updated: 2026-06-10
---
# 🔗 Coordenacao Baseada em Arquivos para Agentes Confiaveis
## Como lock files, status files e JSON protocol tornam o KODA auditável, retomável e seguro

**Tempo Estimado:** 90 minutos  
**Nível:** 3 - Arquitetura Avançada  
**Pré-requisito:** `01-multi-agent-systems.md`  
**Status:** 🟢 CRITICO  
**Data de Criação:** Maio 2026

---

## 📖 Prologo: A noite em que dois agentes quase venderam o mesmo pedido

**Cenário real: terça-feira, 21h08.**

Marina tinha saído do trabalho mais tarde do que o normal.

O treino tinha sido pesado, daqueles que deixam a perna tremendo na escada.

Ela chegou em casa cansada, mas determinada a resolver a compra de suplemento antes de dormir.

O WhatsApp do KODA ainda estava salvo desde a conversa anterior.

Ela abriu o chat e foi direta.

```
21:09 Marina: Oi, quero fechar aquele whey isolado chocolate que voce tinha recomendado.
21:09 Marina: Ainda tenho intolerancia a lactose e meu limite continua R$ 220.
21:10 Marina: Se der para entregar amanha em Pinheiros, melhor.
```
Para Marina, era uma continuação simples.

Para o KODA, era uma jornada com risco.

O Discovery Agent recebeu a mensagem e começou a extrair intenção.

O Order Agent recebeu o mesmo evento por outro caminho interno.

O Fulfillment Agent viu uma alteração de carrinho em cache e tentou reservar estoque.

Cada agente queria ajudar.

Nenhum deles parecia errado olhando de perto.

O problema era que eles não tinham um lugar comum para combinar quem mandava em qual parte.

O Discovery Agent registrou que Marina queria whey isolado, chocolate e sem lactose.

O Order Agent montou um pedido usando uma versão antiga do contexto.

O Fulfillment Agent reservou o último item de estoque antes de o pedido passar pelo Evaluator.

Em poucos segundos, o sistema tinha três verdades diferentes.

```
21:11 Discovery Agent: intenção de compra, whey isolado chocolate, sem lactose.
21:11 Order Agent: pedido criado com whey concentrado chocolate, melhor margem.
21:11 Fulfillment Agent: estoque reservado para SKU antigo, lote SP-17.
```
Fernando, tech lead do KODA, viu o trace e sentiu o tipo de frio que não aparece em dashboard.

Não era um crash.

Não era uma exceção óbvia.

Era uma falha de coordenação.

O sistema respondeu rápido.

Rápido demais.

```
21:12 KODA: Pedido confirmado, Marina. Whey Concentrado Chocolate, entrega amanha.
21:12 Marina: Concentrado? Eu tenho intolerancia a lactose.
```
A confiança da cliente caiu na hora.

Marina não estava pedindo uma recomendação complexa.

Ela tinha dado uma restrição clara.

O KODA ignorou essa restrição na etapa que mais importava.

Fernando abriu os logs e viu o desenho da falha.

O Discovery Agent sabia da intolerância.

O Order Agent não leu o estado mais recente.

O Fulfillment Agent agiu antes da aprovação.

O Delivery worker enviou uma mensagem sem verificar a decisão final.

Nenhum prompt isolado explicava o problema inteiro.

A arquitetura explicava.

Quando agentes trabalham sem coordenação explícita, cada agente pode estar localmente certo.

Mas o sistema pode estar globalmente errado.

Esse é o perigo de long-running agents em fluxo comercial.

Um agente processa duas vezes o mesmo evento.

Outro agente lê estado antigo.

Um terceiro escreve por cima de um arquivo recém criado.

O cliente vê apenas o resultado final.

Pedido perdido.

Pedido duplicado.

Estado inconsistente.

Promessa errada.

Fernando decidiu parar o fluxo automático por alguns minutos.

O time reproduziu a conversa de Marina com uma regra nova.

Nenhum agente poderia agir apenas porque viu uma mensagem.

Todo agente teria que ler arquivos de entrada definidos.

Todo agente teria que escrever arquivos de saída definidos.

Toda alteração de estado compartilhado teria que passar por `lock file`.

Toda etapa teria que declarar progresso em `status.json`.

Toda decisão enviada para cliente teria que apontar para `audit_refs`.

O evento do WhatsApp virou `conversation_event.json`.

O Discovery Agent leu esse arquivo e escreveu `discovery.json`.

O Order Agent esperou `discovery.status.json` marcar `completed`.

Antes de criar pedido, o Order Agent tentou adquirir `order.lock.json`.

Como o lock estava livre, ele escreveu `order_draft.json.tmp`.

Depois publicou `order_draft.json` com atomic rename.

O Evaluator leu `discovery.json`, `order_draft.json` e `generation.json`.

Ele rejeitaria qualquer produto com lactose.

O Fulfillment Agent só poderia rodar depois de `evaluation.json` com `decision: approved`.

Dessa vez, o sistema demorou alguns segundos a mais.

Mas a resposta saiu correta.

```
21:15 KODA: Marina, confirmei o Whey Isolado Chocolate, sem lactose, R$ 199,90.
21:15 KODA: Temos estoque em SP e entrega estimada para amanha em Pinheiros.
21:15 KODA: Posso gerar o link de pagamento?
21:16 Marina: Pode sim. Obrigada por confirmar sem lactose.
```
A diferença não foi um modelo maior.

Também não foi um prompt mais bonito.

Foi file-based coordination.

Arquivos deram memória externa.

Arquivos deram ordem.

Arquivos deram audit trail.

Arquivos deram um ponto de retomada quando algo falha.

Fernando resumiu o aprendizado no dia seguinte.

Se um agente precisa confiar no output de outro, esse output precisa existir fora da cabeça do agente.

Se dois agentes podem tocar no mesmo estado, precisa existir controle de concorrência.

Se uma etapa pode falhar, precisa existir status visível.

Se uma decisão pode afetar cliente, precisa existir rastro.

Este módulo nasce desse incidente.

Você vai aprender a usar o file system como coordination bus.

Vai aprender como `lock file`, `status file`, `JSON protocol` e `atomic write` trabalham juntos.

No fim, você deve conseguir desenhar um pipeline de pedidos do KODA que não depende de sorte.

---

## 🔗 Conexao com Nivel Anterior

No módulo `01-multi-agent-systems.md`, você viu que agentes precisam trocar informação por algum canal.

Aquele módulo apresentou file-based coordination, message queues e API-based communication.

A recomendação era começar com file-based porque ele é simples, auditável e bom para aprender contratos.

Este módulo pega essa recomendação e transforma em arquitetura prática.

O Planner não precisa chamar o Generator diretamente.

Ele escreve `plan.json`.

O Generator não precisa pedir explicação ao Planner.

Ele lê `plan.json`.

O Evaluator não precisa confiar em memória implícita.

Ele lê `plan.json`, `generation.json` e os arquivos de estado da jornada.

Essa mudança reduz acoplamento.

Também aumenta rastreabilidade.

O módulo anterior explicou por que dividir responsabilidades entre agentes.

Este módulo explica como esses agentes se coordenam sem atropelar uns aos outros.

| Nivel | Arquitetura | Pergunta Principal | Resultado |
| --- | --- | --- | --- |
| **Nível 2** | Generator/Evaluator | Como separar criação de avaliação? | Saídas melhores com rubrica independente |
| **Nível 3, módulo 01** | Multi-agent systems | Como dividir uma jornada longa em papéis? | Planner, Generator e Evaluator com ownership claro |
| **Nível 3, este módulo** | File-based coordination | Como agentes trocam estado com segurança? | Arquivos JSON, locks, status e audit trail |
| **Nível 3, próximo passo** | State persistence avançada | Como retomar jornadas longas? | Estado externo como fonte confiável |

1. `plan.json` representa contrato de trabalho.

2. `generation.json` representa output candidato.

3. `evaluation.json` representa decisão verificável.

4. `status.json` representa progresso observável.

5. `lock.json` representa exclusividade temporária.

6. `delivery.json` representa mensagem aprovada para cliente.

---

## 📁 O Que E File-Based Coordination

File-based coordination é um padrão em que agentes coordenam trabalho por arquivos compartilhados.

Em vez de chamar funções uns dos outros, eles leem e escrevem artefatos no file system.

O file system vira um communication bus simples.

Esse bus não precisa ser sofisticado para ser útil.

Ele precisa ser previsível, auditável e seguro contra escrita parcial.

O modelo mental é direto.

Um agente observa uma pasta.

Ele encontra um arquivo de entrada pronto.

Ele tenta adquirir lock quando precisa alterar estado compartilhado.

Ele escreve um arquivo temporário.

Ele publica o resultado com atomic rename.

Ele atualiza um status file.

Outro agente lê esse status e continua o fluxo.

O Discovery Agent não precisa conhecer a implementação interna do Order Agent.

O Order Agent só precisa conhecer o contrato de `discovery.json`.

O Fulfillment Agent não precisa conversar com o Evaluator.

Ele só precisa saber que `evaluation.json` aprovado libera a próxima etapa.

Esse padrão combina com long-running agents porque agentes longos precisam pausar, retomar e explicar o que aconteceu.

Se o processo cai, os arquivos continuam lá.

Se um output parece errado, você abre o JSON e lê.

Se um agente repetiu trabalho, você compara timestamps e status.

```
Agente A                         Pasta compartilhada                     Agente B
   │                                      │                                  │
   │ escreve input.json                   │                                  │
   │─────────────────────────────────────▶│                                  │
   │                                      │ lê input.json                    │
   │                                      │◀─────────────────────────────────│
   │                                      │                                  │
   │                                      │ escreve output.tmp               │
   │                                      │◀─────────────────────────────────│
   │                                      │ renomeia para output.json        │
   │                                      │                                  │
   │ lê output.json                       │                                  │
   │◀─────────────────────────────────────│                                  │
```

| Motivo | Como ajuda o KODA |
| --- | --- |
| **Persistência simples** | Um arquivo continua existindo depois que o processo termina |
| **Observabilidade direta** | Você abre o JSON e entende o que o agente sabia |
| **Audit trail natural** | Cada artefato vira evidência da jornada |
| **Baixo custo de entrada** | O time aprende contratos antes de operar filas |
| **Debug fácil** | Você copia uma pasta de trace e reproduz a falha |
| **Retomada clara** | Um worker encontra status `failed` ou `pending` e continua |
| **Contratos explícitos** | O JSON mostra campos, autores e leitores |
| **Boa didática** | O padrão é visual e fácil de revisar em code review |

### Regras básicas para começar

1. Comece com uma pasta por conversa ou pedido.

2. Use nomes previsíveis e estáveis.

3. Nunca faça dois agentes escreverem o mesmo arquivo final sem lock.

4. Escreva primeiro em arquivo temporário.

5. Publique com atomic rename.

6. Inclua `schema_version` em todos os JSONs.

7. Inclua `created_at`, `updated_at` ou `completed_at` quando fizer sentido.

8. Inclua `agent_id` para rastrear ownership.

9. Inclua `correlation_id` para ligar arquivos da mesma jornada.

10. Evite guardar segredos ou dados sensíveis sem necessidade.

---

## 🔒 Lock Files e Controle de Concorrencia

Lock files respondem uma pergunta prática.

Quem tem permissão de mexer neste estado agora?

Quando dois agentes podem escrever no mesmo recurso, você tem risco de race condition.

Race condition acontece quando o resultado depende da ordem acidental de operações concorrentes.

No KODA, isso aparece quando dois workers tentam criar o mesmo pedido.

Também aparece quando um agente atualiza `customer_profile.json` enquanto outro lê no meio da escrita.

Sem lock, cada agente pode ver uma versão parcial da realidade.

Com lock, você cria uma regra de exclusividade temporária.

Um agente adquire o lock.

Ele faz a alteração.

Ele publica o resultado com atomic write.

Ele libera o lock.

Outro agente só entra depois.

```
Tempo  Order Agent A                 Order Agent B                 Resultado
T1     lê cart.json vazio             lê cart.json vazio             dois veem carrinho aberto
T2     adiciona whey isolado          adiciona creatina              mudanças paralelas
T3     escreve cart.json              escreve cart.json              última escrita vence
T4     status mostra 1 item           item anterior some             pedido fica inconsistente
```

```
┌────────────────┐
│ lock ausente   │
└───────┬────────┘
        │ agente tenta acquire_lock
        ▼
┌────────────────┐
│ lock criado    │
│ owner definido │
└───────┬────────┘
        │ agente executa seção crítica
        ▼
┌────────────────┐
│ estado escrito │
│ atomic rename  │
└───────┬────────┘
        │ release_lock
        ▼
┌────────────────┐
│ lock removido  │
│ próximo espera │
└────────────────┘

Caminho alternativo:

┌────────────────┐
│ lock existe    │
└───────┬────────┘
        │ is_stale retorna true
        ▼
┌────────────────┐
│ lock recuperado│
│ owner novo     │
└────────────────┘
```

```python
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

class LockFileManager:
    def __init__(self, lock_path, owner_id, ttl_seconds=120):
        self.lock_path = Path(lock_path)
        self.owner_id = owner_id
        self.ttl_seconds = ttl_seconds

    def now_iso(self):
        return datetime.now(timezone.utc).isoformat()

    def read_lock(self):
        with self.lock_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def is_stale(self):
        if not self.lock_path.exists():
            return False
        try:
            payload = self.read_lock()
            created_at = datetime.fromisoformat(payload["created_at"])
            age = datetime.now(timezone.utc) - created_at
            return age.total_seconds() > self.ttl_seconds
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            return True

    def acquire_lock(self, max_attempts=10, sleep_seconds=0.5):
        for attempt in range(1, max_attempts + 1):
            payload = {
                "schema_version": "1.0",
                "owner_id": self.owner_id,
                "created_at": self.now_iso(),
                "ttl_seconds": self.ttl_seconds,
                "attempt": attempt
            }
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            try:
                fd = os.open(self.lock_path, flags)
                with os.fdopen(fd, "w", encoding="utf-8") as file:
                    json.dump(payload, file, indent=2)
                    file.write("\n")
                return True
            except FileExistsError:
                time.sleep(sleep_seconds)
        return False

    def release_lock(self):
        if not self.lock_path.exists():
            return
        payload = self.read_lock()
        if payload.get("owner_id") != self.owner_id:
            raise RuntimeError("lock pertence a outro agente")
        self.lock_path.unlink()
```

Esse pseudocódigo usa `O_EXCL` para criar o lock somente se ele ainda não existir.

Dois agentes podem tentar ao mesmo tempo.

Apenas um consegue criar o arquivo.

O outro recebe `FileExistsError` e entra em retry.

O campo `owner_id` mostra quem segura o lock.

O campo `created_at` permite detectar stale lock.

O campo `ttl_seconds` define quanto tempo o lock pode viver antes de parecer abandonado.

A função `release_lock()` confere ownership antes de remover o arquivo.

Isso evita que um agente apague o lock de outro por engano.

A detecção de stale lock (`is_stale`) é usada pelo supervisor, não pelos agentes concorrentes. O supervisor lê o lock, confere o TTL e, se o dono original não responder mais, remove o lock de forma segura. Agentes que disputam o mesmo recurso devem fazer retry ou reportar `failed` — nunca desbloquear locks que não criaram.

```python
def atomic_write_json(path, payload):
    final_path = Path(path)
    temp_path = final_path.with_suffix(final_path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
        file.write("\n")
        file.flush()
        os.fsync(file.fileno())
    os.replace(temp_path, final_path)
```

| Estratégia | Uso prático |
| --- | --- |
| **Retry curto** | Use quando a seção crítica leva poucos segundos |
| **Backoff simples** | Aumente o intervalo quando vários agentes disputam o mesmo lock |
| **Jitter** | Adicione variação pequena para evitar thundering herd |
| **Timeout claro** | Depois do limite, marque `failed` e registre motivo |
| **Reprocessamento idempotente** | Permita repetir sem duplicar pedido ou cobrança |

### Como reconhecer stale lock

1. O `created_at` é antigo demais para o tipo de operação.

2. O processo dono não aparece mais no supervisor.

3. O `status.json` da etapa está parado em `in_progress` além do limite.

4. Não há atualização em `heartbeat_at` quando esse campo existe.

5. O arquivo temporário relacionado não muda há tempo suficiente.

6. O agente novo consegue provar que a operação anterior não publicou resultado final.

### Checklist de lock no KODA

1. Use lock ao alterar `order_draft.json`.

2. Use lock ao alterar `customer_profile.json`.

3. Use lock ao reservar estoque.

4. Use lock ao publicar `delivery.json`.

5. Não use lock para leitura simples.

6. Não segure lock enquanto espera ferramenta externa lenta sem necessidade.

7. Prefira seção crítica curta.

8. Registre `owner_id` legível.

9. Registre `correlation_id` do pedido.

10. Remova lock apenas se você for o owner.

---

## 📊 Status Files e State Machines

Lock file responde quem pode escrever agora.

Status file responde em que ponto a etapa está.

Um `status.json` transforma execução invisível em state machine observável.

Sem status, você só sabe que um arquivo apareceu ou não apareceu.

Com status, você sabe se uma etapa está `pending`, `in_progress`, `completed` ou `failed`.

Esses quatro estados são suficientes para muitos pipelines do KODA.

Você pode adicionar estados depois, mas comece com poucos.

Poucos estados reduzem ambiguidade.

| Estado | Significado | Quem escreve | Próxima ação |
| --- | --- | --- | --- |
| **pending** | A etapa foi criada, mas ainda não começou | Orchestrator ou agente anterior | Worker pode assumir |
| **in_progress** | Um agente assumiu a etapa | Agente dono | Outros aguardam |
| **completed** | A etapa terminou e publicou output válido | Agente dono | Próxima etapa pode começar |
| **failed** | A etapa falhou com motivo registrado | Agente dono ou supervisor | Retry, revisão ou fallback |

```
┌────────────┐
│  pending   │
└─────┬──────┘
      │ agente assume
      ▼
┌────────────┐
│in_progress │
└─────┬──────┘
      │ output válido
      ▼
┌────────────┐
│ completed  │
└────────────┘

Caminho de falha:

┌────────────┐
│in_progress │
└─────┬──────┘
      │ erro recuperável ou definitivo
      ▼
┌────────────┐
│   failed   │
└─────┬──────┘
      │ retry permitido
      ▼
┌────────────┐
│  pending   │
└────────────┘
```

### Exemplo de status pending

```json
{
  "schema_version": "1.0",
  "status": "pending",
  "step": "order_draft",
  "conversation_id": "wa_2026_05_26_marina",
  "correlation_id": "order_corr_20260526_2110",
  "created_at": "2026-05-26T21:10:05-03:00",
  "updated_at": "2026-05-26T21:10:05-03:00",
  "agent_id": null,
  "input_refs": ["conversation_event.json", "discovery.json"],
  "output_refs": []
}
```

### Exemplo de status in_progress

```json
{
  "schema_version": "1.0",
  "status": "in_progress",
  "step": "order_draft",
  "conversation_id": "wa_2026_05_26_marina",
  "correlation_id": "order_corr_20260526_2110",
  "started_at": "2026-05-26T21:10:09-03:00",
  "updated_at": "2026-05-26T21:10:09-03:00",
  "agent_id": "order-agent-02",
  "lock_ref": "locks/order.lock.json",
  "input_refs": ["conversation_event.json", "discovery.json"],
  "output_refs": []
}
```

### Exemplo de status completed

```json
{
  "schema_version": "1.0",
  "status": "completed",
  "step": "order_draft",
  "conversation_id": "wa_2026_05_26_marina",
  "correlation_id": "order_corr_20260526_2110",
  "completed_at": "2026-05-26T21:10:17-03:00",
  "agent_id": "order-agent-02",
  "input_refs": ["conversation_event.json", "discovery.json"],
  "output_refs": ["order_draft.json"]
}
```

### Exemplo de status failed

```json
{
  "schema_version": "1.0",
  "status": "failed",
  "step": "inventory_reservation",
  "conversation_id": "wa_2026_05_26_marina",
  "correlation_id": "order_corr_20260526_2110",
  "failed_at": "2026-05-26T21:10:31-03:00",
  "agent_id": "fulfillment-agent-01",
  "error_code": "inventory_unavailable",
  "error_message": "SKU whey_iso_choc_900g sem estoque reservado no centro SP",
  "retryable": true,
  "input_refs": ["order_draft.json", "evaluation.json"],
  "output_refs": []
}
```

### Boas práticas para state machines pequenas

1. Defina transições permitidas antes de implementar workers.

2. Não pule de `pending` para `completed` sem registrar início quando a etapa executa trabalho real.

3. Não volte de `completed` para `in_progress`.

4. Para reprocessar, crie nova tentativa com `attempt` incrementado.

5. Inclua `retryable` em falhas.

6. Registre `error_code` estável para automação.

7. Guarde `error_message` legível para humanos.

8. Inclua referências dos arquivos usados como input.

9. Inclua referências dos arquivos produzidos como output.

10. Não esconda falha mudando status para `completed` com output parcial.

---

## 📡 JSON Protocol Entre Agentes

O JSON protocol é o contrato que impede arquivos de virarem texto solto.

Cada agente precisa saber exatamente o que esperar.

Isso inclui versão de schema, timestamps, identificadores de agente, correlation ID e referências de auditoria.

Sem contrato, o file system vira uma gaveta bagunçada.

Com contrato, ele vira um bus legível.

Request payload pede trabalho.

Response payload entrega resultado.

Error payload explica falha.

```json
{
  "schema_version": "1.0",
  "message_type": "agent_request",
  "request_id": "req_20260526_211005_order",
  "correlation_id": "order_corr_20260526_2110",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "created_at": "2026-05-26T21:10:05-03:00",
  "created_by": "orchestrator",
  "target_agent_id": "order-agent",
  "priority": "normal",
  "input_refs": ["conversation_event.json", "discovery.json", "customer_profile.json"],
  "task": {
    "name": "create_order_draft",
    "instructions": "Criar rascunho de pedido sem finalizar pagamento",
    "success_criteria": [
      "produto respeita intolerancia a lactose",
      "total fica abaixo de 220 BRL",
      "entrega em Pinheiros e viavel"
    ]
  }
}
```

```json
{
  "schema_version": "1.0",
  "message_type": "agent_response",
  "response_id": "res_20260526_211017_order",
  "request_id": "req_20260526_211005_order",
  "correlation_id": "order_corr_20260526_2110",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "created_at": "2026-05-26T21:10:17-03:00",
  "agent_id": "order-agent-02",
  "status": "completed",
  "output_refs": ["order_draft.json"],
  "summary": "Rascunho criado com whey isolado chocolate dentro do orçamento",
  "evidence_refs": ["catalog_snapshot.json", "customer_profile.json"]
}
```

```json
{
  "schema_version": "1.0",
  "message_type": "agent_error",
  "error_id": "err_20260526_211031_inventory",
  "request_id": "req_20260526_211018_fulfillment",
  "correlation_id": "order_corr_20260526_2110",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "created_at": "2026-05-26T21:10:31-03:00",
  "agent_id": "fulfillment-agent-01",
  "error_code": "inventory_unavailable",
  "error_message": "Estoque local indisponivel para SKU whey_iso_choc_900g",
  "retryable": true,
  "safe_customer_message": "Vou confirmar uma alternativa segura antes de fechar seu pedido.",
  "input_refs": ["order_draft.json", "evaluation.json"]
}
```

| Campo | Por que existe |
| --- | --- |
| **`schema_version`** | Permite evoluir formato sem quebrar leitores |
| **`message_type`** | Diferencia request, response, error e evento |
| **`correlation_id`** | Conecta todos os arquivos da mesma jornada |
| **`conversation_id`** | Liga o arquivo à conversa do WhatsApp |
| **`turn_id`** | Localiza a etapa dentro da conversa |
| **`created_at`** | Ordena eventos e ajuda a detectar stale state |
| **`agent_id`** | Mostra quem produziu o arquivo |
| **`input_refs`** | Lista arquivos usados como fonte |
| **`output_refs`** | Lista arquivos produzidos |
| **`audit_refs`** | Ajuda humanos e Evaluator a reconstruir decisão |

### Exemplo de plan.json

```json
{
  "schema_version": "1.0",
  "artifact_type": "plan",
  "plan_id": "plan_20260526_2110",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "correlation_id": "order_corr_20260526_2110",
  "created_at": "2026-05-26T21:10:06-03:00",
  "agent_id": "discovery-agent-01",
  "customer_intent": "fechar pedido de whey isolado chocolate",
  "constraints": ["intolerancia a lactose", "orcamento maximo de 220 BRL", "preferencia por chocolate", "entrega em Pinheiros amanha"],
  "success_criteria": ["nenhum produto com lactose", "total menor ou igual a 220 BRL", "produto existe em catalog_snapshot.json", "mensagem final pede confirmacao antes de pagamento"]
}
```

### Exemplo de generation.json

```json
{
  "schema_version": "1.0",
  "artifact_type": "generation",
  "generation_id": "gen_20260526_211014",
  "plan_id": "plan_20260526_2110",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "correlation_id": "order_corr_20260526_2110",
  "created_at": "2026-05-26T21:10:14-03:00",
  "agent_id": "order-agent-02",
  "draft_response": "Marina, confirmei o Whey Isolado Chocolate por R$ 199,90, sem lactose, com entrega estimada para amanha em Pinheiros. Posso gerar o link de pagamento?",
  "order_draft_ref": "order_draft.json",
  "evidence": [{"source_ref": "catalog_snapshot.json", "claim": "SKU whey_iso_choc_900g marcado como sem lactose"}],
  "assumptions": ["endereco completo sera confirmado antes da entrega final", "pagamento ainda nao foi criado"]
}
```

### Exemplo de evaluation.json

```json
{
  "schema_version": "1.0",
  "artifact_type": "evaluation",
  "evaluation_id": "eval_20260526_211019",
  "plan_id": "plan_20260526_2110",
  "generation_id": "gen_20260526_211014",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "correlation_id": "order_corr_20260526_2110",
  "created_at": "2026-05-26T21:10:19-03:00",
  "agent_id": "evaluator-agent-01",
  "decision": "approved",
  "checks": [{"name": "lactose_constraint", "status": "pass"}, {"name": "budget_constraint", "status": "pass"}],
  "customer_visible_response": "Marina, confirmei o Whey Isolado Chocolate por R$ 199,90, sem lactose, com entrega estimada para amanha em Pinheiros. Posso gerar o link de pagamento?",
  "audit_refs": ["plan.json", "generation.json", "order_draft.json"]
}
```

### Validação prática do protocolo

1. Um arquivo sem `schema_version` deve reprovar validação.

2. Um arquivo sem `created_at` deve reprovar validação.

3. Um arquivo sem `agent_id` em response deve reprovar validação.

4. Um `evaluation.json` sem `decision` deve reprovar validação.

5. Um `delivery.json` sem `audit_refs` deve reprovar validação.

6. Um arquivo com JSON inválido deve manter a etapa em `failed`.

7. Um arquivo temporário nunca deve ser lido como artefato final.

8. Um campo desconhecido pode ser ignorado se o schema permitir extensão.

---

## 🔄 Pipeline de Arquivos: Diagrama Completo

Agora junte as peças.

O pipeline completo começa com uma mensagem da cliente.

Ele termina com uma entrega aprovada.

No meio, cada agente toca arquivos específicos.

Observe como o fluxo evita chamada direta entre agentes.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         KODA FILE-BASED PIPELINE                             │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│ WhatsApp Message │
│ Marina           │
└────────┬─────────┘
         │ escreve
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ state/conversations/wa_2026_05_26_marina/                                   │
│                                                                              │
│  ┌──────────────────────────┐                                                │
│  │ conversation_event.json  │                                                │
│  └────────────┬─────────────┘                                                │
│               │ lido por Discovery Agent                                     │
│               ▼                                                              │
│  ┌──────────────────────────┐      ┌──────────────────────────┐              │
│  │ discovery.status.json    │◀────▶│ discovery.lock.json      │              │
│  └────────────┬─────────────┘      └──────────────────────────┘              │
│               │ completed                                                    │
│               ▼                                                              │
│  ┌──────────────────────────┐                                                │
│  │ discovery.json           │                                                │
│  └────────────┬─────────────┘                                                │
│               │ lido por Planner                                             │
│               ▼                                                              │
│  ┌──────────────────────────┐      ┌──────────────────────────┐              │
│  │ plan.status.json         │◀────▶│ plan.lock.json           │              │
│  └────────────┬─────────────┘      └──────────────────────────┘              │
│               │ completed                                                    │
│               ▼                                                              │
│  ┌──────────────────────────┐                                                │
│  │ plan.json                │                                                │
│  └────────────┬─────────────┘                                                │
│               │ lido por Order Agent                                         │
│               ▼                                                              │
│  ┌──────────────────────────┐      ┌──────────────────────────┐              │
│  │ order.status.json        │◀────▶│ order.lock.json          │              │
│  └────────────┬─────────────┘      └──────────────────────────┘              │
│               │ completed                                                    │
│               ▼                                                              │
│  ┌──────────────────────────┐                                                │
│  │ order_draft.json         │                                                │
│  └────────────┬─────────────┘                                                │
│               │ lido por Generator                                           │
│               ▼                                                              │
│  ┌──────────────────────────┐                                                │
│  │ generation.json          │                                                │
│  └────────────┬─────────────┘                                                │
│               │ lido por Evaluator                                           │
│               ▼                                                              │
│  ┌──────────────────────────┐      ┌──────────────────────────┐              │
│  │ evaluation.status.json   │◀────▶│ evaluation.lock.json     │              │
│  └────────────┬─────────────┘      └──────────────────────────┘              │
│               │ completed (status)                                            │
│               │ decision dentro de evaluation.json                             │
│               ▼                                                              │
│  ┌──────────────────────────┐                                                │
│  │ evaluation.json          │                                                │
│  └────────────┬─────────────┘                                                │
│               │ lido por Fulfillment Agent                                   │
│               ▼                                                              │
│  ┌──────────────────────────┐      ┌──────────────────────────┐              │
│  │ fulfillment.status.json  │◀────▶│ inventory.lock.json      │              │
│  └────────────┬─────────────┘      └──────────────────────────┘              │
│               │ completed                                                    │
│               ▼                                                              │
│  ┌──────────────────────────┐                                                │
│  │ delivery.json            │                                                │
│  └────────────┬─────────────┘                                                │
│               │ enviado para WhatsApp                                        │
│               ▼                                                              │
│  ┌──────────────────────────┐                                                │
│  │ delivery_receipt.json    │                                                │
│  └──────────────────────────┘                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Ordem de transição

1. Mensagem recebida vira `conversation_event.json`.

2. Discovery Agent cria `discovery.json`.

3. Planner cria `plan.json`.

4. Order Agent cria `order_draft.json`.

5. Generator cria `generation.json` com resposta candidata.

6. Evaluator cria `evaluation.json`.

7. Fulfillment Agent cria reserva e `delivery.json`.

8. Delivery worker envia mensagem aprovada.

9. Receipt worker cria `delivery_receipt.json`.

10. Supervisor arquiva a pasta quando todos os status estão `completed`.

---

## 📋 Tabela de Tipos de Arquivo e Propositos

| Tipo de Arquivo | Proposito | Escrito Por | Lido Por | Formato | Persistencia |
| --- | --- | --- | --- | --- | --- |
| **`conversation_event.json`** | Registrar mensagem recebida e metadados | WhatsApp adapter | Discovery Agent, Planner | JSON event | Curta a média |
| **`customer_profile.json`** | Guardar preferências, restrições e histórico resumido | Discovery Agent | Order Agent, Evaluator | JSON state | Longa |
| **`plan.json`** | Definir etapas, constraints e critérios | Planner | Generator, Order Agent, Evaluator | JSON contract | Média |
| **`generation.json`** | Guardar resposta candidata e evidências | Generator | Evaluator | JSON artifact | Média |
| **`evaluation.json`** | Aprovar ou rejeitar output com checks | Evaluator | Fulfillment Agent, Delivery worker | JSON decision | Longa |
| **`lock.json`** | Proteger seção crítica contra escrita concorrente | Agente dono temporário | Workers concorrentes, supervisor | JSON control | Curta |
| **`status.json`** | Expor state machine da etapa | Agente dono, supervisor | Orchestrator, dashboards, workers | JSON control | Média |
| **`order_draft.json`** | Representar pedido antes de pagamento | Order Agent | Evaluator, Fulfillment Agent | JSON business object | Média |
| **`delivery.json`** | Guardar mensagem aprovada para cliente | Fulfillment Agent | WhatsApp adapter, audit tools | JSON delivery | Longa |
| **`delivery_receipt.json`** | Registrar envio e confirmação técnica | WhatsApp adapter | Supervisor, support tools | JSON receipt | Longa |
| **`inventory_snapshot.json`** | Congelar visão de estoque usada na decisão | Catalog adapter | Order Agent, Evaluator | JSON snapshot | Média |
| **`error.json`** | Explicar falha estruturada e ação segura | Qualquer agente | Supervisor, retry worker | JSON error | Média |

A primeira coluna é contrato.

Se você muda o nome, muda a integração.

A coluna Persistencia ajuda a decidir retenção.

Decisões que afetam cliente precisam ficar auditáveis.

---

## ⚖️ Tabela Comparativa de Estrategias de Coordenacao

| Estrategia | Latencia | Confiabilidade | Complexidade | Quando Usar |
| --- | --- | --- | --- | --- |
| **File-based coordination** | Baixa a média | Alta com atomic write, locks e schema | Baixa a média | Currículo, protótipos sérios, audit trail, workflows longos |
| **Message queues Redis/RabbitMQ** | Baixa | Média a alta com ack, retry e dead letter queue | Média a alta | Alto volume, múltiplos workers e backpressure |
| **API-based REST/gRPC** | Média no REST, baixa no gRPC | Alta com idempotência e contratos fortes | Média a alta | Serviços separados, fronteiras entre times e deploy independente |
| **In-memory coordination** | Muito baixa | Baixa fora de processo único | Baixa no começo, alta quando cresce | Scripts locais, demos e tarefas curtas sem retomada |

File-based é excelente quando você quer clareza antes de escala.

Message queues resolvem throughput melhor.

APIs resolvem fronteiras de serviço melhor.

In-memory resolve simplicidade temporária melhor.

Para KODA, contratos vêm antes de infraestrutura sofisticada.

### Sinais de evolução

1. Migre para queue quando workers estão bloqueados esperando arquivos demais.

2. Migre para queue quando throughput importa mais do que leitura manual de traces.

3. Migre para API quando agentes viram serviços com deploy próprio.

4. Mantenha file-based quando auditabilidade é mais valiosa que latência mínima.

5. Mantenha file-based em ambientes de aprendizado e design de contrato.

6. Evite in-memory quando você precisa retomar depois de crash.

---

## 🎓 Aplicacao KODA: Pipeline de Pedidos

Vamos aplicar tudo ao pipeline de pedidos do KODA.

O objetivo é coordenar Discovery Agent, Order Agent e Fulfillment Agent sem criar dependência direta entre eles.

Marina continua conversando com um único KODA.

Por trás, cada agente tem responsabilidade clara.

O Discovery Agent entende intenção e contexto.

O Order Agent transforma intenção em pedido válido.

O Fulfillment Agent confirma estoque, entrega e preparação para pagamento.

O Evaluator aparece como gate entre geração e entrega.

```
Antes:
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ Discovery Agent  │      │ Order Agent      │      │ Fulfillment Agent│
│ atualiza memória │      │ cria pedido      │      │ reserva estoque  │
└────────┬─────────┘      └────────┬─────────┘      └────────┬─────────┘
         └──────────────┬──────────┴──────────────┬──────────┘
                        ▼                         ▼
              estado inconsistente        resposta arriscada

Depois:
┌──────────────────────────┐
│ conversation_event.json  │
└───────┬──────────────────┘
        ▼
┌──────────────────┐
│ Discovery Agent  │
└───────┬──────────┘
        ▼
┌──────────────────────────┐
│ discovery.json           │
└───────┬──────────────────┘
        ▼
┌──────────────────┐
│ Order Agent      │
└───────┬──────────┘
        ▼
┌──────────────────────────┐
│ order_draft.json         │
└───────┬──────────────────┘
        ▼
┌──────────────────┐
│ Evaluator Agent  │
└───────┬──────────┘
        ▼
┌──────────────────────────┐
│ evaluation.json          │
└───────┬──────────────────┘
        ▼
┌──────────────────┐
│ Fulfillment Agent│
└───────┬──────────┘
        ▼
┌──────────────────────────┐
│ delivery.json            │
└──────────────────────────┘
```

| Aspecto | Antes | Depois |
| --- | --- | --- |
| **Fonte da verdade** | Memória interna e logs | Arquivos JSON por etapa |
| **Concorrência** | Agentes escrevem quando conseguem | Lock files controlam seção crítica |
| **Progresso** | Difícil de ver sem logs | Status files mostram state machine |
| **Falha** | Pode ficar invisível | Error payload e status `failed` ficam explícitos |
| **Retomada** | Depende de reprocessar tudo | Worker retoma do último arquivo completo |
| **Auditoria** | Reconstrução manual | Audit refs ligam decisão aos inputs |

```bash
state/conversations/wa_2026_05_26_marina/
├── conversation_event.json
├── customer_profile.json
├── discovery.json
├── discovery.status.json
├── plan.json
├── order.lock.json
├── order.status.json
├── order_draft.json
├── generation.json
├── evaluation.status.json
├── evaluation.json
├── fulfillment.status.json
├── delivery.json
└── delivery_receipt.json
```

### Exemplo KODA, conversation_event.json

```json
{
  "schema_version": "1.0",
  "artifact_type": "conversation_event",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "correlation_id": "order_corr_20260526_2110",
  "channel": "whatsapp",
  "received_at": "2026-05-26T21:10:02-03:00",
  "customer": {"customer_id": "cust_marina_4821", "display_name": "Marina"},
  "message": "Quero fechar aquele whey isolado chocolate. Ainda tenho intolerancia a lactose e meu limite continua R$ 220.",
  "known_context_refs": ["customer_profile.json", "previous_conversation_summary.json"]
}
```

### Exemplo KODA, discovery.json

```json
{
  "schema_version": "1.0",
  "artifact_type": "discovery",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "correlation_id": "order_corr_20260526_2110",
  "created_at": "2026-05-26T21:10:07-03:00",
  "agent_id": "discovery-agent-01",
  "intent": "purchase_confirmation",
  "customer_constraints": {"dietary_restrictions": ["intolerancia_lactose"], "max_budget_brl": 220, "preferred_flavor": "chocolate", "delivery_region": "Pinheiros, Sao Paulo"},
  "risk_notes": ["nao recomendar whey concentrado", "nao finalizar pagamento sem confirmacao explicita"]
}
```

### Exemplo KODA, order_draft.json

```json
{
  "schema_version": "1.0",
  "artifact_type": "order_draft",
  "order_draft_id": "draft_20260526_211016",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "correlation_id": "order_corr_20260526_2110",
  "created_at": "2026-05-26T21:10:16-03:00",
  "agent_id": "order-agent-02",
  "items": [{"sku": "whey_iso_choc_900g", "name": "Whey Isolado Chocolate 900g", "quantity": 1, "unit_price_brl": 199.90, "dietary_flags": ["sem_lactose"]}],
  "totals": {"items_brl": 199.90, "shipping_estimate_brl": 0, "grand_total_brl": 199.90},
  "not_finalized": true,
  "requires_customer_confirmation": true,
  "input_refs": ["conversation_event.json", "discovery.json", "customer_profile.json"]
}
```

### Exemplo KODA, delivery.json

```json
{
  "schema_version": "1.0",
  "artifact_type": "delivery",
  "conversation_id": "wa_2026_05_26_marina",
  "turn_id": "turn_041",
  "correlation_id": "order_corr_20260526_2110",
  "created_at": "2026-05-26T21:10:24-03:00",
  "agent_id": "fulfillment-agent-01",
  "channel": "whatsapp",
  "recipient": "cust_marina_4821",
  "message": "Marina, confirmei o Whey Isolado Chocolate por R$ 199,90, sem lactose, com entrega estimada para amanha em Pinheiros. Posso gerar o link de pagamento?",
  "send_after": "evaluation.approved",
  "audit_refs": ["conversation_event.json", "discovery.json", "order_draft.json", "evaluation.json"]
}
```

| Agente | Coordenação por arquivos |
| --- | --- |
| **Discovery Agent** | Lê `conversation_event.json`, escreve `discovery.json`, atualiza `discovery.status.json` |
| **Order Agent** | Espera discovery `completed`, adquire `order.lock.json`, escreve `order_draft.json` |
| **Evaluator Agent** | Lê plano, geração e pedido, escreve `evaluation.json` com decisão |
| **Fulfillment Agent** | Só segue se avaliação for `approved`, reserva estoque e escreve `delivery.json` |
| **WhatsApp adapter** | Lê `delivery.json`, envia mensagem e escreve `delivery_receipt.json` |

Nenhum agente precisa confiar em timing acidental.

Nenhum agente finaliza pedido apenas porque uma mensagem parece clara.

Cada etapa tem arquivos de entrada e saída.

Cada etapa pode ser revisada depois.

---

## ⚠️ Quando NAO Usar File-Based Coordination

File-based coordination é útil, mas não é remédio universal.

Você deve reconhecer quando o padrão adiciona peso demais.

Arquivos trazem auditabilidade, mas também trazem disciplina operacional.

Se a tarefa é pequena, essa disciplina pode ser excesso.

| Cenário | Por que evitar |
| --- | --- |
| **Uma função síncrona simples resolve** | Se uma única função recebe input e devolve output rápido, não crie pipeline de arquivos |
| **Não existe retomada relevante** | Se perder o processo não importa, persistence pode não valer o custo |
| **O volume exige latência muito baixa** | Se cada milissegundo importa, fila ou chamada direta pode ser melhor |
| **O time não consegue operar arquivos com disciplina** | Sem naming, schema e limpeza, o workspace vira bagunça |
| **O dado é sensível demais para disco comum** | Se o risco é alto, você precisa de controles extras ou outro storage |
| **O fluxo é totalmente interno a um serviço** | Se não há agentes independentes, um módulo interno pode bastar |
| **A coordenação exige fanout massivo** | Muitos consumidores simultâneos podem ser mais fáceis em queue |
| **A fronteira entre times já é API** | Quando contratos organizacionais já são REST ou gRPC, arquivos podem atrapalhar |

### Sinais de overengineering

1. Você cria arquivos que ninguém abre.

2. Cada arquivo exige explicação oral para ser entendido.

3. O time passa mais tempo limpando artefatos do que entendendo o fluxo.

4. O lock fica stale toda hora.

5. O pipeline tem mais etapas do que decisões reais.

6. O mesmo agente escreve e lê todos os arquivos sem concorrência.

7. O cliente não ganha confiabilidade, suporte ou retomada.

8. A latência extra não compra auditabilidade útil.

---

### Laboratório guiado: lendo uma pasta de pedido

1. Abra a pasta da conversa antes de olhar logs.

2. Confirme se existe `conversation_event.json`.

3. Leia `correlation_id` e use esse valor em toda investigação.

4. Confira se `discovery.status.json` terminou em `completed`.

5. Abra `discovery.json` e procure restrições críticas.

6. Procure `order.lock.json` apenas se a etapa ainda estiver em andamento.

7. Se o lock existir depois do tempo esperado, avalie stale lock.

8. Abra `order.status.json` e veja qual agente assumiu a etapa.

9. Leia `order_draft.json` e compare itens com restrições do cliente.

10. Abra `generation.json` e identifique a mensagem candidata.

11. Leia `evaluation.json` e confirme se a decisão foi `approved`.

12. Veja `delivery.json` apenas depois da aprovação.

13. Confirme que `delivery.json` possui `audit_refs` completos.

14. Procure `delivery_receipt.json` para saber se a mensagem saiu pelo canal.

15. Se algo falhou, leia `error_code` antes de ler stack trace.

16. Se faltou arquivo, volte um passo na state machine.

17. Se dois arquivos discordam, confie no mais próximo da fonte de verdade.

18. Se a fonte de verdade está errada, registre o bug no agente que escreveu aquele arquivo.

19. Se o output está correto mas a mensagem está ruim, revise Generator e rubrica.

20. Se a mensagem foi enviada sem aprovação, revise o gate do Delivery worker.

### Padrões de nomes recomendados

| Nome | Uso |
| --- | --- |
| **`conversation_event.json`** | Evento principal do turno atual |
| **`conversation_event.turn_041.json`** | Evento versionado por turno |
| **`order.lock.json`** | Lock de recurso de pedido |
| **`order.status.json`** | Status da etapa de pedido |
| **`order_draft.attempt_01.json`** | Tentativa específica de pedido |
| **`evaluation.attempt_01.json`** | Avaliação ligada à tentativa |
| **`delivery.approved.json`** | Entrega aprovada para canal |
| **`delivery_receipt.whatsapp.json`** | Recibo de envio por canal específico |

### Revisão de segurança para arquivos do KODA

1. Não grave token de API em JSON de coordenação.

2. Não grave número completo de cartão ou dado de pagamento sensível.

3. Não grave credenciais do WhatsApp adapter.

4. Reduza dados pessoais ao mínimo necessário para a etapa.

5. Use customer ID quando nome completo não for necessário.

6. Controle permissões da pasta de estado.

7. Defina retenção para artefatos antigos.

8. Separe ambiente de desenvolvimento, staging e produção.

9. Inclua logs de acesso quando arquivos forem usados para auditoria sensível.

10. Não copie traces reais para exemplos de currículo sem anonimização.

11. Revise `delivery.json` porque ele contém texto enviado ao cliente.

12. Revise `error.json` para não vazar stack trace ao cliente.

### Checklist operacional para Fernando

1. Existe uma pasta por conversa crítica.

2. Existe `correlation_id` comum em todos os artefatos do fluxo.

3. Todo arquivo final é escrito com atomic write.

4. Todo recurso compartilhado tem lock ou alternativa transacional.

5. Todo lock tem `owner_id` e `created_at`.

6. Todo status tem estado de state machine.

7. Toda falha tem `error_code` estável.

8. Toda entrega ao cliente tem `audit_refs`.

9. Todo Evaluator registra checks individuais.

10. Todo worker ignora arquivos temporários.

11. Todo retry é idempotente ou bloqueado por chave única.

12. Todo arquivo sensível tem retenção definida.

13. Todo schema tem exemplo válido em teste.

14. Todo novo agente declara arquivos que lê e escreve.

15. Todo reviewer consegue reproduzir a jornada a partir da pasta.

| Anti-padrão | Risco |
| --- | --- |
| **Arquivo final escrito direto** | Outro agente pode ler conteúdo parcial |
| **Lock sem TTL** | Um crash pode bloquear o pipeline indefinidamente |
| **Status sem `agent_id`** | Ninguém sabe quem assumiu a etapa |
| **JSON sem `schema_version`** | Evolução de contrato fica perigosa |
| **Delivery sem `audit_refs`** | Suporte não consegue provar por que a mensagem foi enviada |
| **Dois writers para o mesmo arquivo** | A última escrita vence e apaga evidência |
| **Retry sem idempotência** | Pedido pode ser duplicado |
| **Pasta sem política de retenção** | Dados antigos acumulam risco e custo |
| **Erro apenas em log** | Supervisor e agentes não conseguem reagir pelo file system |
| **Nome de arquivo dinâmico demais** | Leitores não descobrem artefatos sem conhecimento oculto |

### Perguntas de design antes de criar um novo arquivo

1. Qual agente escreve este arquivo?

2. Qual agente lê este arquivo?

3. Este arquivo é dado de negócio, controle ou auditoria?

4. Ele precisa de `schema_version`?

5. Ele precisa de `correlation_id`?

6. Ele pode conter dados sensíveis?

7. Ele precisa sobreviver depois do pedido?

8. Ele pode ser reescrito ou deve ser imutável?

9. Ele precisa de lock para ser criado?

10. Ele será lido por humanos durante suporte?

11. Ele será usado em testes de regressão?

12. Ele tem relação clara com um status file?

13. Ele precisa de attempt number?

14. Ele participa de retry?

15. Ele pode ser arquivado com segurança?

```bash
state/
└── conversations/
    └── wa_2026_05_26_marina/
        ├── inputs/
        │   ├── conversation_event.json
        │   └── customer_profile.json
        ├── work/
        │   ├── discovery.json
        │   ├── plan.json
        │   ├── order_draft.json
        │   ├── generation.json
        │   └── evaluation.json
        ├── control/
        │   ├── discovery.status.json
        │   ├── order.status.json
        │   ├── evaluation.status.json
        │   └── fulfillment.status.json
        ├── locks/
        │   ├── order.lock.json
        │   └── inventory.lock.json
        └── outputs/
            ├── delivery.json
            └── delivery_receipt.json
```

Essa convenção separa intenção operacional.

`inputs` guarda o que veio de fora.

`work` guarda artefatos intermediários.

`control` guarda state machines.

`locks` guarda exclusividade temporária.

`outputs` guarda o que saiu para o cliente ou canal.

Você não precisa usar essa estrutura exata.

Mas precisa escolher uma estrutura e segui-la.

| Cenário | Como investigar |
| --- | --- |
| **Pedido duplicado** | Procure dois `delivery_receipt.json` com o mesmo `correlation_id` e verifique lock |
| **Produto errado** | Compare `order_draft.json` com `customer_profile.json` e veja constraint |
| **Resposta sem evidência** | Abra `generation.json` e confirme se há `evidence` suficiente |
| **Falha sem retry** | Leia `error.json` e veja se `retryable` foi definido |
| **Pipeline parado** | Procure status `in_progress` antigo e lock stale relacionado |
| **Arquivo parcial** | Verifique se existe escrita direta no arquivo final |
| **Schema quebrado** | Compare `schema_version` com leitores ativos |
| **Cliente recebeu mensagem antiga** | Confirme se `delivery.json` aponta para avaliação recente |
| **Estoque reservado cedo** | Veja se Fulfillment rodou antes de `evaluation.approved` |
| **Orçamento ignorado** | Procure constraint no `plan.json` e check no `evaluation.json` |

### Quando o Discovery Agent falha

O `discovery.json` pode não capturar uma restrição explícita.

O Planner passa a trabalhar com uma verdade incompleta.

O Evaluator pode salvar o fluxo se verificar a mensagem original.

Por isso `conversation_event.json` deve permanecer como input auditável.

A correção deve melhorar extração de intenção, não mascarar no Fulfillment.

### Quando o Order Agent falha

O `order_draft.json` pode escolher SKU errado.

O lock pode estar correto e mesmo assim o conteúdo pode ser ruim.

Coordenação não substitui rubrica.

O Evaluator deve rejeitar com feedback específico.

O retry deve criar nova tentativa, não editar silenciosamente a tentativa antiga.

### Quando o Fulfillment Agent falha

O produto pode estar correto, mas o estoque pode ter mudado.

O agente deve registrar falha estruturada.

A mensagem ao cliente precisa ser segura e honesta.

Nunca envie confirmação de entrega sem evidência de reserva.

Se a falha for retryable, o supervisor pode tentar de novo com backoff.

### Quando o Delivery worker falha

O `delivery.json` pode estar aprovado, mas o canal pode estar fora.

O sistema deve criar `delivery_receipt.json` apenas quando o canal aceitar envio.

Falha de canal não deve apagar a decisão aprovada.

Retry de envio precisa ser idempotente.

O suporte deve conseguir ver se a mensagem foi preparada ou enviada.

## 🎯 Key Takeaways

1. File-based coordination transforma o file system em communication bus auditável entre agentes.

2. Lock files previnem race condition quando dois agentes podem tocar no mesmo estado.

3. Atomic write impede que leitores vejam arquivos parciais.

4. Status files tornam progresso e falha visíveis por meio de uma state machine simples.

5. JSON protocol dá contrato claro para request, response e error payloads.

6. No KODA, Discovery Agent, Order Agent e Fulfillment Agent ficam mais confiáveis quando trocam arquivos.

7. O padrão é melhor quando auditabilidade, retomada e aprendizado de contrato valem mais que latência mínima.

---

## 🚀 Checkpoint: O Que Voce Aprendeu

- [ ] Consigo explicar por que file-based coordination usa arquivos como communication bus entre agentes.

- [ ] Consigo diferenciar arquivo de dado, arquivo de controle e arquivo de auditoria.

- [ ] Consigo explicar por que lock files previnem race conditions entre agentes.

- [ ] Consigo desenhar o ciclo de vida de um lock file.

- [ ] Consigo escrever um `status.json` com estados `pending`, `in_progress`, `completed` e `failed`.

- [ ] Consigo explicar por que atomic write evita leitura de arquivo parcial.

- [ ] Consigo definir um JSON protocol com `schema_version`, timestamps e agent IDs.

- [ ] Consigo criar exemplos de request, response e error payloads.

- [ ] Consigo mostrar como `plan.json`, `generation.json` e `evaluation.json` fluem pelo file system.

- [ ] Consigo desenhar o pipeline de pedidos do KODA usando arquivos.

- [ ] Consigo identificar quando file-based coordination é overkill.

- [ ] Consigo comparar file-based, message queues, API-based e in-memory coordination.

- [ ] Consigo revisar um trace e descobrir qual agente escreveu cada artefato.

- [ ] Consigo propor retry strategy para lock contention sem duplicar pedido.

- [ ] Consigo explicar para Fernando por que Marina recebeu a resposta correta no fluxo coordenado.

---

## 📚 Referencias & Proximas Leituras

- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` para revisar Planner, Generator, Evaluator e canais de comunicação.

- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` para aprofundar persistência de estado em jornadas longas.

- `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md` para entender como resumir contexto sem perder rastreabilidade.

- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` para evoluir o harness sem criar acoplamento invisível.

- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` para revisar separação entre criação e avaliação.

- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` para praticar leitura de artefatos e logs.

- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md` para aplicar o padrão em jornadas reais do KODA.

- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` para conectar `evaluation.json` a rubricas específicas.

- Documentação de POSIX file locking para entender limites de locks em file systems locais.

- Documentação de Redis Streams e RabbitMQ para comparar quando o fluxo pedir filas.

---

## 💭 Reflexao Final

Volte para Marina por um instante.

Ela não pediu uma arquitetura distribuída.

Ela pediu um whey isolado chocolate, sem lactose, dentro do orçamento, com entrega rápida.

Esse é o ponto.

Clientes não sentem `lock file` diretamente.

Eles sentem quando o pedido não duplica.

Eles sentem quando a restrição alimentar é respeitada.

Eles sentem quando o KODA lembra o que foi dito antes.

Eles sentem quando a promessa enviada no WhatsApp corresponde ao estoque real.

File-based coordination é uma técnica humilde.

Ela não tenta impressionar com infraestrutura complexa.

Ela coloca fatos em arquivos.

Coloca ownership em campos explícitos.

Coloca progresso em state machines pequenas.

Coloca exclusividade em locks curtos.

Coloca decisão em JSON auditável.

Para Fernando, isso muda a conversa com o time.

Em vez de perguntar qual agente estava certo, ele pergunta qual arquivo prova a decisão.

Em vez de debugar lembranças internas, ele lê artefatos.

Em vez de torcer para a ordem de execução dar certo, ele define transições.

Essa é a maturidade que o Nível 3 quer construir.

Não é complexidade pela complexidade.

É confiança operacional a serviço de uma experiência humana.

Quando Marina recebe a resposta correta, a arquitetura desaparece.

E esse é o melhor elogio que ela poderia receber.

---

## 📋 Metadata

| Campo | Valor |
| --- | --- |
| Arquivo | `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` |
| Nível | 3 - Arquitetura Avançada |
| Tempo | 90 minutos |
| Status | Completo |
| Próximo | `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md` |
| Atualizado | Maio 2026 |
