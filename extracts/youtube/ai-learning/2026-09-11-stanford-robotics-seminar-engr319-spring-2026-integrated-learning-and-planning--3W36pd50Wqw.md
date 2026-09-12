---
title: "Stanford Robotics Seminar ENGR319 | Spring 2026 | Integrated Learning and Planning"
type: "extract"
source: "youtube"
video_id: "3W36pd50Wqw"
url: "https://www.youtube.com/watch?v=3W36pd50Wqw"
channel: "Stanford Online"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-robotics-seminar-engr319-spring-2026-integrated-learning-and-planning--3W36pd50Wqw.txt]]"
tags: ["agents", "arquitetura", "frameworks", "harness", "model-selection", "multi-agent", "ontologia", "process", "roadmap", "runtime", "state"]
thesis: "Combinar aprendizado de máquina (representações neurais, diffusion models, LLMs/VLMs) com planejamento baseado em modelos via otimização restrita e conceitos neuro-simbólicos permite que robôs aprendam habilidades de 1-10 demonstrações e generalizem de forma confiável para novos objetos, estados e objetivos, em contraste com a baixa eficiência de dados da abordagem pura de ajuste a dados."
concepts: ["Inteligência física de propósito geral", "Aprendizado por ajuste a dados (data fitting) vs. planejamento com modelo de mundo", "Conceitos neuro-simbólicos: abstração composicional de estados e ações", "Geração de ações como otimização restrita (constraints de caminho, subobjetivos, dinâmica)", "Composicionabilidade de habilidades (policies não podem ser costuradas diretamente)", "Aprendizado one-shot de habilidades com correspondência visual guiada", "Verificação de propostas neurais via planejamento baseado em modelo (análise de estabilidade, simulador físico)", "Diffusion models composicionais com campos de energia/gradientes por relação espacial", "Amostragem por dinâmica de Langevin não ajustada (unbiased)", "Raciocínio espacial com grafos de relações abstratas gerados por VLM", "Esqueleto de tarefa (task skeleton) vs. viabilidade física", "Modelo de transição para simulação interna antes da execução", "Planejamento de longo horizonte (ordem deliberada de ações, evitar colisões)", "Execução assíncrona e tipagem explícita de tempo (time-explicit typing)", "Orquestrador de modelos compondo modelos-fundação com raciocínio probabilístico", "Aprendizado contínuo e modelos autoditados por exploração (self-improving loop)", "Distilação mútua entre modelos-fundação (ex.: VLM + segmentação)"]
tools: ["DINOv2", "Physical Intelligence (exemplo de empresa)", "Gemini (video language model)", "Segment Anything (SAM)", "Retriever (framework open-source para agentes robóticos em loop fechado)", "Simuladores físicos", "Planejadores de movimento (motion planners)"]
people: ["Jiayuan (palestrante)", "Amazon FAR", "UPenn", "Physical Intelligence (empresa)"]
claims: ["Modele geração de ações como otimização restrita em vez de policy única, para que restrições se componham temporal e espacialmente (pick + place vira soma de constraints) e habilidades possam ser combinadas", "Use features visuais pré-treinadas (DINOv2) apenas como guia ruidoso de correspondência funcional e valide propostas com planejamento baseado em modelo (3D, simulador, análise de estabilidade) — obtém >90% de sucesso one-shot em formas alfabéticas não vistas onde policy pura marca ~0", "Treine um diffusion model dedicado por tipo de relação (left-of, near-edge etc.) prevendo gradientes de energia, e componha-os somando gradientes na inferência via Langevin não ajustada, sem retreino para novos conjuntos de relações", "Deixe LLMs/VLMs fornecerem conhecimento de senso comum em nível simbólico (grafo de relações espaciais, esqueleto de tarefa, segmentação de trajetória) em vez de aprender esse conhecimento com demonstrações robóticas", "Separe responsabilidades na arquitetura: VLM cuida de semântica/meta da tarefa; modelos de transição e trajetória aprendidos cuidam de viabilidade física (colisão, estabilidade)", "Adote execução assíncrona com anotação explícita da frequência de controle de cada módulo (ex.: planejador a 0.5 Hz, rastreamento de memória a 1 Hz) para viabilizar loop fechado com atualização de plano a partir de novas observações", "Fatore preferências do usuário como funções de utilidade/restrições adicionais no problema de planejamento, aproveitando a composicionalidade do sistema na inferência", "Use raciocínio/exploração para gerar nova experiência no mundo como dados de treinamento da próxima geração de modelos-fundação, fechando o loop de auto-melhoria", "Prefira composição principiada de modelos-fundação via algoritmos probabilísticos/planejamento a cadeias simples de pensamento quando escalar múltiplos modelos especializados"]
deep_dive: "medium"
deep_dive_reason: "Alta densidade técnica e novidade em planejamento neuro-simbólico e arquitetura composicional (inclusive framework runtime assíncrono e orquestração de modelos análoga a agent harness), porém o domínio central é manipulação robótica, com relevância apenas parcial aos eixos de harness/context-engineering/evals de agentes de IA."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs25-transformers-united-v6-i-from-language-models-to-native-multimodal--NDdc39KYqDU|Stanford CS25: Transformers United V6 I From Language Models to Native Multimodal Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-webinar-large-language-models-get-the-hype-but-compound-systems-are-the--vRTcE19M-KE|Stanford Webinar - Large Language Models Get the Hype, but Compound Systems Are the Future of AI]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-s-1b-bet-against-llms-part-1--kYkIdXwW2AE|Yann LeCun's $1B Bet Against LLMs [Part 1]]]"]
theme: "Fundamentos e Arquitetura de LLMs"
---

