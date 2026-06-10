---
title: "Template de Evaluation Rubric para Agentes Confiáveis"
type: curriculum-guide
aliases: ["template rubrica", "rubric template", "modelo avaliacao", "guia implementacao"]
tags: [curriculo-conteudo, guia-implementacao, rubric, scoring, avaliacao, criterios-de-qualidade, calibracao, versionamento, feedback-estruturado, criterios-de-bloqueio]
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics Concept]]"]
last_updated: 2026-06-10
---
# 🎯 Template de Evaluation Rubric para Agentes Confiáveis
## Guia prático para transformar critérios de qualidade em scoring auditável

**Tempo Estimado:** 150 minutos  
**Nível:** 7 - Implementation Guides  
**Pré-requisito:** `02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` e `02-nivel-2-practical-patterns/03-rubric-design.md`  
**Status:** 🟢 Pronto para uso em implementação  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: A Noite em Que KODA Precisou de um Rubric Template

Era 21h37 em uma quinta-feira de Maio de 2026 quando KODA entrou em modo de campanha. A loja tinha acabado de lançar um desconto relâmpago de creatina, whey protein, multivitamínicos e snacks proteicos. O WhatsApp não parava. A equipe esperava volume alto, mas não esperava o tipo de pressão que aparece quando um agente precisa manter qualidade por centenas de conversas simultâneas.

No começo, tudo parecia bem. O Generator recebia o contexto do cliente, lia preferências, consultava inventory e montava recomendações com explicações claras. O Evaluator lia cada draft output e decidia se podia seguir para o cliente. A arquitetura Generator/Evaluator estava ativa, os logs estavam limpos, e os primeiros dashboards mostravam aprovação acima de 90%.

Então os casos difíceis começaram a chegar. Uma cliente queria whey sem lactose, mas aceitava produtos processados em instalação com leite desde que o risco fosse baixo. Outro cliente queria ganho de massa, mas tinha restrição de cafeína por orientação médica. Um terceiro queria presentear o pai diabético e perguntava se algum snack era seguro. Cada conversa parecia simples por fora. Por dentro, cada uma exigia julgamento fino.

O primeiro sinal de problema veio de um trace. O Evaluator aprovou uma recomendação porque o produto estava em stock, o preço batia com o catálogo e a resposta era educada. O que ele não checou foi a severidade da restrição. A frase do cliente, perdida no início da conversa, dizia: "minha reação a leite é forte". O Generator tinha mencionado um produto com aviso de contaminação cruzada. O Evaluator viu qualidade textual, mas não viu risco.

O segundo sinal veio de outro trace. O Evaluator rejeitou uma recomendação boa porque a explicação tinha apenas duas frases. O cliente era recorrente, conhecia a marca, e tinha pedido uma resposta objetiva. O Generator acertou ao ser curto. O Evaluator aplicou uma preferência de estilo como se fosse critério crítico. A rejeição atrasou a conversa, consumiu token budget e gerou uma segunda tentativa pior.

O terceiro sinal foi o mais incômodo. Dois Evaluators diferentes avaliaram drafts quase idênticos e chegaram a decisões diferentes. Um aprovou com score 8.2. Outro rejeitou por falta de justificativa nutricional. Nenhum estava totalmente errado. O problema era outro: não existia um rubric template comum. Cada pessoa da equipe tinha escrito sua própria ideia de qualidade.

Na sala de incidentes, a equipe voltou ao módulo de `rubric-design.md`. Todos conheciam os sete elementos de um bom rubric: Critério, Dimensão, Escala, Exemplos, Pesos, Lógica de Decisão e Feedback. Todos entendiam o problema de sycophancy. Todos sabiam por que self-evaluation falha. Mesmo assim, faltava uma peça operacional: um template completo que forçasse cada rubric novo a nascer com a mesma estrutura.

Foi aí que a conversa mudou. A pergunta deixou de ser "como explicamos qualidade para o Evaluator?" e virou "como impedimos que cada equipe invente qualidade de um jeito diferente?". A resposta foi criar um template único. Não um texto bonito para documentação. Um artefato copiável, auditável, versionado e pronto para entrar no harness.

Um bom rubric template faz três coisas ao mesmo tempo. Primeiro, obriga o autor a separar dimensões de critérios. Segundo, transforma escalas vagas em score levels observáveis. Terceiro, deixa a decisão final previsível, com approval threshold, blocker criteria, escalation e feedback format.

Na manhã seguinte, KODA já tinha uma versão inicial. A equipe aplicou o template em recomendações de produto, avaliação de texto e code review interno. O impacto apareceu rápido. Discussões subjetivas caíram. O Evaluator ficou mais consistente. O Generator recebeu feedback melhor. O time passou a debugar falhas olhando para campos concretos, não para impressões soltas.

Este guia nasce desse momento. Ele não tenta convencer você de que rubrics importam. Esse argumento já foi feito no Nível 2. Aqui o objetivo é mais direto: entregar um template de rubric que você possa copiar hoje, adaptar ao seu domínio e colocar em produção com segurança.

Se `rubric-design.md` ensinou a pensar, este guia ensina a executar. Você vai sair com uma estrutura pronta, três exemplos preenchidos, checklists de validação, uma tabela comparativa de abordagens e um mapa claro de como KODA se beneficia quando todos os Evaluators avaliam com o mesmo padrão.

---

## 🎯 O Que Você Vai Aprender

- Transformar os sete elementos de um bom rubric em um documento operacional copiável.
- Definir Dimensões com peso, descrição, intenção e risco de interpretação errada.
- Escrever Critérios que um Evaluator consegue aplicar sem adivinhar o que o autor queria dizer.
- Desenhar Escalas com score levels observáveis, exemplos positivos e exemplos negativos.
- Calcular Scores em formato raw, normalized e weighted sem misturar matemática com julgamento subjetivo.
- Criar Lógica de Decisão com approval threshold, blocker criteria, escalation e limites de retry.
- Gerar Feedback Format estruturado para que o Generator consiga corrigir o draft output na próxima tentativa.
- Adaptar o mesmo template para recomendações de produto, avaliação de texto e code review.
- Comparar Binary Validation, Simple Scoring, Full Rubric e Human Review sem romantizar nenhuma opção.
- Aplicar o template ao contexto KODA, incluindo safety, inventory, customer fit, clarity e trace auditability.
- Validar um rubric antes de colocar no harness usando checklist técnico, checklist de negócio e checklist de calibragem.
- Versionar rubrics para que feedback loop melhore o sistema sem quebrar decisões anteriores.

Ao final, você deve ser capaz de abrir este arquivo, copiar o Template Principal, adaptar os campos ao seu domínio e entregar um rubric que outro Evaluator consiga usar com o mesmo resultado que você esperava.

---

## 🔗 Como Este Guia Se Conecta

Este guia depende de dois módulos anteriores e assume que você já entende a diferença entre teoria de avaliação e execução dentro de um harness.

### Conexão com `rubric-design.md`

`rubric-design.md` explica por que um Evaluator sem rubric vira um juiz instável. Ele apresenta a história da Ana, mostra como um rubric vago deixou passar risco de alergia, e organiza a anatomia de qualidade em sete elementos: Critério, Dimensão, Escala, Exemplos, Pesos, Lógica de Decisão e Feedback.

Este guia pega esses sete elementos e transforma em arquivo de trabalho. O foco não é discutir se um critério é importante. O foco é dar forma para que qualquer critério importante tenha campo, escala, peso, exemplo, decisão e feedback.

### Conexão com `generator-evaluator-pattern.md`

`generator-evaluator-pattern.md` ensina que o Generator cria e o Evaluator critica. Essa separação reduz sycophancy porque o mesmo agente não precisa defender a própria resposta. Mas separação sem rubric ainda deixa espaço para julgamento solto.

Este guia serve como contrato operacional entre Generator e Evaluator. O Generator sabe quais dimensões importam. O Evaluator sabe como pontuar. O trace mostra por que a decisão aconteceu. O feedback loop fica objetivo porque cada rejeição aponta para critérios específicos.

### Conexão com implementação real

- Em um sistema simples, o rubric pode ser um arquivo markdown revisado por humanos.
- Em um harness automatizado, o rubric pode virar JSON carregado pelo Evaluator antes da avaliação.
- Em KODA, o rubric pode ser associado a uma feature, como product recommendation, order validation ou customer support reply.
- Em pipelines de qualidade, o rubric pode ser usado para comparar Generator versions sem depender de preferência pessoal.
- Em incident review, o rubric mostra se a falha veio de critério ausente, peso errado, threshold baixo ou avaliação incorreta.

---

## 📊 Posicionamento no Programa

| Camada | Arquivo ou prática | Papel no aprendizado | O que este guia entrega |
|--------|--------------------|----------------------|-------------------------|
| Fundamentos | `01-why-agents-lose-plot.md` | Mostra por que agentes perdem contexto, plano e julgamento | Lembra que rubric é um checkpoint contra falhas silenciosas |
| Padrão prático | `01-generator-evaluator-pattern.md` | Separa criação e avaliação | Dá ao Evaluator uma ferramenta para avaliar com rigor |
| Design de rubric | `03-rubric-design.md` | Ensina conceitos e erros comuns | Converte conceitos em template pronto para uso |
| Implementation Guides | Este arquivo | Transforma teoria em asset operacional | Entrega template, exemplos, checklist, tabela e diagrama |
| KODA específico | Guides e case studies de KODA | Aplica padrões ao e-commerce conversacional | Mostra como o mesmo template protege customer trust |

Este guia fica no Nível 7 porque a pessoa leitora já deve ter maturidade suficiente para aplicar padrões em produção. Aqui não basta entender o conceito. É preciso escrever um artefato que aguente uso real, revisão por pares e auditoria posterior.

---

## 🏗️ Template Principal

Use esta seção como o modelo base para qualquer rubric novo. Copie o bloco de markdown quando a avaliação ainda estiver em discussão. Copie o bloco JSON quando o rubric já estiver pronto para entrar no Evaluator.

### Regras de uso do template

- Cada rubric deve ter um `rubric_id` estável e uma `version` explícita.
- Cada dimensão deve ter peso numérico e soma total igual a 1.0 ou 100%.
- Cada critério deve pertencer a exatamente uma dimensão.
- Cada critério deve ter score levels com comportamento observável.
- Cada blocker criterion deve explicar por que bloqueia aprovação mesmo com score alto.
- Cada approval threshold deve ser testado contra exemplos reais antes de produção.
- Cada feedback format deve ser escrito para o Generator, não para o gerente do projeto.
- Cada rubric deve declarar `target_success_rate` para que o time saiba qual nível de precisão espera.
- Cada mudança de peso ou threshold deve gerar nova versão.
- Cada domínio deve registrar quais dados o Evaluator precisa ler antes de pontuar.

### Template em Markdown

```markdown
# Nome do Rubric

## Metadata

- rubric_id:
- version:
- domain:
- created_by:
- reviewed_by:
- created_at:
- target_success_rate:
- intended_evaluator:
- intended_generator:
- token_budget:
- review_cadence:
- owner_team:
- trace_storage:

## Propósito

- Avaliar se o draft output atende ao objetivo do domínio.
- Separar qualidade textual de segurança, factualidade e aderência ao contexto.
- Produzir score, decisão e feedback acionável para o Generator.

## Inputs Necessários

- input_original:
- contexto_relevante:
- draft_output:
- dados_de_referência:
- restrições_do_sistema:
- histórico_de_feedback:

## Dimensões

| ID | Nome | Peso | Descrição | Risco se falhar |
|----|------|------|-----------|-----------------|
| D1 | | | | |
| D2 | | | | |
| D3 | | | | |
| D4 | | | | |

## Critérios

### C1

- dimensão:
- nome:
- descrição:
- tipo: critical ou standard
- peso dentro da dimensão:
- dados que o Evaluator deve consultar:
- erro comum que este critério evita:

| Score | Significado | Evidência esperada | Exemplo de aprovação | Exemplo de rejeição |
|-------|-------------|--------------------|----------------------|---------------------|
| 0 | Falha total | | | |
| 1 | Fraco | | | |
| 2 | Aceitável com ressalvas | | | |
| 3 | Bom | | | |
| 4 | Excelente | | | |

## Scores

- raw_score: soma dos scores dos critérios antes de normalização.
- normalized_score: raw_score convertido para escala 0 a 100.
- weighted_score: normalized_score ponderado pelos pesos das dimensões.
- confidence_score: confiança do Evaluator na própria avaliação.
- evidence_count: quantidade de evidências concretas usadas.

## Lógica de Decisão

- approval_threshold:
- conditional_approval_threshold:
- blocker_criteria:
- escalation_criteria:
- retry_limit:
- reject_if_missing_evidence:
- approve_if_all_critical_pass:
- decision_labels: APPROVE, REJECT, ESCALATE, NEEDS_REVISION

## Feedback Format

- decision:
- score_summary:
- failed_criteria:
- strongest_points:
- required_changes:
- optional_improvements:
- evidence_used:
- next_generator_instruction:

## Calibration Set

- exemplo_aprovado:
- exemplo_rejeitado:
- exemplo_escalado:
- exemplo_limite:

## Versionamento

- mudança:
- motivo:
- impacto esperado:
- métricas a acompanhar:
```

