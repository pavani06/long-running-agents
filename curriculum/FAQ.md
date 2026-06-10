---
title: "❓ FAQ: Perguntas Frequentes sobre o Currículo"
type: curriculum-index
aliases: ["perguntas frequentes", "duvidas", "faq"]
tags: [curriculo-conteudo, reference]
last_updated: 2026-06-10
---
# ❓ FAQ: Perguntas Frequentes sobre o Currículo
## Respostas claras para aprender, aplicar e mentorar Long-Running Agents no KODA

**Tempo Estimado:** 30 min  
**Nível:** Todos os Níveis  
**Pré-requisito:** Nenhum  
**Status:** ✅ Completo  
**Data de Criação:** Maio 2026

---

## 📖 Prólogo:

### Por Que Uma FAQ Muda a Velocidade de Aprendizado

Imagine a primeira semana de uma equipe entrando no currículo de Long-Running Agents. Todo
mundo está motivado. Alguém acabou de ler sobre Context Window. Outra pessoa abriu
Generator/Evaluator e já quer aplicar no KODA. Um líder técnico está tentando reservar tempo
no calendário. Um mentor está preparando a primeira sessão de perguntas. Parece tudo pronto.

Então surgem as dúvidas pequenas. Elas não parecem perigosas. "Preciso ler tudo em ordem?"
"Quanto tempo isso leva de verdade?" "Quando eu sei que entendi Token Budgeting?" "Como aplico
isso em uma conversa real de WhatsApp?" "O que faço quando uma pessoa do time pula direto para
Nível 4?" Cada dúvida, sozinha, custa cinco minutos. Juntas, elas viram uma manhã inteira
perdida.

O problema não é falta de inteligência. É falta de resposta compartilhada. Quando cada pessoa
resolve a mesma dúvida em silêncio, o time paga o mesmo custo várias vezes. Pior: respostas
diferentes começam a circular. Um participante acha que exercícios são opcionais. Um líder
acha que ROI aparece em uma semana. Um mentor avalia memorização em vez de raciocínio. O
currículo continua bom, mas a experiência fica irregular.

Esta FAQ existe para cortar esse ruído. Ela é o balcão de informação do programa. Não
substitui `curriculum/QUICK_START.md`, não substitui `curriculum/MASTER_PLAN.md`, não
substitui os módulos profundos. Ela ajuda você a escolher o próximo arquivo, entender o motivo
da escolha e transformar dúvida em ação.

Pense nela como um mentor paciente sentado ao lado do time. Quando alguém pergunta, ela não
responde com uma frase curta e vai embora. Ela explica o contexto, mostra um exemplo de KODA,
aponta o arquivo certo, descreve o erro comum e sugere como verificar entendimento. Esse
formato é intencional, porque perguntas frequentes quase nunca são apenas perguntas. Elas são
sintomas de onde o aprendizado pode travar.

A promessa é simples: se você está começando, esta FAQ reduz ansiedade. Se você lidera, ela
reduz improviso. Se você mentora, ela reduz ambiguidade. Se você está trabalhando na parte
técnica, ela liga termos como Context Window, Token Budgeting, State Persistence e Harness
Evolution a decisões que aparecem no KODA todos os dias.

---

## 🙋 Para Participantes

### 1. Sou iniciante total. Por onde começo sem me perder?

**Resposta curta:** Comece por `curriculum/QUICK_START.md`, depois leia o Nível 1 na ordem
indicada. O objetivo inicial não é dominar arquitetura, é entender por que agentes perdem o
foco em tarefas longas.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/QUICK_START.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: um cliente conversa por duas horas, muda preferências,
pergunta sobre whey protein, e KODA precisa lembrar restrições antigas antes de sugerir
compra. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma conversa de
WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por um Evaluator
antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token Budgeting,
Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é tentar começar por arquitetura avançada porque parece mais interessante. Esse
erro parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é ler o Quick Start, abrir o primeiro módulo de Nível 1 e fazer uma
anotação curta para cada um dos 3 problemas fundamentais. Faça isso de forma visível. Anote o
arquivo lido, a pergunta respondida, o exemplo de KODA usado e a evidência de que a pessoa
entendeu. Evidência pode ser um diagrama simples, uma rubric curta, uma trace comentada, ou
uma decisão registrada em Sprint Contract. O importante é não aceitar sensação de entendimento
como conclusão.

O resultado esperado é clareza sobre o mapa do programa e confiança para avançar sem pular a
fundação. Quando esse resultado aparece, você percebe a mudança no vocabulário do time. As
pessoas deixam de dizer apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda
de estado depois da compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint
Contract não definiu o failure mode". Esse é o sinal de que a pergunta foi respondida no nível
certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/QUICK_START.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/QUICK_START.md`
- `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 2. Preciso seguir os 4 níveis em ordem?

**Resposta curta:** Na maioria dos casos, sim. A ordem foi desenhada para construir
vocabulário comum antes de entrar em padrões e arquitetura. Pessoas experientes podem
acelerar, mas ainda devem validar os checkpoints.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/MASTER_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/06-knowledge-graphs/03-learning-progression.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: uma pessoa quer discutir Multi-Agent Systems sem conseguir
explicar por que Self-Evaluation Collapse afeta recomendações de produto. A dúvida deixa de
ser acadêmica quando alguém precisa decidir se uma conversa de WhatsApp deve continuar, ser
compactada, ser escalada para humano, ou passar por um Evaluator antes de chegar ao cliente.
Nessa hora, conceitos como Context Window, Token Budgeting, Generator/Evaluator, Sprint
Contracts e Rubric Design viram ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é confundir experiência geral em software com domínio dos problemas específicos
de agentes longos. Esse erro parece pequeno no começo, mas cria ruído: participantes pulam
fundamentos, líderes cobram métricas antes de definir critérios, mentores corrigem respostas
sem descobrir a causa da confusão, e o time interpreta falhas de agente como falhas de prompt.
O currículo tenta evitar isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões
práticos, Nível 3 para arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é usar os checkpoints de cada nível e só pular conteúdo quando conseguir
explicar os conceitos com exemplos de KODA. Faça isso de forma visível. Anote o arquivo lido,
a pergunta respondida, o exemplo de KODA usado e a evidência de que a pessoa entendeu.
Evidência pode ser um diagrama simples, uma rubric curta, uma trace comentada, ou uma decisão
registrada em Sprint Contract. O importante é não aceitar sensação de entendimento como
conclusão.

O resultado esperado é progressão mais rápida sem buracos invisíveis de entendimento. Quando
esse resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de
dizer apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois
da compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/MASTER_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/06-knowledge-graphs/03-learning-progression.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/MASTER_PLAN.md`
- `curriculum/06-knowledge-graphs/03-learning-progression.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 3. Quanto tempo preciso reservar por semana?

**Resposta curta:** Reserve blocos reais de estudo. O programa completo foi pensado para 12
semanas, mas cada pessoa pode ajustar ritmo conforme contexto, senioridade e responsabilidade
no KODA.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/EXECUTION_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use `curriculum/README.md`
como segunda leitura. A dupla funciona bem porque um arquivo explica o problema e o outro
mostra como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: o time tenta encaixar leitura entre incidentes de produção e
reuniões, depois percebe que ninguém fez os exercícios com atenção. A dúvida deixa de ser
acadêmica quando alguém precisa decidir se uma conversa de WhatsApp deve continuar, ser
compactada, ser escalada para humano, ou passar por um Evaluator antes de chegar ao cliente.
Nessa hora, conceitos como Context Window, Token Budgeting, Generator/Evaluator, Sprint
Contracts e Rubric Design viram ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é tratar o currículo como leitura casual de fim de expediente. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é bloquear agenda, combinar checkpoints semanais e alinhar expectativas com
o líder técnico. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o
exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama
simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract.
O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é cadência sustentável, menos culpa individual e mais consistência
coletiva. Quando esse resultado aparece, você percebe a mudança no vocabulário do time. As
pessoas deixam de dizer apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda
de estado depois da compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint
Contract não definiu o failure mode". Esse é o sinal de que a pergunta foi respondida no nível
certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/EXECUTION_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/README.md` e procure o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/EXECUTION_PLAN.md`
- `curriculum/README.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 4. Quais pré-requisitos eu realmente preciso ter?

**Resposta curta:** Você não precisa ser especialista em LLMs para começar. Precisa de
curiosidade, leitura atenta e disposição para conectar conceitos a exemplos concretos de KODA.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/QUICK_START.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use `curriculum/GLOSSARY.md`
como segunda leitura. A dupla funciona bem porque um arquivo explica o problema e o outro
mostra como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: uma pessoa nova em IA lê Context Window pela primeira vez e
precisa entender por que memória limitada afeta atendimento via WhatsApp. A dúvida deixa de
ser acadêmica quando alguém precisa decidir se uma conversa de WhatsApp deve continuar, ser
compactada, ser escalada para humano, ou passar por um Evaluator antes de chegar ao cliente.
Nessa hora, conceitos como Context Window, Token Budgeting, Generator/Evaluator, Sprint
Contracts e Rubric Design viram ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é achar que falta de vocabulário técnico impede participação. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é usar o Glossary como apoio constante e pedir exemplos sempre que um termo
parecer solto. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o
exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama
simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract.
O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é participação ativa mesmo com repertório técnico desigual. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/QUICK_START.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/GLOSSARY.md` e procure o exemplo aplicado ao KODA ou ao conceito
  relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/QUICK_START.md`
- `curriculum/GLOSSARY.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 5. O que faço quando fico travado em um conceito?

