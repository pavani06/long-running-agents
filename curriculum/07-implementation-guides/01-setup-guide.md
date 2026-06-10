---
title: "Guia de Setup: Preparando o Terreno para Long-Running Agents"
type: curriculum-guide
aliases: []
tags: [curriculo-conteudo, guia-implementacao, setup, infraestrutura, ambiente-de-desenvolvimento, estrutura-de-repositorio, dependencias, configuracao, onboarding, automacao]
relates-to: ["[[curriculum/QUICK_START|Quick Start]]", "[[README|Repository README]]"]
last_updated: 2026-06-10
---
# 🛠️ Guia de Setup: Preparando o Terreno para Long-Running Agents
## Da Máquina Limpa ao Primeiro Agente Funcional em 90 Minutos

**Tempo Estimado:** 90 minutos (leitura + execução)
**Nível:** Guia de Implementação (Independente)
**Pré-requisito:** Nenhum — conhecimento básico de terminal e Python
**Status:** 🟢 GUIA PRÁTICO — Infraestrutura para todos os níveis
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: O Momento em que Tudo Começa

Você acabou de ser nomeado líder técnico de um projeto de long-running agents. Sua equipe está animada. O roadmap está claro. A visão é ambiciosa: construir agentes que operam por horas, mantendo contexto, tomando decisões confiáveis, escalando com elegância.

Mas antes de qualquer linha de código de produção, você enfrenta o primeiro desafio real:

**Como montar o ambiente?**

Não é uma pergunta trivial. Long-running agents não são um script simples. São sistemas complexos que exigem:

- Múltiplos agentes colaborando
- Persistência de estado entre sessões
- Orquestração de ferramentas e APIs
- Logging e tracing para debugging
- Estrutura de arquivos que escala com o projeto

E aqui está a armadilha clássica: **começar sem estrutura**.

Já vi times talentosos perderem semanas porque:
- ❌ Misturaram código de produção com experimentos
- ❌ Não tinham convenção de nomes para arquivos de estado
- ❌ Não sabiam quais logs olhar quando algo falhava
- ❌ Cada desenvolvedor usava uma estrutura diferente
- ❌ Ferramentas de observabilidade eram configuradas de forma inconsistente

**Este guia existe para que você não cometa esses erros.**

Em 90 minutos, você vai:
1. Estruturar um repositório que escala do protótipo à produção
2. Configurar o ambiente de desenvolvimento completo
3. Instalar e validar todas as dependências
4. Criar seu primeiro agente funcional (hello world)
5. Rodar um checklist de verificação de setup

E ao final, você terá **não apenas um ambiente funcionando**, mas um **padrão reproduzível** que sua equipe inteira pode seguir.

### O Que Este Guia NÃO É

- ❌ Não é um tutorial de Python ou JavaScript
- ❌ Não é documentação de API da Anthropic
- ❌ Não é um guia de arquitetura avançada (isso está nos Níveis 1-4)
- ❌ Não substitui a leitura dos conceitos fundamentais

### O Que Este Guia É

- ✅ Um manual prático, passo a passo, para montar seu ambiente
- ✅ Um template de estrutura de repositório que você pode clonar
- ✅ Um conjunto de scripts de verificação que garantem que tudo funciona
- ✅ Um ponto de partida para qualquer projeto de long-running agents

---

## 🏗️ Seção 1: Estrutura de Repositório Recomendada

### O Princípio da Separação de Concerns

Antes de criar pastas, entenda o princípio fundamental:

```
"Um diretório deve ter UMA responsabilidade clara.
 Se você não consegue descrever o que uma pasta contém
 em uma frase curta, ela está fazendo coisa demais."
```

Este princípio evita o "monolito de pastas" — aquele diretório `src/` com 47 arquivos misturando lógica de negócio, utilitários, configuração e experimentos descartados.

### A Estrutura Canônica

```
seu-projeto-long-running-agents/
│
├── README.md                        # Porta de entrada do projeto
├── AGENTS.md                        # Regras para agentes AI no repo
├── .env.example                     # Template de variáveis de ambiente
├── .gitignore                       # Arquivos ignorados pelo git
├── package.json / pyproject.toml    # Dependências e scripts
│
├── src/                             # Código fonte principal
│   ├── agents/                      # Definições de agentes
│   │   ├── base_agent.py           # Classe base para todos agentes
│   │   ├── generator.py            # Exemplo: agente gerador
│   │   └── evaluator.py            # Exemplo: agente avaliador
│   │
│   ├── orchestration/              # Orquestração entre agentes
│   │   ├── pipeline.py             # Pipeline Generator → Evaluator
│   │   ├── router.py               # Roteamento de tarefas
│   │   └── scheduler.py            # Agendamento de execuções
│   │
│   ├── persistence/                # Persistência de estado
│   │   ├── state_manager.py        # Gerenciador de arquivos de estado
│   │   ├── file_store.py           # Leitura/escrita de JSON
│   │   └── context_cache.py        # Cache de contexto do cliente
│   │
│   ├── tools/                      # Ferramentas que agentes usam
│   │   ├── search_tool.py          # Busca em catálogo
│   │   ├── calculator_tool.py      # Cálculos (preço, desconto)
│   │   └── api_client.py           # Cliente HTTP para APIs externas
│   │
│   ├── evaluation/                 # Avaliação de qualidade
│   │   ├── rubric_engine.py        # Motor de rubricas
│   │   ├── metrics.py              # Métricas (precisão, recall)
│   │   └── test_harness.py         # Harness de testes
│   │
│   └── config/                     # Configuração centralizada
│       ├── settings.py             # Configurações do projeto
│       ├── model_config.py         # Configurações de LLM
│       └── logging_config.py       # Configuração de logging
│
├── state/                          # Estado runtime (não commitado)
│   └── {customer_id}/             # Um diretório por cliente/sessão
│       ├── context.json           # Contexto imutável do cliente
│       ├── draft_v1.json          # Rascunho do generator (v1)
│       ├── verdict_v1.json        # Veredito do evaluator (v1)
│       ├── feedback_v1.json       # Feedback se rejeitado
│       └── audit_log.jsonl        # Log imutável de eventos
│
├── tests/                          # Testes automatizados
│   ├── unit/                       # Testes unitários
│   │   ├── test_agents.py
│   │   ├── test_orchestration.py
│   │   └── test_persistence.py
│   │
│   ├── integration/                # Testes de integração
│   │   ├── test_pipeline.py
│   │   └── test_end_to_end.py
│   │
│   └── fixtures/                   # Dados de teste
│       ├── sample_customer.json
│       └── sample_products.json
│
├── logs/                           # Logs de execução
│   ├── agent_traces/              # Traces individuais de agentes
│   └── system/                    # Logs do sistema
│
├── scripts/                        # Scripts operacionais
│   ├── setup.sh                   # Script de setup inicial
│   ├── verify_environment.sh      # Script de verificação
│   └── run_hello_world.sh         # Script do primeiro agente
│
├── docs/                           # Documentação
│   ├── architecture/              # Decisões de arquitetura
│   ├── guides/                    # Guias de uso
│   └── decisions/                 # ADRs (Architecture Decision Records)
│
└── curriculum/                     # Material de treinamento
    └── (níveis 1-4, conceitos, guias)
```

### Por que Esta Estrutura Funciona

Cada diretório tem um propósito cristalino:

| Diretório | Responsabilidade | Quem USA |
|-----------|-----------------|----------|
| `src/agents/` | Definição de agentes individuais | Desenvolvedores |
| `src/orchestration/` | Coordenação entre agentes | Desenvolvedores |
| `src/persistence/` | Estado que sobrevive a sessões | Sistema runtime |
| `src/tools/` | Ferramentas usadas por agentes | Agentes |
| `src/evaluation/` | Métricas e qualidade | QA/Tech Leads |
| `src/config/` | Configuração centralizada | Todos |
| `state/` | Dados runtime por sessão | Sistema runtime |
| `tests/` | Garantia de qualidade | CI/CD |
| `logs/` | Observabilidade | DevOps/Debugging |
| `scripts/` | Automação operacional | Todos |
| `docs/` | Conhecimento compartilhado | Todos |

### O que NÃO colocar no repositório

```
NUNCA COMMITAR:
├── .env                    # Contém secrets reais
├── state/*                 # Dados de runtime de clientes
├── logs/*                  # Logs de execução local
├── __pycache__/            # Cache Python
├── node_modules/           # Dependências Node
├── venv/                   # Ambiente virtual Python
├── .vscode/ (dados locais) # Configurações pessoais de IDE
└── *.pyc                   # Bytecode Python compilado
```

### O .gitignore Essencial

```gitignore
# Secrets e ambiente
.env
.env.local
*.secret

# Estado runtime (dados de cliente)
state/

# Logs
logs/
*.log

# Dependências
node_modules/
__pycache__/
*.pyc
*.pyo
venv/
.venv/

# IDE local
.vscode/settings.json
.idea/

# Build artifacts
dist/
build/
*.egg-info/

# OS
.DS_Store
Thumbs.db
```

---

## 📦 Seção 2: Requisitos de Sistema e Dependências

### Requisitos Mínimos de Sistema

Antes de instalar qualquer coisa, verifique se sua máquina atende aos requisitos:

| Componente | Mínimo | Recomendado | Por que? |
|------------|--------|-------------|----------|
| **Sistema Operacional** | macOS 12+, Ubuntu 22.04+, Windows 11 WSL2 | Ubuntu 24.04 LTS | Compatibilidade com ferramentas |
| **RAM** | 8 GB | 16 GB+ | Múltiplos processos, modelos locais |
| **CPU** | 4 cores | 8+ cores | Execução paralela de agentes |
| **Disco** | 20 GB livre | 50 GB+ SSD | Logs, state files, dependências |
| **Python** | 3.10+ | 3.12+ | Suporte a features modernas |
| **Node.js** | 18.x+ | 20.x+ | Ferramentas de build e scripting |
| **Git** | 2.40+ | 2.44+ | Worktrees e branches |

### Verificando seu Sistema

Execute este script de diagnóstico antes de começar:

```bash
#!/bin/bash
# diagnose_system.sh — Verifica se seu sistema está pronto

echo "=== DIAGNÓSTICO DE SISTEMA ==="
echo ""

# OS
echo "Sistema Operacional:"
uname -a
echo ""

# RAM
echo "Memória RAM:"
free -h 2>/dev/null || vm_stat 2>/dev/null || echo "  (não foi possível detectar)"
echo ""

# CPU
echo "CPU Cores:"
nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "  (não foi possível detectar)"
echo ""

# Disco
echo "Espaço em Disco:"
df -h . 2>/dev/null || echo "  (não foi possível detectar)"
echo ""

# Python
echo "Python:"
python3 --version 2>/dev/null || echo "  Python 3 NÃO encontrado — instale python >= 3.10"
echo ""

# Node.js
echo "Node.js:"
node --version 2>/dev/null || echo "  Node.js NÃO encontrado — instale node >= 18"
echo ""

# Git
echo "Git:"
git --version 2>/dev/null || echo "  Git NÃO encontrado — instale git >= 2.40"
echo ""

# Verificar internet
echo "Conectividade:"
curl -s -o /dev/null -w "%{http_code}" https://api.anthropic.com 2>/dev/null | grep -q "401\|200" && echo "  Internet: OK" || echo "  Internet: FALHA — verifique conexão"
echo ""

echo "=== DIAGNÓSTICO CONCLUÍDO ==="
```

### Dependências Core

#### Python (Ambiente Principal)

