# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Persistent application preferences for GNU TrackGenerator.

Preferences are intentionally stored outside ``.gen`` project files. This
keeps workstation-specific settings independent from portable musical data.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any


DEFAULT_HISTORY_LIMIT = 100
MIN_HISTORY_LIMIT = 1
MAX_HISTORY_LIMIT = 10_000
CONFIG_DIRECTORY_NAME = "GNU TrackGenerator"
CONFIG_FILE_NAME = "settings.json"
CONFIG_ENVIRONMENT_VARIABLE = "GNU_TRACKGENERATOR_CONFIG_DIR"


class SettingsError(ValueError):
    """Raised when an application preference cannot be validated or saved."""


def validate_history_limit(value: Any) -> int:
    """Return a validated history limit.

    The upper bound prevents accidental values large enough to exhaust memory,
    while still allowing advanced users to retain substantially more than the
    default 100 states.
    """
    if isinstance(value, bool):
        raise SettingsError("La limite de l’historique doit être un nombre entier.")
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise SettingsError("La limite de l’historique doit être un nombre entier.") from exc
    if not MIN_HISTORY_LIMIT <= parsed <= MAX_HISTORY_LIMIT:
        raise SettingsError(
            f"La limite de l’historique doit être comprise entre "
            f"{MIN_HISTORY_LIMIT} et {MAX_HISTORY_LIMIT}."
        )
    return parsed


@dataclass(frozen=True)
class AppSettings:
    """Preferences that persist between application sessions."""

    history_limit: int = DEFAULT_HISTORY_LIMIT

    def validate(self) -> None:
        validate_history_limit(self.history_limit)

    def to_dict(self) -> dict[str, int]:
        return {"history_limit": validate_history_limit(self.history_limit)}

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AppSettings":
        return cls(
            history_limit=validate_history_limit(
                payload.get("history_limit", DEFAULT_HISTORY_LIMIT)
            )
        )


def default_settings_path() -> Path:
    """Return the platform-appropriate persistent settings path.

    ``GNU_TRACKGENERATOR_CONFIG_DIR`` can override the directory. This is
    useful for portable installations, automated tests and managed systems.
    """
    override = os.environ.get(CONFIG_ENVIRONMENT_VARIABLE)
    if override:
        return Path(override).expanduser() / CONFIG_FILE_NAME

    home = Path.home()
    if sys.platform.startswith("win"):
        base = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = home / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
    return base / CONFIG_DIRECTORY_NAME / CONFIG_FILE_NAME


def load_app_settings(path: str | Path | None = None) -> AppSettings:
    """Load preferences, falling back safely to defaults when unavailable.

    A missing, unreadable or malformed settings file must never prevent the
    application from starting. Invalid content is ignored and can be replaced
    the next time the user saves the Options dialog.
    """
    source = Path(path) if path is not None else default_settings_path()
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            return AppSettings()
        return AppSettings.from_dict(payload)
    except (OSError, UnicodeError, json.JSONDecodeError, SettingsError, TypeError):
        return AppSettings()


def save_app_settings(
    settings: AppSettings,
    path: str | Path | None = None,
) -> Path:
    """Persist preferences atomically and return the written path."""
    settings.validate()
    target = Path(path) if path is not None else default_settings_path()
    temporary = target.with_suffix(target.suffix + ".tmp")
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary.write_text(
            json.dumps(settings.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(target)
    except OSError as exc:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise SettingsError(
            f"Impossible d’enregistrer les préférences dans « {target} » : {exc}"
        ) from exc
    return target