**Resposta curta:** Volte um nível de abstração. Se o conceito parece difícil, provavelmente
falta a história do problema, o exemplo de KODA ou a definição no Glossary.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/GLOSSARY.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: alguém entende a palavra State Persistence, mas não sabe
quando ela é necessária em uma conversa longa. A dúvida deixa de ser acadêmica quando alguém
precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para
humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como
Context Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram
ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é reler o mesmo parágrafo várias vezes sem mudar a estratégia de estudo. Esse
erro parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é procurar o termo no Glossary, voltar ao módulo que introduz o problema e
explicar o conceito em voz alta com um caso de cliente. Faça isso de forma visível. Anote o
arquivo lido, a pergunta respondida, o exemplo de KODA usado e a evidência de que a pessoa
entendeu. Evidência pode ser um diagrama simples, uma rubric curta, uma trace comentada, ou
uma decisão registrada em Sprint Contract. O importante é não aceitar sensação de entendimento
como conclusão.

O resultado esperado é destravamento rápido e uma pergunta melhor para levar ao mentor. Quando
esse resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de
dizer apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois
da compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/GLOSSARY.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/GLOSSARY.md`
- `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 6. Como sei que estou pronto para avançar de nível?

**Resposta curta:** Você está pronto quando consegue aplicar o conceito, não quando apenas
reconhece o nome. O critério é evidência de raciocínio.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/QUICK_START.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/08-tools-templates/learning-assessment-rubric.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: uma pessoa terminou Nível 2 e precisa mostrar que consegue
desenhar Generator/Evaluator para product discovery. A dúvida deixa de ser acadêmica quando
alguém precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser
escalada para humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora,
conceitos como Context Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric
Design viram ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é usar conclusão de leitura como prova de domínio. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é responder aos checkpoints, fazer exercícios e pedir revisão de um exemplo
aplicado ao KODA. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o
exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama
simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract.
O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é avanço com segurança e menos retrabalho no próximo nível. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/QUICK_START.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/08-tools-templates/learning-assessment-rubric.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/QUICK_START.md`
- `curriculum/08-tools-templates/learning-assessment-rubric.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 7. Os exercícios são obrigatórios?

**Resposta curta:** Sim, se o objetivo é formar habilidade real. A leitura cria vocabulário,
mas o exercício revela se a pessoa consegue operar o conceito sem apoio.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/02-nivel-2-practical-patterns/exercises/exercise-01.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: KODA precisa compactar histórico sem perder alergia, orçamento
e intenção de compra. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é pular exercícios porque a explicação parece óbvia. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é fazer pelo menos um exercício por conceito central e comparar a solução
com os critérios do módulo. Faça isso de forma visível. Anote o arquivo lido, a pergunta
respondida, o exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser
um diagrama simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em
Sprint Contract. O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é aprendizado que aparece em decisões de arquitetura, não apenas em
conversa. Quando esse resultado aparece, você percebe a mudança no vocabulário do time. As
pessoas deixam de dizer apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda
de estado depois da compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint
Contract não definiu o failure mode". Esse é o sinal de que a pergunta foi respondida no nível
certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md` e leia a seção
  que responde diretamente à dúvida.
- Abra `curriculum/02-nivel-2-practical-patterns/exercises/exercise-01.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md`
- `curriculum/02-nivel-2-practical-patterns/exercises/exercise-01.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 8. Posso estudar só o que tem relação com minha função?

**Resposta curta:** Pode priorizar, mas não isole demais. O currículo foi feito para criar
linguagem comum entre engenharia, produto, liderança e mentoria.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/README.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/MASTER_PLAN.md` como segunda leitura. A dupla funciona bem porque um arquivo
explica o problema e o outro mostra como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: um líder quer apenas ROI, enquanto a engenharia discute trace
e rubric sem traduzir impacto. A dúvida deixa de ser acadêmica quando alguém precisa decidir
se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou
passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window,
Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é criar trilhas totalmente separadas que não conversam entre si. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é ler a trilha principal do seu perfil e pelo menos os resumos dos níveis
adjacentes. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é colaboração melhor entre pessoas com responsabilidades diferentes.
Quando esse resultado aparece, você percebe a mudança no vocabulário do time. As pessoas
deixam de dizer apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de
estado depois da compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract
não definiu o failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/README.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/MASTER_PLAN.md` e procure o exemplo aplicado ao KODA ou ao conceito
  relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/README.md`
- `curriculum/MASTER_PLAN.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 9. Como navego quando quero responder uma dúvida pontual?

**Resposta curta:** Use esta FAQ como porta de entrada, depois vá para o arquivo
especializado. A pergunta te diz o caminho, não o destino final.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/FAQ.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use `curriculum/INDEX.md` como
segunda leitura. A dupla funciona bem porque um arquivo explica o problema e o outro mostra
como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: alguém pergunta como avaliar recomendação de produto e precisa
chegar em Rubric Design, KODA rubrics e templates. A dúvida deixa de ser acadêmica quando
alguém precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser
escalada para humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora,
conceitos como Context Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric
Design viram ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é esperar que um único documento resolva todos os detalhes. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é identificar a categoria da dúvida, abrir o arquivo recomendado e
registrar a resposta no contexto do time. Faça isso de forma visível. Anote o arquivo lido, a
pergunta respondida, o exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência
pode ser um diagrama simples, uma rubric curta, uma trace comentada, ou uma decisão registrada
em Sprint Contract. O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é menos tempo procurando e mais tempo aplicando. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/FAQ.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/INDEX.md` e procure o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/FAQ.md`
- `curriculum/INDEX.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 10. Como medir meu progresso sem transformar estudo em burocracia?

**Resposta curta:** Meça evidência simples: explicação, aplicação, exercício, revisão e
contribuição. Não precisa de processo pesado para saber se alguém está evoluindo.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/08-tools-templates/team-progress-tracker.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/08-tools-templates/learning-assessment-rubric.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: um participante entende Token Budgeting e contribui para
reduzir custo em uma conversa longa. A dúvida deixa de ser acadêmica quando alguém precisa
decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano,
ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context
Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram
ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é contar apenas arquivos lidos ou horas registradas. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é usar uma planilha leve com nível, conceito, evidência e próxima ação.
Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA
usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é visibilidade suficiente para apoiar pessoas sem criar
microgerenciamento. Quando esse resultado aparece, você percebe a mudança no vocabulário do
time. As pessoas deixam de dizer apenas "o agente ficou confuso" e passam a dizer "a trace
mostra perda de estado depois da compactação", "o Evaluator aprovou sem checar alergia", ou "o
Sprint Contract não definiu o failure mode". Esse é o sinal de que a pergunta foi respondida
no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/08-tools-templates/team-progress-tracker.md` e leia a seção que responde
  diretamente à dúvida.
