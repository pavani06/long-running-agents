---
title: "System Design Course – APIs, Databases, Caching, CDNs, Load Balancing & Production Infra"
type: "extract"
source: "youtube"
video_id: "C842vFY5kRo"
url: "https://www.youtube.com/watch?v=C842vFY5kRo"
channel: "freeCodeCamp.org"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-system-design-course-apis-databases-caching-cdns-load-balancing-production-infra--C842vFY5kRo.txt]]"
tags: ["arquitetura", "data-platform", "stack-tooling", "production", "roadmap", "curriculo-conteudo", "monitoramento"]
thesis: "A transição de dev pleno para sênior exige dominar design de sistemas do zero — evoluindo de um setup single-server para arquiteturas de produção com escolhas conscientes de banco de dados, escalabilidade, load balancing e protocolos de API."
concepts: ["system design", "single-server setup", "DNS e resolução de domínio", "SQL vs NoSQL", "transações ACID (atomicidade, consistência, isolamento, durabilidade)", "escalabilidade vertical vs horizontal", "load balancing (round robin, least connections, least response time, IP hash, weighted, geográfico, consistent hashing)", "health checks", "single point of failure", "redundância e self-healing", "REST vs GraphQL vs gRPC", "princípios de design de API (consistência, simplicidade, segurança, performance)", "contrato de API e versionamento", "protocolos de aplicação (HTTP/HTTPS, WebSockets, AMQP, gRPC/protocol buffers)", "estado stateless em REST", "cache HTTP vs cache em nível de aplicação", "join operations em bancos relacionais"]
tools: ["DNS", "PostgreSQL", "MySQL", "Oracle Database", "SQLite", "MongoDB", "Cassandra", "Redis", "Neo4j", "Cosmos DB", "Memcached", "Amazon Neptune", "Nginx", "HAProxy", "F5", "Citrix", "AWS Elastic Load Balancing", "Azure Load Balancer", "Google Cloud Load Balancing", "GraphQL", "gRPC", "WebSockets", "AMQP"]
people: ["Hayek (autor do curso)", "Hikimon (canal do YouTube)", "Amazon", "Google", "AWS", "Microsoft Azure", "Google Cloud"]
claims: ["Empresas pagam salários sênior por decisões arquiteturais e tradeoffs com requisitos vagos, não por capacidade de codificar", "Comece todo design de sistema com um setup single-server simples e escale incrementalmente para entender cada componente", "Use bancos SQL quando os dados são bem estruturados com relacionamentos claros ou quando é exigida consistência forte e integridade transacional (ex.: aplicações financeiras)", "Use NoSQL quando a aplicação exige latência baixíssima, dados não estruturados/semiestruturados ou armazenamento escalável de grandes volumes", "Prefira escalabilidade horizontal para aplicações de alto tráfego por oferecer tolerância a falhas e elasticidade superiores à vertical", "Configure health checks nos load balancers para que tráfego não seja direcionado a servidores indisponíveis", "Elimine pontos únicos de falha com redundância (múltiplos load balancers), health checks e sistemas self-healing que substituem instâncias caídas", "Escolha REST para aplicações web/mobile, GraphQL para UIs complexas com dados aninhados e mínimos round trips, e gRPC para comunicação interna entre microserviços", "A melhor API é aquela que desenvolvedores conseguem usar sem ler a documentação", "Proteja APIs com autenticação, autorização, validação de inputs e rate limiting", "Otimize APIs com paginação, payloads minimizados, caching e redução de round trips", "O ciclo de vida de uma API inclui design, desenvolvimento, deploy, monitoramento, manutenção e eventual deprecação/versionamento"]
deep_dive: "low"
deep_dive_reason: "Conteúdo é um curso introdutório padrão de system design (bancos, load balancing, APIs), útil mas redundante, sem novidade e sem relevância para tópicos específicos de agentes de IA como harness, context-engineering, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-system-design-explained-apis-databases-caching-cdns-load-balancing-production-in--oYxTTirKY8M|System Design Explained: APIs, Databases, Caching, CDNs, Load Balancing & Production Infra]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-best-software-engineers-focus-on-system-design--LeUUxLRdvho|Why The Best Software Engineers Focus On System Design]]", "[[extracts/youtube/ai-learning/2026-09-11-google-aws-veteran-what-top-tier-software-architects-do-differently--F8X9_Dp3ZUk|Google & AWS Veteran: What Top Tier Software Architects Do Differently]]"]
theme: "Processo de Engenharia Agêntica"
---