# Stanford Robotics Seminar ENGR319 | Spring 2026 | Integrated Learning and Planning

## Tese
Combinar aprendizado de máquina (representações neurais, diffusion models, LLMs/VLMs) com planejamento baseado em modelos via otimização restrita e conceitos neuro-simbólicos permite que robôs aprendam habilidades de 1-10 demonstrações e generalizem de forma confiável para novos objetos, estados e objetivos, em contraste com a baixa eficiência de dados da abordagem pura de ajuste a dados.

## Conceitos-chave
- Inteligência física de propósito geral
- Aprendizado por ajuste a dados (data fitting) vs. planejamento com modelo de mundo
- Conceitos neuro-simbólicos: abstração composicional de estados e ações
- Geração de ações como otimização restrita (constraints de caminho, subobjetivos, dinâmica)
- Composicionabilidade de habilidades (policies não podem ser costuradas diretamente)
- Aprendizado one-shot de habilidades com correspondência visual guiada
- Verificação de propostas neurais via planejamento baseado em modelo (análise de estabilidade, simulador físico)
- Diffusion models composicionais com campos de energia/gradientes por relação espacial
- Amostragem por dinâmica de Langevin não ajustada (unbiased)
- Raciocínio espacial com grafos de relações abstratas gerados por VLM
- Esqueleto de tarefa (task skeleton) vs. viabilidade física
- Modelo de transição para simulação interna antes da execução
- Planejamento de longo horizonte (ordem deliberada de ações, evitar colisões)
- Execução assíncrona e tipagem explícita de tempo (time-explicit typing)
- Orquestrador de modelos compondo modelos-fundação com raciocínio probabilístico
- Aprendizado contínuo e modelos autoditados por exploração (self-improving loop)
- Distilação mútua entre modelos-fundação (ex.: VLM + segmentação)

## Ferramentas & pessoas
**Ferramentas:** DINOv2, Physical Intelligence (exemplo de empresa), Gemini (video language model), Segment Anything (SAM), Retriever (framework open-source para agentes robóticos em loop fechado), Simuladores físicos, Planejadores de movimento (motion planners)

**Pessoas/orgs:** Jiayuan (palestrante), Amazon FAR, UPenn, Physical Intelligence (empresa)

## Claims acionáveis
- Modele geração de ações como otimização restrita em vez de policy única, para que restrições se componham temporal e espacialmente (pick + place vira soma de constraints) e habilidades possam ser combinadas
- Use features visuais pré-treinadas (DINOv2) apenas como guia ruidoso de correspondência funcional e valide propostas com planejamento baseado em modelo (3D, simulador, análise de estabilidade) — obtém >90% de sucesso one-shot em formas alfabéticas não vistas onde policy pura marca ~0
- Treine um diffusion model dedicado por tipo de relação (left-of, near-edge etc.) prevendo gradientes de energia, e componha-os somando gradientes na inferência via Langevin não ajustada, sem retreino para novos conjuntos de relações
- Deixe LLMs/VLMs fornecerem conhecimento de senso comum em nível simbólico (grafo de relações espaciais, esqueleto de tarefa, segmentação de trajetória) em vez de aprender esse conhecimento com demonstrações robóticas
- Separe responsabilidades na arquitetura: VLM cuida de semântica/meta da tarefa; modelos de transição e trajetória aprendidos cuidam de viabilidade física (colisão, estabilidade)
- Adote execução assíncrona com anotação explícita da frequência de controle de cada módulo (ex.: planejador a 0.5 Hz, rastreamento de memória a 1 Hz) para viabilizar loop fechado com atualização de plano a partir de novas observações
- Fatore preferências do usuário como funções de utilidade/restrições adicionais no problema de planejamento, aproveitando a composicionalidade do sistema na inferência
- Use raciocínio/exploração para gerar nova experiência no mundo como dados de treinamento da próxima geração de modelos-fundação, fechando o loop de auto-melhoria
- Prefira composição principiada de modelos-fundação via algoritmos probabilísticos/planejamento a cadeias simples de pensamento quando escalar múltiplos modelos especializados

> **Deep dive:** `medium` — Alta densidade técnica e novidade em planejamento neuro-simbólico e arquitetura composicional (inclusive framework runtime assíncrono e orquestração de modelos análoga a agent harness), porém o domínio central é manipulação robótica, com relevância apenas parcial aos eixos de harness/context-engineering/evals de agentes de IA.