```bash
# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Instale as dependências core
pip install "anthropic>=0.39.0"      # API Anthropic (Claude)
pip install "openai>=1.50.0"         # API OpenAI (opcional)
pip install "pydantic>=2.0"          # Validação de dados
pip install "python-dotenv>=1.0"     # Carregar .env
pip install "structlog>=24.0"        # Logging estruturado
pip install "rich>=13.0"             # Output colorido no terminal
pip install "pytest>=8.0"            # Testes
pip install "pytest-asyncio>=0.24"   # Testes assíncronos

# Alternativa: criar requirements.txt e instalar de uma vez
# (veja o bloco requirements.txt abaixo)
```

#### requirements.txt (para instalação reproduzível)

Crie `requirements.txt` na raiz do projeto:

```text
# requirements.txt — Dependências Python do projeto

# API de LLMs
anthropic>=0.39.0
openai>=1.50.0

# Validação e Configuração
pydantic>=2.0
python-dotenv>=1.0

# Logging e Output
structlog>=24.0
rich>=13.0

# Testes
pytest>=8.0
pytest-asyncio>=0.24
pytest-cov>=5.0
```

Depois instale tudo com um comando:

```bash
pip install -r requirements.txt
```

#### Node.js (Ferramentas Auxiliares)

```bash
# Inicialize se ainda não tiver package.json
npm init -y

# Ferramentas de desenvolvimento
npm install --save-dev \
  eslint \
  prettier \
  nodemon

# Ferramentas de projeto (opcional)
npm install dotenv
```

#### Ferramentas de Sistema

```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install -y \
  build-essential \
  curl \
  wget \
  jq \
  tree \
  htop

# macOS
brew install \
  jq \
  tree \
  htop \
  wget
```

### Variáveis de Ambiente (.env)

Crie um arquivo `.env.example` (que PODE ser commitado):

```bash
# .env.example — Template de variáveis de ambiente
# Copie para .env e preencha com seus valores reais

# === API Keys (OBRIGATÓRIO) ===
# Anthropic (Claude) — https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# OpenAI (opcional, para modelos alternativos)
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# === Configuração do Projeto ===
# Ambiente: development | staging | production
APP_ENV=development

# Nível de log: DEBUG | INFO | WARNING | ERROR
LOG_LEVEL=INFO

# Diretório de estado (onde agentes salvam arquivos)
STATE_DIR=./state

# === Configuração de Agentes ===
# Modelo padrão para agentes
DEFAULT_MODEL=claude-sonnet-4-6

# Máximo de tokens por chamada
DEFAULT_MAX_TOKENS=2000

# Temperatura padrão (0.0 = determinístico, 1.0 = criativo)
DEFAULT_TEMPERATURE=0.7

# Máximo de iterações do loop Generator/Evaluator
MAX_RETRY_ITERATIONS=3

# === Configuração de Logging ===
# Diretório de logs
LOG_DIR=./logs

# Formato: json | text
LOG_FORMAT=json

# === Configuração de Observabilidade ===
# Ativar trace detalhado? (custa tokens extras)
ENABLE_DETAILED_TRACING=false

# === Configurações Específicas do Projeto ===
# Ex: KODA
KODA_CATALOG_API_URL=https://api.koda.example.com/v1/catalog
KODA_INVENTORY_API_URL=https://api.koda.example.com/v1/inventory
```

### Validando as Dependências

Crie um script `scripts/verify_dependencies.sh`:

```bash
#!/bin/bash
# verify_dependencies.sh — Confirma que todas dependências estão instaladas

echo "=== VERIFICAÇÃO DE DEPENDÊNCIAS ==="
ERRORS=0

# Python packages
echo ""
echo "Python packages:"
for pkg in anthropic openai pydantic dotenv structlog rich pytest; do
    if python3 -c "import ${pkg}" 2>/dev/null; then
        echo "  ✅ ${pkg}"
    else
        echo "  ❌ ${pkg} — NÃO INSTALADO"
        ERRORS=$((ERRORS + 1))
    fi
done

# Node tools
echo ""
echo "Node tools:"
for tool in eslint prettier; do
    if npx ${tool} --version 2>/dev/null; then
        echo "  ✅ ${tool}"
    else
        echo "  ⚠️  ${tool} — não encontrado (opcional)"
    fi
done

# System tools
echo ""
echo "System tools:"
for tool in curl jq tree git; do
    if command -v ${tool} &> /dev/null; then
        echo "  ✅ ${tool}"
    else
        echo "  ❌ ${tool} — NÃO INSTALADO"
        ERRORS=$((ERRORS + 1))
    fi
done

# .env file
echo ""
echo "Configuração:"
if [ -f .env ]; then
    echo "  ✅ .env existe"
    if grep -q "ANTHROPIC_API_KEY=sk-ant-" .env; then
        # Rejeita placeholder (ex: sk-ant-xxxxxxxxxxxxx)
        if grep -q "xxxx" .env; then
            echo "  ❌ ANTHROPIC_API_KEY contém placeholder (xxxxxxxxxxxxx)"
            echo "     Substitua pela sua key real em .env"
            ERRORS=$((ERRORS + 1))
        else
            echo "  ✅ ANTHROPIC_API_KEY configurada"
        fi
    else
        echo "  ❌ ANTHROPIC_API_KEY NÃO configurada em .env"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  ❌ .env NÃO encontrado — copie de .env.example"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "=== ✅ TODAS AS DEPENDÊNCIAS VERIFICADAS ==="
else
    echo "=== ❌ ${ERRORS} ERRO(S) ENCONTRADO(S) ==="
    echo "Corrija os erros acima antes de continuar."
fi
```

---

## ⚙️ Seção 3: Configuração do Ambiente de Desenvolvimento

### Estrutura de Configuração Centralizada

Em vez de espalhar `os.environ.get()` pelo código, centralize toda configuração:

```python
# src/config/settings.py
"""Configuração centralizada do projeto."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env apenas em desenvolvimento
if os.getenv("APP_ENV", "development") == "development":
    load_dotenv()

# Paths base
PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_DIR = Path(os.getenv("STATE_DIR", str(PROJECT_ROOT / "state")))
LOG_DIR = Path(os.getenv("LOG_DIR", str(PROJECT_ROOT / "logs")))


class Settings:
    """Configurações imutáveis carregadas do ambiente."""

    # Ambiente
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")

    # APIs
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Agentes
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-6")
    DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "2000"))
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    MAX_RETRY_ITERATIONS: int = int(os.getenv("MAX_RETRY_ITERATIONS", "3"))

    # Tracing
    ENABLE_DETAILED_TRACING: bool = (
        os.getenv("ENABLE_DETAILED_TRACING", "false").lower() == "true"
    )

    # Paths
    STATE_DIR: Path = STATE_DIR
    LOG_DIR: Path = LOG_DIR

    @classmethod
    def validate(cls) -> list[str]:
        """Valida configurações obrigatórias. Retorna lista de erros."""
        errors = []
        if not cls.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY não configurada")
        if cls.DEFAULT_MAX_TOKENS < 100:
            errors.append("DEFAULT_MAX_TOKENS muito baixo (< 100)")
        if not (0.0 <= cls.DEFAULT_TEMPERATURE <= 2.0):
            errors.append("DEFAULT_TEMPERATURE fora do range [0.0, 2.0]")
        return errors


# Singleton de configuração
settings = Settings()
```

```python
# src/config/logging_config.py
"""Configuração centralizada de logging."""

import structlog
import logging
import json
from pathlib import Path
from src.config.settings import settings


def setup_logging() -> None:
    """Configura logging estruturado para o projeto."""

    # Garante diretório de logs
    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Configura o nível base
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="%(message)s",
    )

    # Configura structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
            if settings.LOG_FORMAT == "text"
            else structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Retorna um logger configurado."""
    return structlog.get_logger(name)
```

```python
# src/config/model_config.py
"""Configuração de modelos LLM."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModelConfig:
    """Configuração imutável para chamadas de LLM."""

    model: str
    max_tokens: int
    temperature: float
    system_prompt: str = ""

    def with_system_prompt(self, prompt: str) -> "ModelConfig":
        """Retorna nova config com system_prompt atualizado."""
        return ModelConfig(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system_prompt=prompt,
        )


# Configs pré-definidas para casos de uso comuns
GENERATOR_CONFIG = ModelConfig(
    model="claude-sonnet-4-6",
    max_tokens=2000,
    temperature=0.7,
)

EVALUATOR_CONFIG = ModelConfig(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    temperature=0.2,
)

FAST_CONFIG = ModelConfig(
    model="claude-sonnet-4-6",
    max_tokens=500,
    temperature=0.0,
)
```

### Configuração do Ambiente Virtual

```bash
#!/bin/bash
# scripts/setup_venv.sh — Cria e configura ambiente virtual Python

set -e  # Para no primeiro erro

echo "=== CONFIGURANDO AMBIENTE VIRTUAL ==="

# Cria venv se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
else
    echo "Ambiente virtual já existe."
fi

# Ativa
source venv/bin/activate

# Upgrade pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instala dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Verifica instalação
echo ""
echo "Verificando instalação..."
python3 -c "
import anthropic
import pydantic
import structlog
print('✅ Todas as dependências core instaladas com sucesso')
"

echo ""
echo "=== AMBIENTE VIRTUAL CONFIGURADO ==="
echo "Para ativar: source venv/bin/activate"
```

### Script de Setup Completo

Crie `scripts/setup.sh` como entry point único:

```bash
#!/bin/bash
# setup.sh — Entry point único para setup completo do projeto

set -e

echo "========================================="
echo "  SETUP: Long-Running Agents Project"
echo "========================================="
echo ""

# Passo 1: Verificar sistema
echo "[1/5] Verificando requisitos de sistema..."
python3 --version > /dev/null 2>&1 || { echo "❌ Python 3 não encontrado"; exit 1; }
node --version > /dev/null 2>&1 || { echo "❌ Node.js não encontrado"; exit 1; }
git --version > /dev/null 2>&1 || { echo "❌ Git não encontrado"; exit 1; }
echo "  ✅ Sistema OK"
echo ""

# Passo 2: Configurar ambiente virtual
echo "[2/5] Configurando ambiente virtual Python..."
bash scripts/setup_venv.sh
echo ""

# Passo 3: Criar diretórios necessários
echo "[3/5] Criando estrutura de diretórios..."
mkdir -p state logs/{agent_traces,system} tests/{unit,integration,fixtures}
echo "  ✅ Diretórios criados"
echo ""

# Passo 4: Configurar variáveis de ambiente
echo "[4/5] Verificando variáveis de ambiente..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  ⚠️  Arquivo .env criado de .env.example"
    echo "  ⚠️  IMPORTANTE: Edite .env e configure ANTHROPIC_API_KEY"
    echo "  ⚠️  Obtenha sua key em: https://console.anthropic.com/"
else
    echo "  ✅ .env já existe"
fi
echo ""

# Passo 5: Rodar verificação
echo "[5/5] Rodando verificação de ambiente..."
python3 scripts/verify_setup.py
echo ""

echo "========================================="
echo "  SETUP CONCLUÍDO"
echo "========================================="
echo ""
echo "Próximos passos:"
echo "  1. Edite .env com sua ANTHROPIC_API_KEY"
echo "  2. Rode: source venv/bin/activate"
echo "  3. Execute o hello world: python3 src/hello_agent.py"
echo ""
```

---

## 🔧 Seção 4: Ferramentas e Infraestrutura

### Cliente Anthropic Padronizado

Cada chamada de API não deve configurar o cliente do zero. Use um cliente centralizado:

```python
# src/config/anthropic_client.py
"""Cliente Anthropic centralizado e configurável."""

from anthropic import Anthropic
from src.config.settings import settings


def get_anthropic_client() -> Anthropic:
    """Retorna cliente Anthropic configurado."""
    if not settings.ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY não configurada. "
            "Configure em .env ou variável de ambiente."
        )
    return Anthropic(api_key=settings.ANTHROPIC_API_KEY)


# Singleton lazy
_anthropic_client: Anthropic | None = None


def get_client() -> Anthropic:
    """Retorna singleton do cliente Anthropic."""
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = get_anthropic_client()
    return _anthropic_client
```