- Abra `curriculum/08-tools-templates/learning-assessment-rubric.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/08-tools-templates/team-progress-tracker.md`
- `curriculum/08-tools-templates/learning-assessment-rubric.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 11. O que faço se discordar de uma recomendação do currículo?

**Resposta curta:** Trate a discordância como uma hipótese técnica. O currículo ensina
padrões, mas cada decisão real precisa respeitar evidência, custo e risco do KODA.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/MASTER_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: um engenheiro acha que Generator/Evaluator é caro demais para
uma feature de baixo risco. A dúvida deixa de ser acadêmica quando alguém precisa decidir se
uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar
por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é descartar o padrão inteiro sem avaliar contexto. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é documentar a hipótese, comparar com case studies e propor um experimento
pequeno. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de
KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é maturidade para adaptar sem quebrar coerência do programa. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/MASTER_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/MASTER_PLAN.md`
- `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 12. Como conecto teoria com código real?

**Resposta curta:** Procure sempre o caminho conceito, padrão, aplicação KODA, template. Essa
sequência transforma ideia em decisão implementável.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/05-core-concepts/03-generator-evaluator-pattern.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: o time quer melhorar recomendações e precisa sair de teoria
para design de feature. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é ir direto para código sem rubric, trace ou contrato. Esse erro parece pequeno
no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é mapear o conceito central, escolher o padrão e escrever o primeiro Sprint
Contract. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é implementações mais claras e menos discussão subjetiva. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/05-core-concepts/03-generator-evaluator-pattern.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/05-core-concepts/03-generator-evaluator-pattern.md`
- `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 13. Como estudo com outra pessoa do time?

**Resposta curta:** Estudo em par funciona muito bem quando cada pessoa assume um papel. Uma
explica o conceito, outra desafia com caso KODA.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/09-case-studies/03-koda-product-discovery.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: duas pessoas leem a mesma trace e procuram onde a recomendação
saiu do trilho. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma conversa
de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por um
Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é estudar junto como leitura silenciosa compartilhada. Esse erro parece pequeno
no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é alternar papéis de explicador, crítico e aplicador a cada sessão. Faça
isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e
a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric
curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não
aceitar sensação de entendimento como conclusão.

O resultado esperado é aprendizado social com feedback imediato. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/09-case-studies/03-koda-product-discovery.md` e procure o exemplo aplicado
  ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`
- `curriculum/09-case-studies/03-koda-product-discovery.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 14. Como lidar com material longo sem perder energia?

**Resposta curta:** Divida por objetivo. Um módulo longo normalmente tem história, conceito,
aplicação, exercício e fechamento. Você não precisa absorver tudo em uma sentada.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md`. Esse arquivo dá
o contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento
do que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/EXECUTION_PLAN.md` como segunda leitura. A dupla funciona bem porque um arquivo
explica o problema e o outro mostra como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: uma pessoa tenta ler 3000 linhas de uma vez e perde o fio da
arquitetura. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma conversa de
WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por um Evaluator
antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token Budgeting,
Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é confundir persistência com maratona de leitura. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é usar blocos de 30 a 45 minutos e terminar cada bloco com uma pergunta
respondida. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é ritmo mais humano e retenção melhor. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` e leia a
  seção que responde diretamente à dúvida.
- Abra `curriculum/EXECUTION_PLAN.md` e procure o exemplo aplicado ao KODA ou ao conceito
  relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md`
- `curriculum/EXECUTION_PLAN.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 15. O que devo produzir ao final do currículo?

**Resposta curta:** Você deve produzir entendimento aplicado: decisões melhores, rubrics
melhores, traces mais legíveis e propostas de harness mais seguras para KODA.

Para participantes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/04-nivel-4-koda-specific/01-koda-architecture.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/03-harness-design-checklist.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: o time conclui o programa e precisa transformar aprendizado em
melhorias concretas no agente de vendas. A dúvida deixa de ser acadêmica quando alguém precisa
decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano,
ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context
Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram
ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é achar que certificado informal é o principal resultado. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é escolher uma melhoria pequena no KODA e documentar como o currículo guiou
a decisão. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é aprendizado visível no produto e na conversa técnica do time. Quando
esse resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de
dizer apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois
da compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/03-harness-design-checklist.md` e procure o
  exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md`
- `curriculum/07-implementation-guides/03-harness-design-checklist.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

## 👔 Para Líderes

### 1. Como faço rollout do currículo para uma equipe ocupada?

**Resposta curta:** Comece pequeno, com calendário protegido e expectativas claras. O rollout
bom não tenta ensinar tudo em uma semana.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/EXECUTION_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/02-team-progression-guide.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: o time precisa manter KODA rodando enquanto aprende padrões
novos. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma conversa de
WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por um Evaluator
antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token Budgeting,
Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é lançar o programa como mais uma obrigação sem reduzir outra carga. Esse erro
parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é definir coortes, blocos semanais e critérios mínimos por nível. Faça isso
de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a
evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta,
uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar
sensação de entendimento como conclusão.

O resultado esperado é adoção constante sem sacrificar operação. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/EXECUTION_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/02-team-progression-guide.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/EXECUTION_PLAN.md`
- `curriculum/07-implementation-guides/02-team-progression-guide.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 2. Como justifico tempo de estudo para negócio?

**Resposta curta:** Conecte estudo a risco, qualidade e receita. Long-Running Agents afetam
conversão, satisfação, custo de tokens e confiança do cliente.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/MASTER_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/09-case-studies/04-koda-order-processing.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: uma recomendação errada causa devolução, suporte e perda de
confiança. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma conversa de
WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por um Evaluator
antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token Budgeting,
Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é apresentar o currículo como benefício abstrato de capacitação. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é usar exemplos de KODA para mostrar onde cada padrão reduz erro ou aumenta
controle. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é conversa executiva baseada em impacto mensurável. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/MASTER_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/09-case-studies/04-koda-order-processing.md` e procure o exemplo aplicado
  ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/MASTER_PLAN.md`
- `curriculum/09-case-studies/04-koda-order-processing.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 3. Como acompanho progresso sem virar cobrança vazia?

**Resposta curta:** Acompanhe evidência, não presença. O indicador bom mostra se a pessoa
consegue aplicar um conceito em KODA.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/08-tools-templates/team-progress-tracker.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/08-tools-templates/learning-assessment-rubric.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: um líder vê 100% de presença, mas ninguém sabe explicar Sprint
Contracts. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma conversa de
WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por um Evaluator
antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token Budgeting,
Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é medir participação como se fosse competência. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é pedir artefatos pequenos: rubric, trace comentada, decisão de harness ou
explicação gravada. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o
exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama
simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract.
O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é progresso honesto e acionável. Quando esse resultado aparece, você
percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou
confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator
aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal
de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/08-tools-templates/team-progress-tracker.md` e leia a seção que responde
  diretamente à dúvida.
- Abra `curriculum/08-tools-templates/learning-assessment-rubric.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/08-tools-templates/team-progress-tracker.md`
- `curriculum/08-tools-templates/learning-assessment-rubric.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 4. Quanto tempo devo reservar no calendário da equipe?

**Resposta curta:** Use o cronograma de 12 semanas como base e ajuste pela urgência do KODA. O
importante é proteger blocos recorrentes.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/EXECUTION_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use `curriculum/README.md`
como segunda leitura. A dupla funciona bem porque um arquivo explica o problema e o outro
mostra como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: a equipe entra em sprint de feature e tenta estudar apenas nos
intervalos. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma conversa de
WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por um Evaluator
antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token Budgeting,
Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é deixar estudo competir com reuniões ad hoc. Esse erro parece pequeno no começo,
mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de definir
critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time interpreta
falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas: Nível 1
para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e Nível 4 para
KODA em produção.

A ação recomendada é reservar blocos fixos para leitura, prática e discussão. Faça isso de
forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a
evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta,
uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar
sensação de entendimento como conclusão.

O resultado esperado é menos interrupção e maior previsibilidade. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/EXECUTION_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/README.md` e procure o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/EXECUTION_PLAN.md`
- `curriculum/README.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 5. Como integrar o currículo com trabalho real?

**Resposta curta:** Escolha uma feature KODA por ciclo e use o currículo para melhorar a
decisão sobre ela. Não crie um mundo separado de treinamento.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/03-harness-design-checklist.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: o time está redesenhando product discovery e precisa decidir
onde colocar Evaluator. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é fazer exercícios totalmente desconectados do backlog. Esse erro parece pequeno
no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é ligar cada módulo a uma conversa, feature ou bug real. Faça isso de forma
visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a evidência de
que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta, uma trace
comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar sensação
de entendimento como conclusão.

O resultado esperado é aprendizado que reduz risco no roadmap. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/03-harness-design-checklist.md` e procure o
  exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`
- `curriculum/07-implementation-guides/03-harness-design-checklist.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 6. Como medir ROI do programa?

**Resposta curta:** Meça antes e depois nos pontos onde agentes longos falham: precisão,
retrabalho, tempo de debug, custo de tokens e satisfação.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/MASTER_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` como segunda
leitura. A dupla funciona bem porque um arquivo explica o problema e o outro mostra como o
problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: o time implementa Evaluator para recomendação e acompanha
queda de erro residual. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é procurar ROI financeiro antes de definir métrica operacional. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é estabelecer baseline, aplicar padrão em escopo pequeno e medir evolução.
Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA
usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é ROI defendível com evidência técnica e de negócio. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/MASTER_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` e procure
  o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/MASTER_PLAN.md`
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 7. Devo fazer workshops ou estudo assíncrono?

