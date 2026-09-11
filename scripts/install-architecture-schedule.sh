#!/usr/bin/env bash
# Install a frozen local copy; enabling the timer is an explicit separate step.
set -euo pipefail
architecture_source="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
architecture_install="$HOME/.local/share/architecture-monitor"
architecture_state="$HOME/.local/state/architecture-monitor"
architecture_units="$HOME/.config/systemd/user"
architecture_node="$(command -v node)"
architecture_opencode="$(command -v opencode)"
architecture_gh="$(command -v gh)"
umask 077
mkdir -p "$architecture_install/scripts/lib" "$architecture_install/tests/unit" \
  "$architecture_install/.opencode/agents" "$architecture_state" "$architecture_units"
for architecture_file in \
  scripts/architecture-scheduled.js scripts/architecture-monitor.js scripts/architecture-review.sh \
  scripts/lib/architecture-map.js scripts/lib/architecture-html.js scripts/lib/architecture-review.js \
  tests/unit/architecture-monitor.test.js tests/unit/architecture-review.test.js \
  .opencode/agents/repository-architecture-monitor.md; do
  install -m 600 "$architecture_source/$architecture_file" "$architecture_install/$architecture_file"
done
chmod 700 "$architecture_install/scripts/architecture-review.sh"
printf '{"private":true,"type":"module"}\n' > "$architecture_install/package.json"
{
  printf 'export ARCHITECTURE_NODE=%q\n' "$architecture_node"
  printf 'export ARCHITECTURE_OPENCODE=%q\n' "$architecture_opencode"
  printf 'export ARCHITECTURE_GH=%q\n' "$architecture_gh"
  printf 'export ARCHITECTURE_STATE=%q\n' "$architecture_state"
  printf 'export ARCHITECTURE_REPO=%q\n' 'pavani06/long-running-agents'
  printf 'export ARCHITECTURE_MODEL=%q\n' 'zai-coding-plan/glm-5.3-flash'
  printf 'export PATH=%q\n' "$(dirname "$architecture_node"):$(dirname "$architecture_opencode"):$(dirname "$architecture_gh"):/usr/local/bin:/usr/bin:/bin"
} > "$architecture_install/runtime.env"
install -m 600 "$architecture_source/scripts/systemd/architecture-review.service" "$architecture_units/architecture-review.service"
install -m 600 "$architecture_source/scripts/systemd/architecture-review.timer" "$architecture_units/architecture-review.timer"
printf 'Installed in %s\nEnable: systemctl --user daemon-reload && systemctl --user enable --now architecture-review.timer\nRun now: systemctl --user start architecture-review.service\n' "$architecture_install"