### Gerenciador de Estado (State Manager)

Agentes precisam persistir estado em arquivos. Centralize esta lógica:

```python
# src/persistence/state_manager.py
"""Gerenciador de estado para long-running agents."""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Optional
from src.config.settings import settings


class StateManager:
    """Gerencia arquivos de estado para um caso/sessão."""

    def __init__(self, case_id: str, customer_id: str):
        self.case_id = case_id
        self.customer_id = customer_id
        self.case_dir = settings.STATE_DIR / customer_id / case_id
        self.case_dir.mkdir(parents=True, exist_ok=True)

    # === LEITURA ===

    def read_context(self) -> dict[str, Any]:
        """Lê o contexto imutável do cliente."""
        return self._read_json("context.json")

    def read_draft(self, iteration: int) -> dict[str, Any]:
        """Lê o rascunho do generator de uma iteração."""
        return self._read_json(f"draft_v{iteration}.json")

    def read_verdict(self, iteration: int) -> dict[str, Any]:
        """Lê o veredito do evaluator de uma iteração."""
        return self._read_json(f"verdict_v{iteration}.json")

    # === ESCRITA ===

    def write_context(self, data: dict[str, Any]) -> None:
        """Escreve contexto imutável do cliente."""
        data["created_at"] = self._now()
        self._write_json("context.json", data)

    def write_draft(self, iteration: int, data: dict[str, Any]) -> None:
        """Escreve rascunho do generator."""
        data["iteration"] = iteration
        data["timestamp"] = self._now()
        self._write_json(f"draft_v{iteration}.json", data)
        self._audit_log("draft_written", {"iteration": iteration})

    def write_verdict(self, iteration: int, data: dict[str, Any]) -> None:
        """Escreve veredito do evaluator."""
        data["iteration"] = iteration
        data["timestamp"] = self._now()
        self._write_json(f"verdict_v{iteration}.json", data)
        self._audit_log(
            "verdict_written",
            {"iteration": iteration, "verdict": data.get("verdict")},
        )

    # === AUDIT LOG ===

    def _audit_log(self, event: str, metadata: dict[str, Any]) -> None:
        """Adiciona evento ao audit log imutável."""
        log_entry = {
            "timestamp": self._now(),
            "event": event,
            "case_id": self.case_id,
            **metadata,
        }
        log_path = self.case_dir / "audit_log.jsonl"
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def read_audit_log(self) -> list[dict[str, Any]]:
        """Lê o audit log completo."""
        log_path = self.case_dir / "audit_log.jsonl"
        if not log_path.exists():
            return []
        with open(log_path) as f:
            return [json.loads(line) for line in f if line.strip()]

    # === UTILITÁRIOS ===

    def _read_json(self, filename: str) -> dict[str, Any]:
        path = self.case_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        with open(path) as f:
            return json.load(f)

    def _write_json(self, filename: str, data: dict[str, Any]) -> None:
        path = self.case_dir / filename
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def case_exists(self) -> bool:
        """Verifica se este caso já foi inicializado."""
        return (self.case_dir / "context.json").exists()
```

### Base Agent Class

Uma classe base para todos os agentes do sistema:

```python
# src/agents/base_agent.py
"""Classe base para todos os agentes do sistema."""

from abc import ABC, abstractmethod
from typing import Any
from src.config.anthropic_client import get_client
from src.config.model_config import ModelConfig
from src.config.logging_config import get_logger


class BaseAgent(ABC):
    """Classe base abstrata para agentes.

    Todo agente no sistema herda desta classe e implementa:
    - execute(): lógica principal do agente
    - system_prompt(): instruções do sistema
    """

    def __init__(self, name: str, config: ModelConfig):
        self.name = name
        self.config = config
        self.client = get_client()
        self.logger = get_logger(f"agent.{name}")

    @abstractmethod
    def system_prompt(self) -> str:
        """Retorna o system prompt para este agente."""
        ...

    @abstractmethod
    def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Executa a lógica principal do agente."""
        ...

    def call_llm(
        self,
        messages: list[dict[str, str]],
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """Faz chamada padronizada ao LLM."""
        self.logger.info(
            "llm_call_start",
            agent=self.name,
            model=self.config.model,
            message_count=len(messages),
        )

        response = self.client.messages.create(
            model=self.config.model,
            system=self.system_prompt(),
            messages=messages,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=(
                temperature
                if temperature is not None
                else self.config.temperature
            ),
        )

        text = response.content[0].text
        self.logger.info(
            "llm_call_end",
            agent=self.name,
            output_tokens=response.usage.output_tokens,
        )
        return text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
```

### Logger Estruturado para Agentes

```python
# src/persistence/trace_logger.py
"""Logger de traces para debugging de agentes."""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any
from src.config.settings import settings


class TraceLogger:
    """Registra cada ação de um agente para debugging."""

    def __init__(self, agent_name: str, session_id: str):
        self.agent_name = agent_name
        self.session_id = session_id
        self.trace_dir = settings.LOG_DIR / "agent_traces" / session_id
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.events: list[dict[str, Any]] = []

    def log(
        self,
        event: str,
        data: dict[str, Any] | None = None,
        level: str = "INFO",
    ) -> None:
        """Registra um evento no trace."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": self.agent_name,
            "session": self.session_id,
            "event": event,
            "level": level,
            "data": data or {},
        }
        self.events.append(entry)

    def log_llm_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
    ) -> None:
        """Registra métricas de uma chamada LLM."""
        self.log(
            "llm_call",
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_ms": round(latency_ms, 2),
            },
        )

    def log_error(self, error: str, context: dict[str, Any] | None = None) -> None:
        """Registra um erro."""
        self.log("error", {"error": error, "context": context or {}}, level="ERROR")

    def flush(self) -> Path:
        """Persiste o trace em disco."""
        filename = (
            f"{self.agent_name}_"
            f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        )
        path = self.trace_dir / filename
        with open(path, "w") as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2, default=str)
        return path
```

---

## 🤖 Seção 5: Primeiro Agente Funcional (Hello World)

### O Agente Mais Simples Possível

Vamos criar um agente que faz uma única coisa: recebe um nome e retorna uma saudação personalizada. Este é o "Hello World" dos long-running agents.

```python
# src/agents/hello_agent.py
"""Hello World — seu primeiro long-running agent."""

from src.agents.base_agent import BaseAgent
from src.config.model_config import FAST_CONFIG
from src.persistence.trace_logger import TraceLogger


class HelloAgent(BaseAgent):
    """Agente mínimo que demonstra o ciclo completo."""

    def __init__(self):
        super().__init__(name="hello_agent", config=FAST_CONFIG)
        self.tracer: TraceLogger | None = None

    def system_prompt(self) -> str:
        return """Você é um agente de saudação amigável.
Sua única tarefa é gerar uma saudação personalizada e calorosa.
Seja criativo mas mantenha a resposta concisa (1-2 frases).
Responda APENAS com a saudação, sem explicações adicionais."""

    def execute(self, input_data: dict) -> dict:
        """Gera saudação personalizada."""
        self.tracer = TraceLogger(self.name, "hello_session")
        self.tracer.log("execution_start", {"input": input_data})

        name = input_data.get("name", "Mundo")
        language = input_data.get("language", "pt")

        messages = [{
            "role": "user",
            "content": f"Gere uma saudação para {name} em {language}.",
        }]

        greeting = self.call_llm(messages, max_tokens=100)

        self.tracer.log("execution_end", {"greeting": greeting})
        self.tracer.flush()

        return {
            "greeting": greeting.strip(),
            "name": name,
            "language": language,
            "status": "success",
        }
```

### O Script de Entrada

```python
# src/hello_agent.py (na raiz de src/)
#!/usr/bin/env python3
"""Script de entrada: execute seu primeiro agente.

Uso:
    python3 src/hello_agent.py
    python3 src/hello_agent.py --name "Maria" --language en
"""

import sys
import argparse
from src.agents.hello_agent import HelloAgent
from src.config.settings import settings
from src.config.logging_config import setup_logging


def main():
    parser = argparse.ArgumentParser(description="Hello World Agent")
    parser.add_argument("--name", default="Mundo", help="Nome para saudar")
    parser.add_argument(
        "--language", default="pt", help="Idioma (pt, en, es)"
    )
    args = parser.parse_args()

    # Setup
    setup_logging()

    # Validar configuração
    errors = settings.validate()
    if errors:
        print("❌ Erros de configuração:")
        for error in errors:
            print(f"  - {error}")
        print("\nConfigure .env com sua ANTHROPIC_API_KEY")
        sys.exit(1)

    # Executar agente
    print(f"\n🚀 Executando HelloAgent para '{args.name}'...\n")

    agent = HelloAgent()
    result = agent.execute({
        "name": args.name,
        "language": args.language,
    })

    # Mostrar resultado
    print("═" * 50)
    print(f"  {result['greeting']}")
    print("═" * 50)
    print(f"\n✅ Agente executado com sucesso!")
    print(f"   Nome: {result['name']}")
    print(f"   Idioma: {result['language']}")
    print(f"   Trace salvo em: logs/agent_traces/hello_session/")


if __name__ == "__main__":
    main()
```

### Teste Unitário do Hello Agent

```python
# tests/unit/test_hello_agent.py
"""Testes unitários para HelloAgent."""

import pytest
from unittest.mock import Mock, patch
from src.agents.hello_agent import HelloAgent


class TestHelloAgent:
    """Testes para o agente hello world."""

    def test_agent_initialization(self):
        """Verifica que o agente inicializa corretamente."""
        agent = HelloAgent()
        assert agent.name == "hello_agent"
        assert agent.config.model == "claude-sonnet-4-6"

    def test_system_prompt_not_empty(self):
        """System prompt deve conter instruções."""
        agent = HelloAgent()
        prompt = agent.system_prompt()
        assert len(prompt) > 50
        assert "agente" in prompt.lower()

    @patch("src.agents.hello_agent.HelloAgent.call_llm")
    def test_execute_returns_greeting(self, mock_call_llm):
        """Executar deve retornar saudação no formato esperado."""
        mock_call_llm.return_value = "Olá, Teste! Bem-vindo ao mundo dos agentes!"

        agent = HelloAgent()
        result = agent.execute({"name": "Teste", "language": "pt"})

        assert result["status"] == "success"
        assert result["name"] == "Teste"
        assert "Olá" in result["greeting"]
        assert result["language"] == "pt"

    @patch("src.agents.hello_agent.HelloAgent.call_llm")
    def test_execute_default_name(self, mock_call_llm):
        """Nome padrão deve ser 'Mundo' quando não fornecido."""
        mock_call_llm.return_value = "Olá, Mundo!"

        agent = HelloAgent()
        result = agent.execute({})

        assert result["name"] == "Mundo"
```

### Executando o Hello World

**Importante:** O script `hello_agent.py` importa do pacote `src/`. Para que o Python encontre o módulo, use um destes métodos:

**Método 1 (recomendado):** Instale o projeto em modo editável:

```bash
# Adicione um setup.py ou pyproject.toml mínimo, ou use:
pip install -e .
```

**Método 2:** Execute com PYTHONPATH:

```bash
# Ative o ambiente virtual
source venv/bin/activate

# Execute com PYTHONPATH apontando para a raiz do projeto
PYTHONPATH="$(pwd)" python3 src/hello_agent.py
```

**Método 3:** Crie um `pyproject.toml` mínimo na raiz:

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "long-running-agents"
version = "0.1.0"

[tool.setuptools]
packages = ["src", "src.agents", "src.orchestration", "src.persistence", "src.config", "src.tools", "src.evaluation"]
```

Depois instale:

```bash
pip install -e .
```

Agora execute:

```bash
python3 src/hello_agent.py