**Resposta curta:** Use os dois. Assíncrono serve para leitura e exercícios individuais.
Workshop serve para alinhar interpretação e discutir casos difíceis.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/EXECUTION_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/02-team-progression-guide.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: pessoas leem o mesmo módulo e saem com interpretações
diferentes sobre Rubric Design. A dúvida deixa de ser acadêmica quando alguém precisa decidir
se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou
passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window,
Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é achar que reunião substitui estudo ou que estudo substitui debate. Esse erro
parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é combinar leitura antes, discussão durante e artefato depois. Faça isso de
forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a
evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta,
uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar
sensação de entendimento como conclusão.

O resultado esperado é menos ambiguidade e mais responsabilidade individual. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/EXECUTION_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/02-team-progression-guide.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/EXECUTION_PLAN.md`
- `curriculum/07-implementation-guides/02-team-progression-guide.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 8. Como escolher mentores internos?

**Resposta curta:** Escolha pessoas que explicam bem, fazem boas perguntas e conectam conceito
a KODA. Senioridade ajuda, mas não basta.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/08-tools-templates/learning-assessment-rubric.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: um mentor precisa avaliar se alguém entendeu State Persistence
ou apenas decorou a definição. A dúvida deixa de ser acadêmica quando alguém precisa decidir
se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou
passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window,
Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é nomear mentores apenas por cargo. Esse erro parece pequeno no começo, mas cria
ruído: participantes pulam fundamentos, líderes cobram métricas antes de definir critérios,
mentores corrigem respostas sem descobrir a causa da confusão, e o time interpreta falhas de
agente como falhas de prompt. O currículo tenta evitar isso com camadas: Nível 1 para raiz do
problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e Nível 4 para KODA em
produção.

A ação recomendada é observar quem consegue dar feedback específico e respeitoso em
exercícios. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é mentoria mais útil e menos hierárquica. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/08-tools-templates/learning-assessment-rubric.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/08-tools-templates/learning-assessment-rubric.md`
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 9. Como lidar com níveis diferentes no mesmo time?

**Resposta curta:** Crie trilha comum mínima e trilhas de aprofundamento. Todos precisam
entender os fundamentos, mas nem todos precisam virar arquitetos no mesmo ritmo.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/README.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/MASTER_PLAN.md` como segunda leitura. A dupla funciona bem porque um arquivo
explica o problema e o outro mostra como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: um PM, um engenheiro sênior e uma pessoa de suporte estudam o
mesmo programa com objetivos diferentes. A dúvida deixa de ser acadêmica quando alguém precisa
decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano,
ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context
Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram
ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é forçar ritmo único para perfis muito diferentes. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é definir Nível 1 como base comum e personalizar Níveis 2 a 4 por função.
Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA
usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é inclusão sem nivelar por baixo. Quando esse resultado aparece, você
percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou
confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator
aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal
de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/README.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/MASTER_PLAN.md` e procure o exemplo aplicado ao KODA ou ao conceito
  relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/README.md`
- `curriculum/MASTER_PLAN.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 10. Quando devo pausar o rollout e corrigir rota?

**Resposta curta:** Pause quando sinais de entendimento não aparecem, quando o time está só
cumprindo leitura, ou quando dúvidas repetidas indicam buraco na facilitação.

Para líderes, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/08-tools-templates/team-progress-tracker.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use `curriculum/FAQ.md` como
segunda leitura. A dupla funciona bem porque um arquivo explica o problema e o outro mostra
como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: três sessões seguidas têm perguntas básicas sobre Context
Window depois de o Nível 1 ter acabado. A dúvida deixa de ser acadêmica quando alguém precisa
decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano,
ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context
Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram
ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é continuar avançando porque o calendário manda. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é revisar perguntas frequentes, voltar ao módulo raiz e ajustar a cadência.
Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA
usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é programa mais forte e menos teatral. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/08-tools-templates/team-progress-tracker.md` e leia a seção que responde
  diretamente à dúvida.
- Abra `curriculum/FAQ.md` e procure o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/08-tools-templates/team-progress-tracker.md`
- `curriculum/FAQ.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

## 🧑‍🏫 Para Mentores

### 1. Como avalio entendimento sem aplicar uma prova pesada?

**Resposta curta:** Peça explicação aplicada. A pessoa deve conseguir usar o conceito para
tomar uma decisão sobre KODA.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/08-tools-templates/learning-assessment-rubric.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: um participante explica por que uma recomendação precisa
passar por Evaluator. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é avaliar memorização de termos isolados. Esse erro parece pequeno no começo, mas
cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de definir
critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time interpreta
falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas: Nível 1
para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e Nível 4 para
KODA em produção.

A ação recomendada é usar perguntas de cenário, mini rubrics e revisão de exercícios. Faça
isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e
a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric
curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não
aceitar sensação de entendimento como conclusão.

O resultado esperado é avaliação leve, mas real. Quando esse resultado aparece, você percebe a
mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou confuso" e
passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator aprovou
sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal de que
a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/08-tools-templates/learning-assessment-rubric.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/08-tools-templates/learning-assessment-rubric.md`
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 2. Quais tropeços aparecem mais no Nível 1?

**Resposta curta:** Os mais comuns são tratar Context Window como memória infinita, subestimar
Token Budgeting e achar que prompt resolve tudo.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: KODA esquece alergia depois de muitas mensagens e alguém quer
apenas reforçar o system prompt. A dúvida deixa de ser acadêmica quando alguém precisa decidir
se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou
passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window,
Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é transformar problema arquitetural em ajuste de frase. Esse erro parece pequeno
no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é pedir que a pessoa desenhe onde a informação vive ao longo da conversa.
Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA
usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é fundação mais sólida para padrões práticos. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md` e procure o exemplo aplicado
  ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 3. Quais tropeços aparecem mais no Nível 2?

**Resposta curta:** Pessoas confundem padrão com ferramenta. Generator/Evaluator, Sprint
Contracts, Rubric Design e Trace Reading são formas de pensar sobre responsabilidade.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md`. Esse arquivo dá
o contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento
do que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` como segunda
leitura. A dupla funciona bem porque um arquivo explica o problema e o outro mostra como o
problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: o time cria dois agentes, mas ambos fazem a mesma validação
sem critérios claros. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é implementar nomes de componentes sem separar responsabilidades. Esse erro
parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é pedir que a pessoa descreva input, output, critérios e failure modes.
Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA
usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é uso correto dos padrões, não apenas da nomenclatura. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md` e leia a
  seção que responde diretamente à dúvida.
- Abra `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` e procure
  o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/koda-applications/nivel-2-koda.md`
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 4. Como dou feedback sem desmotivar participantes?

**Resposta curta:** Feedback bom aponta evidência e próximo passo. Ele não diz apenas que está
errado, mostra onde o raciocínio perdeu contato com o caso.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/08-tools-templates/learning-assessment-rubric.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/05-trace-analysis-guide.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: uma pessoa lê uma trace e acusa o Generator, mas a falha está
no contrato entre módulos. A dúvida deixa de ser acadêmica quando alguém precisa decidir se
uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar
por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é corrigir com resposta pronta sem explicar método. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é perguntar qual evidência sustenta a conclusão e sugerir uma próxima
leitura. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de
KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é confiança maior e aprendizado mais profundo. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/08-tools-templates/learning-assessment-rubric.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/05-trace-analysis-guide.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/08-tools-templates/learning-assessment-rubric.md`
- `curriculum/07-implementation-guides/05-trace-analysis-guide.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 5. Qual cadência de mentoria funciona melhor?

**Resposta curta:** Uma cadência semanal curta costuma funcionar melhor que sessões longas e
raras. O currículo precisa de continuidade.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/EXECUTION_PLAN.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/02-team-progression-guide.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: participantes passam duas semanas sem discutir dúvidas e
chegam perdidos ao workshop. A dúvida deixa de ser acadêmica quando alguém precisa decidir se
uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar
por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é guardar todas as dúvidas para uma reunião grande. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é fazer check-ins de 30 a 45 minutos com foco em uma pergunta central. Faça
isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e
a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric
curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não
aceitar sensação de entendimento como conclusão.