### Template em JSON

```json
{
  "metadata": {
    "rubric_id": "",
    "version": "",
    "domain": "",
    "created_by": "",
    "reviewed_by": "",
    "created_at": "",
    "target_success_rate": "",
    "intended_evaluator": "",
    "intended_generator": "",
    "token_budget": {
      "max_input_tokens": 0,
      "max_rubric_tokens": 0,
      "max_feedback_tokens": 0
    },
    "review_cadence": "",
    "owner_team": "",
    "trace_storage": ""
  },
  "purpose": {
    "primary_goal": "",
    "quality_risk": "",
    "business_risk": "",
    "customer_risk": ""
  },
  "inputs_required": [
    "input_original",
    "contexto_relevante",
    "draft_output",
    "dados_de_referencia",
    "restricoes_do_sistema",
    "historico_de_feedback"
  ],
  "dimensions": [
    {
      "dimension_id": "D1",
      "name": "",
      "weight": 0,
      "description": "",
      "risk_if_failed": "",
      "criteria_ids": []
    }
  ],
  "criteria": [
    {
      "criterion_id": "C1",
      "dimension_id": "D1",
      "name": "",
      "description": "",
      "type": "standard",
      "weight_within_dimension": 0,
      "required_evidence": [],
      "common_failure_prevented": "",
      "scale": {
        "min": 0,
        "max": 4,
        "levels": [
          { "score": 0, "label": "falha_total", "definition": "", "positive_example": "", "negative_example": "" },
          { "score": 1, "label": "fraco", "definition": "", "positive_example": "", "negative_example": "" },
          { "score": 2, "label": "aceitavel_com_ressalvas", "definition": "", "positive_example": "", "negative_example": "" },
          { "score": 3, "label": "bom", "definition": "", "positive_example": "", "negative_example": "" },
          { "score": 4, "label": "excelente", "definition": "", "positive_example": "", "negative_example": "" }
        ]
      }
    }
  ],
  "scores": {
    "raw_score_formula": "sum(criteria.score)",
    "normalized_score_formula": "raw_score / max_raw_score * 100",
    "weighted_score_formula": "sum(dimension.normalized_score * dimension.weight)",
    "confidence_score_formula": "evidence_quality * evaluator_certainty",
    "rounding_policy": "round_to_one_decimal"
  },
  "decision_logic": {
    "approval_threshold": 0,
    "conditional_approval_threshold": 0,
    "blocker_criteria": [],
    "escalation_criteria": [],
    "retry_limit": 0,
    "reject_if_missing_evidence": true,
    "approve_if_all_critical_pass": false,
    "decision_labels": ["APPROVE", "REJECT", "ESCALATE", "NEEDS_REVISION"]
  },
  "feedback_format": {
    "decision": "",
    "score_summary": {},
    "failed_criteria": [],
    "strongest_points": [],
    "required_changes": [],
    "optional_improvements": [],
    "evidence_used": [],
    "next_generator_instruction": ""
  },
  "calibration_set": {
    "approved_example": {},
    "rejected_example": {},
    "escalated_example": {},
    "borderline_example": {}
  }
}
```

### Como preencher as Dimensões

| Dimensão sugerida | Quando usar | Peso típico | Observação prática |
|-------------------|------------|-------------|--------------------|
| D1 Factualidade | Confirma se a resposta respeita dados verificáveis, como preço, stock, regra de negócio e fonte consultada. | 10% a 35% | Ajuste o peso conforme o custo de erro no domínio. |
| D2 Aderência ao Contexto | Confirma se a resposta usa as restrições, preferências e histórico do cliente sem inventar necessidades. | 10% a 35% | Ajuste o peso conforme o custo de erro no domínio. |
| D3 Segurança | Confirma se riscos de saúde, privacidade, pagamento, compliance ou produção foram tratados como critérios críticos. | 10% a 35% | Ajuste o peso conforme o custo de erro no domínio. |
| D4 Clareza | Confirma se o output é fácil de entender, direto, completo e no tom adequado para o canal. | 10% a 35% | Ajuste o peso conforme o custo de erro no domínio. |
| D5 Ação Correta | Confirma se a recomendação ou decisão leva o fluxo para o próximo passo certo. | 10% a 35% | Ajuste o peso conforme o custo de erro no domínio. |
| D6 Auditabilidade | Confirma se o Evaluator consegue justificar a decisão com evidências rastreáveis no trace. | 10% a 35% | Ajuste o peso conforme o custo de erro no domínio. |

### Como escrever Critérios

- Um critério bom começa com verbo observável: verifica, compara, confirma, bloqueia, mede ou identifica.
- Um critério ruim usa intenção vaga: parece bom, soa natural, tem qualidade ou está completo.
- Cada critério deve dizer qual evidência o Evaluator consulta antes de pontuar.
- Cada critério deve deixar claro se é `critical` ou `standard`.
- Critério `critical` pode reprovar sozinho quando protege saúde, dinheiro, privacidade, segurança ou confiança.
- Critério `standard` contribui para score e feedback, mas não bloqueia sozinho.
- Se dois critérios sempre falham juntos, revise se eles deveriam ser um único critério.
- Se um critério nunca muda a decisão, remova ou reduza o peso.
- Se humanos discordam sobre o score, adicione exemplos por score level.
- Se o Generator não consegue agir sobre o feedback, reescreva o critério com linguagem mais concreta.

### Escala padrão recomendada

| Score | Nome | Interpretação | Uso recomendado |
|-------|------|---------------|-----------------|
| 0 | Falha total | O output viola o critério de forma clara ou ignora dado obrigatório. | Use quando o Generator precisa refazer a parte avaliada. |
| 1 | Fraco | O output tenta atender, mas deixa lacuna importante. | Use quando há sinal de intenção correta, mas risco ainda alto. |
| 2 | Aceitável com ressalvas | O output atende ao mínimo, mas precisa melhoria para confiança alta. | Use para aprovar apenas se nenhum critério crítico falhar. |
| 3 | Bom | O output atende bem, com pequenas melhorias opcionais. | Use como padrão esperado em produção. |
| 4 | Excelente | O output atende completamente e mostra cuidado contextual. | Use quando a resposta deve virar exemplo de calibragem. |

### Fórmulas de scoring

- `raw_score` soma os pontos de todos os critérios antes de considerar peso.
- `max_raw_score` é a quantidade de critérios multiplicada pelo maior score possível.
- `normalized_score` converte `raw_score` para escala 0 a 100.
- `dimension_score` calcula a média normalizada dos critérios dentro de uma dimensão.
- `weighted_score` soma cada `dimension_score` multiplicado pelo peso da dimensão.
- `confidence_score` mede se o Evaluator encontrou evidência suficiente para confiar no julgamento.
- `final_score` deve ser igual ao `weighted_score`, exceto quando blocker criteria forçam rejeição.

```text
raw_score = soma(criteria_scores)
normalized_score = raw_score / max_raw_score * 100
dimension_score = media(criteria_scores_da_dimensao) / max_score * 100
weighted_score = soma(dimension_score * dimension_weight)
final_decision = decision_logic(weighted_score, blocker_criteria, escalation_criteria)
```

### Lógica de Decisão padrão

- APPROVE quando `weighted_score` é maior ou igual ao `approval_threshold` e nenhum blocker criterion falha.
- NEEDS_REVISION quando o score está perto do threshold e os problemas são corrigíveis pelo Generator em uma nova tentativa.
- REJECT quando blocker criterion falha ou quando o score fica abaixo do limite mínimo de qualidade.
- ESCALATE quando há falta de evidência, conflito entre fontes, risco de saúde, risco financeiro ou ambiguidade que o Evaluator não deve resolver sozinho.
- CONDITIONAL_APPROVE apenas quando o domínio aceita pequenos ajustes automáticos sem nova geração completa.

### Feedback Format padrão

```json
{
  "decision": "NEEDS_REVISION",
  "final_score": 78.5,
  "approval_threshold": 85,
  "blockers_triggered": [],
  "failed_criteria": [
    {
      "criterion_id": "C3",
      "criterion_name": "Compatibilidade com restrição do cliente",
      "score": 1,
      "expected": "A resposta precisa citar a restrição e recomendar apenas opções compatíveis.",
      "observed": "A resposta recomenda produto compatível, mas não menciona a restrição registrada.",
      "required_change": "Reescrever a recomendação citando a restrição e a evidência de compatibilidade."
    }
  ],
  "strongest_points": [
    "Preço e stock foram consultados corretamente.",
    "Tom de conversa está adequado para WhatsApp."
  ],
  "next_generator_instruction": "Refaça mantendo os produtos aprovados, mas explique por que cada um respeita a restrição do cliente."
}
```

---

## 📋 Guia de Adaptação por Domínio

O mesmo template funciona em vários domínios, mas os pesos, blocker criteria e exemplos precisam mudar. A regra prática é simples: o critério mais caro de errar deve aparecer como dimensão de alto peso ou blocker criterion.

| Domínio | Contexto típico | Dimensões centrais | Blockers prováveis | Threshold inicial |
|---------|-----------------|--------------------|--------------------|------------------|
| Recomendação de Produto | KODA, e-commerce, catálogo, inventory | Compatibilidade com restrições, stock, preço, benefício explicado | Alergia, produto fora de stock, preço incorreto, recomendação contra objetivo do cliente | 85 a 92 |
| Avaliação de Texto | conteúdo de blog, resposta de suporte, copy de campanha | Clareza, aderência ao briefing, factualidade, tom de marca | Afirmação falsa, promessa proibida, tom ofensivo, informação sensível | 80 a 88 |
| Code Review | pull request, patch de agente, script operacional | Correção, segurança, testabilidade, escopo, manutenibilidade | Bug crítico, secret, quebra de contrato, ausência de teste obrigatório | 82 a 90 |
| Order Validation | checkout, pagamento, fulfillment | Campos obrigatórios, preço final, endereço, estoque, regra promocional | Cobrança duplicada, item errado, endereço inválido, fraude provável | 93 a 98 |
| Customer Support | WhatsApp, chat, email | Empatia, precisão, resolução, política correta, escalonamento | Promessa fora de política, dado pessoal exposto, orientação insegura | 84 a 91 |
| Planning Agent | sprint plan, task breakdown, long-running agent plan | Sequência, dependências, riscos, definição de done, token budget | Plano sem verificação, dependência bloqueante omitida, ação destrutiva sem aprovação | 80 a 88 |
| Trace Analysis | debugging, incident review, evaluation audit | Evidência, causalidade, timeline, hipótese testável, recomendação | Conclusão sem trace, culpa sem evidência, risco de repetir incidente | 86 a 94 |
| Safety Review | saúde, finanças, privacidade, compliance | Risco, limites, fonte, escalonamento, linguagem segura | Conselho médico indevido, exposição de dado, ação de alto risco sem humano | 95 a 99 |

### Adaptação para Recomendação de Produto

- Contexto de uso: KODA, e-commerce, catálogo, inventory.
- Dimensões que costumam importar: Compatibilidade com restrições, stock, preço, benefício explicado.
- Blocker criteria comuns: Alergia, produto fora de stock, preço incorreto, recomendação contra objetivo do cliente.
- Threshold inicial recomendado: 85 a 92.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Adaptação para Avaliação de Texto

- Contexto de uso: conteúdo de blog, resposta de suporte, copy de campanha.
- Dimensões que costumam importar: Clareza, aderência ao briefing, factualidade, tom de marca.
- Blocker criteria comuns: Afirmação falsa, promessa proibida, tom ofensivo, informação sensível.
- Threshold inicial recomendado: 80 a 88.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Adaptação para Code Review

- Contexto de uso: pull request, patch de agente, script operacional.
- Dimensões que costumam importar: Correção, segurança, testabilidade, escopo, manutenibilidade.
- Blocker criteria comuns: Bug crítico, secret, quebra de contrato, ausência de teste obrigatório.
- Threshold inicial recomendado: 82 a 90.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Adaptação para Order Validation

- Contexto de uso: checkout, pagamento, fulfillment.
- Dimensões que costumam importar: Campos obrigatórios, preço final, endereço, estoque, regra promocional.
- Blocker criteria comuns: Cobrança duplicada, item errado, endereço inválido, fraude provável.
- Threshold inicial recomendado: 93 a 98.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Adaptação para Customer Support

