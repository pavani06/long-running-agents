#!/bin/bash
# =============================================================================
# setup-analysis.sh — Bootstrap para o pipeline analyze-and-improve
#
# Cria PROGRESS.md e harness/test-results.json no repo alvo com os parâmetros
# de uma nova sessão de análise. Portátil — funciona em qualquer repo que
# tenha o skill analyze-and-improve instalado.
#
# Uso:
#   ./setup-analysis.sh --source <path|url> [--date YYYY-MM-DD] [--source-slug <slug>] [--target-repo <path>] [--dry-run]
#
# Parâmetros:
#   --source       (obrigatório) Path absoluto ou URL do documento fonte
#   --date         (opcional)    Data no formato YYYY-MM-DD. Default: hoje
#   --source-slug  (opcional)    Slug curto para output dir. Default: derivado do nome do arquivo
#   --target-repo  (opcional)    Path do repo alvo. Default: diretório corrente
#   --dry-run      (opcional)    Apenas preview, não escreve arquivos
#   --help, -h                   Mostra esta mensagem
#
# Dependências: apenas bash builtins + date + mkdir + sed (sem python3/jq)
# =============================================================================

set -euo pipefail

# ── Cores para output ───────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}   $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ── Resolve o diretório do script (para encontrar templates) ────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="${SCRIPT_DIR}/templates"

# ── Defaults ────────────────────────────────────────────────────────────────────
SOURCE=""
DATE=""
SOURCE_SLUG=""
TARGET_REPO="$(pwd)"
DRY_RUN=false

# ── Help ────────────────────────────────────────────────────────────────────────
show_help() {
    sed -n '2,18p' "$0" | sed 's/^# //'
    echo ""
    echo "Exemplos:"
    echo "  $0 --source Raw-Knowledge/sources/2026-06-11-minha-talk.md"
    echo "  $0 --source Raw-Knowledge/sources/talk.md --date 2026-06-11 --source-slug minha-talk"
    echo "  $0 --source https://example.com/article --target-repo /home/user/meu-repo --dry-run"
    exit 0
}

# ── Parse argumentos ────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --source)
            SOURCE="${2:-}"
            shift 2
            ;;
        --date)
            DATE="${2:-}"
            shift 2
            ;;
        --source-slug)
            SOURCE_SLUG="${2:-}"
            shift 2
            ;;
        --target-repo)
            TARGET_REPO="${2:-}"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            show_help
            ;;
        *)
            log_error "Argumento desconhecido: $1"
            echo "Use --help para ver as opções."
            exit 1
            ;;
    esac
done

# ── Validação ───────────────────────────────────────────────────────────────────
if [ -z "$SOURCE" ]; then
    log_error "--source é obrigatório."
    echo "Use --help para ver as opções."
    exit 1
fi

# Deriva date se não fornecido
if [ -z "$DATE" ]; then
    DATE=$(date +%Y-%m-%d 2>/dev/null) || {
        log_error "Não foi possível obter a data atual. Forneça --date explicitamente."
        exit 1
    }
fi