O resultado esperado é menos acúmulo de confusão. Quando esse resultado aparece, você percebe
a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou confuso" e
passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator aprovou
sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal de que
a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/EXECUTION_PLAN.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/02-team-progression-guide.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/EXECUTION_PLAN.md`
- `curriculum/07-implementation-guides/02-team-progression-guide.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 6. Como mentorar pessoas muito avançadas?

**Resposta curta:** Dê problemas mais abertos, mas exija precisão. Pessoas avançadas devem
justificar trade-offs e desenhar critérios de avaliação.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: um arquiteto propõe Multi-Agent System para KODA sem explicar
custo de coordenação. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é aceitar complexidade como sinal automático de senioridade. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é pedir comparação entre alternativa simples e arquitetura avançada. Faça
isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e
a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric
curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não
aceitar sensação de entendimento como conclusão.

O resultado esperado é decisões sofisticadas com disciplina. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` e leia a seção
  que responde diretamente à dúvida.
- Abra `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` e procure o
  exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md`
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 7. Como mentorar pessoas novas sem simplificar demais?

**Resposta curta:** Use histórias de KODA, não simplificações falsas. Pessoas novas conseguem
entender problemas reais quando o caminho é bem guiado.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/QUICK_START.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/01-nivel-1-fundamentals/koda-applications/nivel-1-koda.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: uma pessoa sem background em IA entende que KODA precisa
lembrar alergia porque isso afeta confiança. A dúvida deixa de ser acadêmica quando alguém
precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para
humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como
Context Window, Token Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram
ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é retirar todo detalhe técnico e deixar só analogia. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é alternar definição simples, exemplo real e pergunta de verificação. Faça
isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e
a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric
curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não
aceitar sensação de entendimento como conclusão.

O resultado esperado é aprendizado acessível sem perder rigor. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/QUICK_START.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/01-nivel-1-fundamentals/koda-applications/nivel-1-koda.md` e procure o
  exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/QUICK_START.md`
- `curriculum/01-nivel-1-fundamentals/koda-applications/nivel-1-koda.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 8. Como saber se alguém está pronto para mentorar outros?

**Resposta curta:** A pessoa está pronta quando explica com clareza, identifica erros de
raciocínio e recomenda leituras sem humilhar ou confundir.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/08-tools-templates/learning-assessment-rubric.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use `curriculum/FAQ.md` como
segunda leitura. A dupla funciona bem porque um arquivo explica o problema e o outro mostra
como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: um participante ajuda outro a encontrar o módulo certo e
revisar um exercício. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é confundir domínio técnico com habilidade de ensino. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é observar uma sessão curta de explicação e feedback. Faça isso de forma
visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a evidência de
que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta, uma trace
comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar sensação
de entendimento como conclusão.

O resultado esperado é rede de mentoria sustentável. Quando esse resultado aparece, você
percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou
confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator
aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal
de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/08-tools-templates/learning-assessment-rubric.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/FAQ.md` e procure o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/08-tools-templates/learning-assessment-rubric.md`
- `curriculum/FAQ.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 9. Como usar traces em sessões de mentoria?

**Resposta curta:** Trace é excelente para sair de opinião e entrar em evidência. Use como
narrativa de decisão do agente.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/05-trace-analysis-guide.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: KODA recomenda produto fora do orçamento e a trace mostra onde
o orçamento foi perdido. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é ler trace como log bruto sem pergunta orientadora. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é começar com hipótese, localizar evidência e revisar conclusão. Faça isso
de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a
evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta,
uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar
sensação de entendimento como conclusão.

O resultado esperado é mentoria prática e menos abstrata. Quando esse resultado aparece, você
percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou
confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator
aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal
de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/05-trace-analysis-guide.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`
- `curriculum/07-implementation-guides/05-trace-analysis-guide.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 10. Como avaliar exercícios em grupo?

**Resposta curta:** Avalie o raciocínio coletivo e a clareza dos critérios. A resposta final
importa, mas o caminho importa mais.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/exercises/exercise-01.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/08-tools-templates/evaluation-rubric-template.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: um grupo desenha Evaluator para recomendações e precisa
defender cada critério. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é premiar apenas quem chegou na resposta mais parecida com a solução. Esse erro
parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é pedir que cada grupo explique trade-offs, riscos e lacunas. Faça isso de
forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a
evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta,
uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar
sensação de entendimento como conclusão.

O resultado esperado é grupo aprende a pensar como sistema. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/exercises/exercise-01.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/08-tools-templates/evaluation-rubric-template.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/exercises/exercise-01.md`
- `curriculum/08-tools-templates/evaluation-rubric-template.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 11. Como transformar dúvidas repetidas em melhoria do programa?

**Resposta curta:** Dúvidas repetidas são dados. Elas mostram onde o currículo, a facilitação
ou a ordem de leitura precisam de ajuste.

Para mentores, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é `curriculum/FAQ.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use `curriculum/MASTER_PLAN.md`
como segunda leitura. A dupla funciona bem porque um arquivo explica o problema e o outro
mostra como o problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: várias pessoas perguntam quando usar Rubric Design mesmo
depois do módulo. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Context Window, Token
Budgeting, Generator/Evaluator, Sprint Contracts e Rubric Design viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é culpar participantes por não terem lido direito. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é registrar a dúvida, revisar a explicação e criar exemplo adicional em
sessão. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de
KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é currículo vivo, sem perder consistência. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/FAQ.md` e leia a seção que responde diretamente à dúvida.
- Abra `curriculum/MASTER_PLAN.md` e procure o exemplo aplicado ao KODA ou ao conceito
  relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/FAQ.md`
- `curriculum/MASTER_PLAN.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

## 🔧 Técnica

### 1. O que é Context Window na prática?

**Resposta curta:** Context Window é o espaço de informação que o modelo consegue considerar
em uma chamada. Em agentes longos, ele define o limite da memória imediata.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/01-context-management.md` como segunda leitura. A dupla funciona
bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: KODA precisa responder levando em conta histórico, catálogo,
preferências, restrições e estado do pedido. A dúvida deixa de ser acadêmica quando alguém
precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para
humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como
Context Window, Context Management, State Persistence e Server-Side Compaction viram
ferramentas de trabalho, não vocabulário bonito para reunião.

O erro comum é achar que o modelo lembra tudo porque a conversa está salva no sistema. Esse
erro parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é mapear quais informações precisam estar no contexto ativo e quais devem
viver em estado persistido. Faça isso de forma visível. Anote o arquivo lido, a pergunta
respondida, o exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser
um diagrama simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em
Sprint Contract. O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é respostas mais consistentes em conversas longas. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/05-core-concepts/01-context-management.md` e procure o exemplo aplicado ao
  KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
- `curriculum/05-core-concepts/01-context-management.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 2. Como Token Budgeting afeta custo e qualidade?

**Resposta curta:** Token Budgeting é a prática de decidir quanto contexto entra, quanto
espaço fica para resposta e quanto custo é aceitável.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/01-context-management.md` como segunda leitura. A dupla funciona
bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: uma conversa de compra cresce e começa a carregar histórico
demais para cada recomendação. A dúvida deixa de ser acadêmica quando alguém precisa decidir
se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou
passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Token
Budgeting, Context Window, History Compression e Cost Management viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é mandar todo o histórico sempre porque parece mais seguro. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é definir orçamento por etapa, compactar histórico e medir impacto em
latência e precisão. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida,
o exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama
simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract.
O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é menos custo sem perder informações críticas. Quando esse resultado
aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o
agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação",
"o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode".
Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md` e leia a seção que responde
  diretamente à dúvida.
- Abra `curriculum/05-core-concepts/01-context-management.md` e procure o exemplo aplicado ao
  KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md`