- Contexto de uso: WhatsApp, chat, email.
- Dimensões que costumam importar: Empatia, precisão, resolução, política correta, escalonamento.
- Blocker criteria comuns: Promessa fora de política, dado pessoal exposto, orientação insegura.
- Threshold inicial recomendado: 84 a 91.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Adaptação para Planning Agent

- Contexto de uso: sprint plan, task breakdown, long-running agent plan.
- Dimensões que costumam importar: Sequência, dependências, riscos, definição de done, token budget.
- Blocker criteria comuns: Plano sem verificação, dependência bloqueante omitida, ação destrutiva sem aprovação.
- Threshold inicial recomendado: 80 a 88.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Adaptação para Trace Analysis

- Contexto de uso: debugging, incident review, evaluation audit.
- Dimensões que costumam importar: Evidência, causalidade, timeline, hipótese testável, recomendação.
- Blocker criteria comuns: Conclusão sem trace, culpa sem evidência, risco de repetir incidente.
- Threshold inicial recomendado: 86 a 94.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Adaptação para Safety Review

- Contexto de uso: saúde, finanças, privacidade, compliance.
- Dimensões que costumam importar: Risco, limites, fonte, escalonamento, linguagem segura.
- Blocker criteria comuns: Conselho médico indevido, exposição de dado, ação de alto risco sem humano.
- Threshold inicial recomendado: 95 a 99.
- Ajuste os pesos depois de revisar pelo menos 30 exemplos reais.
- Inclua um exemplo aprovado, um rejeitado e um caso limite antes do rollout.
- Registre no trace quais evidências foram usadas para cada score.
- Use feedback curto quando o Generator só precisa corrigir uma lacuna.
- Use feedback detalhado quando a falha envolve múltiplas dimensões.
- Escale para humano quando o Evaluator não consegue distinguir risco real de ambiguidade no input.

### Biblioteca de Critérios Reutilizáveis por Domínio

#### Recomendação de Produto

1. **Compatibilidade nutricional:** Confirma se o produto respeita alergias, intolerâncias e restrições declaradas.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

2. **Disponibilidade real:** Confirma se cada item recomendado está em stock no canal correto.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

3. **Preço atualizado:** Confirma se preço, desconto e assinatura batem com a fonte de catálogo.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

4. **Objetivo do cliente:** Confirma se o produto atende ao objetivo declarado, como ganho de massa ou praticidade.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

5. **Justificativa de recomendação:** Confirma se a resposta explica por que aquele produto foi escolhido.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

6. **Alternativa segura:** Confirma se há alternativa quando a primeira opção falha por restrição ou stock.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

7. **Transparência de tradeoff:** Confirma se limitações como sabor, preço ou dose são apresentadas sem esconder custo.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

8. **Ação próxima:** Confirma se a resposta leva o cliente para escolha, carrinho ou pergunta objetiva.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

#### Avaliação de Texto

1. **Aderência ao briefing:** Confirma se o texto cumpre objetivo, público e formato solicitados.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

2. **Clareza da mensagem:** Confirma se a ideia principal aparece cedo e sem ambiguidade.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

3. **Factualidade:** Confirma se afirmações concretas têm base ou fonte interna.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

4. **Tom de marca:** Confirma se voz, formalidade e vocabulário combinam com o canal.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

5. **Ausência de exagero:** Confirma se o texto não promete resultado que o produto não garante.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

6. **Estrutura:** Confirma se parágrafos, bullets e ordem ajudam a leitura.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

7. **Ação desejada:** Confirma se o leitor sabe o próximo passo depois de ler.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

8. **Economia de palavras:** Confirma se não há repetição que consome atenção sem valor.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

#### Code Review

1. **Correção funcional:** Confirma se o código implementa o comportamento solicitado.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

2. **Cobertura de testes:** Confirma se há teste proporcional ao risco da mudança.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

3. **Segurança:** Confirma se não há secret, action perigosa ou validação ausente em boundary externo.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

4. **Escopo mínimo:** Confirma se a mudança não inclui refactor ou feature fora do pedido.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

5. **Legibilidade:** Confirma se nomes, fluxo e separação de responsabilidades são claros.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

6. **Contrato de API:** Confirma se entradas, saídas e erros respeitam o contrato existente.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

7. **Observabilidade:** Confirma se logs e traces ajudam sem vazar dado sensível.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

8. **Compatibilidade com arquitetura:** Confirma se a solução segue padrões do repositório.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

#### Order Validation

1. **Identidade do cliente:** Confirma se pedido está ligado ao cliente correto sem misturar sessões.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

2. **Itens do pedido:** Confirma se SKU, quantidade e variação correspondem à escolha final.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

3. **Preço final:** Confirma subtotal, desconto, frete e total antes de pagamento.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

4. **Endereço:** Confirma se endereço é entregável e completo.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

5. **Stock reservado:** Confirma se inventory foi reservado antes de confirmação final.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

6. **Política promocional:** Confirma se cupom ou campanha foram aplicados corretamente.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

7. **Risco de duplicidade:** Confirma se o pedido não repete uma cobrança anterior.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

8. **Escalonamento de anomalia:** Confirma se fraude, conflito de dados ou ausência de evidência vai para humano.
   - Score 0: evidência contradiz o critério ou o draft ignora dado obrigatório.
   - Score 1: há tentativa parcial, mas falta evidência central para confiar.
   - Score 2: atende ao mínimo, com ressalva que deve aparecer no feedback.
   - Score 3: atende bem e permite aprovação se nenhum blocker falhar.
   - Score 4: atende completamente e pode entrar no calibration set como exemplo forte.

---

## 📝 3 Exemplos Preenchidos

Os três exemplos abaixo são completos o bastante para copiar como ponto de partida. Eles mostram como o mesmo template muda de pesos, blockers e feedback conforme o domínio.

### Exemplo 1: Recomendação de Produto para e-commerce KODA

- `rubric_id`: `koda-product-recommendation-v1`
- `domain`: `product_recommendation`
- `target_success_rate`: `98%`
- Cenário: Cliente no WhatsApp procura suplemento para ganho de massa, informa intolerância à lactose, orçamento de R$ 120 e preferência por sabor chocolate. KODA precisa recomendar até três produtos compatíveis sem inventar preço ou stock.

#### Dimensões preenchidas

| ID | Nome | Peso | Descrição |
|----|------|------|-----------|
| D1 | Segurança e restrições | 0.30 | Protege saúde, alergias, intolerâncias e restrições explícitas. |
| D2 | Factualidade comercial | 0.25 | Confirma stock, preço, SKU, desconto e disponibilidade. |
| D3 | Fit com objetivo do cliente | 0.20 | Avalia se a recomendação ajuda o objetivo declarado. |
| D4 | Clareza conversacional | 0.15 | Mede se a resposta é clara para WhatsApp. |
| D5 | Próximo passo | 0.10 | Confirma se o cliente sabe o que fazer depois. |

#### Critérios preenchidos

| ID | Dimensão | Nome | Tipo | Descrição | Exemplo positivo | Exemplo negativo |
|----|----------|------|------|-----------|------------------|------------------|
| C1 | D1 | Compatibilidade com lactose | critical | Produto não pode conter lactose quando cliente declara intolerância. | Cliente intolerante recebe whey sem lactose confirmado por ficha técnica. | Produto com lactose ou risco não explicado. |
| C2 | D1 | Risco de contaminação | critical | Avisos de fábrica compartilhada precisam ser tratados quando restrição é forte. | Resposta avisa contaminação cruzada e sugere opção vegana segura. | Resposta omite aviso presente no rótulo. |
| C3 | D2 | Preço e desconto | standard | Valores precisam bater com catálogo consultado. | R$ 109,90 aparece igual no catálogo e na resposta. | Resposta usa preço antigo de campanha encerrada. |
| C4 | D2 | Stock no canal correto | critical | Produto precisa estar disponível para entrega no CEP informado. | Produto disponível no centro SP com entrega em 2 dias. | Produto aparece em stock nacional, mas indisponível para o CEP. |
| C5 | D3 | Aderência ao objetivo | standard | Produto deve ajudar ganho de massa com argumento nutricional correto. | Recomenda hipercalórico sem lactose com proteína e calorias adequadas. | Recomenda multivitamínico como principal solução para ganho de massa. |
| C6 | D4 | Explicação curta e útil | standard | Resposta deve caber no ritmo de WhatsApp sem perder informação crítica. | Duas opções com motivo, preço e pergunta de escolha. | Texto longo com detalhes técnicos que escondem a recomendação. |
| C7 | D5 | CTA seguro | standard | Próximo passo deve pedir escolha ou confirmação, não forçar compra. | Pergunta se cliente prefere sabor chocolate ou baunilha sem lactose. | Afirma que vai fechar pedido sem confirmação explícita. |

#### Escala por critério

##### C1: Compatibilidade com lactose

- Score 0: Produto com lactose ou risco não explicado. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Compatibilidade com lactose`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Cliente intolerante recebe whey sem lactose confirmado por ficha técnica. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C2: Risco de contaminação

- Score 0: Resposta omite aviso presente no rótulo. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Risco de contaminação`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Resposta avisa contaminação cruzada e sugere opção vegana segura. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C3: Preço e desconto

- Score 0: Resposta usa preço antigo de campanha encerrada. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Preço e desconto`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: R$ 109,90 aparece igual no catálogo e na resposta. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C4: Stock no canal correto

- Score 0: Produto aparece em stock nacional, mas indisponível para o CEP. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Stock no canal correto`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Produto disponível no centro SP com entrega em 2 dias. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C5: Aderência ao objetivo

- Score 0: Recomenda multivitamínico como principal solução para ganho de massa. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Aderência ao objetivo`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Recomenda hipercalórico sem lactose com proteína e calorias adequadas. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C6: Explicação curta e útil

- Score 0: Texto longo com detalhes técnicos que escondem a recomendação. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Explicação curta e útil`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Duas opções com motivo, preço e pergunta de escolha. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C7: CTA seguro

- Score 0: Afirma que vai fechar pedido sem confirmação explícita. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `CTA seguro`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Pergunta se cliente prefere sabor chocolate ou baunilha sem lactose. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

#### Lógica de decisão preenchida

- Regra principal: APPROVE se score >= 88, nenhum critério critical falhar, e confidence_score >= 0.85.
- REJECT quando qualquer critério `critical` recebe score 0 ou 1.
- NEEDS_REVISION quando não há blocker, mas o score fica até 7 pontos abaixo do threshold.
- ESCALATE quando a evidência necessária não está disponível ou há conflito entre fontes oficiais.
- APPROVE quando o score passa o threshold e o feedback não contém mudança obrigatória.

#### Feedback Format preenchido

- Diretriz: Quando rejeitar, cite o produto problemático, a restrição violada, a fonte consultada e a instrução exata para nova tentativa.
- Inclua `criterion_id` para cada problema.
- Inclua evidência concreta, não apenas opinião.
- Inclua uma instrução que o Generator consiga executar em uma nova tentativa.
- Separe mudança obrigatória de melhoria opcional.

```json
{
  "rubric_id": "koda-product-recommendation-v1",
  "decision": "NEEDS_REVISION",
  "final_score": 81.5,
  "approval_threshold": 86,
  "blockers_triggered": [],
  "failed_criteria": [
    {
      "criterion_id": "C1",
      "criterion_name": "Compatibilidade com lactose",
      "observed": "O draft não mostrou evidência suficiente para score alto neste critério.",
      "required_change": "Revisar o trecho afetado usando a fonte oficial indicada no input."
    }
  ],
  "next_generator_instruction": "Gerar nova versão mantendo os pontos aprovados e corrigindo apenas os critérios listados."
}
```

### Exemplo 2: Avaliação de Texto para content quality

- `rubric_id`: `content-quality-evaluation-v1`
- `domain`: `content_quality`
- `target_success_rate`: `92%`
- Cenário: Equipe de marketing pede um texto curto para explicar o novo bundle de creatina e whey sem prometer resultado médico. O Generator escreve a copy. O Evaluator precisa checar clareza, aderência ao briefing, tom de marca e ausência de claims proibidos.

#### Dimensões preenchidas

| ID | Nome | Peso | Descrição |
|----|------|------|-----------|
| D1 | Aderência ao briefing | 0.25 | Confirma objetivo, público, canal e formato. |
| D2 | Factualidade e claims | 0.30 | Impede promessas não comprovadas e erro de produto. |
| D3 | Clareza e estrutura | 0.20 | Garante leitura rápida e mensagem central nítida. |
| D4 | Tom de marca | 0.15 | Mantém voz confiável, próxima e sem pressão indevida. |
| D5 | CTA | 0.10 | Fecha com ação apropriada ao funil. |

#### Critérios preenchidos