# Valida formato da data
if [[ ! "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    log_error "Formato de data inválido: '$DATE'. Use YYYY-MM-DD."
    exit 1
fi

# Deriva source-slug se não fornecido
if [ -z "$SOURCE_SLUG" ]; then
    # Extrai o nome do arquivo (último componente do path) e remove extensão
    SOURCE_SLUG=$(basename "$SOURCE" 2>/dev/null || echo "$SOURCE")
    SOURCE_SLUG="${SOURCE_SLUG%.md}"
    SOURCE_SLUG="${SOURCE_SLUG%.txt}"
    SOURCE_SLUG="${SOURCE_SLUG%.pdf}"

    # Remove prefixo de data se presente (ex: 2026-06-11- → "")
    SOURCE_SLUG=$(echo "$SOURCE_SLUG" | sed -E 's/^[0-9]{4}-[0-9]{2}-[0-9]{2}-//')

    if [ -z "$SOURCE_SLUG" ]; then
        log_error "Não foi possível derivar source-slug do path '$SOURCE'. Forneça --source-slug explicitamente."
        exit 1
    fi
fi

# Valida target-repo
if [ ! -d "$TARGET_REPO" ]; then
    log_error "Target repo não encontrado: $TARGET_REPO"
    exit 1
fi

if [ ! -d "$TARGET_REPO/.git" ] && [ ! -f "$TARGET_REPO/.git" ]; then
    log_warn "$TARGET_REPO não parece ser um repositório git. Continuando mesmo assim."
fi

# Verifica templates
if [ ! -f "$TEMPLATES_DIR/PROGRESS.md" ]; then
    log_error "Template PROGRESS.md não encontrado em: $TEMPLATES_DIR/PROGRESS.md"
    exit 1
fi

if [ ! -f "$TEMPLATES_DIR/test-results.json" ]; then
    log_error "Template test-results.json não encontrado em: $TEMPLATES_DIR/test-results.json"
    exit 1
fi

# ── Variáveis derivadas ─────────────────────────────────────────────────────────
DATE_SLUG="${DATE}-${SOURCE_SLUG}"
OUTPUT_DIR="docs/analysis/${DATE_SLUG}"
PROGRESS_OUT="${TARGET_REPO}/PROGRESS.md"
RESULTS_OUT="${TARGET_REPO}/harness/test-results.json"
HARNESS_DIR="${TARGET_REPO}/harness"

# ── Preview ─────────────────────────────────────────────────────────────────────

echo ""
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  analyze-and-improve — Setup de Sessão de Análise${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo ""
log_info "Parâmetros resolvidos:"
echo "  source:       $SOURCE"
echo "  date:         $DATE"
echo "  source-slug:  $SOURCE_SLUG"
echo "  target-repo:  $TARGET_REPO"
echo "  output_dir:   $OUTPUT_DIR"
echo ""

# ── Verifica se arquivos já existem ─────────────────────────────────────────────
EXISTING_FILES=""
if [ -f "$PROGRESS_OUT" ]; then
    EXISTING_FILES="$EXISTING_FILES  - PROGRESS.md (já existe)\n"
fi
if [ -f "$RESULTS_OUT" ]; then
    EXISTING_FILES="$EXISTING_FILES  - harness/test-results.json (já existe)\n"
fi

if [ -n "$EXISTING_FILES" ]; then
    log_warn "Arquivos já existem no repo alvo:"
    echo -e "$EXISTING_FILES"
    if [ "$DRY_RUN" = false ]; then
        echo ""
        log_warn "Execute com --dry-run primeiro para revisar, ou remova os arquivos manualmente."
        log_info "Para resetar o estado para uma nova análise, delete:"
        echo "  rm $PROGRESS_OUT"
        echo "  rm $RESULTS_OUT"
        echo ""
        read -rp "Sobrescrever mesmo assim? [s/N] " CONFIRM
        if [[ ! "$CONFIRM" =~ ^[Ss]$ ]]; then
            log_info "Abortado pelo usuário."
            exit 0
        fi
    fi
fi

# ── Dry-run: apenas preview ─────────────────────────────────────────────────────
if [ "$DRY_RUN" = true ]; then
    echo ""
    log_info "DRY-RUN: Nenhum arquivo será escrito."
    echo ""
    log_info "Arquivos que seriam criados:"
    echo "  1. $PROGRESS_OUT"
    echo "  2. $RESULTS_OUT"
    echo "  3. $OUTPUT_DIR/ (diretório de output)"
    echo "  4. $HARNESS_DIR/ (diretório do harness, se não existir)"
    echo "  5. $HARNESS_DIR/templates/STEER.md (se não existir)"
    echo ""
    log_info "Conteúdo que seria gerado (PROGRESS.md):"
    echo "---"
    sed -e "s|{{SOURCE}}|$SOURCE|g" \
        -e "s|{{DATE}}|$DATE|g" \
        -e "s|{{SOURCE_SLUG}}|$SOURCE_SLUG|g" \
        "$TEMPLATES_DIR/PROGRESS.md"
    echo "---"
    echo ""
    log_info "Conteúdo que seria gerado (test-results.json — primeiro e último bloco):"
    echo "---"
    sed -e "s|{{DATE_SLUG}}|$DATE_SLUG|g" \
        "$TEMPLATES_DIR/test-results.json" | {
        # Mostra phase-0 e phase-6 para preview
        awk 'BEGIN{count=0} /"phase-0"/{p=1} p{print; if(/^\s{2}\},?$/)p=0; count++} /"phase-6"/{p=1} p{print; if(/^\s{2}\},?$/)p=0}' || true
    }
    echo "---"
    echo ""
    log_ok "Dry-run concluído. Remova --dry-run para aplicar."
    exit 0
fi

# ── Criação dos diretórios ──────────────────────────────────────────────────────
log_info "Criando diretórios..."
mkdir -p "$TARGET_REPO/$OUTPUT_DIR" || {
    log_error "Falha ao criar diretório de output: $TARGET_REPO/$OUTPUT_DIR"
    exit 1
}
log_ok "Criado: $OUTPUT_DIR"

mkdir -p "$HARNESS_DIR/templates" || {
    log_error "Falha ao criar diretório do harness: $HARNESS_DIR"
    exit 1
}
log_ok "Criado: harness/templates/"

# ── Geração do PROGRESS.md ─────────────────────────────────────────────────────
log_info "Gerando PROGRESS.md..."
sed -e "s|{{SOURCE}}|$SOURCE|g" \
    -e "s|{{DATE}}|$DATE|g" \
    -e "s|{{SOURCE_SLUG}}|$SOURCE_SLUG|g" \
    "$TEMPLATES_DIR/PROGRESS.md" > "$PROGRESS_OUT"

if [ -s "$PROGRESS_OUT" ]; then
    log_ok "PROGRESS.md gerado com sucesso ($(wc -l < "$PROGRESS_OUT") linhas)"
else
    log_error "PROGRESS.md gerado vazio. Abortando."
    exit 1
fi

# ── Geração do test-results.json ───────────────────────────────────────────────
log_info "Gerando harness/test-results.json..."
sed -e "s|{{DATE_SLUG}}|$DATE_SLUG|g" \
    "$TEMPLATES_DIR/test-results.json" > "$RESULTS_OUT"

# Valida JSON gerado
if command -v python3 &>/dev/null; then
    if python3 -c "import json; json.load(open('$RESULTS_OUT'))" 2>/dev/null; then
        log_ok "test-results.json gerado com sucesso (JSON válido)"
    else
        log_error "test-results.json gerado com JSON inválido."
        exit 1
    fi
else
    # Fallback: verifica se o arquivo tem conteúdo e começa com {
    if [ -s "$RESULTS_OUT" ] && head -c1 "$RESULTS_OUT" | grep -q '{'; then
        log_ok "test-results.json gerado ($(wc -l < "$RESULTS_OUT") linhas)"
    else
        log_error "test-results.json parece inválido."
        exit 1
    fi
fi

# ── STEER.md (se não existir) ───────────────────────────────────────────────────
STEER_OUT="${HARNESS_DIR}/templates/STEER.md"
if [ ! -f "$STEER_OUT" ]; then
    log_info "Criando harness/templates/STEER.md..."
    cat > "$STEER_OUT" <<'STEEREOF'
# STEER.md — Canal de Redirecionamento

> Este arquivo é monitorado pelo harness. Escreva aqui para redirecionar o
> agente no meio de uma sessão longa sem precisar reiniciar.
>
> O harness lê este arquivo antes de cada fase. Se encontrar conteúdo, ele:
> 1. Lê a orientação
> 2. Incorpora imediatamente (prioridade sobre o plano atual)
> 3. Limpa o arquivo (para evitar re-leitura)
>
> **Uso:** `echo "sua orientação aqui" > harness/templates/STEER.md`
>
> **Exemplos:**
> - "Phase-3: o classification.md está genérico. Use os patterns extraídos
>   na fase 2 como input. Compare cada pattern com o que já existe em
>   docs/canonical/. Seja específico."
> - "Pule a phase-6 — não há Missing patterns para integrar."
> - "Antes de continuar, verifique que todos os YAML têm aliases no frontmatter."
>
<!-- Apague esta mensagem placeholder na primeira vez que usar o canal -->
STEEREOF
    log_ok "STEER.md criado."
else
    log_info "STEER.md já existe — mantido."
fi

# ── Sumário ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Setup concluído com sucesso!${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
echo ""
log_info "Arquivos criados/modificados:"
echo "  ✓ $PROGRESS_OUT"
echo "  ✓ $RESULTS_OUT"
echo "  ✓ $TARGET_REPO/$OUTPUT_DIR/"
if [ ! -f "$STEER_OUT" ]; then true; else
echo "  ✓ $STEER_OUT"
fi
echo ""
log_info "Próximos passos:"
echo "  1. Verifique PROGRESS.md e ajuste se necessário"
echo "  2. Execute o pipeline:"
echo "     - Modo nativo:   Load harness-analyze-and-improve"
echo "     - Modo bash:     ./harness/harness-analysis.sh"
echo "  3. Acompanhe o progresso: cat PROGRESS.md"