- `curriculum/05-core-concepts/01-context-management.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 3. Quando usar Generator/Evaluator?

**Resposta curta:** Use quando qualidade importa mais que velocidade e quando há critérios
explícitos para aprovar ou rejeitar uma saída.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`. Esse arquivo dá
o contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento
do que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/03-generator-evaluator-pattern.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: KODA recomenda suplemento para cliente com restrição alimentar
e orçamento claro. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Generator/Evaluator,
Rubric Design, Evaluator Verdict e Feedback Loop viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é usar Generator/Evaluator em toda resposta simples e aumentar custo sem
necessidade. Esse erro parece pequeno no começo, mas cria ruído: participantes pulam
fundamentos, líderes cobram métricas antes de definir critérios, mentores corrigem respostas
sem descobrir a causa da confusão, e o time interpreta falhas de agente como falhas de prompt.
O currículo tenta evitar isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões
práticos, Nível 3 para arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é aplicar primeiro em decisões críticas, como recomendação, checkout e
avaliação de risco. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o
exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama
simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract.
O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é erro residual menor e auditoria melhor. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` e leia a
  seção que responde diretamente à dúvida.
- Abra `curriculum/05-core-concepts/03-generator-evaluator-pattern.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
- `curriculum/05-core-concepts/03-generator-evaluator-pattern.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 4. O que torna um Sprint Contract bom?

**Resposta curta:** Um Sprint Contract bom define input, output, success criteria, constraints
e failure modes antes da execução.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/08-tools-templates/sprint-contract-template.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: um módulo de KODA recebe carrinho, endereço e cupom, mas não
sabe o que fazer se estoque mudar no meio. A dúvida deixa de ser acadêmica quando alguém
precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para
humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como
Sprint Contracts, Success Criteria, Constraints e Failure Modes viram ferramentas de trabalho,
não vocabulário bonito para reunião.

O erro comum é escrever contrato como descrição vaga de intenção. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é converter expectativas em campos verificáveis e critérios de aceite. Faça
isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e
a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric
curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não
aceitar sensação de entendimento como conclusão.

O resultado esperado é menos surpresa entre módulos e revisão mais objetiva. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/08-tools-templates/sprint-contract-template.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md`
- `curriculum/08-tools-templates/sprint-contract-template.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 5. Como desenhar uma rubric útil?

**Resposta curta:** Rubric útil transforma qualidade subjetiva em critérios observáveis. Ela
diz o que aprovar, rejeitar e investigar.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/03-rubric-design.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/08-evaluation-rubrics.md` como segunda leitura. A dupla funciona
bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: KODA precisa avaliar se a recomendação foi segura, relevante,
clara e dentro do orçamento. A dúvida deixa de ser acadêmica quando alguém precisa decidir se
uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar
por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Rubric Design,
Evaluation Rubrics, Thresholds e Quality Dimensions viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é criar rubric genérica demais, que aprova qualquer resposta bem escrita. Esse
erro parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é definir dimensões, pesos, exemplos de falha e thresholds de aprovação.
Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA
usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é avaliação mais justa e reproduzível. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/05-core-concepts/08-evaluation-rubrics.md` e procure o exemplo aplicado ao
  KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md`
- `curriculum/05-core-concepts/08-evaluation-rubrics.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 6. O que é State Persistence e quando preciso dela?

**Resposta curta:** State Persistence guarda informações críticas fora da janela imediata do
modelo para que sobrevivam ao tempo, compactação e troca de etapas.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/05-state-persistence.md` como segunda leitura. A dupla funciona
bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: cliente informa alergia, endereço, objetivo de treino e
orçamento em momentos diferentes da conversa. A dúvida deixa de ser acadêmica quando alguém
precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para
humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como
State Persistence, Working Memory, Long-Term State e Conversation State viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é confiar apenas no transcript bruto para recuperar estado. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é definir quais fatos viram estado, quem pode atualizar e como validar
consistência. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o
exemplo de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama
simples, uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract.
O importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é memória operacional mais confiável. Quando esse resultado aparece, você
percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou
confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator
aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal
de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md` e leia a seção
  que responde diretamente à dúvida.
- Abra `curriculum/05-core-concepts/05-state-persistence.md` e procure o exemplo aplicado ao
  KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/03-nivel-3-advanced-architecture/02-state-persistence.md`
- `curriculum/05-core-concepts/05-state-persistence.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 7. Como Multi-Agent Systems ajudam KODA?

**Resposta curta:** Multi-Agent Systems ajudam quando uma tarefa tem responsabilidades
distintas demais para um único agente manter com clareza.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/07-multi-agent-coordination.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: um fluxo completo envolve descoberta de produto, validação de
estoque, cálculo de frete, pagamento e suporte. A dúvida deixa de ser acadêmica quando alguém
precisa decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para
humano, ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como
Multi-Agent Systems, Coordination, Specialist Agents e Orchestration viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é criar agentes demais sem necessidade de coordenação explícita. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é separar responsabilidades apenas quando o contrato entre agentes for
claro. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de
KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma
rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante
é não aceitar sensação de entendimento como conclusão.

O resultado esperado é especialização sem caos operacional. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` e leia a seção
  que responde diretamente à dúvida.
- Abra `curriculum/05-core-concepts/07-multi-agent-coordination.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md`
- `curriculum/05-core-concepts/07-multi-agent-coordination.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 8. O que é Harness Evolution?

**Resposta curta:** Harness Evolution é a melhoria contínua da estrutura que cerca o agente.
Não é trocar prompt, é evoluir o sistema de suporte.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/06-harness-evolution.md` como segunda leitura. A dupla funciona
bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: KODA começa com validações simples e depois precisa de traces,
rubrics, compactação e coordenação. A dúvida deixa de ser acadêmica quando alguém precisa
decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano,
ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Harness
Evolution, Observability, Rollback e Incremental Architecture viram ferramentas de trabalho,
não vocabulário bonito para reunião.

O erro comum é fazer grandes reescritas sem evidência de onde o harness falha. Esse erro
parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é evoluir por hipóteses pequenas, métricas e rollback claro. Faça isso de
forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a
evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta,
uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar
sensação de entendimento como conclusão.

O resultado esperado é arquitetura que aprende com produção. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` e leia a seção
  que responde diretamente à dúvida.
- Abra `curriculum/05-core-concepts/06-harness-evolution.md` e procure o exemplo aplicado ao
  KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`
- `curriculum/05-core-concepts/06-harness-evolution.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 9. Como Server-Side Compaction se relaciona com memória?

**Resposta curta:** Server-Side Compaction reduz histórico sem apagar fatos importantes. Ela
transforma conversa longa em resumo operacional confiável.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/05-core-concepts/01-context-management.md` como segunda leitura. A dupla funciona
bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: uma conversa de duas horas precisa continuar rápida e barata
sem perder restrições do cliente. A dúvida deixa de ser acadêmica quando alguém precisa
decidir se uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano,
ou passar por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Server-Side
Compaction, Context Management, State Persistence e Token Budgeting viram ferramentas de
trabalho, não vocabulário bonito para reunião.

O erro comum é compactar tudo como resumo narrativo bonito, mas sem campos críticos. Esse erro
parece pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram
métricas antes de definir critérios, mentores corrigem respostas sem descobrir a causa da
confusão, e o time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar
isso com camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é definir o que nunca pode sumir e validar o resumo contra estado
persistido. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é contexto menor com segurança maior. Quando esse resultado aparece, você
percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente ficou
confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o Evaluator
aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse é o sinal
de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md` e leia a
  seção que responde diretamente à dúvida.
- Abra `curriculum/05-core-concepts/01-context-management.md` e procure o exemplo aplicado ao
  KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md`
- `curriculum/05-core-concepts/01-context-management.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 10. Como File-Based Coordination entra no currículo?

**Resposta curta:** File-Based Coordination ensina coordenação simples e auditável entre
partes do sistema usando arquivos estruturados.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md`. Esse arquivo dá o
contexto principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do
que é detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` como segunda
leitura. A dupla funciona bem porque um arquivo explica o problema e o outro mostra como o
problema aparece no ecossistema do KODA.

Pense no cenário de KODA assim: Generator grava uma recomendação e Evaluator lê o artefato
para aprovar ou rejeitar. A dúvida deixa de ser acadêmica quando alguém precisa decidir se uma
conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar por
um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como File-Based Coordination,
Structured Artifacts, Generator/Evaluator e Traceability viram ferramentas de trabalho, não
vocabulário bonito para reunião.

O erro comum é usar arquivo como depósito informal sem schema. Esse erro parece pequeno no
começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de
definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time
interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas:
Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e
Nível 4 para KODA em produção.

A ação recomendada é definir formato, ownership, estado e ciclo de vida do arquivo. Faça isso
de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e a
evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric curta,
uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não aceitar
sensação de entendimento como conclusão.

O resultado esperado é coordenação fácil de auditar e debugar. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` e leia a
  seção que responde diretamente à dúvida.
- Abra `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` e procure
  o exemplo aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md`
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 11. Como Trace Reading ajuda a debugar agentes?

**Resposta curta:** Trace Reading mostra a sequência real de decisões. Ela troca palpite por
evidência.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/07-implementation-guides/05-trace-analysis-guide.md` como segunda leitura. A dupla
funciona bem porque um arquivo explica o problema e o outro mostra como o problema aparece no
ecossistema do KODA.