| ID | Dimensão | Nome | Tipo | Descrição | Exemplo positivo | Exemplo negativo |
|----|----------|------|------|-----------|------------------|------------------|
| C1 | D1 | Formato solicitado | standard | Texto precisa respeitar canal e tamanho combinados. | Copy de WhatsApp com até 600 caracteres. | Texto vira artigo longo sem pedido. |
| C2 | D1 | Público correto | standard | A linguagem deve falar com cliente iniciante em suplementos. | Explica benefícios em termos simples. | Usa jargão de fisiculturismo sem contexto. |
| C3 | D2 | Claims permitidos | critical | Não pode prometer cura, perda de peso garantida ou resultado médico. | Diz que produto apoia rotina de treino. | Diz que produto garante ganho muscular em 7 dias. |
| C4 | D2 | Dados do produto | critical | Ingredientes, sabores e preço precisam estar corretos. | Cita bundle com whey chocolate e creatina 300g conforme catálogo. | Cita sabor baunilha que não existe no bundle. |
| C5 | D3 | Mensagem principal | standard | O leitor deve entender oferta e motivo em poucos segundos. | Primeira frase explica o bundle e para quem serve. | Primeira metade fala de histórico da marca sem explicar oferta. |
| C6 | D4 | Tom confiável | standard | Texto deve vender sem parecer agressivo. | Convida o cliente a conhecer opções. | Pressiona com medo de perder saúde se não comprar. |
| C7 | D5 | CTA proporcional | standard | A ação deve combinar com etapa de descoberta. | Pergunta se quer ver preço e sabores disponíveis. | Pede pagamento imediato sem contexto. |

#### Escala por critério

##### C1: Formato solicitado

- Score 0: Texto vira artigo longo sem pedido. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Formato solicitado`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Copy de WhatsApp com até 600 caracteres. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C2: Público correto

- Score 0: Usa jargão de fisiculturismo sem contexto. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Público correto`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Explica benefícios em termos simples. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C3: Claims permitidos

- Score 0: Diz que produto garante ganho muscular em 7 dias. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Claims permitidos`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Diz que produto apoia rotina de treino. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C4: Dados do produto

- Score 0: Cita sabor baunilha que não existe no bundle. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Dados do produto`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Cita bundle com whey chocolate e creatina 300g conforme catálogo. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C5: Mensagem principal

- Score 0: Primeira metade fala de histórico da marca sem explicar oferta. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Mensagem principal`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Primeira frase explica o bundle e para quem serve. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C6: Tom confiável

- Score 0: Pressiona com medo de perder saúde se não comprar. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Tom confiável`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Convida o cliente a conhecer opções. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C7: CTA proporcional

- Score 0: Pede pagamento imediato sem contexto. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `CTA proporcional`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Pergunta se quer ver preço e sabores disponíveis. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

#### Lógica de decisão preenchida

- Regra principal: APPROVE se score >= 84, sem claim proibido, sem dado de produto errado e com no máximo uma ressalva de clareza.
- REJECT quando qualquer critério `critical` recebe score 0 ou 1.
- NEEDS_REVISION quando não há blocker, mas o score fica até 7 pontos abaixo do threshold.
- ESCALATE quando a evidência necessária não está disponível ou há conflito entre fontes oficiais.
- APPROVE quando o score passa o threshold e o feedback não contém mudança obrigatória.

#### Feedback Format preenchido

- Diretriz: Quando rejeitar, marque o trecho problemático e sugira reescrita curta que preserve o objetivo do briefing.
- Inclua `criterion_id` para cada problema.
- Inclua evidência concreta, não apenas opinião.
- Inclua uma instrução que o Generator consiga executar em uma nova tentativa.
- Separe mudança obrigatória de melhoria opcional.

```json
{
  "rubric_id": "content-quality-evaluation-v1",
  "decision": "NEEDS_REVISION",
  "final_score": 81.5,
  "approval_threshold": 86,
  "blockers_triggered": [],
  "failed_criteria": [
    {
      "criterion_id": "C1",
      "criterion_name": "Formato solicitado",
      "observed": "O draft não mostrou evidência suficiente para score alto neste critério.",
      "required_change": "Revisar o trecho afetado usando a fonte oficial indicada no input."
    }
  ],
  "next_generator_instruction": "Gerar nova versão mantendo os pontos aprovados e corrigindo apenas os critérios listados."
}
```

### Exemplo 3: Code Review para code quality

- `rubric_id`: `code-review-quality-v1`
- `domain`: `code_review`
- `target_success_rate`: `95%`
- Cenário: Um patch altera o Evaluator de KODA para carregar rubric JSON por feature. O Generator implementa a mudança. O Evaluator de code review precisa decidir se o patch pode seguir sem quebrar segurança, testes ou padrões do repositório.

#### Dimensões preenchidas

| ID | Nome | Peso | Descrição |
|----|------|------|-----------|
| D1 | Correção funcional | 0.30 | Código entrega o comportamento solicitado. |
| D2 | Segurança e dados | 0.25 | Evita secrets, vazamento de PII e ações perigosas. |
| D3 | Testabilidade | 0.20 | Garante validação automatizada proporcional ao risco. |
| D4 | Escopo e arquitetura | 0.15 | Mantém mudança pequena e alinhada aos padrões. |
| D5 | Manutenção | 0.10 | Código é fácil de ler e revisar. |

#### Critérios preenchidos

| ID | Dimensão | Nome | Tipo | Descrição | Exemplo positivo | Exemplo negativo |
|----|----------|------|------|-----------|------------------|------------------|
| C1 | D1 | Contrato preservado | critical | Inputs e outputs públicos continuam compatíveis. | Evaluator aceita rubric_id e retorna decision no formato existente. | Mudança renomeia decision para verdict sem adaptar callers. |
| C2 | D1 | Erro tratado no boundary | standard | Falha de leitura de rubric retorna erro claro no boundary externo. | Mensagem informa rubric ausente e feature afetada. | Erro genérico quebra processo sem contexto. |
| C3 | D2 | Sem secrets | critical | Patch não adiciona chaves, tokens ou dados sensíveis. | Config lê caminho local sem credencial. | Teste inclui token real em fixture. |
| C4 | D2 | PII protegida | critical | Logs não expõem telefone, email ou endereço. | Trace usa customer_id mascarado. | Log imprime conversa completa do cliente. |
| C5 | D3 | Teste de caminho feliz | standard | Há teste cobrindo rubric válido e aprovação. | Unit test carrega JSON e espera APPROVE. | Sem teste para novo loader. |
| C6 | D3 | Teste de falha crítica | standard | Há teste cobrindo rubric ausente ou inválido. | Unit test espera erro claro quando version falta. | Só testa entrada perfeita. |
| C7 | D4 | Escopo mínimo | standard | Patch não muda partes não relacionadas. | Altera loader e tests relacionados. | Também refatora customer service sem necessidade. |
| C8 | D5 | Nomes claros | standard | Funções e tipos comunicam intenção. | loadRubricForFeature descreve responsabilidade. | Função process faz leitura, scoring e logging juntos. |

#### Escala por critério

##### C1: Contrato preservado

- Score 0: Mudança renomeia decision para verdict sem adaptar callers. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Contrato preservado`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Evaluator aceita rubric_id e retorna decision no formato existente. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C2: Erro tratado no boundary

- Score 0: Erro genérico quebra processo sem contexto. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Erro tratado no boundary`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Mensagem informa rubric ausente e feature afetada. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C3: Sem secrets

- Score 0: Teste inclui token real em fixture. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Sem secrets`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Config lê caminho local sem credencial. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C4: PII protegida

- Score 0: Log imprime conversa completa do cliente. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `PII protegida`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Trace usa customer_id mascarado. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C5: Teste de caminho feliz

- Score 0: Sem teste para novo loader. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Teste de caminho feliz`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Unit test carrega JSON e espera APPROVE. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C6: Teste de falha crítica

- Score 0: Só testa entrada perfeita. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Teste de falha crítica`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Unit test espera erro claro quando version falta. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C7: Escopo mínimo

- Score 0: Também refatora customer service sem necessidade. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Escopo mínimo`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: Altera loader e tests relacionados. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

##### C8: Nomes claros

- Score 0: Função process faz leitura, scoring e logging juntos. A falha é clara e deve bloquear ou reduzir fortemente o score.
- Score 1: O draft tenta atender `Nomes claros`, mas falta evidência principal ou há conflito relevante.
- Score 2: O draft atende ao mínimo, porém exige ressalva no feedback para reduzir risco.
- Score 3: loadRubricForFeature descreve responsabilidade. A evidência é suficiente para aprovar se o restante do rubric passar.
- Score 4: Além de cumprir o critério, o draft antecipa dúvida provável e mantém rastreabilidade.

#### Lógica de decisão preenchida

- Regra principal: APPROVE se score >= 86, todos os critical passarem, testes relevantes existirem e lint não apontar erro no arquivo alterado.
- REJECT quando qualquer critério `critical` recebe score 0 ou 1.
- NEEDS_REVISION quando não há blocker, mas o score fica até 7 pontos abaixo do threshold.
- ESCALATE quando a evidência necessária não está disponível ou há conflito entre fontes oficiais.
- APPROVE quando o score passa o threshold e o feedback não contém mudança obrigatória.

#### Feedback Format preenchido

- Diretriz: Quando rejeitar, aponte arquivo, critério, risco concreto e teste ou mudança mínima necessária.
- Inclua `criterion_id` para cada problema.
- Inclua evidência concreta, não apenas opinião.
- Inclua uma instrução que o Generator consiga executar em uma nova tentativa.
- Separe mudança obrigatória de melhoria opcional.

```json
{
  "rubric_id": "code-review-quality-v1",
  "decision": "NEEDS_REVISION",
  "final_score": 81.5,
  "approval_threshold": 86,
  "blockers_triggered": [],
  "failed_criteria": [
    {
      "criterion_id": "C1",
      "criterion_name": "Contrato preservado",
      "observed": "O draft não mostrou evidência suficiente para score alto neste critério.",
      "required_change": "Revisar o trecho afetado usando a fonte oficial indicada no input."
    }
  ],
  "next_generator_instruction": "Gerar nova versão mantendo os pontos aprovados e corrigindo apenas os critérios listados."
}
```

---

## 🔧 Checklist de Validação de Rubric

Antes de colocar um rubric em produção, revise com três lentes: estrutura, comportamento e operação. Um rubric pode parecer completo e ainda falhar se o Evaluator não tiver evidência, se o threshold estiver baixo demais ou se o feedback não orientar o Generator.

### Checklist de Estrutura

- [ ] O `rubric_id` é único e segue padrão de nomenclatura do time.
- [ ] A `version` muda quando pesos, thresholds ou blockers mudam.
- [ ] O `target_success_rate` está explícito e combina com o risco do domínio.
- [ ] Todas as dimensões têm peso e a soma é 1.0 ou 100%.
- [ ] Cada dimensão descreve o risco de falha em linguagem concreta.
- [ ] Cada critério pertence a uma única dimensão.
- [ ] Cada critério tem tipo `critical` ou `standard`.
- [ ] Cada critério tem dados de evidência definidos.
- [ ] Cada score level tem definição observável.
- [ ] Cada score level tem exemplo positivo ou negativo quando há risco de discordância.

### Checklist de Comportamento

- [ ] O approval threshold rejeita exemplos ruins do calibration set.
- [ ] O approval threshold aprova exemplos bons do calibration set.
- [ ] Casos limite recebem NEEDS_REVISION ou ESCALATE de forma previsível.
- [ ] Blocker criteria realmente bloqueiam aprovação mesmo com score alto.
- [ ] Critérios standard influenciam score sem virar blocker escondido.
- [ ] O Evaluator consegue justificar cada score com evidência.
- [ ] Dois Evaluators aplicando o rubric chegam a decisões compatíveis.
- [ ] O Generator consegue corrigir uma rejeição usando apenas o feedback recebido.
- [ ] O feedback não contradiz a decisão final.
- [ ] A lógica de retry não incentiva tentativas infinitas.

### Checklist de Operação

- [ ] O rubric cabe no token budget do Evaluator.
- [ ] O rubric não exige fonte que o Evaluator não consegue acessar.
- [ ] O trace registra input, draft output, score, decision e feedback.
- [ ] O time sabe onde o rubric versionado fica armazenado.
- [ ] Existe owner responsável por revisar métricas do rubric.
- [ ] Existe cadence de revisão baseada em incidentes e feedback loop.
- [ ] Mudanças no rubric são comunicadas ao time que mantém o Generator.
- [ ] Casos escalados têm rota clara para humano.
- [ ] O rubric não contém dados sensíveis de clientes reais.
- [ ] O rubric foi testado em exemplos de produção anonimizados.

### Sinais de que o rubric ainda não está pronto