# Output esperado:
# 🚀 Executando HelloAgent para 'Mundo'...
# ══════════════════════════════════════════════════
#   Olá, Mundo! Que alegria ter você aqui...
# ══════════════════════════════════════════════════
# ✅ Agente executado com sucesso!

# Com parâmetros customizados
python3 src/hello_agent.py --name "Fernando" --language pt

# Em inglês
python3 src/hello_agent.py --name "Alice" --language en
```

---

## 📊 Seção 6: Diagrama de Arquitetura do Setup

### Visão Geral do Ambiente

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SEU AMBIENTE DE DESENVOLVIMENTO                 │
└─────────────────────────────────────────────────────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   SUA MÁQUINA    │   │   APIs EXTERNAS  │   │   FERRAMENTAS    │
│                  │   │                  │   │   AUXILIARES     │
│  ┌────────────┐  │   │  ┌────────────┐  │   │                  │
│  │ Python 3   │──┼───┼─▶│ Anthropic   │  │   │  ┌────────────┐  │
│  │ venv/      │  │   │  │ (Claude)    │  │   │  │ Git        │  │
│  └────────────┘  │   │  └────────────┘  │   │  └────────────┘  │
│                  │   │                  │   │                  │
│  ┌────────────┐  │   │  ┌────────────┐  │   │  ┌────────────┐  │
│  │ Node.js    │  │   │  │ OpenAI      │  │   │  │ VS Code /  │  │
│  │ npm        │  │   │  │ (opcional)  │  │   │  │ Cursor     │  │
│  └────────────┘  │   │  └────────────┘  │   │  └────────────┘  │
│                  │   │                  │   │                  │
│  ┌────────────┐  │   │                  │   │  ┌────────────┐  │
│  │ .env       │  │   │                  │   │  │ Docker      │  │
│  │ Config     │  │   │                  │   │  │ (opcional)  │  │
│  └────────────┘  │   │                  │   │  └────────────┘  │
└──────────────────┘   └──────────────────┘   └──────────────────┘
```

### Fluxo de Inicialização do Projeto

```
git clone repo
      │
      ▼
┌─────────────────┐
│ bash setup.sh   │  ← Entry point único
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│Python │ │Node   │
│venv   │ │npm i  │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│ Copiar .env     │
│ .example → .env │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Configurar      │
│ ANTHROPIC_API   │
│ _KEY            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ verify_setup.py │  ← Validação automatizada
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  ✅ OK    ❌ ERRO
    │         │
    ▼         ▼
 Pronto!   Corrigir
```

---

## 📋 Seção 7: Tabela Comparativa de Estratégias de Setup

Diferentes projetos têm diferentes necessidades. Compare as abordagens:

| Dimensão | Setup Mínimo | Setup Recomendado | Setup Enterprise |
|----------|-------------|-------------------|-----------------|
| **Ambiente Python** | pip install manual | venv + requirements.txt | Poetry + lock file |
| **Variáveis de Ambiente** | hardcoded no código | .env + python-dotenv | Vault + CI/CD secrets |
| **Configuração** | inline strings | src/config/ centralizado | Remote config + feature flags |
| **Logging** | print() statements | structlog + JSON | ELK Stack / Datadog |
| **State Files** | arquivos soltos | StateManager + audit_log | PostgreSQL + event sourcing |
| **Testes** | manual | pytest + CI | pytest + coverage gates |
| **Tracing** | nenhum | TraceLogger em arquivo | OpenTelemetry + Jaeger |
| **Dependências** | instalação manual | requirements.txt | Poetry + Dependabot |
| **CI/CD** | nenhum | GitHub Actions básico | Multi-stage pipeline |
| **Monitoramento** | nenhum | Logs estruturados | Prometheus + Grafana |
| **Tempo de Setup** | 10 min | 30 min | 2-4 horas |
| **Manutenção** | Alta (quebra fácil) | Média (scripts ajudam) | Baixa (automatizado) |
| **Para quem?** | Prototipagem solo | Time de 3-8 pessoas | Time 10+ / produção |

### Quando Usar Cada Abordagem

**Setup Mínimo:**
- Ideias e experimentos rápidos
- Hackathons
- Provas de conceito que não vão para produção
- ⚠️ Risco: dívida técnica explode rápido

**Setup Recomendado (este guia):**
- Projetos que vão para produção
- Times pequenos a médios
- Agentes que precisam de confiabilidade
- ✅ Equilíbrio entre velocidade e robustez

**Setup Enterprise:**
- Sistemas críticos (financeiro, saúde)
- Times grandes e distribuídos
- Múltiplos ambientes (dev, staging, prod)
- Requisitos de compliance (SOC2, GDPR)
- ⚠️ Overhead: setup inicial mais lento

---

## 🏢 Seção 8: Aplicação em KODA — Setup do Ambiente Real

### Como o Time KODA Configurou o Ambiente

O time KODA seguiu este guia para montar o ambiente de desenvolvimento. O que eles adaptaram:

### Estrutura Específica KODA

```
koda-project/
│
├── src/
│   ├── agents/
│   │   ├── whatsapp_agent.py        # KODA: agente de conversa
│   │   ├── product_advisor.py       # KODA: recomendador de produtos
│   │   └── order_processor.py       # KODA: processador de pedidos
│   │
│   ├── tools/
│   │   ├── catalog_search.py        # Busca no catálogo KODA
│   │   ├── inventory_check.py       # Verificação de estoque
│   │   ├── price_calculator.py      # Cálculo de preços + descontos
│   │   └── payment_gateway.py       # Integração com gateway
│   │
│   ├── orchestration/
│   │   ├── conversation_pipeline.py # Pipeline da conversa completa
│   │   └── order_pipeline.py        # Pipeline de processamento
│   │
│   └── evaluation/
│       ├── recommendation_rubric.py # Rubrica de recomendações
│       └── order_quality_check.py   # Verificação de qualidade
│
├── state/
│   └── wa_{phone_number}/          # Um diretório por cliente WhatsApp
│       ├── customer_profile.json   # Perfil + histórico + alergias
│       ├── conversation_state.json # Estado atual da conversa
│       └── order_{id}/            # Um subdiretório por pedido
│           ├── context.json
│           ├── draft_v1.json
│           ├── verdict_v1.json
│           └── audit_log.jsonl
│
├── tests/
│   ├── unit/
│   │   ├── test_price_calculator.py
│   │   └── test_inventory_check.py
│   │
│   └── integration/
│       ├── test_conversation_flow.py
│       └── test_order_pipeline.py
│
└── config/
    ├── koda_models.py              # Configs específicas de modelos
    └── koda_rubrics.py             # Definições de rubricas
```

### Configuração Específica KODA

```python
# src/config/koda_settings.py
"""Configurações específicas do KODA."""

from src.config.settings import settings


class KodaSettings:
    """Configurações estendidas para o ecossistema KODA."""

    # APIs KODA
    CATALOG_API_URL: str = "https://api.koda.example.com/v1/catalog"
    INVENTORY_API_URL: str = "https://api.koda.example.com/v1/inventory"
    PAYMENT_API_URL: str = "https://api.koda.example.com/v1/payments"
    FULFILLMENT_API_URL: str = "https://api.koda.example.com/v1/fulfillment"

    # Configurações de conversa
    MAX_CONVERSATION_HISTORY_TOKENS: int = 50000
    CONTEXT_COMPRESSION_THRESHOLD: int = 40000
    SESSION_TIMEOUT_MINUTES: int = 240  # 4 horas

    # Configurações de produto
    MAX_RECOMMENDATIONS_PER_RESPONSE: int = 5
    DEFAULT_BUDGET_FALLBACK: float = 200.0

    # Configurações de qualidade
    MIN_RECOMMENDATION_SCORE: float = 7.0  # 0-10
    MAX_RETRY_ATTEMPTS_ORDER: int = 3

    # IDs de teste (sandbox)
    TEST_CUSTOMER_WHATSAPP: str = "5511999999999"
    TEST_PRODUCT_SKU: str = "WHEY-TEST-001"
```

### Script de Setup KODA

```bash
#!/bin/bash
# scripts/setup_koda.sh — Setup específico para ambiente KODA

echo "=== SETUP KODA ==="

# Verifica .env com variáveis KODA
if ! grep -q "KODA_CATALOG_API_URL" .env 2>/dev/null; then
    echo "⚠️  Variáveis KODA não encontradas no .env"
    echo "   Adicione:"
    echo "   KODA_CATALOG_API_URL=https://..."
    echo "   KODA_INVENTORY_API_URL=https://..."
fi

# Cria diretórios específicos KODA
mkdir -p state/wa_test

# Cria perfil de cliente de teste
cat > state/wa_test/customer_profile.json << 'EOF'
{
  "customer_id": "wa_5511999999999",
  "name": "Cliente Teste",
  "goal": "ganho_muscular",
  "level": "intermediário",
  "restrictions": ["sem lactose"],
  "budget_max": 200,
  "club_member": true
}
EOF

echo "✅ Ambiente KODA configurado"
```

### Lições Aprendidas pelo Time KODA

1. **State directory por cliente WhatsApp** foi essencial para isolar dados
2. **Audit log** salvou horas de debugging quando algo falhava em produção
3. **Configuração centralizada** permitiu mudar de modelo sem alterar código
4. **Trace logger** virou ferramenta principal de debugging
5. **Estrutura de diretórios consistente** permitiu onboard de novos devs em horas

---

## ✅ Seção 9: Checklist de Verificação de Setup

Este script automatizado verifica que tudo está configurado:

```python
#!/usr/bin/env python3
# scripts/verify_setup.py
"""Verificação automatizada do ambiente de desenvolvimento."""

import sys
from pathlib import Path


def check(label: str, condition: bool, detail: str = "") -> bool:
    """Verifica uma condição e reporta."""
    status = "✅" if condition else "❌"
    msg = f"  {status} {label}"
    if detail and not condition:
        msg += f" — {detail}"
    print(msg)
    return condition


def main():
    print("=" * 60)
    print("  VERIFICAÇÃO DE SETUP — Long-Running Agents")
    print("=" * 60)

    all_ok = True
    errors = []

    # === 1. Python e Dependências ===
    print("\n📦 Python e Dependências:")

    try:
        import anthropic
        all_ok &= check("anthropic", True)
    except ImportError:
        all_ok &= check("anthropic", False, "pip install anthropic")

    try:
        import pydantic
        all_ok &= check("pydantic", True)
    except ImportError:
        all_ok &= check("pydantic", False, "pip install pydantic")

    try:
        import dotenv
        all_ok &= check("python-dotenv", True)
    except ImportError:
        all_ok &= check("python-dotenv", False, "pip install python-dotenv")

    try:
        import structlog
        all_ok &= check("structlog", True)
    except ImportError:
        all_ok &= check("structlog", False, "pip install structlog")

    try:
        import pytest
        all_ok &= check("pytest", True)
    except ImportError:
        all_ok &= check("pytest", False, "pip install pytest")

    # === 2. Variáveis de Ambiente ===
    print("\n🔑 Variáveis de Ambiente:")

    from dotenv import load_dotenv
    import os

    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    # Rejeita chaves placeholder (ex: sk-ant-xxxxxxxxxxxxx)
    is_placeholder = "xxxx" in api_key or "placeholder" in api_key.lower()
    has_key = bool(
        api_key
        and api_key.startswith("sk-ant-")
        and len(api_key) > 30
        and not is_placeholder
    )
    all_ok &= check(
        "ANTHROPIC_API_KEY configurada",
        has_key,
        "Configure sua key real em .env (não use placeholder)",
    )

    # === 3. Estrutura de Diretórios ===
    print("\n📁 Estrutura de Diretórios:")

    required_dirs = [
        "src/agents",
        "src/orchestration",
        "src/persistence",
        "src/tools",
        "src/config",
        "src/evaluation",
        "state",
        "logs",
        "tests/unit",
        "tests/integration",
    ]

    for dir_path in required_dirs:
        exists = Path(dir_path).is_dir()
        all_ok &= check(
            f"{dir_path}/",
            exists,
            f"Crie com: mkdir -p {dir_path}",
        )

    # === 4. Arquivos Essenciais ===
    print("\n📄 Arquivos Essenciais:")

    required_files = [
        ".env",
        ".gitignore",
        "README.md",
    ]

    for file_path in required_files:
        exists = Path(file_path).is_file()
        all_ok &= check(
            file_path,
            exists,
            f"Crie o arquivo {file_path}",
        )

    # === 5. Git ===
    print("\n🔧 Git:")

    git_dir = Path(".git").is_dir()
    all_ok &= check("Repositório Git inicializado", git_dir)

    gitignore = Path(".gitignore")
    if gitignore.exists():
        content = gitignore.read_text()
        checks = [
            (".env" in content, ".env no .gitignore"),
            ("state/" in content, "state/ no .gitignore"),
            ("logs/" in content, "logs/ no .gitignore"),
            ("venv/" in content, "venv/ no .gitignore"),
        ]
        for condition, msg in checks:
            all_ok &= check(msg, condition)

    # === 6. Node.js (opcional) ===
    print("\n🟢 Node.js (opcional):")

    import subprocess
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        all_ok &= check("Node.js instalado", True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        all_ok &= check("Node.js instalado", False, "Opcional para ferramentas")

    # === Resultado Final ===
    print("\n" + "=" * 60)

    if all_ok:
        print("✅ AMBIENTE COMPLETAMENTE CONFIGURADO!")
        print("   Pronto para executar seu primeiro agente:")
        print("   python3 src/hello_agent.py")
    else:
        print("⚠️  ALGUNS ITENS PRECISAM DE ATENÇÃO")
        print("   Corrija os itens marcados com ❌ acima.")
        print("   Depois rode: python3 scripts/verify_setup.py novamente")

    print("=" * 60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
```

