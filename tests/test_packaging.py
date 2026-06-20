from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_editable_install_exposes_agentos_cli(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    venv = tmp_path / "venv"

    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    python = venv / "bin" / "python"
    env = {**os.environ, "PYTHONPATH": ""}

    subprocess.run(
        [str(python), "-m", "pip", "install", "-e", str(repo)],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    result = subprocess.run(
        [str(python), "-m", "agentos.cli", "status"],
        check=True,
        env={**env, "AGENTOS_WORKDIR": str(repo)},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert "Project: racing" in result.stdout