- O Evaluator escreve feedback como "melhore a qualidade" sem apontar critério.
- O Generator recebe rejeição e não sabe qual parte refazer.
- Score alto ainda permite falha de segurança, saúde, privacidade ou dinheiro.
- Score baixo aparece em respostas que humanos consideram claramente boas.
- Dois revisores humanos discordam sobre o mesmo critério sem conseguir resolver pela escala.
- O rubric depende de conhecimento que não está no input nem em fonte acessível.
- A soma de pesos não fecha ou muda entre documentos.
- A decisão usa regras que não aparecem no rubric.
- O threshold foi escolhido por intuição, sem calibration set.
- O feedback loop gera novas tentativas que repetem a mesma falha.

---

## 🚀 Aplicação KODA

KODA se beneficia de rubric templates porque seu risco principal não é apenas responder errado. O risco é responder errado com confiança, em escala, dentro de uma conversa que o cliente percebe como pessoal. Um template comum reduz esse risco em pontos específicos do harness.

| Área KODA | Uso do rubric template | Benefício direto |
|-----------|------------------------|------------------|
| Product Discovery | Evaluator pontua se a recomendação respeita restrições, objetivo, inventory, preço e canal. | Decisão mais consistente e trace mais fácil de auditar. |
| Order Processing | Evaluator valida se item, quantidade, endereço, pagamento e promoção batem antes de fulfillment. | Decisão mais consistente e trace mais fácil de auditar. |
| Customer Support | Evaluator checa política, tom, resolução e necessidade de escalation. | Decisão mais consistente e trace mais fácil de auditar. |
| Content Generation | Evaluator revisa mensagens de campanha para evitar claim proibido ou promessa exagerada. | Decisão mais consistente e trace mais fácil de auditar. |
| Code Changes | Evaluator de code review protege harness, traces, tests e security constraints. | Decisão mais consistente e trace mais fácil de auditar. |
| Trace Reading | Evaluator pós-incidente mede se a análise explica causa, evidência e ação corretiva. | Decisão mais consistente e trace mais fácil de auditar. |

### Como KODA aplica o template no fluxo diário

1. O Product Manager define a feature que precisa de avaliação, como recomendação de produto.
2. O owner copia o Template Principal e escolhe dimensões conforme risco do domínio.
3. A equipe adiciona critérios críticos para alergia, preço, stock, política e privacidade.
4. O time monta calibration set com exemplos aprovados, rejeitados, escalados e casos limite.
5. O Evaluator usa o rubric versionado para pontuar drafts do Generator.
6. O harness salva score, decision, feedback e rubric version no trace.
7. Quando o cliente dá feedback negativo, o time revisa se o rubric já cobria a falha.
8. Se a falha não estava coberta, uma nova version do rubric adiciona critério, exemplo ou blocker.
9. Se a falha estava coberta, o time revisa o prompt do Evaluator ou a evidência disponível.
10. O feedback loop fecha quando a próxima rodada de traces mostra queda na mesma classe de erro.

### Benefícios mensuráveis para KODA

- Menos recomendações incompatíveis com restrições de cliente.
- Menos rejeições falsas causadas por preferência subjetiva de estilo.
- Mais consistência entre Evaluators e entre versões do mesmo Evaluator.
- Melhor uso de token budget porque o Generator recebe feedback específico.
- Mais auditabilidade em incidentes porque o trace mostra critério, score e evidência.
- Mais velocidade para lançar novas features porque o template reduz trabalho inicial.
- Mais segurança em domínios sensíveis porque blockers ficam explícitos.
- Melhor onboarding de novos membros porque qualidade fica documentada em formato comum.

---

## 📊 Tabela Comparativa

| Abordagem | Custo | Velocidade | Consistência | Auditabilidade | Escalabilidade | Precisão | Melhor uso |
|-----------|-------|------------|--------------|----------------|----------------|----------|------------|
| Binary Validation | Baixo | Muito alta | Média quando critérios são simples | Baixa, pois só mostra passa ou falha | Alta para checks objetivos | Boa para regras determinísticas | Validar campo obrigatório, status de stock, formato JSON |
| Simple Scoring | Baixo a médio | Alta | Média, depende da escala | Média, mostra número mas pouca causa | Alta | Boa para triagem inicial | Rankear drafts similares antes de avaliação completa |
| Full Rubric | Médio | Média | Alta quando calibrado | Alta, porque liga score a critério e evidência | Alta com versionamento | Alta para tarefas complexas | Avaliar recomendação, texto, code review, order validation |
| Human Review | Alto | Baixa | Variável, depende do revisor | Alta quando bem documentada | Baixa | Muito alta em casos ambíguos | Risco de saúde, compliance, exceções comerciais e conflitos |

### Como escolher a abordagem

- Use Binary Validation quando a pergunta tem resposta objetiva, como "o campo existe?".
- Use Simple Scoring quando precisa ordenar opções, mas o custo de erro é baixo.
- Use Full Rubric quando múltiplas dimensões podem estar certas ou erradas ao mesmo tempo.
- Use Human Review quando a decisão envolve risco alto, ambiguidade real ou responsabilidade legal.
- Combine Full Rubric com Human Review quando o Evaluator detecta blocker, mas não tem autoridade para decidir sozinho.

---

## 🏗️ Diagrama ASCII

O diagrama abaixo mostra o pipeline completo. O ponto principal é que o rubric template entra no Evaluator antes da decisão, não depois.

```text
+------------------+
|      Input       |
| cliente, tarefa, |
| contexto, dados  |
+--------+---------+
         |
         v
+------------------+        +-------------------------+
|    Generator     |        |  Rubric Template Store |
| cria solução     |        | rubric_id, version,    |
| sem se aprovar   |        | dimensions, criteria   |
+--------+---------+        +-----------+-------------+
         |                              |
         v                              |
+------------------+                    |
|   Draft Output   |                    |
| recomendação,    |                    |
| texto ou patch   |                    |
+--------+---------+                    |
         |                              |
         v                              v
+----------------------------------------------------+
|             Evaluator with Rubric                  |
| lê draft output, aplica critérios, coleta evidência |
| calcula raw_score, normalized_score, weighted_score |
+-------------------------+--------------------------+
                          |
                          v
+----------------------------------------------------+
|                      Score                         |
| final_score, confidence_score, blockers_triggered  |
+-------------------------+--------------------------+
                          |
                          v
+----------------------------------------------------+
|                    Decision                        |
| APPROVE / REJECT / NEEDS_REVISION / ESCALATE       |
+-------------------------+--------------------------+
                          |
          +---------------+----------------+
          |                                |
          v                                v
+------------------+              +-------------------+
| Approved Output  |              | Feedback Loop     |
| segue para user  |              | volta ao Generator|
+------------------+              +-------------------+
```

---

## ✅ O Que Você Aprendeu

- Um rubric template transforma julgamento subjetivo em estrutura operacional.
- Dimensões agrupam critérios por tipo de risco e permitem pesos claros.
- Critérios precisam ser observáveis, ligados a evidência e escritos para uso por Evaluator.
- Escalas ficam confiáveis quando cada score level tem definição e exemplo.
- Scores raw, normalized e weighted resolvem partes diferentes do problema de avaliação.
- Lógica de Decisão impede que score alto esconda falha crítica.
- Feedback Format é parte do rubric, não detalhe posterior.
- KODA usa rubric templates para proteger customer trust em product recommendation, order validation, support e code review.
- Binary Validation, Simple Scoring, Full Rubric e Human Review têm custos e usos diferentes.
- Um rubric bom precisa de calibration set, versionamento e feedback loop.

A maior mudança mental é esta: o rubric não é documento auxiliar. Ele é parte do harness. Se o Generator precisa produzir com qualidade e o Evaluator precisa julgar com justiça, o rubric template é o contrato que mantém os dois alinhados.

---

## 🎓 Critérios de Conclusão

- [ ] Você consegue explicar a diferença entre Dimensão e Critério sem usar exemplo vago.
- [ ] Você consegue criar um `rubric_id`, `version` e `target_success_rate` para um domínio real.
- [ ] Você consegue escrever pelo menos quatro dimensões com pesos que somam 1.0.
- [ ] Você consegue escrever critérios com score levels de 0 a 4 e exemplos concretos.
- [ ] Você consegue definir approval threshold, blocker criteria e escalation criteria.
- [ ] Você consegue criar Feedback Format que o Generator pode seguir em nova tentativa.
- [ ] Você consegue adaptar o template para product recommendation, content quality ou code review.
- [ ] Você consegue comparar sua escolha de avaliação com Binary Validation, Simple Scoring e Human Review.
- [ ] Você consegue montar calibration set com exemplo aprovado, rejeitado, escalado e caso limite.
- [ ] Você consegue revisar um trace e dizer se a falha veio do Generator, do Evaluator ou do rubric.

Quando todos os itens acima estiverem claros, você está pronto para criar rubrics de produção em sistemas de agentes long-running.

---

## 📚 Apêndice A: Matriz Operacional de Critérios

Este apêndice oferece uma matriz extensa de critérios que podem ser copiados para novos rubrics. Cada item inclui intenção, evidência, falha comum e sinal de bom score. Use como biblioteca de trabalho, não como lista obrigatória.

### Domínio: Product Recommendation

#### Critério PRO01: Controle de restrição do cliente

- Intenção: garantir que `restrição do cliente` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `restrição do cliente`.
- Falha comum: o Evaluator assume que `restrição do cliente` está correto porque o draft output soa confiante.
- Score 0: `restrição do cliente` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `restrição do cliente` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `restrição do cliente` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `restrição do cliente` está correto, claro e apoiado por evidência rastreável.
- Score 4: `restrição do cliente` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO02: Controle de stock

- Intenção: garantir que `stock` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `stock`.
- Falha comum: o Evaluator assume que `stock` está correto porque o draft output soa confiante.
- Score 0: `stock` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `stock` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `stock` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `stock` está correto, claro e apoiado por evidência rastreável.
- Score 4: `stock` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO03: Controle de preço

- Intenção: garantir que `preço` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `preço`.
- Falha comum: o Evaluator assume que `preço` está correto porque o draft output soa confiante.
- Score 0: `preço` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `preço` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `preço` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `preço` está correto, claro e apoiado por evidência rastreável.
- Score 4: `preço` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO04: Controle de benefício

- Intenção: garantir que `benefício` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `benefício`.
- Falha comum: o Evaluator assume que `benefício` está correto porque o draft output soa confiante.
- Score 0: `benefício` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `benefício` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `benefício` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `benefício` está correto, claro e apoiado por evidência rastreável.
- Score 4: `benefício` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO05: Controle de alternativa

- Intenção: garantir que `alternativa` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `alternativa`.
- Falha comum: o Evaluator assume que `alternativa` está correto porque o draft output soa confiante.
- Score 0: `alternativa` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `alternativa` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `alternativa` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `alternativa` está correto, claro e apoiado por evidência rastreável.
- Score 4: `alternativa` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO06: Controle de risco

- Intenção: garantir que `risco` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `risco`.
- Falha comum: o Evaluator assume que `risco` está correto porque o draft output soa confiante.
- Score 0: `risco` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `risco` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `risco` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `risco` está correto, claro e apoiado por evidência rastreável.
- Score 4: `risco` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO07: Controle de comparação

- Intenção: garantir que `comparação` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `comparação`.
- Falha comum: o Evaluator assume que `comparação` está correto porque o draft output soa confiante.
- Score 0: `comparação` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `comparação` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `comparação` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `comparação` está correto, claro e apoiado por evidência rastreável.
- Score 4: `comparação` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO08: Controle de CTA

- Intenção: garantir que `CTA` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `CTA`.
- Falha comum: o Evaluator assume que `CTA` está correto porque o draft output soa confiante.
- Score 0: `CTA` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `CTA` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `CTA` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `CTA` está correto, claro e apoiado por evidência rastreável.
- Score 4: `CTA` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO09: Controle de personalização

- Intenção: garantir que `personalização` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `personalização`.
- Falha comum: o Evaluator assume que `personalização` está correto porque o draft output soa confiante.
- Score 0: `personalização` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `personalização` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `personalização` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `personalização` está correto, claro e apoiado por evidência rastreável.
- Score 4: `personalização` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PRO10: Controle de fonte de catálogo

- Intenção: garantir que `fonte de catálogo` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `fonte de catálogo`.
- Falha comum: o Evaluator assume que `fonte de catálogo` está correto porque o draft output soa confiante.
- Score 0: `fonte de catálogo` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `fonte de catálogo` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `fonte de catálogo` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `fonte de catálogo` está correto, claro e apoiado por evidência rastreável.
- Score 4: `fonte de catálogo` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

### Domínio: Content Quality

#### Critério CON01: Controle de briefing

- Intenção: garantir que `briefing` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `briefing`.
- Falha comum: o Evaluator assume que `briefing` está correto porque o draft output soa confiante.
- Score 0: `briefing` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `briefing` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `briefing` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `briefing` está correto, claro e apoiado por evidência rastreável.
- Score 4: `briefing` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON02: Controle de clareza