### Checklist Manual (para revisão humana)

Antes de começar a desenvolver, verifique manualmente:

- [ ] **API Key funciona:** Rodei `hello_agent.py` e recebi resposta do Claude
- [ ] **Estado persiste:** Criei um `context.json` e consegui lê-lo com `StateManager`
- [ ] **Logs são gerados:** Encontrei arquivos em `logs/agent_traces/`
- [ ] **Testes passam:** `pytest tests/ -v` retorna tudo verde
- [ ] **.env não foi commitado:** `git status` não mostra `.env` como tracked
- [ ] **.gitignore cobre secrets:** `.env`, `state/`, `logs/` estão no `.gitignore`
- [ ] **Script de setup é reproduzível:** Colega conseguiu rodar `setup.sh` do zero
- [ ] **Estrutura de diretórios segue o padrão:** Compare com a seção 1
- [ ] **Configuração está centralizada:** Não tem `os.environ.get()` solto no código
- [ ] **README.md está atualizado:** Tem instruções de setup e hello world

---

## 🔗 Seção 10: Onde Cada Peça se Encaixa no Ecossistema

### Como Este Setup se Conecta aos Níveis do Currículo

```
┌──────────────────────────────────────────────────────────────────┐
│              ECOSSISTEMA DE LONG-RUNNING AGENTS                   │
└──────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  FUNDAMENTOS  │     │   PADRÕES     │     │  ARQUITETURA  │
│  (Nível 1)    │     │   (Nível 2)   │     │  (Nível 3)    │
│               │     │               │     │               │
│ • Context     │     │ • Generator/  │     │ • Multi-Agent │
│   Amnesia     │     │   Evaluator   │     │ • State       │
│ • Token       │     │ • Sprint      │     │   Persistence │
│   Budgeting   │     │   Contracts   │     │ • Harness     │
│ • Basic       │     │ • Rubric      │     │   Evolution   │
│   Harness     │     │   Design      │     │               │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────┐
          │         KODA APLICAÇÃO (Nível 4)        │
          │  • WhatsApp Agent                       │
          │  • Product Recommendation               │
          │  • Order Processing                     │
          │  • Fulfillment                          │
          └─────────────────────────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────┐
          │     ESTE GUIA (Implementation Guide)     │
          │     ──────────────────────────────       │
          │     Infraestrutura que suporta TUDO      │
          │     • Estrutura de diretórios            │
          │     • Configuração centralizada          │
          │     • State persistence                  │
          │     • Logging & tracing                  │
          │     • Testes automatizados               │
          └─────────────────────────────────────────┘
```

### Matriz de Responsabilidades

| Componente | Setup Guide | Nível 1 | Nível 2 | Nível 3 | Nível 4 |
|------------|:-----------:|:-------:|:-------:|:-------:|:-------:|
| Estrutura de diretórios | ✅ Cria | 🔍 Usa | 🔍 Usa | 🔍 Usa | 🔍 Usa |
| Configuração centralizada | ✅ Define | 🔍 Usa | 🔍 Usa | 🔍 Usa | 🔍 Usa |
| State Manager | ✅ Provê | 🔍 Usa | 🔍 Usa | 📖 Aprofunda | 🔍 Usa |
| Base Agent | ✅ Provê | 🔍 Usa | 🔍 Usa | 📖 Estende | 📖 Estende |
| Trace Logger | ✅ Provê | - | 🔍 Usa | 📖 Aprofunda | 🔍 Usa |
| Testes | ✅ Estrutura | - | 🔍 Usa | 🔍 Usa | 📖 Expande |

Legenda: ✅ = Cria/Provê, 🔍 = Usa/Referencia, 📖 = Aprofunda/Expande, - = Não aborda

---

## 🐛 Seção 11: Troubleshooting — Problemas Comuns e Soluções

### API Key não funciona

**Sintoma:** `AuthenticationError: invalid x-api-key`

**Causas e soluções:**
1. Key está incorreta → verifique em https://console.anthropic.com/
2. Key expirou → gere uma nova no console
3. Key não tem créditos → verifique o billing
4. `.env` não está sendo carregado → verifique se `python-dotenv` está instalado
5. Variável de ambiente tem nome errado → deve ser `ANTHROPIC_API_KEY`

```bash
# Teste rápido da API key
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('ANTHROPIC_API_KEY', '')
print(f'Key encontrada: {\"Sim\" if key else \"Não\"}')
print(f'Formato correto: {\"Sim\" if key.startswith(\"sk-ant-\") else \"Não\"}')
print(f'Tamanho: {len(key)} caracteres')
"
```

### Módulo não encontrado

**Sintoma:** `ModuleNotFoundError: No module named 'src'`

**Causa:** Python não sabe que `src/` faz parte do projeto.

**Soluções:**
```bash
# Opção 1: Instalar em modo editável
pip install -e .

# Opção 2: PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Opção 3: Adicionar no início do script
import sys
sys.path.insert(0, ".")
```

### State directory não persiste

**Sintoma:** Arquivos em `state/` somem entre execuções.

**Verificações:**
```bash
# Verifique permissões
ls -la state/

# Verifique se o diretório existe
test -d state/ && echo "Existe" || echo "Não existe — crie com mkdir -p state/"

# Verifique se está no .gitignore
grep "state/" .gitignore
```

### Logs não aparecem

**Sintoma:** Diretório `logs/` vazio.

**Soluções:**
```bash
# Crie os diretórios manualmente
mkdir -p logs/{agent_traces,system}

# Verifique LOG_LEVEL
# Se for ERROR, logs INFO não aparecem
export LOG_LEVEL=INFO

# Force um log de teste
python3 -c "
import logging
logging.basicConfig(level=logging.INFO)
logging.info('Teste de log')
"
```

---

## 🎯 Seção 12: O Que Você Aprendeu

### Em 5 Pontos

**1. Estrutura de repositório é estratégia, não acidente**
Um diretório bagunçado custa semanas de debugging. Uma estrutura clara com responsabilidades definidas (agents/, orchestration/, persistence/, state/) escala do protótipo à produção sem reescrita.

**2. Configuração centralizada evita o caos**
Variáveis de ambiente espalhadas pelo código são impossíveis de auditar. Centralize em `src/config/` com classes imutáveis. Use `.env.example` como contrato com sua equipe.

**3. State persistence é a espinha dorsal**
Agentes são stateless — cada chamada de API começa do zero. O `StateManager` com arquivos JSON por caso/sessão é o que mantém contexto através de horas de execução. O `audit_log.jsonl` é seu melhor amigo no debugging.

**4. Ferramentas certas, configuradas uma vez**
Cliente Anthropic centralizado, BaseAgent com logging estruturado, TraceLogger para debugging — cada ferramenta instalada e configurada uma vez, usada por todos os agentes. Zero duplicação.

**5. Verificação automatizada como ritual**
O `verify_setup.py` não é opcional. Ele é a diferença entre "achei que estava funcionando" e "sei que está funcionando". Rode-o no primeiro dia, depois de cada mudança de dependência, e antes de cada demo.

### O que fazer AGORA

- [ ] Complete o setup se ainda não o fez
- [ ] Rode `python3 scripts/verify_setup.py` e veja ✅ em tudo
- [ ] Execute `python3 src/hello_agent.py` e veja sua primeira resposta do Claude
- [ ] Leia o arquivo de trace gerado em `logs/agent_traces/`
- [ ] Compartilhe este guia com sua equipe
- [ ] Agende 30 minutos para todos seguirem o setup juntos

---

## 🚀 Próximos Passos

Agora que seu ambiente está pronto, você tem duas opções:

### Opção A: Começar pelos Fundamentos
→ Vá para o **Nível 1**: `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`

Entenda os 3 problemas que fazem agentes falharem e como o Generator/Evaluator resolve todos eles de uma vez.

### Opção B: Ir direto para padrões práticos
→ Vá para o **Nível 2**: `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md`

Implemente o padrão Generator/Evaluator, Sprint Contracts e Rubric Design usando a infraestrutura que você acabou de configurar.

### Guias complementares neste módulo

- `02-team-progression-guide.md` — Como evoluir sua equipe pelos níveis
- `03-harness-design-checklist.md` — Checklist para desenhar harnesses
- `04-evaluation-rubric-template.md` — Template de rubrica de avaliação
- `05-trace-analysis-guide.md` — Guia de leitura de traces

---

## ❓ Perguntas Frequentes

### P: "Preciso realmente de toda essa estrutura? Meu projeto é pequeno."

**R:** A estrutura escala para baixo. Se seu projeto tem 3 arquivos, você usa `src/agents/` com 1 arquivo. Mas quando crescer para 30 arquivos (o que acontece rápido com agentes), a estrutura já está lá. O custo de adicionar estrutura depois é 10x maior que começar com ela.

### P: "Posso usar JavaScript/TypeScript em vez de Python?"

**R:** Sim. Os princípios são os mesmos. Use `src/agents/`, `src/orchestration/`, `state/` etc. A classe `BaseAgent` seria uma classe TypeScript. O `StateManager` usaria `fs.readFileSync`. A estrutura de diretórios é linguagem-agnóstica.

### P: "Preciso de Docker?"

**R:** Não para começar. Para produção com múltiplos ambientes e deploys, Docker é recomendado. Mas você pode ir longe com venv + scripts de setup.

### P: "E se eu já tenho um projeto existente?"

**R:** Migre incrementalmente:
1. Comece criando `src/config/` e centralize a configuração
2. Depois organize os agentes em `src/agents/`
3. Depois adicione `StateManager` para persistência
4. Por último, estruture `state/` e `logs/`

Não tente migrar tudo de uma vez.

### P: "Qual modelo Claude devo usar para começar?"

