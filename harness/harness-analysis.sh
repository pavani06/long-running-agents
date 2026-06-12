#!/bin/bash
# =============================================================================
# harness-analysis.sh — Loop de qualidade para analyze-and-improve
#
# Adaptado de harness.sh para o pipeline analyze-and-improve.
# Cada feature = uma fase do pipeline (phase-0 a phase-6).
#
# Uso:
#   ./harness/harness-analysis.sh                    # loop interativo
#   ./harness/harness-analysis.sh --once             # executa UMA iteração e para
#   ./harness/harness-analysis.sh --feature phase-0  # executa apenas a fase especificada
#   AGENT_STOP=1 ./harness/harness-analysis.sh       # para na próxima iteração
#
# Dependências:
#   - OpenCode CLI (opencode) instalado
#   - PROGRESS.md, harness/test-results.json configurados
#   - Skill analyze-and-improve instalada
# =============================================================================

set -euo pipefail

# ── Configuração (apontando para arquivos DENTRO do repo) ───────────────────────

RESULTS_FILE="${RESULTS_FILE:-harness/test-results.json}"
EVIDENCE_LOG="${EVIDENCE_LOG:-harness/.evidence-reads}"
PROGRESS_FILE="${PROGRESS_FILE:-PROGRESS.md}"
STEER_FILE="${STEER_FILE:-harness/templates/STEER.md}"
STOP_FILE="${STOP_FILE:-AGENT_STOP}"
MAX_ITERATIONS="${MAX_ITERATIONS:-20}"
AGENT_CLI="${AGENT_CLI:-opencode}"
EVALUATOR_AGENT="${EVALUATOR_AGENT:-evaluator}"

# ── Minimum Environment Requirements ────────────────────────────────────────────
#
# Este script foi adaptado para funcionar em ambientes com PATH restrito.
# Dependencias obrigatorias:
#   - /bin/bash (shebang #!/bin/bash, NAO #!/usr/bin/env bash)
#   - git (para commits, diffs, e verificacao de repo)
#   - opencode CLI (para delegacao de fases)
#
# Dependencias removidas (implementacoes bash-only como fallback):
#   - python3: substituido por bash regex em get_next_feature() e run_evaluator()
#   - jq: nao necessario (bash regex cobre o parse de JSON simples)
#   - grep -P: substituido por bash [[ =~ ]] com regex em run_builder()
#   - date: removido de commit_checkpoint() (mensagem estatica)
#   - mkdir/cp/chmod: use write/edit tools do opencode para manipulacao de arquivos
#   - ls/find: use read tool do opencode para listagem de diretorios
#
# Se python3 ou jq estiverem disponiveis, as funcoes os utilizam preferencialmente.
# As implementacoes bash-only sao fallbacks automaticos quando as ferramentas faltam.

# ── Cores para output ───────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ── Utilidades ────────────────────────────────────────────────────────────────

log_section() {
    echo ""
    echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

log_info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}   $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ── Verificações de pré-condição ──────────────────────────────────────────────

check_prerequisites() {
    local errors=0

    if ! command -v "$AGENT_CLI" &>/dev/null; then
        log_error "CLI do agente '$AGENT_CLI' não encontrada. Instale ou defina AGENT_CLI."
        errors=$((errors + 1))
    fi

    # JSON parsing uses bash builtins — no external dependency required

    if ! git rev-parse --git-dir &>/dev/null; then
        log_error "Não está em um repositório git. Execute de dentro do projeto."
        errors=$((errors + 1))
    fi

    if [ ! -f "$PROGRESS_FILE" ]; then
        log_error "$PROGRESS_FILE não encontrado. Crie com as fases do analyze-and-improve."
        errors=$((errors + 1))
    fi

    if [ ! -f "$RESULTS_FILE" ]; then
        log_error "$RESULTS_FILE não encontrado. Crie com os contratos de cada fase."
        errors=$((errors + 1))
    fi

    return $errors
}

# ── Lógica de contrato ────────────────────────────────────────────────────────

