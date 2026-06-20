from __future__ import annotations

import subprocess
from pathlib import Path


def current_branch(repo: Path) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip() or "detached"


def has_remote(repo: Path, name: str = "origin") -> bool:
    result = subprocess.run(
        ["git", "remote", "get-url", name],
        cwd=repo,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