**R:** Para desenvolvimento e testes: **Claude Sonnet 4** (rápido, barato, 200K tokens). Para avaliações críticas em produção: **Claude Opus 4** (mais preciso, mais tokens, mais caro). O `ModelConfig` permite alternar entre eles sem mudar código.

### P: "Como faço deploy disso?"

**R:** Este guia cobre ambiente de desenvolvimento local. Para deploy:
- Use Docker para empacotar
- Mova `state/` para um volume persistente ou banco de dados
- Configure `LOG_FORMAT=json` e envie logs para um aggregator
- Use variáveis de ambiente do sistema (não .env) em produção
- Adicione health checks e métricas

---

## 📊 Métricas de Sucesso do Setup

Após completar este guia, seu ambiente está saudável quando:

| Métrica | Alvo | Como Medir |
|---------|------|-----------|
| Tempo de setup para novo dev | < 30 min | Cronometrar `setup.sh` |
| Hello agent executa | 1o try | `python3 src/hello_agent.py` |
| Testes passam | 100% | `pytest tests/ -v` |
| API key válida | Confirmado | Hello agent retorna resposta real |
| Logs são gerados | Sim | Arquivos em `logs/agent_traces/` |
| .env não commitado | Confirmado | `git status` limpo |
| Estrutura segue padrão | 100% | `verify_setup.py` ✅ |
| Documentação acessível | Sim | README.md atualizado |

---

## 💭 Reflexão Final

> "Antes de construir agentes que rodam por horas, você precisa de um ambiente que não quebra em 5 minutos."

As próximas 12 semanas do currículo vão te ensinar padrões sofisticados de arquitetura, coordenação multi-agente, e design de avaliação. Mas tudo isso assume que seu ambiente **simplesmente funciona**.

Quando algo falhar em produção — e vai falhar — você não vai querer descobrir que o problema era uma variável de ambiente mal configurada ou um diretório de estado que não estava sendo criado.

Este guia existe para que você possa **confiar no chão que pisa**. Uma vez que o ambiente está sólido, você pode focar 100% no que importa: construir agentes incríveis.

O setup não é o destino. É o ponto de partida.

**Agora vá construir algo.**

---

## 🔬 Seção 13: Segundo Agente — Um Generator/Evaluator Mínimo

### Além do Hello World

O `HelloAgent` provou que sua API key funciona. Agora vamos criar um **Generator/Evaluator mínimo** — dois agentes que colaboram usando arquivos de estado.

Este é o padrão que você vai usar em produção. A diferença entre um agente solo e um par Generator/Evaluator é a diferença entre um protótipo e um sistema confiável.

### Generator: Criador de Recomendações

```python
# src/agents/simple_generator.py
"""Generator simples que recomenda produtos."""

from src.agents.base_agent import BaseAgent
from src.config.model_config import GENERATOR_CONFIG
from src.persistence.state_manager import StateManager
from src.persistence.trace_logger import TraceLogger
import json


class SimpleGenerator(BaseAgent):
    """Agente que gera recomendações de produtos."""

    def __init__(self):
        super().__init__(name="simple_generator", config=GENERATOR_CONFIG)

    def system_prompt(self) -> str:
        return """Você é um gerador de recomendações de suplementos.
Sua função é criar recomendações de produtos baseadas no perfil do cliente.

Para cada recomendação, forneça:
- Nome do produto
- Preço
- Justificativa (1-2 frases)
- Restrições atendidas (ex: sem lactose, vegano)

Gere entre 3 e 5 opções diferentes.
NÃO avalie suas próprias recomendações — isso é trabalho do Evaluator.
Responda em JSON com formato:
{
  "recommendations": [
    {
      "name": "...",
      "price": 0.0,
      "rationale": "...",
      "restrictions_met": ["..."]
    }
  ]
}"""

    def execute(self, input_data: dict) -> dict:
        """Gera recomendações baseadas no perfil do cliente."""
        tracer = TraceLogger(self.name, input_data.get("session_id", "gen_default"))
        tracer.log("execution_start", {"input_keys": list(input_data.keys())})

        customer_goal = input_data.get("goal", "ganho muscular")
        budget = input_data.get("budget", 200)
        restrictions = input_data.get("restrictions", [])

        messages = [{
            "role": "user",
            "content": (
                f"Cliente quer: {customer_goal}\n"
                f"Orçamento máximo: R$ {budget}\n"
                f"Restrições: {', '.join(restrictions) if restrictions else 'nenhuma'}\n\n"
                f"Gere 3-5 recomendações de suplementos. Responda em JSON."
            ),
        }]

        response_text = self.call_llm(messages)
        tracer.log("llm_response_received")

        try:
            recommendations = json.loads(response_text)
        except json.JSONDecodeError:
            tracer.log_error("json_parse_failed", {"raw": response_text[:200]})
            recommendations = {"recommendations": [], "error": "JSON inválido"}

        tracer.log("execution_end", {"count": len(recommendations.get("recommendations", []))})
        tracer.flush()

        return recommendations
```

### Evaluator: Validador de Recomendações

```python
# src/agents/simple_evaluator.py
"""Evaluator simples que valida recomendações."""

from src.agents.base_agent import BaseAgent
from src.config.model_config import EVALUATOR_CONFIG
from src.persistence.trace_logger import TraceLogger
import json


class SimpleEvaluator(BaseAgent):
    """Agente que avalia criticamente recomendações."""

    def __init__(self):
        super().__init__(name="simple_evaluator", config=EVALUATOR_CONFIG)

    def system_prompt(self) -> str:
        return """Você é um avaliador CRÍTICO de recomendações de produtos.
Sua função é ENCONTRAR PROBLEMAS — não aprovar cegamente.

Para cada recomendação, verifique:
1. Preço está dentro do orçamento?
2. Restrições do cliente são respeitadas?
3. Justificativa faz sentido?
4. Há informações contraditórias?

Responda em JSON com formato:
{
  "evaluations": [
    {
      "product_name": "...",
      "checks": {
        "budget_ok": true/false,
        "restrictions_ok": true/false,
        "rationale_clear": true/false
      },
      "score": 0-10,
      "notes": "..."
    }
  ],
  "overall_score": 0-10,
  "verdict": "APPROVED" ou "REJECTED",
  "issues": ["..."]
}"""

    def execute(self, input_data: dict) -> dict:
        """Avalia recomendações contra critérios de qualidade."""
        tracer = TraceLogger(self.name, input_data.get("session_id", "eval_default"))
        tracer.log("execution_start")

        recommendations = input_data.get("recommendations", [])
        budget = input_data.get("budget", 200)
        restrictions = input_data.get("restrictions", [])

        messages = [{
            "role": "user",
            "content": (
                f"Avalie estas recomendações:\n{json.dumps(recommendations, indent=2, ensure_ascii=False)}\n\n"
                f"Orçamento máximo: R$ {budget}\n"
                f"Restrições do cliente: {', '.join(restrictions) if restrictions else 'nenhuma'}\n\n"
                f"Avalie CADA recomendação. Seja crítico. Responda em JSON."
            ),
        }]

        response_text = self.call_llm(messages)
        tracer.log("llm_response_received")

        try:
            evaluation = json.loads(response_text)
        except json.JSONDecodeError:
            tracer.log_error("json_parse_failed")
            evaluation = {"verdict": "ERROR", "issues": ["Falha ao parsear avaliação"]}

        tracer.log("execution_end", {"verdict": evaluation.get("verdict")})
        tracer.flush()

        return evaluation
```

### Pipeline: Generator → Evaluator com Persistência

```python
# src/orchestration/simple_pipeline.py
"""Pipeline mínimo Generator → Evaluator com persistência."""

import sys
from src.agents.simple_generator import SimpleGenerator
from src.agents.simple_evaluator import SimpleEvaluator
from src.persistence.state_manager import StateManager
from src.config.settings import settings
from src.config.logging_config import setup_logging, get_logger


def run_pipeline(
    customer_id: str,
    case_id: str,
    goal: str = "ganho muscular",
    budget: float = 200.0,
    restrictions: list[str] | None = None,
) -> dict:
    """Executa pipeline Generator → Evaluator completo.

    Args:
        customer_id: ID do cliente (ex: wa_5511999999999)
        case_id: ID do caso (ex: rec_001)
        goal: Objetivo do cliente
        budget: Orçamento máximo
        restrictions: Restrições (ex: ["sem lactose"])

    Returns:
        Dicionário com resultado final.
    """
    logger = get_logger("pipeline")
    sm = StateManager(case_id=case_id, customer_id=customer_id)
    restrictions = restrictions or []

    # 1. Salvar contexto
    context = {
        "customer_id": customer_id,
        "goal": goal,
        "budget": budget,
        "restrictions": restrictions,
    }
    sm.write_context(context)
    logger.info("context_saved", case_id=case_id)

    # 2. Generator: criar recomendações
    generator = SimpleGenerator()
    draft = generator.execute({
        "goal": goal,
        "budget": budget,
        "restrictions": restrictions,
        "session_id": case_id,
    })
    sm.write_draft(1, draft)
    logger.info("draft_generated", case_id=case_id)

    # 3. Evaluator: avaliar recomendações
    evaluator = SimpleEvaluator()
    verdict = evaluator.execute({
        "recommendations": draft.get("recommendations", []),
        "budget": budget,
        "restrictions": restrictions,
        "session_id": case_id,
    })
    sm.write_verdict(1, verdict)
    logger.info("verdict_generated", verdict=verdict.get("verdict"))

    # 4. Mostrar resultado
    print("\n" + "=" * 60)
    print(f"  PIPELINE RESULTADO — {case_id}")
    print("=" * 60)
    print(f"\n  📋 Recomendações geradas: {len(draft.get('recommendations', []))}")
    print(f"  📊 Score geral: {verdict.get('overall_score', 'N/A')}/10")
    print(f"  🏷️  Veredito: {verdict.get('verdict', 'DESCONHECIDO')}")

    if verdict.get("issues"):
        print(f"\n  ⚠️  Issues encontradas:")
        for issue in verdict["issues"]:
            print(f"     - {issue}")

    print(f"\n  📁 Arquivos de estado salvos em:")
    print(f"     state/{customer_id}/{case_id}/")
    print("=" * 60)

    return {
        "case_id": case_id,
        "draft": draft,
        "verdict": verdict,
        "state_dir": str(sm.case_dir),
    }


if __name__ == "__main__":
    setup_logging()

    errors = settings.validate()
    if errors:
        print("❌ Configure ANTHROPIC_API_KEY em .env")
        sys.exit(1)

    # Executa com dados de exemplo
    run_pipeline(
        customer_id="wa_teste",
        case_id="demo_001",
        goal="ganho muscular",
        budget=150.0,
        restrictions=["sem lactose"],
    )
```

### Executando o Pipeline

```bash
# Ative o ambiente
source venv/bin/activate

# Execute o pipeline de demonstração
python3 src/orchestration/simple_pipeline.py

# Output esperado:
# ============================================================
#   PIPELINE RESULTADO — demo_001
# ============================================================
#   📋 Recomendações geradas: 4
#   📊 Score geral: 8.5/10
#   🏷️  Veredito: APPROVED
#   📁 Arquivos de estado salvos em:
#      state/wa_teste/demo_001/
# ============================================================
```

### Verificando os Arquivos de Estado

```bash
# Liste os arquivos de estado da execução
ls -la state/wa_teste/demo_001/

# Leia o contexto do cliente
cat state/wa_teste/demo_001/context.json | python3 -m json.tool

# Leia o rascunho do generator
cat state/wa_teste/demo_001/draft_v1.json | python3 -m json.tool

# Leia o veredito do evaluator
cat state/wa_teste/demo_001/verdict_v1.json | python3 -m json.tool

# Leia o audit log
cat state/wa_teste/demo_001/audit_log.jsonl
```

