# Reescrita do README.md — Plano de Execução

**Objetivo:** Reescrever `README.md` para refletir o estado real do repositório (85+ padrões canônicos, harnees, dashboards, novos diretórios) e comunicar com clareza o motivo de existir, o que há aqui, como navegar e o que é possível fazer.
**Fase:** Implementação
**Dependências:** Nenhuma (trabalho autocontido em um arquivo)
**Duração estimada:** 2h

---

## Diagnóstico de gaps (linha de base)

O README atual (`README.md:1-141`) está defasado em múltiplas dimensões:

| Afirmação no README | Realidade | Severidade |
|---|---|---|
| "16 padrões canônicos ativos" (L55) | `docs/canonical/` tem 85 arquivos | Crítico |
| Árvore de diretórios (L34-77) | Omite `concepts/`, `dashboards/`, `harness/`, `templates/`, `sources/`, `docs/articles/`, `webpage/`, `mapa-mental-repo/`, `eslint-rules/` | Crítico |
| "10 skills" em `.opencode/` (L64) | São 25+ skills | Médio |
| Tabela de padrões (L94-104) lista 8 de 85+ | Cobertura < 10% | Crítico |
| Sem menção ao sistema de harness (`harness/`) | Pipeline analyze-and-improve com 7 fases existe | Alto |
| Sem menção a dashboards (`dashboards/`) | 3 dashboards Obsidian ativos | Médio |
| Sem menção a artigos (`docs/articles/`) | 4 artigos publicados | Baixo |
| Sem menção ao `index.md` (knowledge index) | Mapa completo de wikilinks existe | Médio |
| Stack não menciona `obsidian-eval` | Ferramenta core de runtime | Médio |

---

### Tarefa 1: Estrutura-alvo do novo README

**Artefatos:**
- Entrada: README atual, `docs/system-of-record.md`, `index.md`, inventário de diretórios
- Saída: Esqueleto markdown com seções definidas e hierarquia aprovada

- [ ] **Passo 1: Definir seções do novo README**
  Decisões de design a tomar:
  - Manter ou substituir a árvore ASCII de diretórios (34-77)?
  - A tabela "Navegue pelo seu perfil" (L20-30) permanece ou é substituída?
  - Os 8 padrões canônicos listados (L94-104) viram uma seção "Principais padrões" com ~12 destaques ou a lista completa?
  - O currículo em 4 níveis (L80-87) é movido para o `curriculum/README.md` e referenciado de forma enxuta aqui?
  
  Estrutura proposta:
  1. Bloco de abertura: o que é + grande motivo de existir (2-3 parágrafos)
  2. O problema que atacamos (manter, refinar)
  3. Para quem é (manter, atualizar)
  4. O que você encontra aqui — mapa de navegação visual substituindo a árvore ASCII
  5. Padrões canônicos — highlights (12-15 mais relevantes para builders) + link para lista completa
  6. O que é possível fazer — casos de uso concretos
  7. Quick start (manter, atualizar stack)
  8. Governança (manter, enxugar)

  Comando: Leitura comparativa de `index.md` e `docs/system-of-record.md` para garantir consistência.
  Esperado: Esqueleto com seções numeradas e 1-2 frases descrevendo o conteúdo de cada uma.

- [ ] **Passo 2: Validar esqueleto contra system-of-record**
  Comando: Conferir que toda seção nova referencia domínios e fontes listados em `docs/system-of-record.md`.
  Esperado: Cada seção do README mapeia para um domínio do SOR ou é intencionalmente "porta de entrada" (não requer entrada no SOR).

- [ ] **Verificação**
  Critério: Esqueleto aprovado — seções não conflitam com `docs/system-of-record.md`, não duplicam conteúdo de `curriculum/README.md` ou `index.md`, e cobrem os 4 pedidos do usuário (motivo, conteúdo, navegação, possibilidades).

---

### Tarefa 2: Redação do conteúdo

**Artefatos:**
- Entrada: Esqueleto da Tarefa 1, inventário de diretórios, system-of-record
- Saída: `README.md` completo com todas as seções preenchidas

- [ ] **Passo 1: Escrever seção de abertura (grande motivo de existir)**
  Comando: Redigir 2-3 parágrafos que respondam "por que este repositório existe?" — conectando o problema (agentes falham em execuções longas) com a solução (harness engineering + padrões canônicos + currículo), e declarando a tese central: confiabilidade em agentes não é questão de modelo melhor, é questão de engenharia de harness.
  Esperado: Texto que alguém lendo pela primeira vez entende o propósito em 30 segundos.