# Retorna o nome da próxima fase com passes=false (bash puro)
get_next_feature() {
    local in_block=false
    local current_key=""
    while IFS= read -r line; do
        # Detect start of a phase block: "phase-N": {
        if [[ "$line" =~ ^[[:space:]]*\"(phase-[0-9]+)\"[[:space:]]*:[[:space:]]*\{$ ]]; then
            current_key="${BASH_REMATCH[1]}"
            in_block=true
            continue
        fi
        # Inside a block, look for "passes": false
        if $in_block && [[ "$line" =~ \"passes\"[[:space:]]*:[[:space:]]*false ]]; then
            echo "$current_key"
            return 0
        fi
        # End of block
        if $in_block && [[ "$line" =~ ^[[:space:]]*\},?$ ]]; then
            in_block=false
            current_key=""
        fi
    done < "$RESULTS_FILE"
    return 1
}

# Retorna true se ainda há fases pendentes
has_pending_features() {
    local feature
    feature=$(get_next_feature 2>/dev/null)
    [ -n "$feature" ]
}

# ── Kill Switch ────────────────────────────────────────────────────────────────

check_kill_switch() {
    if [ -f "$STOP_FILE" ]; then
        log_warn "Kill switch ativo: $STOP_FILE existe."
        log_info "Remova o arquivo para continuar: rm $STOP_FILE"
        return 1
    fi
    return 0
}

# ── Steering ───────────────────────────────────────────────────────────────────

check_steering() {
    if [ -f "$STEER_FILE" ] && [ -s "$STEER_FILE" ]; then
        local steer_content
        steer_content=$(cat "$STEER_FILE")
        log_warn "STEER.md tem conteúdo. Injetando no builder..."
        echo "$steer_content"
        # Restaura o placeholder completo após leitura (nunca deixa vazio)
        cat > "$STEER_FILE" <<'EOF'
# STEER.md — Canal de Redirecionamento

> Este arquivo é monitorado pelo agente. Escreva aqui para redirecionar o
> agente no meio de uma sessão longa sem precisar reiniciar.
>
> O agente lê este arquivo periodicamente. Se encontrar conteúdo, ele:
> 1. Lê a orientação
> 2. Incorpora imediatamente (prioridade sobre o plano atual)
> 3. Limpa o arquivo (para evitar re-leitura)
>
> **Uso:** `echo "sua orientação aqui" > STEER.md`
>
> **Exemplos:**
> - "Pare de usar PostgreSQL. Migre tudo para SQLite."
> - "Ignore a feature atual. Priorize correção de bug no login."
> - "O layout está muito escuro. Use tons mais claros no tema."
> - "Antes de continuar, adicione testes para o módulo auth."

<!-- Apague esta mensagem placeholder na primeira vez que usar o canal -->
EOF
        return 0
    fi
    return 1
}

# ── Evidência ──────────────────────────────────────────────────────────────────

check_evidence() {
    if [ ! -f "$EVIDENCE_LOG" ] || [ ! -s "$EVIDENCE_LOG" ]; then
        log_error "DENY: Nenhuma evidência foi lida nesta sessão."
        log_info "O builder deve abrir os outputs da fase com Read antes de concluir."
        return 1
    fi

    local valid_evidence=0
    while IFS= read -r evidence_file; do
        if [ -f "$evidence_file" ] && [ -s "$evidence_file" ]; then
            log_ok "Evidência válida: $evidence_file"
            valid_evidence=$((valid_evidence + 1))
        else
            log_warn "Evidência inválida ou vazia: $evidence_file"
        fi
    done < "$EVIDENCE_LOG"

    if [ "$valid_evidence" -eq 0 ]; then
        log_error "DENY: Nenhuma evidência válida encontrada."
        return 1
    fi

    : > "$EVIDENCE_LOG"
    return 0
}

# ── Métricas ────────────────────────────────────────────────────────────────────

# Registra um campo de métrica no test-results.json usando bash builtins.
# Uso: write_metric <phase> <field> <value>
write_metric() {
    local phase="$1"
    local field="$2"
    local value="$3"
    local tmpfile="${RESULTS_FILE}.tmp"
    local in_target=false

    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*\"$phase\"[[:space:]]*:[[:space:]]*\{$ ]]; then
            in_target=true
            echo "$line"
        elif $in_target && [[ "$line" =~ \"$field\"[[:space:]]*:[[:space:]]* ]]; then
            # Substitui o valor do campo (null, 0, ou string existente)
            if [[ "$value" =~ ^[0-9]+$ ]] || [ "$value" = "null" ]; then
                echo "$line" | sed -E "s/(\"$field\"[[:space:]]*:[[:space:]]*)[^,]*,/\1$value,/"
            else
                echo "$line" | sed -E "s/(\"$field\"[[:space:]]*:[[:space:]]*)[^,]*,/\1\"$value\",/"
            fi
        else
            if $in_target && [[ "$line" =~ ^[[:space:]]*\},?$ ]]; then
                in_target=false
            fi
            echo "$line"
        fi
    done < "$RESULTS_FILE" > "$tmpfile" && command mv "$tmpfile" "$RESULTS_FILE" 2>/dev/null || true
}

# Gera sumário de métricas a partir do test-results.json.
report_metrics() {
    echo ""
    echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Pipeline Metrics Summary${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo ""

    local total_duration=0
    local total_retries=0
    local phase
    local in_block=false
    local current_phase=""
    local current_duration=""
    local current_retries=""

    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*\"(phase-[0-9]+)\"[[:space:]]*:[[:space:]]*\{$ ]]; then
            # Print previous phase metrics if available
            if [ -n "$current_phase" ]; then
                local flag=""
                if [ -n "$current_duration" ] && [ "$current_duration" != "null" ] && [ "$current_duration" -gt 600 ] 2>/dev/null; then
                    flag=" $(echo -e "${YELLOW}← bottleneck${NC}")"
                fi
                if [ -n "$current_retries" ] && [ "$current_retries" != "0" ] && [ "$current_retries" != "null" ]; then
                    flag="$flag ($current_retries retries)"
                fi
                printf "  %-12s %6ss%s\n" "$current_phase" "${current_duration:-?}" "$flag"
            fi
            current_phase="${BASH_REMATCH[1]}"
            current_duration=""
            current_retries=""
            in_block=true
        elif $in_block; then
            if [[ "$line" =~ \"duration_seconds\"[[:space:]]*:[[:space:]]*([0-9]+|null) ]]; then
                current_duration="${BASH_REMATCH[1]}"
                if [ "$current_duration" != "null" ] && [ "$current_duration" -gt 0 ] 2>/dev/null; then
                    total_duration=$((total_duration + current_duration))
                fi
            elif [[ "$line" =~ \"retry_count\"[[:space:]]*:[[:space:]]*([0-9]+) ]]; then
                current_retries="${BASH_REMATCH[1]}"
                if [ -n "$current_retries" ] && [ "$current_retries" -gt 0 ] 2>/dev/null; then
                    total_retries=$((total_retries + current_retries))
                fi
            elif [[ "$line" =~ ^[[:space:]]*\},?$ ]]; then
                in_block=false
            fi
        fi
    done < "$RESULTS_FILE"

    # Print last phase
    if [ -n "$current_phase" ]; then
        local flag=""
        if [ -n "$current_duration" ] && [ "$current_duration" != "null" ] && [ "$current_duration" -gt 600 ] 2>/dev/null; then
            flag=" $(echo -e "${YELLOW}← bottleneck${NC}")"
        fi
        if [ -n "$current_retries" ] && [ "$current_retries" != "0" ] && [ "$current_retries" != "null" ]; then
            flag="$flag ($current_retries retries)"
        fi
        printf "  %-12s %6ss%s\n" "$current_phase" "${current_duration:-?}" "$flag"
    fi

    echo ""
    printf "  %-12s %6ss (%d total retries)\n" "TOTAL" "$total_duration" "$total_retries"
    echo ""
}

# ── Builder (adaptado para fases do analyze-and-improve) ───────────────────────

run_builder() {
    local feature="$1"
    local steer_msg="$2"

    # Extrai o número da fase de "phase-N"
    local phase_num="${feature#phase-}"

    log_section "BUILDER: $feature (Phase $phase_num)"

    # Lê o contexto da sessão de análise
    local source_url date slug output_dir
    # Extract fields from PROGRESS.md using bash regex (no grep -P dependency)
    source_url=""
    date=""
    slug=""
    while IFS= read -r line; do
        if [[ "$line" =~ \*\*source\*\*:[[:space:]]+(.+) ]]; then
            source_url="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ \*\*date\*\*:[[:space:]]+(.+) ]]; then
            date="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ \*\*source-slug\*\*:[[:space:]]+(.+) ]]; then
            slug="${BASH_REMATCH[1]}"
        fi
    done < "$PROGRESS_FILE"
    output_dir="docs/analysis/${date}-${slug}"

    local prompt="TASK: Run Phase $phase_num of the analyze-and-improve skill.

SOURCE DOCUMENT: $source_url
OUTPUT DIRECTORY: $output_dir
TARGET REPOSITORY: $(pwd)
SYSTEM OF RECORD: docs/system-of-record.md

IMPORTANT: Run ONLY Phase $phase_num. Do NOT run other phases.
The output of this phase goes to $output_dir.

Load the skill 'analyze-and-improve' and execute ONLY Phase $phase_num.
Use the skill's delegation pattern (task() with the correct category and prompt).

After the phase completes:
1. Verify the output files were created in $output_dir
2. Open each output file with Read (this is required evidence)
3. Update PROGRESS.md: move '$feature' to Done
4. Commit with message: 'analysis(${slug}): phase $phase_num'
5. Do NOT modify harness/test-results.json — the harness handles that."

    if [ -n "$steer_msg" ]; then
        prompt="OPERATOR STEERING: $steer_msg

$prompt"
    fi

    log_info "Prompt: $prompt"
    log_info "Executando $AGENT_CLI..."

    # Registra o momento de início da fase
    local started_at
    started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo "")
    if [ -n "$started_at" ]; then
        write_metric "$feature" "started_at" "$started_at"
        log_info "Métrica: started_at=$started_at"
    fi

    $AGENT_CLI run "$prompt"

    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Builder falhou com código $exit_code"
        return 1
    fi

    log_ok "Builder concluiu Phase $phase_num."
    return 0
}

# ── Guardian ───────────────────────────────────────────────────────────────────

run_guardian() {
    local feature="$1"

    log_section "GUARDIAN: $feature"

    if ! check_evidence; then
        log_error "Guardian: DENY"
        return 1
    fi

    log_ok "Guardian: ALLOW"
    return 0
}

# ── Evaluator (adaptado para fases do analyze-and-improve) ─────────────────────

run_evaluator() {
    local feature="$1"

    log_section "EVALUATOR: $feature"

    local review_prompt="You are the evaluator (skills/evaluator.md).

Review the analysis phase '$feature' from PROGRESS.md.

CONTEXT: This is a phase from the analyze-and-improve pipeline.
Each phase produces markdown + YAML outputs in docs/analysis/<date>-<slug>/.

TASKS:
1. Read PROGRESS.md to find the current output_dir
2. Read the output files for this phase (listed in harness/test-results.json evidence field)
3. Run 'git diff HEAD~1' to see what changed
4. Evaluate:
   a. Do the output files exist and have substantial content (not empty/templates)?
   b. Does the content match the phase objective (mental model, extraction, patterns, etc.)?
   c. Are Obsidian conventions followed (YAML frontmatter, wikilinks, tags)?
   d. Is the content substantive (not generic, not repetitive)?
5. Run 'bash scripts/check-obsidian-conventions.sh' to verify conventions
6. Return PASS or NEEDS_WORK with specific findings.

If NEEDS_WORK, list exactly what is missing or wrong.
If PASS, state it clearly as the first word of your response."

    log_info "Executando $AGENT_CLI --agent $EVALUATOR_AGENT..."

    local verdict
    verdict=$($AGENT_CLI run "$review_prompt" 2>&1) || true

    echo "$verdict"

    local verdict_line
    verdict_line=$(echo "$verdict" | head -1)

    if [ "$verdict_line" = "PASS" ]; then
        log_ok "Evaluator: PASS"

        # Calcula duração e registra completed_at
        local completed_at duration_sec
        completed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo "")

        # Extrai started_at do JSON para calcular duração
        local started_at_val
        started_at_val=$(while IFS= read -r line; do
            if [[ "$line" =~ \"started_at\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
                echo "${BASH_REMATCH[1]}"
                break
            fi
        done < <(sed -n "/\"$feature\"/,/^\s*\},/p" "$RESULTS_FILE"))

        if [ -n "$started_at_val" ] && [ -n "$completed_at" ]; then
            local start_epoch end_epoch
            start_epoch=$(date -d "$started_at_val" +%s 2>/dev/null || echo "0")
            end_epoch=$(date -d "$completed_at" +%s 2>/dev/null || echo "0")
            if [ "$start_epoch" != "0" ] && [ "$end_epoch" != "0" ]; then
                duration_sec=$((end_epoch - start_epoch))
                write_metric "$feature" "duration_seconds" "$duration_sec"
                write_metric "$feature" "completed_at" "$completed_at"
                log_info "Métrica: duration=${duration_sec}s, completed_at=$completed_at"
            fi
        fi

        # Mark as evaluated using bash builtins (no python3 dependency)
        local tmpfile="${RESULTS_FILE}.tmp"
        local in_target=false
        while IFS= read -r line; do
            if [[ "$line" =~ ^[[:space:]]*\"$feature\"[[:space:]]*:[[:space:]]*\{$ ]]; then
                in_target=true
                echo "$line"
            elif $in_target && [[ "$line" =~ \"evaluated_by\"[[:space:]]*:[[:space:]]*null ]]; then
                echo "${line/null/\"evaluator\"}"
            else
                if $in_target && [[ "$line" =~ ^[[:space:]]*\},?$ ]]; then
                    in_target=false
                fi
                echo "$line"
            fi
        done < "$RESULTS_FILE" > "$tmpfile" && command mv "$tmpfile" "$RESULTS_FILE" 2>/dev/null || true
        return 0
    else
        log_error "Evaluator: NEEDS_WORK"
        echo "$verdict" > NEXT_FINDINGS.md
        log_info "Achados salvos em NEXT_FINDINGS.md"
        return 1
    fi
}

# ── Commit de checkpoint ────────────────────────────────────────────────────────

commit_checkpoint() {
    if ! git diff --quiet || ! git diff --cached --quiet; then
        log_info "Commit de checkpoint..."
        git add -A
        git commit -m "checkpoint: harness analysis" || true
        log_ok "Commit realizado."
    fi
}

# ── Loop principal ─────────────────────────────────────────────────────────────

main_loop() {
    local mode="${1:-loop}"
    local target_feature="${2:-}"

    check_prerequisites || exit 1

    local iteration=0

    while [ "$iteration" -lt "$MAX_ITERATIONS" ]; do
        iteration=$((iteration + 1))
        echo ""
        log_info "═══════ Iteração $iteration / $MAX_ITERATIONS ═══════"

        # Kill switch
        check_kill_switch || break

        # Steering
        local steer_msg=""
        if check_steering; then
            steer_msg=$(cat "$STEER_FILE" 2>/dev/null || echo "")
        fi

        # Próxima fase
        local feature
        if [ -n "$target_feature" ]; then
            feature="$target_feature"
        else
            feature=$(get_next_feature)
        fi

        if [ -z "$feature" ]; then
            log_ok "Nenhuma fase pendente. Pipeline completo!"
            break
        fi

        # ── Ciclo build → guardian → evaluate ──
        log_info "Feature: $feature"

        # 1. Builder
        run_builder "$feature" "$steer_msg" || {
            log_error "Builder falhou. Registrando e continuando..."
            commit_checkpoint
            continue
        }

        # 2. Guardian (verifica evidência)
        run_guardian "$feature" || {
            log_error "Guardian rejeitou. Voltando ao builder..."
            echo "GUARDIAN DENIED: abra evidência antes de concluir a fase." > NEXT_FINDINGS.md
            commit_checkpoint
            continue
        }

        # 3. Evaluator
        if run_evaluator "$feature"; then
            log_ok "Fase '$feature' APROVADA pelo evaluator."
        else
            log_warn "Fase '$feature' REPROVADA. Achados em NEXT_FINDINGS.md."

            # Incrementa retry_count no test-results.json
            local current_retries
            current_retries=$(while IFS= read -r line; do
                if [[ "$line" =~ \"retry_count\"[[:space:]]*:[[:space:]]*([0-9]+) ]]; then
                    echo "${BASH_REMATCH[1]}"
                    break
                fi
            done < <(sed -n "/\"$feature\"/,/^\s*\},/p" "$RESULTS_FILE"))
            local new_retries=$(( ${current_retries:-0} + 1 ))
            write_metric "$feature" "retry_count" "$new_retries"
            log_info "Métrica: retry_count=$new_retries"

            commit_checkpoint
            continue
        fi

        # 4. Commit checkpoint
        commit_checkpoint

        # Se modo --once, para após uma fase
        if [ "$mode" = "once" ]; then
            log_info "Modo --once: encerrando após uma iteração."
            break
        fi
    done

    log_section "LOOP ENCERRADO"
    if has_pending_features; then
        log_warn "Ainda há fases pendentes. Execute novamente para continuar."
    else
        log_ok "Pipeline analyze-and-improve completo!"
    fi
    report_metrics
}

# ── Entrada ─────────────────────────────────────────────────────────────────────

case "${1:-loop}" in
    --once)
        main_loop "once" "${2:-}"
        ;;
    --feature)
        if [ -z "${2:-}" ]; then
            log_error "Uso: $0 --feature <phase-N>"
            exit 1
        fi
        main_loop "once" "$2"
        ;;
    --help|-h)
        echo "Uso: $0 [--once|--feature <phase-N>]"
        echo ""
        echo "  (sem flags)  Loop contínuo até todas as fases passarem"
        echo "  --once       Executa uma iteração e para"
        echo "  --feature    Executa apenas a fase especificada (ex: phase-0)"
        echo ""
        echo "Controles:"
        echo "  touch AGENT_STOP               Pausa o loop na próxima iteração"
        echo "  echo 'msg' > harness/templates/STEER.md  Redireciona o builder"
        echo ""
        echo "Variáveis de ambiente:"
        echo "  AGENT_CLI            CLI do agente (default: opencode)"
        echo "  MAX_ITERATIONS       Máximo de iterações (default: 20)"
        ;;
    *)
        main_loop "loop" "${2:-}"
        ;;
esac