- Intenção: garantir que `clareza` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `clareza`.
- Falha comum: o Evaluator assume que `clareza` está correto porque o draft output soa confiante.
- Score 0: `clareza` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `clareza` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `clareza` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `clareza` está correto, claro e apoiado por evidência rastreável.
- Score 4: `clareza` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON03: Controle de estrutura

- Intenção: garantir que `estrutura` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `estrutura`.
- Falha comum: o Evaluator assume que `estrutura` está correto porque o draft output soa confiante.
- Score 0: `estrutura` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `estrutura` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `estrutura` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `estrutura` está correto, claro e apoiado por evidência rastreável.
- Score 4: `estrutura` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON04: Controle de tom

- Intenção: garantir que `tom` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `tom`.
- Falha comum: o Evaluator assume que `tom` está correto porque o draft output soa confiante.
- Score 0: `tom` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `tom` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `tom` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `tom` está correto, claro e apoiado por evidência rastreável.
- Score 4: `tom` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON05: Controle de factualidade

- Intenção: garantir que `factualidade` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `factualidade`.
- Falha comum: o Evaluator assume que `factualidade` está correto porque o draft output soa confiante.
- Score 0: `factualidade` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `factualidade` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `factualidade` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `factualidade` está correto, claro e apoiado por evidência rastreável.
- Score 4: `factualidade` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON06: Controle de claim

- Intenção: garantir que `claim` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `claim`.
- Falha comum: o Evaluator assume que `claim` está correto porque o draft output soa confiante.
- Score 0: `claim` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `claim` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `claim` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `claim` está correto, claro e apoiado por evidência rastreável.
- Score 4: `claim` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON07: Controle de CTA

- Intenção: garantir que `CTA` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `CTA`.
- Falha comum: o Evaluator assume que `CTA` está correto porque o draft output soa confiante.
- Score 0: `CTA` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `CTA` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `CTA` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `CTA` está correto, claro e apoiado por evidência rastreável.
- Score 4: `CTA` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON08: Controle de economia

- Intenção: garantir que `economia` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `economia`.
- Falha comum: o Evaluator assume que `economia` está correto porque o draft output soa confiante.
- Score 0: `economia` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `economia` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `economia` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `economia` está correto, claro e apoiado por evidência rastreável.
- Score 4: `economia` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON09: Controle de público

- Intenção: garantir que `público` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `público`.
- Falha comum: o Evaluator assume que `público` está correto porque o draft output soa confiante.
- Score 0: `público` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `público` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `público` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `público` está correto, claro e apoiado por evidência rastreável.
- Score 4: `público` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CON10: Controle de canal

- Intenção: garantir que `canal` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `canal`.
- Falha comum: o Evaluator assume que `canal` está correto porque o draft output soa confiante.
- Score 0: `canal` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `canal` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `canal` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `canal` está correto, claro e apoiado por evidência rastreável.
- Score 4: `canal` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

### Domínio: Code Review

#### Critério COD01: Controle de correção

- Intenção: garantir que `correção` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `correção`.
- Falha comum: o Evaluator assume que `correção` está correto porque o draft output soa confiante.
- Score 0: `correção` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `correção` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `correção` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `correção` está correto, claro e apoiado por evidência rastreável.
- Score 4: `correção` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD02: Controle de teste

- Intenção: garantir que `teste` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `teste`.
- Falha comum: o Evaluator assume que `teste` está correto porque o draft output soa confiante.
- Score 0: `teste` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `teste` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `teste` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `teste` está correto, claro e apoiado por evidência rastreável.
- Score 4: `teste` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD03: Controle de segurança

- Intenção: garantir que `segurança` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `segurança`.
- Falha comum: o Evaluator assume que `segurança` está correto porque o draft output soa confiante.
- Score 0: `segurança` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `segurança` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `segurança` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `segurança` está correto, claro e apoiado por evidência rastreável.
- Score 4: `segurança` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD04: Controle de escopo

- Intenção: garantir que `escopo` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `escopo`.
- Falha comum: o Evaluator assume que `escopo` está correto porque o draft output soa confiante.
- Score 0: `escopo` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `escopo` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `escopo` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `escopo` está correto, claro e apoiado por evidência rastreável.
- Score 4: `escopo` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD05: Controle de contrato

- Intenção: garantir que `contrato` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `contrato`.
- Falha comum: o Evaluator assume que `contrato` está correto porque o draft output soa confiante.
- Score 0: `contrato` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `contrato` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `contrato` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `contrato` está correto, claro e apoiado por evidência rastreável.
- Score 4: `contrato` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD06: Controle de legibilidade

- Intenção: garantir que `legibilidade` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `legibilidade`.
- Falha comum: o Evaluator assume que `legibilidade` está correto porque o draft output soa confiante.
- Score 0: `legibilidade` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `legibilidade` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `legibilidade` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `legibilidade` está correto, claro e apoiado por evidência rastreável.
- Score 4: `legibilidade` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD07: Controle de observabilidade

- Intenção: garantir que `observabilidade` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `observabilidade`.
- Falha comum: o Evaluator assume que `observabilidade` está correto porque o draft output soa confiante.
- Score 0: `observabilidade` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `observabilidade` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `observabilidade` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `observabilidade` está correto, claro e apoiado por evidência rastreável.
- Score 4: `observabilidade` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD08: Controle de performance

- Intenção: garantir que `performance` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `performance`.
- Falha comum: o Evaluator assume que `performance` está correto porque o draft output soa confiante.
- Score 0: `performance` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `performance` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `performance` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `performance` está correto, claro e apoiado por evidência rastreável.
- Score 4: `performance` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD09: Controle de configuração

- Intenção: garantir que `configuração` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `configuração`.
- Falha comum: o Evaluator assume que `configuração` está correto porque o draft output soa confiante.
- Score 0: `configuração` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `configuração` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `configuração` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `configuração` está correto, claro e apoiado por evidência rastreável.
- Score 4: `configuração` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério COD10: Controle de rollback

- Intenção: garantir que `rollback` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `rollback`.
- Falha comum: o Evaluator assume que `rollback` está correto porque o draft output soa confiante.
- Score 0: `rollback` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `rollback` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `rollback` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `rollback` está correto, claro e apoiado por evidência rastreável.
- Score 4: `rollback` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

### Domínio: Order Validation

#### Critério ORD01: Controle de SKU

- Intenção: garantir que `SKU` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `SKU`.
- Falha comum: o Evaluator assume que `SKU` está correto porque o draft output soa confiante.
- Score 0: `SKU` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `SKU` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `SKU` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `SKU` está correto, claro e apoiado por evidência rastreável.
- Score 4: `SKU` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD02: Controle de quantidade

- Intenção: garantir que `quantidade` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `quantidade`.
- Falha comum: o Evaluator assume que `quantidade` está correto porque o draft output soa confiante.
- Score 0: `quantidade` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `quantidade` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `quantidade` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `quantidade` está correto, claro e apoiado por evidência rastreável.
- Score 4: `quantidade` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD03: Controle de endereço

- Intenção: garantir que `endereço` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `endereço`.
- Falha comum: o Evaluator assume que `endereço` está correto porque o draft output soa confiante.
- Score 0: `endereço` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `endereço` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `endereço` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `endereço` está correto, claro e apoiado por evidência rastreável.
- Score 4: `endereço` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD04: Controle de pagamento

- Intenção: garantir que `pagamento` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `pagamento`.
- Falha comum: o Evaluator assume que `pagamento` está correto porque o draft output soa confiante.
- Score 0: `pagamento` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `pagamento` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `pagamento` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `pagamento` está correto, claro e apoiado por evidência rastreável.
- Score 4: `pagamento` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD05: Controle de cupom

- Intenção: garantir que `cupom` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `cupom`.
- Falha comum: o Evaluator assume que `cupom` está correto porque o draft output soa confiante.
- Score 0: `cupom` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `cupom` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `cupom` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `cupom` está correto, claro e apoiado por evidência rastreável.
- Score 4: `cupom` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD06: Controle de frete

- Intenção: garantir que `frete` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `frete`.
- Falha comum: o Evaluator assume que `frete` está correto porque o draft output soa confiante.
- Score 0: `frete` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `frete` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `frete` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `frete` está correto, claro e apoiado por evidência rastreável.
- Score 4: `frete` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD07: Controle de duplicidade

- Intenção: garantir que `duplicidade` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `duplicidade`.
- Falha comum: o Evaluator assume que `duplicidade` está correto porque o draft output soa confiante.
- Score 0: `duplicidade` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `duplicidade` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `duplicidade` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `duplicidade` está correto, claro e apoiado por evidência rastreável.
- Score 4: `duplicidade` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD08: Controle de fraude

- Intenção: garantir que `fraude` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `fraude`.
- Falha comum: o Evaluator assume que `fraude` está correto porque o draft output soa confiante.
- Score 0: `fraude` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `fraude` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `fraude` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `fraude` está correto, claro e apoiado por evidência rastreável.
- Score 4: `fraude` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD09: Controle de fulfillment

- Intenção: garantir que `fulfillment` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `fulfillment`.
- Falha comum: o Evaluator assume que `fulfillment` está correto porque o draft output soa confiante.
- Score 0: `fulfillment` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `fulfillment` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `fulfillment` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `fulfillment` está correto, claro e apoiado por evidência rastreável.
- Score 4: `fulfillment` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério ORD10: Controle de confirmação

- Intenção: garantir que `confirmação` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `confirmação`.
- Falha comum: o Evaluator assume que `confirmação` está correto porque o draft output soa confiante.
- Score 0: `confirmação` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `confirmação` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `confirmação` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `confirmação` está correto, claro e apoiado por evidência rastreável.
- Score 4: `confirmação` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

### Domínio: Customer Support

#### Critério CUS01: Controle de política

- Intenção: garantir que `política` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `política`.
- Falha comum: o Evaluator assume que `política` está correto porque o draft output soa confiante.
- Score 0: `política` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `política` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `política` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `política` está correto, claro e apoiado por evidência rastreável.
- Score 4: `política` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS02: Controle de empatia

- Intenção: garantir que `empatia` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `empatia`.
- Falha comum: o Evaluator assume que `empatia` está correto porque o draft output soa confiante.
- Score 0: `empatia` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `empatia` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `empatia` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `empatia` está correto, claro e apoiado por evidência rastreável.
- Score 4: `empatia` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS03: Controle de resolução

- Intenção: garantir que `resolução` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `resolução`.
- Falha comum: o Evaluator assume que `resolução` está correto porque o draft output soa confiante.
- Score 0: `resolução` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `resolução` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `resolução` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `resolução` está correto, claro e apoiado por evidência rastreável.
- Score 4: `resolução` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS04: Controle de escalation

- Intenção: garantir que `escalation` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `escalation`.
- Falha comum: o Evaluator assume que `escalation` está correto porque o draft output soa confiante.
- Score 0: `escalation` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `escalation` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `escalation` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `escalation` está correto, claro e apoiado por evidência rastreável.
- Score 4: `escalation` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS05: Controle de privacidade

- Intenção: garantir que `privacidade` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `privacidade`.
- Falha comum: o Evaluator assume que `privacidade` está correto porque o draft output soa confiante.
- Score 0: `privacidade` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `privacidade` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `privacidade` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `privacidade` está correto, claro e apoiado por evidência rastreável.
- Score 4: `privacidade` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS06: Controle de tom

- Intenção: garantir que `tom` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `tom`.
- Falha comum: o Evaluator assume que `tom` está correto porque o draft output soa confiante.
- Score 0: `tom` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `tom` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `tom` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `tom` está correto, claro e apoiado por evidência rastreável.
- Score 4: `tom` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS07: Controle de tempo

- Intenção: garantir que `tempo` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `tempo`.
- Falha comum: o Evaluator assume que `tempo` está correto porque o draft output soa confiante.
- Score 0: `tempo` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `tempo` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `tempo` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `tempo` está correto, claro e apoiado por evidência rastreável.
- Score 4: `tempo` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS08: Controle de próximo passo

- Intenção: garantir que `próximo passo` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `próximo passo`.
- Falha comum: o Evaluator assume que `próximo passo` está correto porque o draft output soa confiante.
- Score 0: `próximo passo` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `próximo passo` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `próximo passo` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `próximo passo` está correto, claro e apoiado por evidência rastreável.
- Score 4: `próximo passo` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS09: Controle de histórico

- Intenção: garantir que `histórico` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `histórico`.
- Falha comum: o Evaluator assume que `histórico` está correto porque o draft output soa confiante.
- Score 0: `histórico` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `histórico` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `histórico` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `histórico` está correto, claro e apoiado por evidência rastreável.
- Score 4: `histórico` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério CUS10: Controle de limite de promessa

- Intenção: garantir que `limite de promessa` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `limite de promessa`.
- Falha comum: o Evaluator assume que `limite de promessa` está correto porque o draft output soa confiante.
- Score 0: `limite de promessa` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `limite de promessa` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `limite de promessa` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `limite de promessa` está correto, claro e apoiado por evidência rastreável.
- Score 4: `limite de promessa` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

