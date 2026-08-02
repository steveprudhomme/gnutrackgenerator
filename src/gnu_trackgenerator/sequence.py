# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""Helpers for duplicating and reordering musical-sequence rows.

These functions are independent from CustomTkinter so their behavior can be
tested without opening a graphical window.
"""

from __future__ import annotations

from copy import deepcopy
from typing import MutableSequence, TypeVar


ItemT = TypeVar("ItemT")


def duplicate_row_state(state: dict) -> dict:
    """Return a deep, independent copy of a raw row-state snapshot."""
    return deepcopy(state)


def move_item(items: MutableSequence[ItemT], source_index: int, target_index: int) -> None:
    """Move one item inside ``items`` while preserving all other item order.

    ``target_index`` identifies the final position after the move.
    """
    length = len(items)
    if length == 0:
        raise IndexError("Impossible de déplacer un élément dans une séquence vide.")
    if not 0 <= source_index < length:
        raise IndexError("Indice source hors limites.")
    if not 0 <= target_index < length:
        raise IndexError("Indice cible hors limites.")
    if source_index == target_index:
        return
    item = items.pop(source_index)
    items.insert(target_index, item)
