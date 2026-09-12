---
title: "Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 13: Data (Sources, Datasets)"
type: "extract"
source: "youtube"
video_id: "-qm0ln33G24"
url: "https://www.youtube.com/watch?v=-qm0ln33G24"
channel: "Stanford Online"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-13-data-source---qm0ln33G24.txt]]"
tags: ["analise", "data-platform", "governanca", "permissions", "process", "stack-tooling", "classification", "curriculo-conteudo", "instituicoes"]
thesis: "Os dados são o componente mais crítico e mais deliberadamente secreto do treinamento de modelos de linguagem, e sua obtenção é moldada por restrições técnicas (crawling, robots.txt, autenticação) e legais (copyright, fair use, licenciamento) que se estreitaram drasticamente desde 2023."
concepts: ["estágios do pipeline: pre-training, mid-training e post-training", "crawling da web, deep web e walled gardens", "robots.txt, termos de serviço e bloqueio de bots", "Copyright Act de 1976, domínio público e duração de 75 anos", "fair use e seus quatro fatores", "licenças (Creative Commons, MIT/Apache) vs. licenciamento pago", "shadow libraries (LibGen, Anna's Archive)", "quality filtering baseado em regras vs. baseado em classificador", "deduplicação e identificação de idioma", "extração HTML-para-texto (WARC vs. WET)", "curadoria e limpeza de dados como gargalo de longa cauda", "memorização verbatim vs. violação semântica de copyright", "envenenamento de dumps periódicos (ataque de janela temporal)", "contaminação legal de datasets (Books3/Bibliotik) e efeito watershed", "dados sintéticos e restrições de uso"]
tools: ["Common Crawl", "Wikipedia", "GitHub", "GitHub Archive", "Software Heritage", "arXiv", "Cloudflare", "trafilatura", "resiliparse", "WARC/WET", "Llama 3", "OLMo", "Qwen3.5-397B-A17B", "BERT", "GPT-2 / WebText", "CCNet", "C4 / T5", "GPT-3", "The Pile", "Books3", "Bibliotik", "Project Gutenberg / PG-19", "Smashwords / BooksCorpus", "Stack Exchange", "Enron Emails", "Gopher / MassiveWeb", "Chinchilla", "Llama 1", "RedPajama V1", "RefinedWeb", "FineWeb", "Dolma", "The Stack", "PushShift", "Semantic Scholar", "DCLM / DataComp", "Google Books", "ChatGPT", "Claude"]
people: ["Meta", "OpenAI", "Anthropic", "AI2", "New York Times", "Authors Guild", "Google", "DeepMind", "EleutherAI", "Hugging Face", "Together", "Shane Longpre", "Nicholas Carlini", "Cloudflare", "X AI", "Reddit", "Software Heritage Foundation", "Creative Commons"]
claims: ["Dados são a vantagem competitiva e o principal risco legal: o paper do Llama 3 revela arquitetura e procedimentos de treino, mas nada sobre os dados", "O pipeline segue pre-training (web bruta) → mid-training (alta qualidade, contexto longo) → post-training (chat, RL, safety), com tendência de grandes volumes de baixa qualidade para menores volumes de alta qualidade", "'Treinado na internet' não é preciso: conteúdo dinâmico, deep web, autenticação, robots.txt, CAPTCHAs do Cloudflare, bloqueios de IP e ToS restringem o que é acessível", "Consent in Crisis (Longpre) mostra que restrições no robots.txt saltaram para ~50% dos sites após meados de 2023 e a maioria dos ToS agora proíbe uso para IA — o web legalmente crawlável encolheu muito", "Fair use tem quatro fatores (propósito transformador, natureza factual, quantidade usada, efeito de mercado); o caso Anthropic decretou treinamento como fair use, mas a pirataria em si é ilegal — acordo de US$ 1,5 bi (~US$ 3.000/livro) mesmo com compra e digitalização legais dos livros", "Copyright cobre expressão e semântica (personagens, enredos, efeitos econômicos), não ideias nem N-gram overlap; memorização verbatim é apenas uma das formas de violação", "Prefira dumps oficiais a crawling: Wikipedia, repositórios Git do GitHub, arXiv (bulk) e Stack Exchange publicam dumps — crawling gera carga nos servidores e viola a cidadania digital esperada", "A ferramenta de extração HTML→texto importa: ablação do DataComp LLM mostra que trafilatura e resiliparse superam os WET do Common Crawl", "Wikipedia é envenenável: editar logo antes do dump periódico (Carlini) insere conteúdo malicioso no dataset mesmo com rollback posterior — até fontes de alta qualidade podem conter ataques", "Evolução dos métodos de filtragem: WebText (links do Reddit com >3 karma, 40GB) → CCNet (LM treinado em Wikipedia) → C4 (regras manuais, 156B tokens) → GPT-3 (classificador de qualidade) → RefinedWeb/FineWeb (apenas web, 5T–15T tokens) → DCLM normaliza filtragem baseada em modelo", "Tensão de design recorrente entre filtragem por regras (controle, menos viés) e por classificador (qualidade, escala); RefinedWeb e Dolma evitaram explicitamente filtragem baseada em ML para não enviesar o subset da web", "Books3 (200k livros da shadow library Bibliotik) contaminou The Pile e Llama 1; decisões precoces de copyright têm efeito watershed e datasets posteriores removeram Books3", "Escala do Common Crawl: ~3–5 bilhões de páginas por crawl mensal, ~300 bilhões acumuladas, cada dump com ~2B páginas (~372TB de texto); índice do Google ≥100 petabytes", "A fronteira do 'base model' está desaparecendo (Qwen3.5 não expõe checkpoints intermediários); OLMo da AI2 é a referência aberta para estudar todo o pipeline de dados"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de decisões acionáveis de pipeline de dados (filtragem, dedup, extração, dumps vs. crawl, linhagem de datasets) combinada com desenvolvimentos jurídicos recentes (fair use, acordo de US$ 1,5 bi da Anthropic) diretamente relevantes à governança de dados para LLMs."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-intro-to-fine-tuning-large-language-models--H-oCV5brtU4|Intro to Fine-Tuning Large Language Models]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-webinar-large-language-models-get-the-hype-but-compound-systems-are-the--vRTcE19M-KE|Stanford Webinar - Large Language Models Get the Hype, but Compound Systems Are the Future of AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-amit-jain-from-luma-ai-on-unified-intelligence-s--6nUl_w5W9Wk|Stanford CS153 Frontier Systems | Amit Jain from Luma AI on Unified Intelligence Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-10-inference--EfM546A79aM|Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 10: Inference]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]"]
---

# Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 13: Data (Sources, Datasets)

## Tese
Os dados são o componente mais crítico e mais deliberadamente secreto do treinamento de modelos de linguagem, e sua obtenção é moldada por restrições técnicas (crawling, robots.txt, autenticação) e legais (copyright, fair use, licenciamento) que se estreitaram drasticamente desde 2023.

## Conceitos-chave
- estágios do pipeline: pre-training, mid-training e post-training
- crawling da web, deep web e walled gardens
- robots.txt, termos de serviço e bloqueio de bots
- Copyright Act de 1976, domínio público e duração de 75 anos
- fair use e seus quatro fatores
- licenças (Creative Commons, MIT/Apache) vs. licenciamento pago
- shadow libraries (LibGen, Anna's Archive)
- quality filtering baseado em regras vs. baseado em classificador
- deduplicação e identificação de idioma
- extração HTML-para-texto (WARC vs. WET)
- curadoria e limpeza de dados como gargalo de longa cauda
- memorização verbatim vs. violação semântica de copyright
- envenenamento de dumps periódicos (ataque de janela temporal)
- contaminação legal de datasets (Books3/Bibliotik) e efeito watershed
- dados sintéticos e restrições de uso

## Ferramentas & pessoas
**Ferramentas:** Common Crawl, Wikipedia, GitHub, GitHub Archive, Software Heritage, arXiv, Cloudflare, trafilatura, resiliparse, WARC/WET, Llama 3, OLMo, Qwen3.5-397B-A17B, BERT, GPT-2 / WebText, CCNet, C4 / T5, GPT-3, The Pile, Books3, Bibliotik, Project Gutenberg / PG-19, Smashwords / BooksCorpus, Stack Exchange, Enron Emails, Gopher / MassiveWeb, Chinchilla, Llama 1, RedPajama V1, RefinedWeb, FineWeb, Dolma, The Stack, PushShift, Semantic Scholar, DCLM / DataComp, Google Books, ChatGPT, Claude

**Pessoas/orgs:** Meta, OpenAI, Anthropic, AI2, New York Times, Authors Guild, Google, DeepMind, EleutherAI, Hugging Face, Together, Shane Longpre, Nicholas Carlini, Cloudflare, X AI, Reddit, Software Heritage Foundation, Creative Commons

## Claims acionáveis
- Dados são a vantagem competitiva e o principal risco legal: o paper do Llama 3 revela arquitetura e procedimentos de treino, mas nada sobre os dados
- O pipeline segue pre-training (web bruta) → mid-training (alta qualidade, contexto longo) → post-training (chat, RL, safety), com tendência de grandes volumes de baixa qualidade para menores volumes de alta qualidade
- 'Treinado na internet' não é preciso: conteúdo dinâmico, deep web, autenticação, robots.txt, CAPTCHAs do Cloudflare, bloqueios de IP e ToS restringem o que é acessível
- Consent in Crisis (Longpre) mostra que restrições no robots.txt saltaram para ~50% dos sites após meados de 2023 e a maioria dos ToS agora proíbe uso para IA — o web legalmente crawlável encolheu muito
- Fair use tem quatro fatores (propósito transformador, natureza factual, quantidade usada, efeito de mercado); o caso Anthropic decretou treinamento como fair use, mas a pirataria em si é ilegal — acordo de US$ 1,5 bi (~US$ 3.000/livro) mesmo com compra e digitalização legais dos livros
- Copyright cobre expressão e semântica (personagens, enredos, efeitos econômicos), não ideias nem N-gram overlap; memorização verbatim é apenas uma das formas de violação
- Prefira dumps oficiais a crawling: Wikipedia, repositórios Git do GitHub, arXiv (bulk) e Stack Exchange publicam dumps — crawling gera carga nos servidores e viola a cidadania digital esperada
- A ferramenta de extração HTML→texto importa: ablação do DataComp LLM mostra que trafilatura e resiliparse superam os WET do Common Crawl
- Wikipedia é envenenável: editar logo antes do dump periódico (Carlini) insere conteúdo malicioso no dataset mesmo com rollback posterior — até fontes de alta qualidade podem conter ataques
- Evolução dos métodos de filtragem: WebText (links do Reddit com >3 karma, 40GB) → CCNet (LM treinado em Wikipedia) → C4 (regras manuais, 156B tokens) → GPT-3 (classificador de qualidade) → RefinedWeb/FineWeb (apenas web, 5T–15T tokens) → DCLM normaliza filtragem baseada em modelo
- Tensão de design recorrente entre filtragem por regras (controle, menos viés) e por classificador (qualidade, escala); RefinedWeb e Dolma evitaram explicitamente filtragem baseada em ML para não enviesar o subset da web
- Books3 (200k livros da shadow library Bibliotik) contaminou The Pile e Llama 1; decisões precoces de copyright têm efeito watershed e datasets posteriores removeram Books3
- Escala do Common Crawl: ~3–5 bilhões de páginas por crawl mensal, ~300 bilhões acumuladas, cada dump com ~2B páginas (~372TB de texto); índice do Google ≥100 petabytes
- A fronteira do 'base model' está desaparecendo (Qwen3.5 não expõe checkpoints intermediários); OLMo da AI2 é a referência aberta para estudar todo o pipeline de dados

> **Deep dive:** `high` — Alta densidade de decisões acionáveis de pipeline de dados (filtragem, dedup, extração, dumps vs. crawl, linhagem de datasets) combinada com desenvolvimentos jurídicos recentes (fair use, acordo de US$ 1,5 bi da Anthropic) diretamente relevantes à governança de dados para LLMs.