# System Design Course – APIs, Databases, Caching, CDNs, Load Balancing & Production Infra

## Tese
A transição de dev pleno para sênior exige dominar design de sistemas do zero — evoluindo de um setup single-server para arquiteturas de produção com escolhas conscientes de banco de dados, escalabilidade, load balancing e protocolos de API.

## Conceitos-chave
- system design
- single-server setup
- DNS e resolução de domínio
- SQL vs NoSQL
- transações ACID (atomicidade, consistência, isolamento, durabilidade)
- escalabilidade vertical vs horizontal
- load balancing (round robin, least connections, least response time, IP hash, weighted, geográfico, consistent hashing)
- health checks
- single point of failure
- redundância e self-healing
- REST vs GraphQL vs gRPC
- princípios de design de API (consistência, simplicidade, segurança, performance)
- contrato de API e versionamento
- protocolos de aplicação (HTTP/HTTPS, WebSockets, AMQP, gRPC/protocol buffers)
- estado stateless em REST
- cache HTTP vs cache em nível de aplicação
- join operations em bancos relacionais

## Ferramentas & pessoas
**Ferramentas:** DNS, PostgreSQL, MySQL, Oracle Database, SQLite, MongoDB, Cassandra, Redis, Neo4j, Cosmos DB, Memcached, Amazon Neptune, Nginx, HAProxy, F5, Citrix, AWS Elastic Load Balancing, Azure Load Balancer, Google Cloud Load Balancing, GraphQL, gRPC, WebSockets, AMQP

**Pessoas/orgs:** Hayek (autor do curso), Hikimon (canal do YouTube), Amazon, Google, AWS, Microsoft Azure, Google Cloud

## Claims acionáveis
- Empresas pagam salários sênior por decisões arquiteturais e tradeoffs com requisitos vagos, não por capacidade de codificar
- Comece todo design de sistema com um setup single-server simples e escale incrementalmente para entender cada componente
- Use bancos SQL quando os dados são bem estruturados com relacionamentos claros ou quando é exigida consistência forte e integridade transacional (ex.: aplicações financeiras)
- Use NoSQL quando a aplicação exige latência baixíssima, dados não estruturados/semiestruturados ou armazenamento escalável de grandes volumes
- Prefira escalabilidade horizontal para aplicações de alto tráfego por oferecer tolerância a falhas e elasticidade superiores à vertical
- Configure health checks nos load balancers para que tráfego não seja direcionado a servidores indisponíveis
- Elimine pontos únicos de falha com redundância (múltiplos load balancers), health checks e sistemas self-healing que substituem instâncias caídas
- Escolha REST para aplicações web/mobile, GraphQL para UIs complexas com dados aninhados e mínimos round trips, e gRPC para comunicação interna entre microserviços
- A melhor API é aquela que desenvolvedores conseguem usar sem ler a documentação
- Proteja APIs com autenticação, autorização, validação de inputs e rate limiting
- Otimize APIs com paginação, payloads minimizados, caching e redução de round trips
- O ciclo de vida de uma API inclui design, desenvolvimento, deploy, monitoramento, manutenção e eventual deprecação/versionamento

> **Deep dive:** `low` — Conteúdo é um curso introdutório padrão de system design (bancos, load balancing, APIs), útil mas redundante, sem novidade e sem relevância para tópicos específicos de agentes de IA como harness, context-engineering, evals ou governança.