Pense no cenário de KODA assim: cliente reclama de recomendação errada e o time precisa
descobrir qual etapa falhou. A dúvida deixa de ser acadêmica quando alguém precisa decidir se
uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar
por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Trace Reading,
Observability, Failure Analysis e Debugging viram ferramentas de trabalho, não vocabulário
bonito para reunião.

O erro comum é procurar bug lendo apenas a resposta final. Esse erro parece pequeno no começo,
mas cria ruído: participantes pulam fundamentos, líderes cobram métricas antes de definir
critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o time interpreta
falhas de agente como falhas de prompt. O currículo tenta evitar isso com camadas: Nível 1
para raiz do problema, Nível 2 para padrões práticos, Nível 3 para arquitetura, e Nível 4 para
KODA em produção.

A ação recomendada é seguir a trace do input ao output e comparar cada etapa com o contrato
esperado. Faça isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo
de KODA usado e a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples,
uma rubric curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O
importante é não aceitar sensação de entendimento como conclusão.

O resultado esperado é debug mais rápido e menos emocional. Quando esse resultado aparece,
você percebe a mudança no vocabulário do time. As pessoas deixam de dizer apenas "o agente
ficou confuso" e passam a dizer "a trace mostra perda de estado depois da compactação", "o
Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o failure mode". Esse
é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/07-implementation-guides/05-trace-analysis-guide.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`
- `curriculum/07-implementation-guides/05-trace-analysis-guide.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

### 12. Como conectar Rubric Design com ROI?

**Resposta curta:** Rubric Design afeta ROI quando reduz erro que custa dinheiro, suporte,
devolução ou perda de confiança.

Para pessoas técnicas, a melhor forma de usar esta resposta é tratar a dúvida como um pequeno
checkpoint de aprendizado. O currículo não foi escrito para ser lido como uma apostila linear
sem pausa. Ele foi desenhado como um sistema de navegação: você lê, testa a ideia em KODA,
compara com o material de apoio, e só então avança. Quando uma pergunta aparece, ela
normalmente revela que há uma conexão ainda fraca entre conceito, prática e decisão de
engenharia.

O primeiro lugar para resolver essa dúvida é
`curriculum/02-nivel-2-practical-patterns/03-rubric-design.md`. Esse arquivo dá o contexto
principal, mostra exemplos no tom do programa e ajuda a separar o que é fundamento do que é
detalhe operacional. Se a resposta ainda parecer abstrata, use
`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` como segunda leitura. A
dupla funciona bem porque um arquivo explica o problema e o outro mostra como o problema
aparece no ecossistema do KODA.

Pense no cenário de KODA assim: uma rubric bloqueia recomendação insegura antes que o cliente
compre produto inadequado. A dúvida deixa de ser acadêmica quando alguém precisa decidir se
uma conversa de WhatsApp deve continuar, ser compactada, ser escalada para humano, ou passar
por um Evaluator antes de chegar ao cliente. Nessa hora, conceitos como Rubric Design, ROI,
Quality Gates e Business Metrics viram ferramentas de trabalho, não vocabulário bonito para
reunião.

O erro comum é medir rubric apenas como nota interna sem ligar a resultado. Esse erro parece
pequeno no começo, mas cria ruído: participantes pulam fundamentos, líderes cobram métricas
antes de definir critérios, mentores corrigem respostas sem descobrir a causa da confusão, e o
time interpreta falhas de agente como falhas de prompt. O currículo tenta evitar isso com
camadas: Nível 1 para raiz do problema, Nível 2 para padrões práticos, Nível 3 para
arquitetura, e Nível 4 para KODA em produção.

A ação recomendada é acompanhar taxa de rejeição, erro residual, conversão e satisfação. Faça
isso de forma visível. Anote o arquivo lido, a pergunta respondida, o exemplo de KODA usado e
a evidência de que a pessoa entendeu. Evidência pode ser um diagrama simples, uma rubric
curta, uma trace comentada, ou uma decisão registrada em Sprint Contract. O importante é não
aceitar sensação de entendimento como conclusão.

O resultado esperado é qualidade técnica traduzida em impacto de negócio. Quando esse
resultado aparece, você percebe a mudança no vocabulário do time. As pessoas deixam de dizer
apenas "o agente ficou confuso" e passam a dizer "a trace mostra perda de estado depois da
compactação", "o Evaluator aprovou sem checar alergia", ou "o Sprint Contract não definiu o
failure mode". Esse é o sinal de que a pergunta foi respondida no nível certo.

**Como aplicar em 10 minutos:**
- Abra `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md` e leia a seção que
  responde diretamente à dúvida.
- Abra `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md` e procure o exemplo
  aplicado ao KODA ou ao conceito relacionado.
- Escreva uma frase começando com "No KODA, isso importa porque...".
- Transforme a frase em uma decisão prática: ler, exercitar, medir, revisar ou escalar.
- Compartilhe a decisão com o grupo para reduzir dúvidas repetidas na próxima sessão.

**Exemplo aplicado ao KODA:**
- Cliente informa uma restrição alimentar no começo da conversa.
- KODA recomenda produtos depois de uma conversa longa, com histórico já grande.
- O time precisa saber se a recomendação depende de memória, rubric, trace ou contrato.
- A resposta correta aponta o arquivo de estudo e a evidência operacional que deve existir.

**Sinais de entendimento:**
- [ ] A pessoa consegue explicar a resposta sem repetir o texto do FAQ palavra por palavra.
- [ ] A pessoa consegue citar um arquivo correto do currículo e por que ele ajuda.
- [ ] A pessoa consegue dar um exemplo realista envolvendo KODA, não apenas um exemplo
      genérico.
- [ ] A pessoa consegue dizer qual seria o próximo passo se a dúvida aparecesse em produção.

**Leituras relacionadas:**
- `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md`
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`
- `curriculum/GLOSSARY.md`
- `curriculum/MASTER_PLAN.md`

---

## 📊 Diagrama de Navegação do FAQ

Use este diagrama como mapa rápido. A FAQ fica no centro porque ela recebe dúvidas vindas de
todos os perfis e aponta para o nível, conceito ou aplicação correta.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FAQ DO CURRÍCULO                                   │
│          perguntas comuns, caminhos de leitura, critérios de avanço         │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
┌────────▼────────┐        ┌─────────▼─────────┐        ┌────────▼────────┐
│ Participantes   │        │ Líderes           │        │ Mentores        │
│ estudo e ritmo  │        │ rollout e ROI     │        │ avaliação       │
└────────┬────────┘        └─────────┬─────────┘        └────────┬────────┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     │
┌────────────────────────────────────▼────────────────────────────────────────┐
│                         CURRICULUM ROOT                                    │
│ README.md  MASTER_PLAN.md  QUICK_START.md  GLOSSARY.md  EXECUTION_PLAN.md  │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       │                             │                             │
┌──────▼──────┐              ┌───────▼───────┐              ┌──────▼──────┐
│ Nível 1     │              │ Nível 2       │              │ Nível 3     │
│ Fundamentos │              │ Padrões       │              │ Arquitetura │
│             │              │               │              │             │
│ Context     │              │ Generator     │              │ Multi-Agent │
│ Window      │              │ Evaluator     │              │ Systems     │
│ Token       │              │ Sprint        │              │ State       │
│ Budgeting   │              │ Contracts     │              │ Persistence │
└──────┬──────┘              └───────┬───────┘              └──────┬──────┘
       │                             │                             │
       └─────────────────────────────┼─────────────────────────────┘
                                     │
                              ┌──────▼──────┐
                              │ Nível 4     │
                              │ KODA        │
                              │ Arquitetura │
                              │ Journeys    │
                              │ Rubrics     │
                              └──────┬──────┘
                                     │
             ┌───────────────────────┼───────────────────────┐
             │                       │                       │
      ┌──────▼──────┐        ┌───────▼───────┐        ┌──────▼──────┐
      │ 05 Core     │        │ 06 Knowledge  │        │ 08 Tools    │
      │ Concepts    │        │ Graphs        │        │ Templates   │
      └──────┬──────┘        └───────┬───────┘        └──────┬──────┘
             │                       │                       │
             └───────────────────────┼───────────────────────┘
                                     │
                              ┌──────▼──────┐
                              │ 09 Cases    │
                              │ KODA e      │
                              │ exemplos    │
                              └─────────────┘
```

