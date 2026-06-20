#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

if [[ ! -f .env ]]; then
  cp ops/env.example .env
  echo "Created .env from ops/env.example. Fill secrets before GitHub automation."
fi

mkdir -p data runs artifacts "$HOME/.config/systemd/user"
cp ops/systemd/agent-racing-os.service "$HOME/.config/systemd/user/agent-racing-os.service"
systemctl --user daemon-reload || true

echo "Bootstrap complete."
echo "Start once: .venv/bin/agentos start project racing --once"
echo "Run daemon: systemctl --user start agent-racing-os"

