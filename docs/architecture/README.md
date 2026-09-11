---
title: "Monitor de arquitetura — primeira versão"
type: reference
tags: ["agentes-orquestracao", "governanca", "index"]
aliases: ["monitor de arquitetura", "mapa do repositorio"]
relates-to: ["[[README|Repository Home]]", "[[docs/system-of-record|System of Record]]", "[[AGENTS|Agent Rules]]"]
---

# Monitor de arquitetura

Primeira versão para mapear um repositório e revisar a evolução dos seus componentes.
O mapa é um retrato de um commit. O agente revisa a semântica; a ferramenta calcula
o diff e gera a página. A execução sob demanda continua disponível. O
[[docs/architecture/scheduled-review|fluxo diário com OpenCode]] acrescenta um timer
local, revisão validada e entrega por PR, usando a autenticação existente.

Abra [a visão geral](index.html). A fonte editável é
[repository-map.json](repository-map.json). Há oito componentes e oito relações,
com links para evidências no commit `b1ee8d415f9e0536c29cadeecda3a025d4f4cebf`.
O foco é a base de conhecimento, currículo e pipeline presentes neste repositório.

## Uso

Na raiz do Long Running Agents:

```bash
npm run architecture:validate
npm run architecture:check
npm run test:architecture
```

Para gerar HTML limpo em arquivo, use diretamente o script (sem o banner do npm):

```bash
node scripts/architecture-monitor.js render > /tmp/architecture-preview.html
```

`--output caminho` cria um arquivo novo; recusa sobrescrever arquivo existente.
Depois de conferir uma prévia, o agente pode atualizar `docs/architecture/index.html`.
Para JSON consumido por outras ferramentas, use também diretamente o script ou
`npm run --silent architecture:check`.

```bash
node scripts/architecture-monitor.js check --ref HEAD --output /tmp/architecture-review.json
node /home/pavanpavan/long-running-agents/scripts/architecture-monitor.js check \
  --repo /caminho/outro-repositorio --map docs/architecture/repository-map.json
```

O outro repositório precisa de um mapa próprio. O renderizador desta versão usa links
de evidência GitHub; clones locais são lidos sem acesso à rede.

## Executar o agente

A definição segue o formato dos agentes locais em
[[.opencode/agents/repository-architecture-monitor|repository-architecture-monitor]].
Selecione esse agente no host OpenCode e peça:

> Revise o mapa de arquitetura deste repositório até HEAD. Registre as decisões por
> arquivo e atualize o JSON e a página quando houver evidência suficiente.

O mesmo procedimento pode ser executado pelo agente da sessão atual lendo a definição.
A primeira análise foi feita na sessão de implementação. A extensão agendada usa
essa definição no OpenCode; seus fluxos, limites e comandos operacionais estão em
[[docs/architecture/scheduled-review|Revisão diária de arquitetura]].

## Contrato mínimo

- `version: 1`, `repository`: URL GitHub, `commit`: SHA completo analisado.
- `title`, `summary`, `focus` opcional e `limitations` opcionais.
- `components`: `id`, `name`, `responsibility`, `paths`, `row`, `column`, `evidence`.
- `relations`: `id`, `from`, `to`, `label`, `description`, `evidence`.
- Evidência: `path`, `start`, `end`, com linhas inclusivas, verificadas no commit.
- Escopo com `/` final cobre uma pasta; os demais caminhos são arquivos exatos.
- Até nove componentes, doze relações e uma grade de três linhas por três colunas.
  Conectores unem células vizinhas. O renderer recusa layouts que não suporta.

O HTML é determinístico e derivado do JSON: não o edite manualmente. Tem fontes locais,
SVG acessível, detalhes textuais e links para a revisão exata de cada arquivo.
A composição é inspirada no
[Diagram Design](https://github.com/cathrynlavery/diagram-design/tree/562dbdf93ff3c3da630be4f90f4f6c2548175058),
sem instalar o plugin nem copiar seus templates. Não é uma integração com sua CLI.

## Revisão incremental

`check` compara árvores commitadas e retorna `no-committed-changes` ou
`review-required`. Ambos são resultados normais (exit 0); erro de entrada ou Git
retorna exit não zero. Consumidores devem ler `status`, não usar exit 0 como
aprovação arquitetural. `workingTreeDirty` informa edições locais excluídas.

Cada caminho alterado aponta componentes e relações potencialmente afetados.
Arquivos sem associação recebem `unmapped: true`; o agente deve revisá-los também.
Renomes viram remoção e adição para preservar as duas pontas da investigação.
O comando não faz fetch nem altera o mapa ou seu commit. `--ref` também permite
comparar branches; o resultado é diferença de árvores, não histórico de eventos.

O agente registra decisões em `docs/architecture/reviews/<target-sha>.json`.
Ele só avança o commit do mapa após revisar toda a fila e conferir as evidências no
alvo. Itens incertos mantêm a base anterior. A validação estrutural não substitui
a revisão de significado e não comprova completude do mapa.

## Plano e critério de conclusão

1. Mapear o commit inicial → conferir arquivos, linhas e distinção entre documentação
   e implementação local.
2. Gerar a visão HTML/SVG → saída reproduzível e todas as relações acessíveis em texto.
3. Preparar o agente incremental → procedimento de revisão e registro explícito.
4. Testar o detector → mudanças, novos arquivos, exclusões, renomes, escopos exatos,
   edição local e evidências inválidas em um repositório temporário.
5. Exercitar uma mudança real do histórico → registrar se altera ou não a arquitetura.

## Resultado do primeiro experimento

- Mapa inicial validado: oito componentes e oito relações no commit indicado.
- HTML renderizado e inspecionado em Chromium headless, com evidências navegáveis.
- Sete testes exercitam o detector, validação, CLI, renderização e atualização de uma
  relação após revisão explícita em repositório temporário.
- A atualização real de `obsidian-eval` entre `d01c70c` e `b1ee8d4` gerou dois
  candidatos (`package.json` e lockfile), associados a governança. O diff foi lido
  pelo agente da sessão: não alterou componentes ou relações nesta visão geral.
  [Registro da revisão](reviews/b1ee8d415f9e0536c29cadeecda3a025d4f4cebf.json).
- O lint dos arquivos novos passou. `npm run lint` permanece bloqueado pela
  configuração preexistente que procura `src/`, ausente neste checkout.

O teste histórico foi retrospectivo; a revisão semântica foi realizada nesta sessão.
O teste de remoção de relação simula a edição explícita do agente, sem chamar um LLM.
Esse experimento inicial antecede a extensão agendada com OpenCode.

A primeira versão foi integrada à `main` no commit `a069c11`. A extensão agendada
mantém a publicação em PR separado, sem integração automática na `main`.