### Domínio: Planning

#### Critério PLA01: Controle de objetivo

- Intenção: garantir que `objetivo` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `objetivo`.
- Falha comum: o Evaluator assume que `objetivo` está correto porque o draft output soa confiante.
- Score 0: `objetivo` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `objetivo` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `objetivo` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `objetivo` está correto, claro e apoiado por evidência rastreável.
- Score 4: `objetivo` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA02: Controle de dependência

- Intenção: garantir que `dependência` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `dependência`.
- Falha comum: o Evaluator assume que `dependência` está correto porque o draft output soa confiante.
- Score 0: `dependência` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `dependência` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `dependência` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `dependência` está correto, claro e apoiado por evidência rastreável.
- Score 4: `dependência` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA03: Controle de sequência

- Intenção: garantir que `sequência` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `sequência`.
- Falha comum: o Evaluator assume que `sequência` está correto porque o draft output soa confiante.
- Score 0: `sequência` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `sequência` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `sequência` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `sequência` está correto, claro e apoiado por evidência rastreável.
- Score 4: `sequência` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA04: Controle de risco

- Intenção: garantir que `risco` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `risco`.
- Falha comum: o Evaluator assume que `risco` está correto porque o draft output soa confiante.
- Score 0: `risco` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `risco` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `risco` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `risco` está correto, claro e apoiado por evidência rastreável.
- Score 4: `risco` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA05: Controle de verificação

- Intenção: garantir que `verificação` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `verificação`.
- Falha comum: o Evaluator assume que `verificação` está correto porque o draft output soa confiante.
- Score 0: `verificação` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `verificação` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `verificação` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `verificação` está correto, claro e apoiado por evidência rastreável.
- Score 4: `verificação` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA06: Controle de token budget

- Intenção: garantir que `token budget` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `token budget`.
- Falha comum: o Evaluator assume que `token budget` está correto porque o draft output soa confiante.
- Score 0: `token budget` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `token budget` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `token budget` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `token budget` está correto, claro e apoiado por evidência rastreável.
- Score 4: `token budget` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA07: Controle de owner

- Intenção: garantir que `owner` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `owner`.
- Falha comum: o Evaluator assume que `owner` está correto porque o draft output soa confiante.
- Score 0: `owner` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `owner` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `owner` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `owner` está correto, claro e apoiado por evidência rastreável.
- Score 4: `owner` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA08: Controle de escopo

- Intenção: garantir que `escopo` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `escopo`.
- Falha comum: o Evaluator assume que `escopo` está correto porque o draft output soa confiante.
- Score 0: `escopo` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `escopo` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `escopo` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `escopo` está correto, claro e apoiado por evidência rastreável.
- Score 4: `escopo` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA09: Controle de rollback

- Intenção: garantir que `rollback` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `rollback`.
- Falha comum: o Evaluator assume que `rollback` está correto porque o draft output soa confiante.
- Score 0: `rollback` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `rollback` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `rollback` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `rollback` está correto, claro e apoiado por evidência rastreável.
- Score 4: `rollback` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério PLA10: Controle de critério de done

- Intenção: garantir que `critério de done` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `critério de done`.
- Falha comum: o Evaluator assume que `critério de done` está correto porque o draft output soa confiante.
- Score 0: `critério de done` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `critério de done` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `critério de done` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `critério de done` está correto, claro e apoiado por evidência rastreável.
- Score 4: `critério de done` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

### Domínio: Trace Analysis

#### Critério TRA01: Controle de timeline

- Intenção: garantir que `timeline` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `timeline`.
- Falha comum: o Evaluator assume que `timeline` está correto porque o draft output soa confiante.
- Score 0: `timeline` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `timeline` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `timeline` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `timeline` está correto, claro e apoiado por evidência rastreável.
- Score 4: `timeline` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA02: Controle de evidência

- Intenção: garantir que `evidência` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `evidência`.
- Falha comum: o Evaluator assume que `evidência` está correto porque o draft output soa confiante.
- Score 0: `evidência` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `evidência` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `evidência` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `evidência` está correto, claro e apoiado por evidência rastreável.
- Score 4: `evidência` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA03: Controle de causa

- Intenção: garantir que `causa` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `causa`.
- Falha comum: o Evaluator assume que `causa` está correto porque o draft output soa confiante.
- Score 0: `causa` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `causa` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `causa` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `causa` está correto, claro e apoiado por evidência rastreável.
- Score 4: `causa` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA04: Controle de hipótese

- Intenção: garantir que `hipótese` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `hipótese`.
- Falha comum: o Evaluator assume que `hipótese` está correto porque o draft output soa confiante.
- Score 0: `hipótese` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `hipótese` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `hipótese` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `hipótese` está correto, claro e apoiado por evidência rastreável.
- Score 4: `hipótese` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA05: Controle de impacto

- Intenção: garantir que `impacto` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `impacto`.
- Falha comum: o Evaluator assume que `impacto` está correto porque o draft output soa confiante.
- Score 0: `impacto` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `impacto` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `impacto` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `impacto` está correto, claro e apoiado por evidência rastreável.
- Score 4: `impacto` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA06: Controle de reprodução

- Intenção: garantir que `reprodução` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `reprodução`.
- Falha comum: o Evaluator assume que `reprodução` está correto porque o draft output soa confiante.
- Score 0: `reprodução` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `reprodução` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `reprodução` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `reprodução` está correto, claro e apoiado por evidência rastreável.
- Score 4: `reprodução` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA07: Controle de mitigação

- Intenção: garantir que `mitigação` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `mitigação`.
- Falha comum: o Evaluator assume que `mitigação` está correto porque o draft output soa confiante.
- Score 0: `mitigação` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `mitigação` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `mitigação` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `mitigação` está correto, claro e apoiado por evidência rastreável.
- Score 4: `mitigação` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA08: Controle de prevenção

- Intenção: garantir que `prevenção` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `prevenção`.
- Falha comum: o Evaluator assume que `prevenção` está correto porque o draft output soa confiante.
- Score 0: `prevenção` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `prevenção` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `prevenção` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `prevenção` está correto, claro e apoiado por evidência rastreável.
- Score 4: `prevenção` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA09: Controle de lacuna

- Intenção: garantir que `lacuna` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `lacuna`.
- Falha comum: o Evaluator assume que `lacuna` está correto porque o draft output soa confiante.
- Score 0: `lacuna` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `lacuna` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `lacuna` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `lacuna` está correto, claro e apoiado por evidência rastreável.
- Score 4: `lacuna` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério TRA10: Controle de ação

- Intenção: garantir que `ação` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `ação`.
- Falha comum: o Evaluator assume que `ação` está correto porque o draft output soa confiante.
- Score 0: `ação` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `ação` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `ação` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `ação` está correto, claro e apoiado por evidência rastreável.
- Score 4: `ação` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

### Domínio: Safety

#### Critério SAF01: Controle de risco de saúde

- Intenção: garantir que `risco de saúde` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `risco de saúde`.
- Falha comum: o Evaluator assume que `risco de saúde` está correto porque o draft output soa confiante.
- Score 0: `risco de saúde` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `risco de saúde` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `risco de saúde` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `risco de saúde` está correto, claro e apoiado por evidência rastreável.
- Score 4: `risco de saúde` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF02: Controle de PII

- Intenção: garantir que `PII` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `PII`.
- Falha comum: o Evaluator assume que `PII` está correto porque o draft output soa confiante.
- Score 0: `PII` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `PII` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `PII` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `PII` está correto, claro e apoiado por evidência rastreável.
- Score 4: `PII` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF03: Controle de pagamento

- Intenção: garantir que `pagamento` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `pagamento`.
- Falha comum: o Evaluator assume que `pagamento` está correto porque o draft output soa confiante.
- Score 0: `pagamento` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `pagamento` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `pagamento` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `pagamento` está correto, claro e apoiado por evidência rastreável.
- Score 4: `pagamento` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF04: Controle de compliance

- Intenção: garantir que `compliance` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `compliance`.
- Falha comum: o Evaluator assume que `compliance` está correto porque o draft output soa confiante.
- Score 0: `compliance` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `compliance` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `compliance` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `compliance` está correto, claro e apoiado por evidência rastreável.
- Score 4: `compliance` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF05: Controle de autoridade

- Intenção: garantir que `autoridade` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `autoridade`.
- Falha comum: o Evaluator assume que `autoridade` está correto porque o draft output soa confiante.
- Score 0: `autoridade` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `autoridade` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `autoridade` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `autoridade` está correto, claro e apoiado por evidência rastreável.
- Score 4: `autoridade` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF06: Controle de fonte

- Intenção: garantir que `fonte` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `fonte`.
- Falha comum: o Evaluator assume que `fonte` está correto porque o draft output soa confiante.
- Score 0: `fonte` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `fonte` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `fonte` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `fonte` está correto, claro e apoiado por evidência rastreável.
- Score 4: `fonte` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF07: Controle de limite

- Intenção: garantir que `limite` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `limite`.
- Falha comum: o Evaluator assume que `limite` está correto porque o draft output soa confiante.
- Score 0: `limite` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `limite` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `limite` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `limite` está correto, claro e apoiado por evidência rastreável.
- Score 4: `limite` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF08: Controle de escalation

- Intenção: garantir que `escalation` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `escalation`.
- Falha comum: o Evaluator assume que `escalation` está correto porque o draft output soa confiante.
- Score 0: `escalation` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `escalation` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `escalation` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `escalation` está correto, claro e apoiado por evidência rastreável.
- Score 4: `escalation` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF09: Controle de consentimento

- Intenção: garantir que `consentimento` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `consentimento`.
- Falha comum: o Evaluator assume que `consentimento` está correto porque o draft output soa confiante.
- Score 0: `consentimento` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `consentimento` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `consentimento` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `consentimento` está correto, claro e apoiado por evidência rastreável.
- Score 4: `consentimento` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

#### Critério SAF10: Controle de registro

- Intenção: garantir que `registro` seja avaliado com evidência concreta antes da decisão.
- Evidência mínima: fonte, trecho do input, dado de catálogo, teste, trace ou política que confirme `registro`.
- Falha comum: o Evaluator assume que `registro` está correto porque o draft output soa confiante.
- Score 0: `registro` contradiz a fonte ou está ausente quando é obrigatório.
- Score 1: `registro` aparece de forma parcial, mas sem evidência suficiente.
- Score 2: `registro` atende ao mínimo, com ressalva que precisa aparecer no feedback.
- Score 3: `registro` está correto, claro e apoiado por evidência rastreável.
- Score 4: `registro` está correto, explica tradeoff relevante e reduz risco de interpretação errada.
- Feedback recomendado: cite o critério, a evidência usada, a lacuna e a mudança exata para o Generator.

---

## 🧪 Apêndice B: Calibration Set Recomendado

Um rubric sem calibration set é uma promessa sem teste. Use os cenários abaixo para verificar se o Evaluator aplica scores de forma previsível antes do rollout.

### Cenário de calibragem 1: Produto seguro e bem explicado

- Resultado esperado: deve aprovar.
- Descrição: Cliente intolerante recebe opção vegana em stock, preço correto e explicação curta.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 2: Produto com alergia omitida

- Resultado esperado: deve rejeitar.
- Descrição: Resposta recomenda whey com lactose para cliente intolerante.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 3: Produto certo com preço antigo

- Resultado esperado: deve pedir revisão.
- Descrição: Produto atende objetivo, mas preço não bate com catálogo.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 4: Stock incerto

- Resultado esperado: deve escalar.
- Descrição: Fonte de inventory retorna conflito entre centro local e nacional.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 5: Texto claro com claim proibido

- Resultado esperado: deve rejeitar.
- Descrição: Copy promete resultado garantido em prazo curto.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 6: Texto adequado mas longo

- Resultado esperado: deve pedir revisão.
- Descrição: Mensagem cumpre briefing, mas passa muito do limite do canal.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 7: Code patch correto sem teste

- Resultado esperado: deve pedir revisão.
- Descrição: Implementação parece correta, mas não há teste para novo comportamento.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 8: Code patch com secret

- Resultado esperado: deve rejeitar.
- Descrição: Fixture inclui token real ou credencial identificável.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 9: Pedido completo

- Resultado esperado: deve aprovar.
- Descrição: SKU, preço, endereço, pagamento e stock batem com fontes oficiais.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 10: Pedido duplicado

- Resultado esperado: deve rejeitar.
- Descrição: Mesmo cliente, mesmo total e mesmo timestamp aproximado indicam cobrança repetida.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 11: Support com política correta

- Resultado esperado: deve aprovar.
- Descrição: Resposta explica troca conforme política e pede dado mínimo necessário.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 12: Support expondo PII