---

## 🔄 Seção 14: Integração Contínua — GitHub Actions Básico

### Pipeline de CI para Agentes

Seus agentes precisam de verificação automática. Configure um workflow mínimo:

```yaml
# .github/workflows/ci.yml
name: CI — Long-Running Agents

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Verify project structure
        run: |
          echo "=== Verificando estrutura ==="
          test -d src/agents || { echo "❌ src/agents/ não existe"; exit 1; }
          test -d src/orchestration || { echo "❌ src/orchestration/ não existe"; exit 1; }
          test -d src/config || { echo "❌ src/config/ não existe"; exit 1; }
          test -d src/persistence || { echo "❌ src/persistence/ não existe"; exit 1; }
          test -d tests || { echo "❌ tests/ não existe"; exit 1; }
          echo "✅ Estrutura OK"

      - name: Run unit tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          echo "=== Executando testes ==="
          python -m pytest tests/unit/ -v --tb=short

      - name: Lint check
        run: |
          echo "=== Verificando qualidade de código ==="
          pip install ruff
          ruff check src/ tests/ || echo "⚠️  Issues de lint encontradas"

      - name: Verify setup script
        run: |
          echo "=== Verificando script de setup ==="
          bash -n scripts/setup.sh && echo "✅ setup.sh sintaxe OK"
          bash -n scripts/verify_dependencies.sh && echo "✅ verify_dependencies.sh sintaxe OK"
```

### Pre-commit Hooks

Evite commitar secrets ou código quebrado:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
        args: ["--maxkb=500"]
      - id: check-json
      - id: check-yaml
      - id: detect-private-key
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format

  - repo: local
    hooks:
      - id: check-env
        name: Verificar .env não commitado
        entry: bash -c 'git diff --cached --name-only | grep -q "^.env$" && echo "❌ .env NÃO PODE SER COMMITADO" && exit 1 || exit 0'
        language: system
        pass_filenames: false
```

```bash
# Instale os hooks
pip install pre-commit
pre-commit install

# Teste manualmente
pre-commit run --all-files
```

---

## 📈 Seção 15: Planejamento de Capacidade e Custos

### Entendendo o Consumo de Tokens

Long-running agents consomem tokens. É essencial entender os números antes de colocar em produção:

| Operação | Tokens Aproximados | Custo Estimado (USD) |
|----------|-------------------|----------------------|
| Hello World (1 chamada) | ~200 tokens | ~$0.001 |
| Generator simples (1 chamada) | ~800 tokens | ~$0.004 |
| Evaluator simples (1 chamada) | ~600 tokens | ~$0.003 |
| Pipeline G/E (2 chamadas) | ~1.400 tokens | ~$0.007 |
| Recomendação com 5 produtos | ~2.000 tokens | ~$0.010 |
| Conversa KODA de 1 hora | ~40.000 tokens | ~$0.200 |
| Conversa KODA de 4 horas | ~150.000 tokens | ~$0.750 |

### Calculadora de Custo Mensal

```python
# scripts/estimate_costs.py
"""Estimativa de custos mensais com base em volume."""

def estimate_monthly_cost(
    conversations_per_day: int,
    avg_tokens_per_conversation: int,
    model: str = "claude-sonnet-4-6",
) -> dict:
    """Calcula estimativa de custo mensal.

    Preços aproximados (Maio 2026):
    - Claude Sonnet 4: $3.00 / 1M input tokens, $15.00 / 1M output tokens
    - Claude Opus 4: $15.00 / 1M input tokens, $75.00 / 1M output tokens
    """

    prices = {
        "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
        "claude-opus-4-6": {"input": 15.00, "output": 75.00},
    }

    price = prices.get(model, prices["claude-sonnet-4-6"])

    # Conversas por mês
    monthly_conversations = conversations_per_day * 30

    # Tokens por mês (assume 70% input, 30% output)
    total_tokens = monthly_conversations * avg_tokens_per_conversation
    input_tokens = total_tokens * 0.7
    output_tokens = total_tokens * 0.3

    # Custos
    input_cost = (input_tokens / 1_000_000) * price["input"]
    output_cost = (output_tokens / 1_000_000) * price["output"]
    total_cost = input_cost + output_cost

    return {
        "model": model,
        "monthly_conversations": monthly_conversations,
        "total_tokens_millions": round(total_tokens / 1_000_000, 2),
        "estimated_monthly_cost_usd": round(total_cost, 2),
        "cost_per_conversation_usd": round(total_cost / monthly_conversations, 4),
    }


if __name__ == "__main__":
    # Cenário 1: Protótipo (10 conversas/dia)
    proto = estimate_monthly_cost(10, 40_000)
    print("=== PROTÓTIPO (10 conversas/dia) ===")
    for k, v in proto.items():
        print(f"  {k}: {v}")

    # Cenário 2: Produção leve (100 conversas/dia)
    prod = estimate_monthly_cost(100, 80_000)
    print("\n=== PRODUÇÃO LEVE (100 conversas/dia) ===")
    for k, v in prod.items():
        print(f"  {k}: {v}")

    # Cenário 3: Produção pesada (1000 conversas/dia)
    heavy = estimate_monthly_cost(1000, 100_000)
    print("\n=== PRODUÇÃO PESADA (1000 conversas/dia) ===")
    for k, v in heavy.items():
        print(f"  {k}: {v}")
```

### Estratégias de Otimização de Custo

1. **Use o modelo certo para cada tarefa:**
   - Generator? Sonnet (bom, barato)
   - Evaluator crítico? Opus (melhor, mais caro)
   - Validações simples? Sonnet com temperature=0

2. **Controle o tamanho do prompt:**
   - Comprima histórico de conversa
   - Remova tokens desnecessários (espaços extras, formatação)
   - Use system prompts concisos

3. **Cache de respostas comuns:**
   - Saudação inicial? Cache
   - Perguntas frequentes? Cache
   - Validações repetitivas? Cache

4. **Max tokens bem dimensionado:**
   - Generator: 1000-2000 tokens
   - Evaluator: 500-1000 tokens
   - Nunca use o default (4096) sem necessidade

---

## 🧪 Seção 16: Testes de Integração para o Pipeline

### Teste End-to-End do Pipeline

```python
# tests/integration/test_simple_pipeline.py
"""Testes de integração do pipeline Generator/Evaluator."""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.orchestration.simple_pipeline import run_pipeline


class TestSimplePipeline:
    """Testes de integração do pipeline mínimo."""

    @pytest.fixture
    def mock_generator_response(self):
        return json.dumps({
            "recommendations": [
                {
                    "name": "Whey Vegano Premium",
                    "price": 95.0,
                    "rationale": "100% vegano, sem lactose, alta proteína",
                    "restrictions_met": ["sem lactose", "vegano"],
                },
                {
                    "name": "Whey Isolado",
                    "price": 120.0,
                    "rationale": "Isolado puro, rápida absorção",
                    "restrictions_met": ["sem lactose"],
                },
            ]
        })

    @pytest.fixture
    def mock_evaluator_response(self):
        return json.dumps({
            "evaluations": [
                {
                    "product_name": "Whey Vegano Premium",
                    "checks": {"budget_ok": True, "restrictions_ok": True, "rationale_clear": True},
                    "score": 9,
                    "notes": "Excelente recomendação",
                },
                {
                    "product_name": "Whey Isolado",
                    "checks": {"budget_ok": True, "restrictions_ok": True, "rationale_clear": True},
                    "score": 8,
                    "notes": "Boa alternativa",
                },
            ],
            "overall_score": 8.5,
            "verdict": "APPROVED",
            "issues": [],
        })

    @patch("src.agents.simple_generator.SimpleGenerator.call_llm")
    @patch("src.agents.simple_evaluator.SimpleEvaluator.call_llm")
    def test_pipeline_runs_end_to_end(
        self, mock_eval_call, mock_gen_call,
        mock_generator_response, mock_evaluator_response,
    ):
        """Pipeline deve executar generator → evaluator com sucesso."""
        mock_gen_call.return_value = mock_generator_response
        mock_eval_call.return_value = mock_evaluator_response

        result = run_pipeline(
            customer_id="wa_teste_integration",
            case_id="test_001",
            goal="ganho muscular",
            budget=150.0,
            restrictions=["sem lactose"],
        )

        assert result["verdict"]["verdict"] == "APPROVED"
        assert result["verdict"]["overall_score"] == 8.5
        assert len(result["draft"]["recommendations"]) == 2

        # Verifica que arquivos de estado foram criados
        state_dir = Path(result["state_dir"])
        assert (state_dir / "context.json").exists()
        assert (state_dir / "draft_v1.json").exists()
        assert (state_dir / "verdict_v1.json").exists()
        assert (state_dir / "audit_log.jsonl").exists()

    @patch("src.agents.simple_evaluator.SimpleEvaluator.call_llm")
    @patch("src.agents.simple_generator.SimpleGenerator.call_llm")
    def test_pipeline_handles_rejection(
        self, mock_gen_call, mock_eval_call,
        mock_generator_response,
    ):
        """Pipeline deve lidar com rejeição do evaluator."""
        mock_gen_call.return_value = mock_generator_response
        mock_eval_call.return_value = json.dumps({
            "evaluations": [],
            "overall_score": 3.0,
            "verdict": "REJECTED",
            "issues": ["Produto contém lactose e cliente é intolerante"],
        })

        result = run_pipeline(
            customer_id="wa_teste_rejection",
            case_id="test_002",
            goal="ganho muscular",
            budget=150.0,
            restrictions=["sem lactose"],
        )

        assert result["verdict"]["verdict"] == "REJECTED"
        assert len(result["verdict"]["issues"]) > 0

    def test_pipeline_creates_unique_state_dirs(self):
        """Cada execução deve criar diretório de estado único."""
        with patch("src.agents.simple_generator.SimpleGenerator.call_llm") as mock_gen, \
             patch("src.agents.simple_evaluator.SimpleEvaluator.call_llm") as mock_eval:

            mock_gen.return_value = json.dumps({"recommendations": []})
            mock_eval.return_value = json.dumps({
                "evaluations": [],
                "overall_score": 5,
                "verdict": "REJECTED",
                "issues": [],
            })

            result1 = run_pipeline("wa_a", "case_a")
            result2 = run_pipeline("wa_b", "case_b")

            assert result1["state_dir"] != result2["state_dir"]
```

---

## 📋 Seção 17: Checklist de Verificação de Setup — Versão Detalhada

### Script de Verificação Completo

```python
#!/usr/bin/env python3
# scripts/verify_setup_full.py
"""Verificação detalhada — cobre TODOS os aspectos do ambiente."""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime


class SetupVerifier:
    """Verificador completo do ambiente de desenvolvimento."""

    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0
        self.start_time = datetime.now()

    def check(self, category: str, label: str, condition: bool, fix: str = "") -> None:
        """Executa uma verificação e reporta."""
        status = "✅" if condition else "❌"
        print(f"  {status} [{category}] {label}")
        if not condition:
            self.checks_failed += 1
            if fix:
                print(f"     🔧 Corrigir: {fix}")
        else:
            self.checks_passed += 1

    def warn(self, category: str, label: str, condition: bool, detail: str = "") -> None:
        """Verificação opcional (warning se falhar)."""
        if condition:
            print(f"  ✅ [{category}] {label}")
            self.checks_passed += 1
        else:
            print(f"  ⚠️  [{category}] {label}")
            if detail:
                print(f"     ℹ️  {detail}")
            self.warnings += 1

    def run_all(self) -> bool:
        """Executa todas as verificações."""
        print("=" * 70)
        print("  VERIFICAÇÃO COMPLETA DE SETUP")
        print(f"  Iniciado em: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # === 1. Sistema Operacional ===
        print("\n🖥️  SISTEMA OPERACIONAL")
        import platform
        system = platform.system()
        self.check("Sistema", "Sistema suportado", system in ["Linux", "Darwin"],
                   "Use Linux ou macOS para desenvolvimento")
        self.check("Python", "Python 3.10+", self._check_python_version(),
                   "Instale Python 3.10 ou superior: https://python.org")

        # === 2. Diretórios ===
        print("\n📁 ESTRUTURA DE DIRETÓRIOS")
        required_dirs = {
            "src/agents": "mkdir -p src/agents",
            "src/orchestration": "mkdir -p src/orchestration",
            "src/persistence": "mkdir -p src/persistence",
            "src/tools": "mkdir -p src/tools",
            "src/config": "mkdir -p src/config",
            "src/evaluation": "mkdir -p src/evaluation",
            "state": "mkdir -p state",
            "logs/agent_traces": "mkdir -p logs/agent_traces",
            "logs/system": "mkdir -p logs/system",
            "tests/unit": "mkdir -p tests/unit",
            "tests/integration": "mkdir -p tests/integration",
            "tests/fixtures": "mkdir -p tests/fixtures",
            "scripts": "mkdir -p scripts",
            "docs": "mkdir -p docs",
        }
        for dir_path, fix_cmd in required_dirs.items():
            self.check("Diretório", f"{dir_path}/", Path(dir_path).is_dir(), fix_cmd)

        # === 3. Dependências Python ===
        print("\n📦 DEPENDÊNCIAS PYTHON")
        required_packages = [
            ("anthropic", "pip install anthropic>=0.39.0"),
            ("pydantic", "pip install pydantic>=2.0"),
            ("dotenv", "pip install python-dotenv>=1.0"),
            ("structlog", "pip install structlog>=24.0"),
            ("pytest", "pip install pytest>=8.0"),
        ]
        for pkg, fix in required_packages:
            try:
                __import__(pkg)
                self.check("Python", pkg, True)
            except ImportError:
                self.check("Python", pkg, False, fix)

        # === 4. Variáveis de Ambiente ===
        print("\n🔑 VARIÁVEIS DE AMBIENTE")
        from dotenv import load_dotenv
        import os
        load_dotenv()

        has_env = Path(".env").exists()
        self.check("Config", ".env existe", has_env,
                   "Copie: cp .env.example .env")

        if has_env:
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
            is_placeholder = "xxxx" in api_key or "placeholder" in api_key.lower()
            has_key = bool(
                api_key
                and api_key.startswith("sk-ant-")
                and len(api_key) > 30
                and not is_placeholder
            )
            self.check("Config", "ANTHROPIC_API_KEY configurada", has_key,
                       "Configure sua key real em .env (não use placeholder)")

        # === 5. Git ===
        print("\n🔧 GIT")
        git_dir = Path(".git").is_dir()
        self.check("Git", "Repositório inicializado", git_dir,
                   "Execute: git init")

        gitignore = Path(".gitignore")
        if gitignore.exists():
            content = gitignore.read_text()
            essential_ignores = [
                (".env", ".env no .gitignore"),
                ("state/", "state/ no .gitignore"),
                ("logs/", "logs/ no .gitignore"),
                ("venv/", "venv/ no .gitignore"),
                ("__pycache__/", "__pycache__/ no .gitignore"),
            ]
            for pattern, msg in essential_ignores:
                self.check("Git", msg, pattern in content,
                           f"Adicione '{pattern}' ao .gitignore")
        else:
            self.check("Git", ".gitignore existe", False,
                       "Crie .gitignore com padrões essenciais")

        # === 6. Arquivos de Configuração ===
        print("\n📄 ARQUIVOS DE CONFIGURAÇÃO")
        config_files = {
            ".env.example": "Template de variáveis de ambiente",
            "README.md": "Documentação do projeto",
            "AGENTS.md": "Regras para agentes AI",
        }
        for fname, desc in config_files.items():
            exists = Path(fname).is_file()
            self.warn("Config", f"{fname} ({desc})", exists,
                      f"Arquivo opcional mas recomendado: {fname}")

        # === 7. Scripts ===
        print("\n🛠️  SCRIPTS OPERACIONAIS")
        script_files = {
            "scripts/setup.sh": "Script de setup principal",
            "scripts/verify_dependencies.sh": "Verificação de dependências",
        }
        for fname, desc in script_files.items():
            exists = Path(fname).is_file()
            self.warn("Scripts", f"{fname} ({desc})", exists)

        if Path("scripts/setup.sh").exists():
            self.check("Scripts", "setup.sh é executável",
                       Path("scripts/setup.sh").stat().st_mode & 0o111,
                       "chmod +x scripts/setup.sh")

        # === 8. Testes ===
        print("\n🧪 TESTES")
        test_files = list(Path("tests/unit").glob("test_*.py"))
        self.warn("Testes", f"Testes unitários encontrados: {len(test_files)}", len(test_files) > 0,
                  "Crie testes em tests/unit/")

        # === 9. Node.js (opcional) ===
        print("\n🟢 NODE.JS (opcional)")
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            self.warn("Node.js", f"Node.js {result.stdout.strip()}", True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.warn("Node.js", "Node.js instalado", False,
                      "Opcional. Instale: https://nodejs.org")

        # === 10. Conectividade ===
        print("\n🌐 CONECTIVIDADE")
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                 "--max-time", "5", "https://api.anthropic.com"],
                capture_output=True, text=True, timeout=10,
            )
            status_code = result.stdout.strip()
            reachable = status_code in ["200", "401", "403"]
            self.check("Rede", "api.anthropic.com acessível", reachable,
                       "Verifique sua conexão de internet")
        except Exception:
            self.check("Rede", "api.anthropic.com acessível", False,
                       "Sem conectividade com a API Anthropic")

        # === Resumo ===
        elapsed = (datetime.now() - self.start_time).total_seconds()
        total = self.checks_passed + self.checks_failed + self.warnings

        print(f"\n{'=' * 70}")
        print(f"  RESUMO DA VERIFICAÇÃO")
        print(f"{'=' * 70}")
        print(f"  ✅ Passaram:   {self.checks_passed}/{total}")
        print(f"  ❌ Falharam:   {self.checks_failed}/{total}")
        print(f"  ⚠️  Warnings:   {self.warnings}/{total}")
        print(f"  ⏱️  Tempo:       {elapsed:.1f}s")
        print(f"{'=' * 70}")

        if self.checks_failed == 0:
            print("\n✅ AMBIENTE PRONTO PARA DESENVOLVIMENTO!")
            print("   Execute: python3 src/hello_agent.py")
            return True
        else:
            print(f"\n❌ {self.checks_failed} verificação(ões) crítica(s) falhou(ram).")
            print("   Corrija os itens marcados com ❌ antes de continuar.")
            return False

    @staticmethod
    def _check_python_version() -> bool:
        """Verifica versão do Python."""
        import sys
        return sys.version_info >= (3, 10)


if __name__ == "__main__":
    verifier = SetupVerifier()
    success = verifier.run_all()
    sys.exit(0 if success else 1)
```

---

## 🗺️ Seção 18: Roadmap do Desenvolvedor — Primeira Semana

### Dia 1: Setup e Hello World (2-3 horas)

| Hora | Atividade | Resultado Esperado |
|------|-----------|-------------------|
| 09:00 | Ler este guia (Seções 1-4) | Entender estrutura e dependências |
| 09:45 | Executar `scripts/setup.sh` | Ambiente virtual criado, deps instaladas |
| 10:15 | Configurar `.env` com API key | `ANTHROPIC_API_KEY` funcionando |
| 10:30 | Rodar `python3 src/hello_agent.py` | Primeira resposta do Claude |
| 11:00 | Rodar `verify_setup_full.py` | Todos os checks passando |
| 11:30 | Revisar estrutura de diretórios | Entender o que cada pasta faz |
| 12:00 | Almoço | 🍽️ |

### Dia 2: Segundo Agente e Pipeline (2-3 horas)

| Hora | Atividade | Resultado Esperado |
|------|-----------|-------------------|
| 09:00 | Estudar `SimpleGenerator` (Seção 13) | Entender classe do agente gerador |
| 10:00 | Estudar `SimpleEvaluator` (Seção 13) | Entender classe do agente avaliador |
| 11:00 | Executar `simple_pipeline.py` | Pipeline G/E funcionando |
| 11:30 | Inspecionar arquivos em `state/` | Entender persistência de estado |
| 12:00 | Escrever teste unitário simples | Primeiro teste passando |

### Dia 3: Conceitos Fundamentais (2-3 horas)

| Hora | Atividade | Resultado Esperado |
|------|-----------|-------------------|
| 09:00 | Ler Nível 1: `01-why-agents-lose-plot.md` | Entender os 3 problemas |
| 10:30 | Relacionar problemas com pipeline G/E | Ver como G/E resolve cada problema |
| 11:30 | Discutir com a equipe | Compartilhar descobertas |

### Dia 4-5: Implementação Guiada

| Atividade | Resultado Esperado |
|-----------|-------------------|
| Adaptar `SimpleGenerator` para domínio real | Agente que gera recomendações do seu negócio |
| Criar rubrica de avaliação (baseada em Nível 2) | Critérios de qualidade específicos |
| Rodar pipeline com dados reais (mockados) | Primeiro pipeline de domínio funcionando |
| Implementar `StateManager` para multi-sessão | Estado persiste entre execuções |

---

## 🔗 Seção 19: Referências Rápidas

### Comandos Mais Usados

```bash
# Ativar ambiente
source venv/bin/activate

# Executar hello world
python3 src/hello_agent.py

# Executar pipeline G/E
python3 src/orchestration/simple_pipeline.py

# Rodar testes
pytest tests/ -v

# Rodar testes com coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Verificar setup
python3 scripts/verify_setup_full.py

# Verificar dependências
bash scripts/verify_dependencies.sh

# Limpar estado de testes
rm -rf state/wa_teste/

# Ver logs de trace
ls -la logs/agent_traces/
cat logs/agent_traces/*/simple_generator_*.json | python3 -m json.tool | head -50

# Verificar .env não foi commitado
git status | grep .env && echo "⚠️ Cuidado!" || echo "✅ OK"
```

### Paths Importantes

| Path | Propósito |
|------|----------|
| `src/config/settings.py` | Toda configuração centralizada |
| `src/agents/base_agent.py` | Classe base de agentes |
| `src/persistence/state_manager.py` | Gerenciador de estado |
| `src/persistence/trace_logger.py` | Logger de debugging |
| `state/` | Dados runtime (não commitado) |
| `logs/agent_traces/` | Traces de execução |
| `.env` | API keys e config (NUNCA commitar) |
| `.env.example` | Template de config (commitar) |
| `scripts/setup.sh` | Setup automatizado |
| `scripts/verify_setup_full.py` | Verificação de ambiente |

### Sinais de que o Setup Está Saudável

- [x] `verify_setup_full.py` retorna 0 erros
- [x] `hello_agent.py` retorna saudação do Claude em < 2 segundos
- [x] `simple_pipeline.py` gera arquivos em `state/`
- [x] `pytest tests/ -v` passa todos os testes
- [x] `git status` não mostra `.env` como tracked
- [x] Você consegue explicar a estrutura de diretórios em 30 segundos
- [x] Um novo membro da equipe conseguiu rodar o setup sozinho

---

*Setup validado. Ambiente estável. Primeiro agente funcionando. Você está pronto.*

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | 01-setup-guide.md |
| **Módulo** | 07 - Implementation Guides |
| **Tempo** | 90 minutos |
| **Status** | ✅ Completo |
| **Próximo** | 02-team-progression-guide.md |
| **Dependências** | Nenhuma (independente) |
| **Aplicável a** | Todos os níveis (1-4) |
| **Atualizado** | Maio 2026 |
