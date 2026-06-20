from __future__ import annotations

from enum import StrEnum


class Mode(StrEnum):
    PLAN = "PLAN"
    BUILD = "BUILD"
    REVIEW = "REVIEW"
    DECIDE = "DECIDE"
    MERGE = "MERGE"
    REFLECT = "REFLECT"
    STUCK = "STUCK"
    FROZEN = "FROZEN"

