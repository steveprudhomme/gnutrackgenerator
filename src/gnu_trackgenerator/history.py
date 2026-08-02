# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Generic bounded undo history for GUI state snapshots.

The history manager is deliberately independent from CustomTkinter. Snapshots
may be dictionaries, lists, dataclasses, or any other deep-copyable value.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Generic, TypeVar


SnapshotT = TypeVar("SnapshotT")


class UndoHistory(Generic[SnapshotT]):
    """Store a bounded sequence of previous application states."""

    def __init__(self, max_entries: int = 100) -> None:
        if max_entries < 1:
            raise ValueError("max_entries doit être supérieur ou égal à 1.")
        self.max_entries = max_entries
        self._undo_stack: list[SnapshotT] = []
        self._current: SnapshotT | None = None

    @property
    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    @property
    def depth(self) -> int:
        return len(self._undo_stack)

    def reset(self, snapshot: SnapshotT) -> None:
        """Start a new history with ``snapshot`` as the current state."""
        self._undo_stack.clear()
        self._current = deepcopy(snapshot)

    def record(self, snapshot: SnapshotT) -> bool:
        """Record a new current state and retain the previous one for undo.

        Returns ``True`` when the state changed and was recorded. Identical
        consecutive snapshots are ignored.
        """
        copied = deepcopy(snapshot)
        if self._current is None:
            self._current = copied
            return False
        if copied == self._current:
            return False
        self._undo_stack.append(deepcopy(self._current))
        if len(self._undo_stack) > self.max_entries:
            del self._undo_stack[: len(self._undo_stack) - self.max_entries]
        self._current = copied
        return True

    def undo(self) -> SnapshotT | None:
        """Return and activate the preceding snapshot, if one exists."""
        if not self._undo_stack:
            return None
        previous = self._undo_stack.pop()
        self._current = deepcopy(previous)
        return deepcopy(previous)