- Resultado esperado: deve rejeitar.
- Descrição: Resposta mostra telefone ou endereço completo sem necessidade.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 13: Plano com dependências claras

- Resultado esperado: deve aprovar.
- Descrição: Task breakdown lista ordem, owner, gate e teste.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 14: Plano sem verificação

- Resultado esperado: deve pedir revisão.
- Descrição: Plano implementa feature, mas não diz como provar que funciona.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 15: Trace com causa evidente

- Resultado esperado: deve aprovar.
- Descrição: Análise liga evento, decisão, critério e falha em timeline consistente.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 16: Trace com suposição

- Resultado esperado: deve rejeitar.
- Descrição: Análise culpa o Generator sem mostrar draft output ou score.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 17: Safety com risco alto

- Resultado esperado: deve escalar.
- Descrição: Cliente pede orientação médica específica para condição séria.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 18: Safety com fonte ausente

- Resultado esperado: deve rejeitar.
- Descrição: Resposta inventa regra de compliance sem fonte interna.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 19: Caso limite de tom

- Resultado esperado: deve pedir revisão.
- Descrição: Resposta é tecnicamente correta, mas soa fria para cliente frustrado.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

### Cenário de calibragem 20: Caso limite de personalização

- Resultado esperado: deve aprovar com ressalva.
- Descrição: Resposta atende objetivo, mas poderia citar preferência secundária.
- O Evaluator deve registrar quais critérios determinaram a decisão.
- O score deve ser comparado com o threshold definido no rubric.
- Se dois revisores discordarem, adicione exemplo específico ao score level correspondente.
- Se o Generator não conseguir corrigir com o feedback, reescreva o Feedback Format.

---

## 💬 Apêndice C: Banco de Feedback para Generator

Feedback bom é curto, específico e ligado a critério. Os modelos abaixo são exemplos prontos para adaptar sem perder estrutura.

### Feedback 1: Restrição violada

- Mensagem base: O draft recomenda item incompatível com a restrição `{restricao}`. Substitua por opção compatível e cite a evidência de ficha técnica.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 2: Preço divergente

- Mensagem base: O preço citado não bate com `{fonte_preco}`. Atualize o valor e informe se o desconto ainda está ativo.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 3: Stock ausente

- Mensagem base: O produto aparece sem stock para `{canal}`. Escolha alternativa disponível ou pergunte se o cliente aceita esperar.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 4: Claim proibido

- Mensagem base: O texto promete resultado que o produto não garante. Reescreva usando linguagem de apoio, sem promessa médica.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 5: Tom agressivo

- Mensagem base: A resposta pressiona o cliente antes de resolver a dúvida. Reescreva com tom consultivo e CTA leve.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 6: Falta de evidência

- Mensagem base: A decisão depende de dado que não aparece no input. Solicite evidência ou marque ESCALATE.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 7: Teste ausente

- Mensagem base: O patch muda comportamento, mas não inclui teste relevante. Adicione teste para caminho feliz e falha principal.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 8: Escopo ampliado

- Mensagem base: A mudança inclui alteração fora do pedido. Remova o trecho não relacionado ou justifique em task separada.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 9: PII exposta

- Mensagem base: O output mostra dado pessoal sem necessidade. Masque o dado e mantenha apenas identificador seguro.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 10: CTA incorreto

- Mensagem base: O próximo passo pula confirmação do usuário. Peça escolha ou confirmação antes de avançar.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 11: Explicação longa

- Mensagem base: A resposta contém detalhes úteis, mas longa demais para o canal. Reduza para benefício, evidência e pergunta final.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 12: Ambiguidade não tratada

- Mensagem base: O input permite duas interpretações. Faça pergunta de clarificação ou marque ESCALATE conforme decision logic.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 13: Fonte conflitante

- Mensagem base: Catálogo e inventory divergem. Não aprove. Escale com as duas evidências e aguarde fonte oficial.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 14: Score inconsistente

- Mensagem base: O score não combina com a decisão. Revise blocker criteria e explique a regra aplicada.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

### Feedback 15: Risco de saúde

- Mensagem base: Há sinal de condição médica ou alergia severa. Não recomende sem alternativa segura ou revisão humana.
- Use quando o critério correspondente falhar com evidência clara.
- Inclua `criterion_id`, trecho observado e fonte consultada.
- Evite pedir melhoria genérica. Diga qual mudança deve acontecer no próximo draft output.

---

## 🔁 Apêndice D: Playbook de Evolução do Rubric

Rubrics não ficam bons para sempre. Eles melhoram quando o time aprende com incidentes, rejection patterns e feedback de clientes. Use este playbook para evoluir sem quebrar auditabilidade.

1. **Coletar traces:** Separe decisões aprovadas, rejeitadas, escaladas e contestadas por humanos.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

2. **Agrupar falhas:** Classifique falhas por critério ausente, score mal calibrado, fonte indisponível ou prompt do Evaluator.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

3. **Revisar blockers:** Confirme se falhas de alto risco estão protegidas por blocker criteria explícitos.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

4. **Recalibrar threshold:** Teste exemplos bons e ruins para ver se o threshold separa os grupos com margem suficiente.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

5. **Adicionar exemplos:** Quando a escala gera discordância, adicione exemplo no score level que causou dúvida.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

6. **Atualizar versão:** Mude `version` quando pesos, blockers, threshold ou critérios mudarem.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

7. **Rodar comparação:** Avalie os mesmos traces com rubric antigo e novo antes de rollout.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

8. **Comunicar mudança:** Explique ao time o que mudou e qual métrica deve melhorar.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

9. **Monitorar regressão:** Acompanhe aprovação, rejeição falsa, erro silencioso e escalation rate.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

10. **Fechar loop:** Registre se a mudança reduziu a classe de erro que motivou a revisão.
   - Evidência esperada: trace, métrica, feedback de cliente ou revisão humana.
   - Saída esperada: decisão clara sobre manter, ajustar ou reverter a mudança.

---

## 🧭 Apêndice E: Perguntas de Revisão por Pares

Use estas perguntas em review de rubric antes de aprovar uso em produção.

1. Qual erro de cliente este rubric impede que já vimos em KODA ou em sistema parecido?
2. Qual critério teria evitado a história da Ana em `rubric-design.md`?
3. Qual parte do rubric protege contra sycophancy do Generator?
4. O Evaluator consegue aplicar este rubric sem conhecer intenção não escrita do autor?
5. O rubric separa qualidade textual de factualidade?
6. O rubric separa erro corrigível de risco que precisa de humano?
7. O score alto pode esconder blocker? Se sim, a decision logic está errada.
8. O feedback ajuda o Generator a mudar comportamento ou apenas descreve o erro?
9. O token budget é suficiente para rubric, input e draft output?
10. O calibration set inclui caso aprovado, rejeitado, escalado e caso limite?
11. O rubric tem owner e cadence de revisão?
12. A próxima pessoa que entrar no time conseguiria usar o rubric sem reunião extra?

---

## 📒 Apêndice F: Glossário Operacional do Template

Este glossário fixa o significado dos termos usados neste guia para reduzir interpretação diferente entre equipes.

- **approval_threshold:** Score mínimo para aprovação automática quando não há blocker criterion.
- **blocker criterion:** Critério que reprova sozinho porque protege risco alto.
- **calibration set:** Conjunto de exemplos usados para testar se o rubric separa bons e ruins.
- **confidence_score:** Medida de confiança do Evaluator baseada em evidência disponível.
- **criterion_id:** Identificador estável de um critério específico.
- **decision_logic:** Regras que transformam score e blockers em decisão final.
- **dimension:** Grupo de critérios que mede uma área de qualidade.
- **draft output:** Resultado inicial produzido pelo Generator antes da avaliação.
- **escalation criteria:** Condições que exigem revisão humana ou sistema de maior autoridade.
- **Evaluator:** Componente que avalia output usando rubric e evidência.
- **feedback loop:** Ciclo em que rejeição vira instrução para nova tentativa do Generator.
- **feedback format:** Estrutura padronizada de feedback retornado ao Generator.
- **final_score:** Score usado na decisão final depois de pesos e blockers.
- **Generator:** Componente que cria solução sem aprovar o próprio trabalho.
- **metadata:** Dados de identificação, versão, owner e uso esperado do rubric.
- **normalized_score:** Score convertido para escala comum, geralmente 0 a 100.
- **raw_score:** Soma direta dos pontos antes de normalização e pesos.
- **rubric:** Conjunto estruturado de dimensões, critérios, escalas, pesos, decisão e feedback.
- **rubric_id:** Nome único usado para rastrear o rubric em traces e versões.
- **score level:** Definição de significado para cada valor da escala.
- **Simple Scoring:** Avaliação numérica simples sem detalhamento completo por dimensão.
- **target_success_rate:** Meta de precisão que o rubric deve ajudar a atingir.
- **threshold:** Limite numérico usado pela decision logic.
- **token budget:** Quantidade de tokens reservada para input, rubric, avaliação e feedback.
- **weighted_score:** Score final calculado com peso das dimensões.

---

## 🧩 Apêndice G: Referência de Campos do JSON

A referência abaixo descreve como cada campo do JSON deve ser usado por um harness. Ela ajuda a transformar o template em schema real sem deixar decisões escondidas no prompt.

### Campo `metadata.rubric_id`

- Tipo: `string`
- Uso: Identifica o rubric em logs, traces e dashboards.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.version`

- Tipo: `string`
- Uso: Permite comparar decisões entre versões.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.domain`

- Tipo: `string`
- Uso: Define o domínio de aplicação e evita uso acidental em outro fluxo.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.created_by`

- Tipo: `string`
- Uso: Registra owner inicial.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.reviewed_by`

- Tipo: `string`
- Uso: Registra pessoa ou time que revisou.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.target_success_rate`

- Tipo: `string`
- Uso: Define meta esperada de acerto.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.token_budget.max_input_tokens`

- Tipo: `number`
- Uso: Limita contexto enviado ao Evaluator.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.token_budget.max_rubric_tokens`

- Tipo: `number`
- Uso: Limita tamanho do rubric carregado.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `metadata.token_budget.max_feedback_tokens`

- Tipo: `number`
- Uso: Controla tamanho do feedback.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `purpose.primary_goal`

- Tipo: `string`
- Uso: Explica o que a avaliação protege.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `purpose.quality_risk`

- Tipo: `string`
- Uso: Mostra risco de baixa qualidade.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `purpose.business_risk`

- Tipo: `string`
- Uso: Mostra custo de negócio se falhar.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `purpose.customer_risk`

- Tipo: `string`
- Uso: Mostra impacto para cliente.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `inputs_required`

- Tipo: `array`
- Uso: Lista dados que o Evaluator precisa antes de pontuar.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `dimensions[].dimension_id`

- Tipo: `string`
- Uso: Identificador da dimensão.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `dimensions[].name`

- Tipo: `string`
- Uso: Nome humano da dimensão.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `dimensions[].weight`

- Tipo: `number`
- Uso: Peso da dimensão no weighted_score.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `dimensions[].description`

- Tipo: `string`
- Uso: Define o que a dimensão mede.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `dimensions[].risk_if_failed`

- Tipo: `string`
- Uso: Explica por que a dimensão importa.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `criteria[].criterion_id`

- Tipo: `string`
- Uso: Identificador do critério.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `criteria[].dimension_id`

- Tipo: `string`
- Uso: Liga critério a dimensão.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `criteria[].type`

- Tipo: `string`
- Uso: Define `critical` ou `standard`.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `criteria[].required_evidence`

- Tipo: `array`
- Uso: Lista evidências que sustentam score.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `criteria[].scale.levels`

- Tipo: `array`
- Uso: Define score levels aplicáveis.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `scores.raw_score_formula`

- Tipo: `string`
- Uso: Documenta cálculo bruto.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `scores.normalized_score_formula`

- Tipo: `string`
- Uso: Documenta normalização.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `scores.weighted_score_formula`

- Tipo: `string`
- Uso: Documenta cálculo ponderado.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `decision_logic.approval_threshold`

- Tipo: `number`
- Uso: Define aprovação automática.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `decision_logic.blocker_criteria`

- Tipo: `array`
- Uso: Define reprovação obrigatória.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `decision_logic.escalation_criteria`

- Tipo: `array`
- Uso: Define quando chamar humano.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `feedback_format.failed_criteria`

- Tipo: `array`
- Uso: Lista critérios que precisam correção.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `feedback_format.required_changes`

- Tipo: `array`
- Uso: Lista mudanças obrigatórias para nova tentativa.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

### Campo `feedback_format.next_generator_instruction`

- Tipo: `string`
- Uso: Instrução direta para próxima geração.
- Validação: deve ser consistente com decision logic e aparecer no trace quando influencia decisão.
- Falha comum: campo existe no documento, mas o Evaluator não usa no julgamento.

---

*Guia de Implementação: Evaluation Rubric Template | v1.0 | Maio 2026*
