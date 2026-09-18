---
title: "GlucoFM: foundation model para CGM"
type: "extract"
source: "x"
status_id: "2094501145536315670"
handle: "fazle_karim1"
url: "https://x.com/fazle_karim1/status/2094501145536315670"
created_at: "2026-08-31T19:02:41.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-fazle_karim1-googleresearch-i-wonder-how-it-would-do-on-this-research-of--2094501145536315670.json]]"
tags: ["analise", "arquitetura", "monitoramento", "performance"]
topic: "GlucoFM: foundation model para CGM"
summary: "Google Research anuncia o GlucoFM, modelo fundacional auto-supervisionado para monitores contínuos de glicose (CGM) com design dual-stream que separa tendências glicêmicas lentas de desvios de curto prazo. Supera o melhor GluFormer em +5,8 pp de PR-AUC médio e mostra forte transferência entre coortes e adaptação few-shot com dados clínicos rotulados escassos."
key_points: ["Arquitetura dual-stream separa componente de baixa frequência (tendências lentas/estado) de componente residual (eventos de curto prazo: refeições, atividade, artefatos), preservando hora do dia e máscara de missingness; ablação mostra que o dual-stream completo supera versões raw-input, state-only e event-only.", "Pré-treinamento auto-supervisionado em 109.066 horas de CGM sem rótulos (Wear-CGM), com objetivos de predição latente (masked contextual prediction + previsão da evolução temporal hora a hora) e augmentations realistas de CGM (baseline drift, quedas tipo compressão, amostragem esparsa, desconexões).", "Resultados: PR-AUC médio de 58,8 vs 54,7 do melhor baseline CGM-específico (ganho absoluto de 4,1 pp em 14 avaliações coorte-tarefa); menor MAE na previsão de resposta glicêmica pós-prandial (21,88 vs 22,90 mg/dL) com Dexcom e Libre modelados separadamente.", "Representações congeladas de janelas de 24h podem ser médias em até 7 dias sem retraining do encoder (ganhos de até 14,0 pp em diabetes no coorte Hall); transferência cross-dataset venceu 11 de 12 avaliações (0,5–8,6 pp) e few-shot é superior em todos os orçamentos de dados, inclusive 1 exemplo por classe ou 1% das observações.", "Sete tarefas clínicas avaliadas (risco de diabetes, resistência à insulina, disfunção de células beta, hiperlipidemia, hipoglicemia, obesidade, glucotype) em quatro coortes (CGMacros, Stanford, Hall, ShanghaiT2DM) via linear probing com folds disjuntos por participante."]
entities: ["Google Research", "GlucoFM", "GluFormer", "CGMformer", "CGM-JEPA", "Wear-CGM", "Dexcom", "Libre", "CGMacros", "ShanghaiT2DM", "Ahmed A. Metwally", "Zechen Li"]
content_type: "announcement"
revisit: "medium"
grounded_in: "article"
links: ["https://research.google/blog/glucofm-foundation-model-for-continuous-glucose-monitoring/?utm_source=twitter&utm_medium=social&utm_campaign=social_post&utm_content=gr-acct"]
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-timesfm-3-a-state-of-the-art-time-series-foundat--2094483372718580066|TimesFM-3: forecasting multivariado]]", "[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-12-doctorinigo-very-excited-to-share-these-results-from-our-work-with-bioli--2096296686750666868|Biossensor contínuo de lactato]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371|Modelos estruturados para automação]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-toolgrad-an-efficient-framework-for-generating-t--2098183830968705163|ToolGrad: geração de datasets de tool-use]]", "[[extracts/x/bookmarks/2026-09-16-googleresearch-introducing-retrieve-for-train-a-framework-that-accelerates--2099951761985601580|Retrieve-for-Train: difusão para retrieval]]", "[[extracts/x/bookmarks/2026-09-12-sitkosebastian-you-don-t-need-a-power-meter-to-know-how-many-watts-a-rider--2089763604371218674|estimativa de watts sem medidor]]"]
theme: "Confiabilidade e avaliação de agentes"
---

# GlucoFM: foundation model para CGM

**@fazle_karim1** · [2094501145536315670](https://x.com/fazle_karim1/status/2094501145536315670) · `announcement`

## Resumo
Google Research anuncia o GlucoFM, modelo fundacional auto-supervisionado para monitores contínuos de glicose (CGM) com design dual-stream que separa tendências glicêmicas lentas de desvios de curto prazo. Supera o melhor GluFormer em +5,8 pp de PR-AUC médio e mostra forte transferência entre coortes e adaptação few-shot com dados clínicos rotulados escassos.

## Pontos-chave
- Arquitetura dual-stream separa componente de baixa frequência (tendências lentas/estado) de componente residual (eventos de curto prazo: refeições, atividade, artefatos), preservando hora do dia e máscara de missingness; ablação mostra que o dual-stream completo supera versões raw-input, state-only e event-only.
- Pré-treinamento auto-supervisionado em 109.066 horas de CGM sem rótulos (Wear-CGM), com objetivos de predição latente (masked contextual prediction + previsão da evolução temporal hora a hora) e augmentations realistas de CGM (baseline drift, quedas tipo compressão, amostragem esparsa, desconexões).
- Resultados: PR-AUC médio de 58,8 vs 54,7 do melhor baseline CGM-específico (ganho absoluto de 4,1 pp em 14 avaliações coorte-tarefa); menor MAE na previsão de resposta glicêmica pós-prandial (21,88 vs 22,90 mg/dL) com Dexcom e Libre modelados separadamente.
- Representações congeladas de janelas de 24h podem ser médias em até 7 dias sem retraining do encoder (ganhos de até 14,0 pp em diabetes no coorte Hall); transferência cross-dataset venceu 11 de 12 avaliações (0,5–8,6 pp) e few-shot é superior em todos os orçamentos de dados, inclusive 1 exemplo por classe ou 1% das observações.
- Sete tarefas clínicas avaliadas (risco de diabetes, resistência à insulina, disfunção de células beta, hiperlipidemia, hipoglicemia, obesidade, glucotype) em quatro coortes (CGMacros, Stanford, Hall, ShanghaiT2DM) via linear probing com folds disjuntos por participante.

## Links
- https://research.google/blog/glucofm-foundation-model-for-continuous-glucose-monitoring/?utm_source=twitter&utm_medium=social&utm_campaign=social_post&utm_content=gr-acct

## Entidades
Google Research, GlucoFM, GluFormer, CGMformer, CGM-JEPA, Wear-CGM, Dexcom, Libre, CGMacros, ShanghaiT2DM, Ahmed A. Metwally, Zechen Li

> **Revisit:** `medium` · **fonte:** `article`