A leitura prática do diagrama é simples. Se a dúvida é de orientação, comece no root. Se é de
fundamento, vá para Nível 1. Se envolve qualidade, avaliação ou debug, vá para Nível 2. Se
envolve coordenação, memória persistida ou evolução de harness, vá para Nível 3. Se a pergunta
usa exemplos do WhatsApp, catálogo, checkout ou jornada de cliente, vá para Nível 4.

---

## 📋 Tabela Comparativa: Jornadas de Aprendizado

| Perfil | Nível Inicial | Tempo Estimado | Caminho Recomendado | Resultado Esperado |
|---|---|---:|---|---|
| Iniciante Total | Nível 1 | 12 semanas | `curriculum/QUICK_START.md` → `curriculum/01-nivel-1-fundamentals/` → exercícios → Nível 2 | Entende os problemas fundamentais e aplica padrões simples ao KODA |
| Conhece LLMs | Nível 1 com avanço rápido | 8 a 10 semanas | `curriculum/MASTER_PLAN.md` → revisão de Nível 1 → `curriculum/02-nivel-2-practical-patterns/` | Usa Generator/Evaluator, Sprint Contracts, Rubric Design e Trace Reading com segurança |
| Sênior/Arquiteto | Nível 2 ou 3 após checkpoint | 6 a 8 semanas | `curriculum/MASTER_PLAN.md` → checkpoints → `curriculum/03-nivel-3-advanced-architecture/` → KODA | Desenha arquitetura avançada e avalia trade-offs de harness |
| Líder Técnico | Root + Níveis 1 e 2 | 12 semanas em coorte | `curriculum/EXECUTION_PLAN.md` → `curriculum/08-tools-templates/team-progress-tracker.md` → workshops | Conduz rollout, mede progresso e conecta aprendizado a ROI |
| Mentor | Níveis 1 a 4 com foco em avaliação | Contínuo | `curriculum/08-tools-templates/learning-assessment-rubric.md` → módulos por nível → sessões práticas | Guia participantes, avalia entendimento e transforma dúvidas em aprendizado |

A tabela não é uma regra rígida. Ela é um ponto de partida para conversas de planejamento. O
critério mais importante é evidência: se a pessoa consegue explicar, aplicar e revisar um
conceito com exemplo de KODA, ela pode avançar. Se não consegue, volte ao arquivo certo sem
tratar isso como atraso.

---

## 🚀 Aplicação KODA

A FAQ apoia onboarding de times KODA porque reduz a distância entre currículo e trabalho real.
KODA não é um exemplo decorativo dentro do programa. Ele é o campo de teste onde os conceitos
mostram valor: conversas longas, recomendação de suplementos, restrições alimentares, cálculo
de pedido, checkout, pós-venda e suporte.

Quando uma pessoa nova entra no time, ela pode começar por `curriculum/QUICK_START.md`, usar
esta FAQ para resolver dúvidas de navegação e depois seguir para
`curriculum/04-nivel-4-koda-specific/01-koda-architecture.md`. Esse caminho evita dois
extremos: jogar a pessoa direto em produção sem base, ou prender a pessoa em teoria sem
contato com o produto.

O mapeamento entre perguntas da FAQ e features do KODA deve ser explícito. Perguntas sobre
Context Window apontam para conversas longas no WhatsApp. Perguntas sobre Token Budgeting
apontam para custo e latência. Perguntas sobre Generator/Evaluator apontam para recomendações
de produto. Perguntas sobre Sprint Contracts apontam para fronteiras entre descoberta,
carrinho, estoque e pagamento. Perguntas sobre Rubric Design apontam para segurança,
relevância e clareza da resposta final.

**Mapeamento prático entre dúvidas e features:**
- Dúvidas sobre começo do currículo ajudam onboarding em `curriculum/QUICK_START.md` e reduzem
  tempo até primeira contribuição.
- Dúvidas sobre Context Window ajudam o time a entender por que KODA precisa de memória
  operacional em conversas longas.
- Dúvidas sobre Token Budgeting ajudam a equilibrar qualidade, custo e latência em jornadas
  com muitas mensagens.
- Dúvidas sobre Generator/Evaluator ajudam a proteger recomendações de produto antes de elas
  chegarem ao cliente.
- Dúvidas sobre Sprint Contracts ajudam a definir fronteiras claras entre módulos de catálogo,
  carrinho, estoque e checkout.
- Dúvidas sobre Rubric Design ajudam a transformar critérios como segurança, relevância e tom
  em avaliação reproduzível.
- Dúvidas sobre Trace Reading ajudam suporte e engenharia a explicar por que uma conversa deu
  errado.
- Dúvidas sobre State Persistence ajudam a preservar alergias, preferências, orçamento e
  estado do pedido.
- Dúvidas sobre Harness Evolution ajudam o time a melhorar KODA sem reescrever tudo de uma
  vez.

No ecossistema de documentação, esta FAQ fica entre os documentos de entrada e os módulos
profundos. `curriculum/README.md` apresenta o programa. `curriculum/MASTER_PLAN.md` organiza a
estratégia. `curriculum/EXECUTION_PLAN.md` ajuda líderes a planejar. `curriculum/GLOSSARY.md`
define termos. Esta FAQ responde as dúvidas que aparecem quando esses documentos encontram a
realidade de uma equipe aprendendo enquanto trabalha.

Para KODA, o valor maior é consistência. Uma resposta de FAQ bem usada evita que cada pessoa
invente seu próprio caminho. O time passa a discutir com a mesma base: qual conceito está em
jogo, qual arquivo explica melhor, qual exemplo de KODA prova o ponto, e qual evidência mostra
que a decisão funcionou.

---

## 📝 O Que Você Aprendeu

Se você leu esta FAQ com atenção, já tem um mapa prático para orientar participantes, líderes,
mentores e pessoas técnicas dentro do currículo. Mais importante: você viu que perguntas
frequentes não são interrupções. Elas são sinais de navegação. Cada dúvida mostra onde o
programa precisa conectar melhor conceito, exemplo e decisão.

**Checklist de takeaways:**
- [ ] Se a dúvida é sobre começo, use `curriculum/QUICK_START.md` e valide o caminho pelo
      perfil da pessoa.
- [ ] Se a dúvida é sobre estratégia, use `curriculum/MASTER_PLAN.md` e conecte o tópico aos 4
      níveis.
- [ ] Se a dúvida é sobre agenda, rollout ou acompanhamento, use
      `curriculum/EXECUTION_PLAN.md` e os templates em `curriculum/08-tools-templates/`.
- [ ] Se a dúvida é sobre termo técnico, use `curriculum/GLOSSARY.md` antes de discutir
      arquitetura.
- [ ] Se a dúvida é sobre falha de agente, volte ao Nível 1 e identifique o problema raiz.
- [ ] Se a dúvida é sobre qualidade, avaliação ou debug, procure os módulos de Nível 2.
- [ ] Se a dúvida é sobre coordenação, memória ou evolução de sistema, procure os módulos de
      Nível 3.
- [ ] Se a dúvida envolve WhatsApp, suplemento, jornada do cliente ou feature real, procure
      Nível 4.
- [ ] Se uma pergunta aparece muitas vezes, trate como dado para melhorar facilitação e
      mentoria.
- [ ] Se alguém diz que entendeu, peça uma evidência pequena: exemplo KODA, trace, rubric,
      contrato ou decisão.

> "Uma boa FAQ não elimina perguntas. Ela ensina o time a fazer perguntas melhores."

O próximo passo é simples. Escolha a pergunta que mais parece com sua situação atual. Abra o
arquivo recomendado. Use um exemplo real de KODA. Depois registre a resposta em uma frase
prática. Se essa frase ajudar outra pessoa do time, a FAQ cumpriu seu papel.


**Próximos passos recomendados:**
- Participantes: abrir `curriculum/QUICK_START.md` e escolher seu caminho de leitura.
- Líderes: abrir `curriculum/EXECUTION_PLAN.md` e reservar a primeira cadência de estudo.
- Mentores: abrir `curriculum/08-tools-templates/learning-assessment-rubric.md` e preparar uma
  sessão curta de avaliação.
- Pessoas técnicas: escolher uma feature KODA e mapear quais conceitos do currículo aparecem
  nela.
- Time completo: revisar dúvidas repetidas após a primeira semana e atualizar a facilitação da
  próxima sessão.

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | FAQ.md |
| **Nível** | Todos os Níveis |
| **Tempo** | 30 min |
| **Status** | ✅ Completo |
| **Atualizado** | Maio 2026 |

*FAQ do Currículo Long-Running Agents | FutanBear | v1.0 | Maio 2026*
