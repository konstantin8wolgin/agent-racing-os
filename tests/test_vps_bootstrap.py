from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def test_bootstrap_can_install_system_service_without_user_bus(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    root = tmp_path / "agent-racing-os"
    shutil.copytree(repo / "ops", root / "ops")
    (root / "data").mkdir()
    (root / "runs").mkdir()
    (root / "artifacts").mkdir()

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    calls = tmp_path / "systemctl.calls"
    systemctl = fake_bin / "systemctl"
    systemctl.write_text(
        "#!/usr/bin/env bash\n"
        "echo \"$@\" >> \"$SYSTEMCTL_CALLS\"\n"
        "if [[ \"${1:-}\" == \"--user\" ]]; then\n"
        "  echo 'Failed to connect to bus: No medium found' >&2\n"
        "  exit 1\n"
        "fi\n"
        "exit 0\n",
        encoding="utf-8",
    )
    systemctl.chmod(0o755)

    systemd_dir = tmp_path / "systemd"
    env = {
        **os.environ,
        "PATH": f"{fake_bin}:{os.environ['PATH']}",
        "SYSTEMCTL_CALLS": str(calls),
        "AGENTOS_BOOTSTRAP_ROOT": str(root),
        "AGENTOS_BOOTSTRAP_SKIP_PIP": "1",
        "AGENTOS_SYSTEMD_SCOPE": "system",
        "AGENTOS_SYSTEMD_DIR": str(systemd_dir),
    }

    result = subprocess.run(
        [str(root / "ops" / "vps_bootstrap.sh")],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    service = systemd_dir / "agent-racing-os.service"
    assert service.exists()
    service_text = service.read_text(encoding="utf-8")
    assert f"WorkingDirectory={root}" in service_text
    assert f"ExecStart={root}/.venv/bin/agentos daemon --project racing" in service_text
    assert "Run daemon: systemctl start agent-racing-os" in result.stdout
    assert "daemon-reload" in calls.read_text(encoding="utf-8")

