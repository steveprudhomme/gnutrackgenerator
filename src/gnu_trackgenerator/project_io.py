# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Project serialization helpers for GNU TrackGenerator."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ProjectData


def save_project(project: ProjectData, path: str | Path) -> Path:
    """Save a project as a .gen JSON file and return the written path."""
    project.validate()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(project.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return target


def load_project(path: str | Path) -> ProjectData:
    """Load and validate a .gen JSON project file."""
    source = Path(path)
    payload = json.loads(source.read_text(encoding="utf-8"))
    return ProjectData.from_dict(payload)
