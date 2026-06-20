#!/usr/bin/env bash
set -euo pipefail

ROOT="${AGENTOS_BOOTSTRAP_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$ROOT"

if [[ "${AGENTOS_BOOTSTRAP_SKIP_PIP:-0}" != "1" ]]; then
  python3 -m venv .venv
  . .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install -e ".[dev]"
else
  mkdir -p .venv/bin
fi

if [[ ! -f .env ]]; then
  cp ops/env.example .env
  echo "Created .env from ops/env.example. Fill secrets before GitHub automation."
fi

write_service() {
  local target="$1"
  mkdir -p "$(dirname "$target")"
  cat > "$target" <<SERVICE
[Unit]
Description=Agent Racing OS daemon
After=network-online.target

[Service]
Type=simple
WorkingDirectory=$ROOT
EnvironmentFile=$ROOT/.env
ExecStart=$ROOT/.venv/bin/agentos daemon --project racing
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
SERVICE
}

mkdir -p data runs artifacts

scope="${AGENTOS_SYSTEMD_SCOPE:-auto}"
if [[ "$scope" == "auto" ]]; then
  if systemctl --user show-environment >/dev/null 2>&1; then
    scope="user"
  else
    scope="system"
  fi
fi

if [[ "$scope" == "user" ]]; then
  service_dir="${AGENTOS_USER_SYSTEMD_DIR:-$HOME/.config/systemd/user}"
  write_service "$service_dir/agent-racing-os.service"
  systemctl --user daemon-reload
  start_command="systemctl --user start agent-racing-os"
elif [[ "$scope" == "system" ]]; then
  service_dir="${AGENTOS_SYSTEMD_DIR:-/etc/systemd/system}"
  write_service "$service_dir/agent-racing-os.service"
  systemctl daemon-reload
  start_command="systemctl start agent-racing-os"
elif [[ "$scope" == "none" ]]; then
  start_command=".venv/bin/agentos daemon --project racing"
else
  echo "Unknown AGENTOS_SYSTEMD_SCOPE: $scope" >&2
  exit 2
fi

echo "Bootstrap complete."
echo "Start once: .venv/bin/agentos start project racing --once"
echo "Run daemon: $start_command"