- [ ] **Passo 2: Reescrever mapa de navegação (substituir árvore ASCII)**
  Comando: Criar uma seção "O que você encontra aqui" organizada por domínio funcional (não por diretório), com links para os pontos de entrada. Incluir todos os diretórios novos.
  Esperado: Um leitor consegue identificar em 15 segundos onde está o que procura.

- [ ] **Passo 3: Atualizar destaques de padrões canônicos**
  Comando: Selecionar 12-15 padrões de maior relevância para builders de negócio (cobrindo context engineering, harness, evals, governança) e apresentar em tabela com problema que resolve. Adicionar link para `docs/system-of-record.md` com a lista completa.
  Esperado: Tabela cobre domínios principais sem sobrecarregar; link para lista completa é funcional.

- [ ] **Passo 4: Adicionar seção "O que é possível fazer"**
  Comando: Descrever 4-5 casos de uso concretos: (1) estudar o currículo e aplicar padrões no seu sistema, (2) usar os padrões canônicos como referência de arquitetura, (3) rodar o pipeline analyze-and-improve com o harness, (4) navegar os dashboards e knowledge graphs, (5) usar o sistema `.opencode/` como template para seu próprio agente.
  Esperado: Cada caso de uso tem 1-2 frases e link para o ponto de entrada relevante.

- [ ] **Passo 5: Atualizar Quick Start e Stack**
  Comando: Adicionar `obsidian-eval` na stack, verificar que comandos quick start ainda funcionam, remover ou atualizar menções obsoletas.
  Esperado: `npm run lint` e `npm run test:unit` executam sem erro.

- [ ] **Passo 6: Revisar e enxugar seções mantidas**
  Comando: Revisar "O problema que atacamos", "Para quem é", "Governança" — cortar redundâncias, atualizar números, garantir que links funcionam.
  Esperado: Seções mantidas são concisas e atualizadas.

- [ ] **Verificação**
  Critério: `README.md` completo, todos os links internos funcionam (verificar com `rg` para wikilinks quebrados), números de arquivos/diretórios conferem com `ls` e `find`.

---

### Tarefa 3: Verificação e validação

**Artefatos:**
- Entrada: `README.md` reescrito
- Saída: README validado e pronto para commit

- [ ] **Passo 1: Verificar links internos**
  Comando: `rg '\[\[.*\]\]' README.md` para listar wikilinks; para cada um, verificar que o arquivo alvo existe.
  Comando alternativo: `rg '\]\(.*\.md\)' README.md` para links markdown.
  Esperado: Zero links quebrados.

- [ ] **Passo 2: Verificar consistência com system-of-record**
  Comando: Leitura cruzada de `docs/system-of-record.md` — conferir que números (85 padrões, 25+ skills, 35+ diagramas) batem com o README.
  Esperado: Nenhuma contradição factual entre README e SOR.

- [ ] **Passo 3: Verificar links externos**
  Comando: Para cada URL `https://` no README, verificar com `curl -sI` que retorna 2xx ou 3xx.
  Esperado: Zero links quebrados para fora do repo.

- [ ] **Passo 4: Linter e testes**
  Comando: `npm run lint && npm run test:unit` no diretório do repositório.
  Esperado: Ambos passam (mudança é só em markdown, não deve quebrar nada).

- [ ] **Verificação**
  Critério: Todos os checks acima passam. README está pronto para ser commitado.

---

## Análise por Eixo

### Eixo 1 — Verificação e dependências
A mudança é autocontida em um arquivo (`README.md`). Não altera dependências, scripts de build, ou contratos de API. O gate de conclusão são os 4 checks da Tarefa 3: links internos funcionais, consistência com `system-of-record.md`, links externos válidos, lint e testes passando. Nenhuma dependência externa é afetada.

### Eixo 2 — Manutenção futura
O risco de retrabalho é baixo: o README é porta de entrada, não fonte autoritativa (precedência 6 no SOR). Se novos diretórios ou padrões canônicos forem adicionados, o README precisará de atualização pontual — mas isso já é verdade hoje e o gap atual (16 vs 85) mostra que a manutenção não aconteceu. A solução proposta reduz o custo de manutenção ao usar links para fontes autoritativas (`system-of-record.md`, `index.md`) em vez de duplicar listas. Números específicos (ex: "85 padrões") devem ser evitados quando possível, substituídos por "85+" ou referências ao SOR.

### Eixo 3 — Impacto arquitetural
A mudança não altera componentes compartilhados, padrões de arquitetura, ou fluxo de dados. Não requer ADR — é documentação de porta de entrada, não decisão arquitetural. Alinha-se com o roadmap ao refletir o estado real do repositório, facilitando onboarding e descoberta. O único cuidado é não contradizer o `system-of-record.md`, que tem precedência superior.
