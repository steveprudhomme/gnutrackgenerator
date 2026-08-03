# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""CustomTkinter GUI for GNU TrackGenerator."""

from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk
except ImportError as exc:  # Friendly failure when launched without dependency.
    raise SystemExit(
        "CustomTkinter n'est pas installé. Exécutez: pip install -r requirements.txt"
    ) from exc

from .arpeggiator import (
    ARP_PATTERN_LABELS,
    ARP_PATTERN_LABEL_TO_VALUE,
    ARP_RHYTHM_LABELS,
    ARP_RHYTHM_LABEL_TO_VALUE,
    ArpeggiatorError,
    ArpeggiatorSettings,
)
from .chords import ChordParseError, SUPPORTED_CHORD_EXAMPLES, chord_symbol_to_lilypond_chord
from .generator import GenerationError, generate_project
from .history import UndoHistory
from .history_snapshot import (
    build_project_history_snapshot,
    validate_project_history_snapshot,
    validate_row_history_state,
)
from .sequence import duplicate_row_state, move_item
from .models import (
    APP_NAME,
    APP_VERSION,
    CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
    CHORD_INSTRUMENT_PIANO,
    CHORD_INSTRUMENT_STRINGS,
    CHORD_MODE_GRID,
    CHORD_MODE_LINE,
    CHORD_MODE_MEASURE,
    CHORD_MODE_NONE,
    ProjectData,
    Segment,
    ValidationError,
)
from .project_io import load_project, save_project
from .rhythm import (
    RHYTHM_LABEL_TO_UNIT,
    RHYTHM_QUARTER,
    RHYTHM_UNIT_DURATIONS,
    RHYTHM_UNIT_LABELS,
    chord_grid_durations,
    lilypond_duration,
    measure_duration,
)


INSTRUMENT_LABEL_TO_VALUE = {
    "Piano": CHORD_INSTRUMENT_PIANO,
    "Strings": CHORD_INSTRUMENT_STRINGS,
    "Guitare sèche": CHORD_INSTRUMENT_ACOUSTIC_GUITAR,
}

INSTRUMENT_VALUE_TO_LABEL = {value: label for label, value in INSTRUMENT_LABEL_TO_VALUE.items()}


def _arpeggiator_button_text(settings: ArpeggiatorSettings) -> str:
    """Return a compact visual state for a chord-field arpeggiator button."""
    return "A✓" if settings.enabled else "A"


class ArpeggiatorDialog(ctk.CTkToplevel):
    """Modal editor for one chord field's arpeggiator settings."""

    def __init__(self, master, settings: ArpeggiatorSettings, on_save) -> None:
        super().__init__(master)
        self.title("Réglages de l’arpégiateur")
        self.geometry("520x500")
        self.resizable(False, False)
        self.transient(master.winfo_toplevel())
        self.grab_set()
        self.on_save = on_save

        self.enabled_var = ctk.BooleanVar(value=settings.enabled)
        self.pattern_var = ctk.StringVar(
            value=ARP_PATTERN_LABELS.get(settings.pattern, next(iter(ARP_PATTERN_LABELS.values())))
        )
        self.octaves_var = ctk.StringVar(value=str(settings.octaves))
        self.rhythm_var = ctk.StringVar(
            value=ARP_RHYTHM_LABELS.get(settings.rhythm, next(iter(ARP_RHYTHM_LABELS.values())))
        )
        self.dotted_var = ctk.BooleanVar(value=settings.dotted)
        self.tuplet_var = ctk.StringVar(value=str(settings.normalized_tuplet_count))

        self.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            self,
            text="Arpégiateur de l’accord",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 12), sticky="w")

        ctk.CTkSwitch(
            self,
            text="Activer l’arpégiateur (désactivé = accord joué normalement)",
            variable=self.enabled_var,
        ).grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")

        ctk.CTkLabel(self, text="Mouvement").grid(row=2, column=0, padx=20, pady=8, sticky="w")
        ctk.CTkOptionMenu(
            self, variable=self.pattern_var, values=list(ARP_PATTERN_LABEL_TO_VALUE.keys())
        ).grid(row=2, column=1, padx=20, pady=8, sticky="ew")

        ctk.CTkLabel(self, text="Nombre d’octaves").grid(
            row=3, column=0, padx=20, pady=8, sticky="w"
        )
        ctk.CTkEntry(self, textvariable=self.octaves_var, width=100).grid(
            row=3, column=1, padx=20, pady=8, sticky="w"
        )

        ctk.CTkLabel(self, text="Valeur rythmique").grid(
            row=4, column=0, padx=20, pady=8, sticky="w"
        )
        ctk.CTkOptionMenu(
            self, variable=self.rhythm_var, values=list(ARP_RHYTHM_LABEL_TO_VALUE.keys())
        ).grid(row=4, column=1, padx=20, pady=8, sticky="ew")

        ctk.CTkSwitch(
            self, text="Valeur pointée", variable=self.dotted_var
        ).grid(row=5, column=0, columnspan=2, padx=20, pady=8, sticky="w")

        ctk.CTkLabel(self, text="N-olet").grid(
            row=6, column=0, padx=20, pady=8, sticky="w"
        )
        ctk.CTkEntry(
            self,
            textvariable=self.tuplet_var,
            width=100,
            placeholder_text="0, 3, 4, 5…",
        ).grid(row=6, column=1, padx=20, pady=8, sticky="w")

        ctk.CTkLabel(
            self,
            text=(
                "N-olet : 0 désactive le N-olet; la valeur choisie est alors la durée de chaque note. "
                "Avec N ≥ 3, la valeur rythmique devient la durée totale du groupe et exactement N notes "
                "sont réparties dans cette durée. Exemple : Ronde + 7 = sept notes dans une ronde "
                "(LilyPond : 7/4). Le motif aléatoire reste reproductible."
            ),
            wraplength=470,
            justify="left",
            font=ctk.CTkFont(size=12),
        ).grid(row=7, column=0, columnspan=2, padx=20, pady=(8, 18), sticky="w")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=8, column=0, columnspan=2, padx=20, pady=(4, 20), sticky="ew")
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(actions, text="Annuler", command=self.destroy).grid(
            row=0, column=0, padx=(0, 6), sticky="ew"
        )
        ctk.CTkButton(actions, text="Enregistrer", command=self._save).grid(
            row=0, column=1, padx=(6, 0), sticky="ew"
        )

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after(50, self.focus_force)

    def _save(self) -> None:
        try:
            settings = ArpeggiatorSettings(
                enabled=bool(self.enabled_var.get()),
                pattern=ARP_PATTERN_LABEL_TO_VALUE[self.pattern_var.get()],
                octaves=int(self.octaves_var.get()),
                rhythm=ARP_RHYTHM_LABEL_TO_VALUE[self.rhythm_var.get()],
                dotted=bool(self.dotted_var.get()),
                tuplet_count=int(self.tuplet_var.get() or "0"),
            )
            settings.validate()
        except (KeyError, ValueError, ArpeggiatorError) as exc:
            messagebox.showerror("Arpégiateur", str(exc), parent=self)
            return
        self.on_save(settings)
        self.destroy()


class SegmentRow(ctk.CTkFrame):
    """One editable musical segment row in the scrollable list."""

    def __init__(
        self,
        master: ctk.CTkFrame,
        on_add_after,
        on_remove,
        on_duplicate=None,
        on_drag_start=None,
        on_drag_motion=None,
        on_drag_end=None,
        on_change=None,
        defaults: Segment | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self.on_add_after = on_add_after
        self.on_remove = on_remove
        self.on_duplicate = on_duplicate or (lambda _row: None)
        self.on_drag_start = on_drag_start or (lambda _row, _event: None)
        self.on_drag_motion = on_drag_motion or (lambda _row, _event: None)
        self.on_drag_end = on_drag_end or (lambda _row, _event: None)
        self.on_change = on_change or (lambda: None)
        self.menu_visible = False
        self.chord_mode = CHORD_MODE_NONE
        self.line_chord_visible = False
        self.measure_chord_visible = False
        self.grid_chord_visible = False
        self.measure_chord_vars: list[ctk.StringVar] = []
        self.grid_chord_vars: list[ctk.StringVar] = []
        self.line_arpeggiator = ArpeggiatorSettings()
        self.measure_arpeggiators: list[ArpeggiatorSettings] = []
        self.grid_arpeggiators: list[ArpeggiatorSettings] = []

        segment = defaults or Segment(bpm=120, numerator=4, denominator=4, measures=4)
        self.bpm_var = ctk.StringVar(value=str(segment.bpm))
        self.numerator_var = ctk.StringVar(value=str(segment.numerator))
        self.denominator_var = ctk.StringVar(value=str(segment.denominator))
        self.measures_var = ctk.StringVar(value=str(segment.measures))
        self.chord_symbol_var = ctk.StringVar(value=segment.chord_symbol or "")
        self.chord_instrument_var = ctk.StringVar(
            value=INSTRUMENT_VALUE_TO_LABEL.get(segment.chord_instrument, "Piano")
        )
        self.chord_grid_unit_var = ctk.StringVar(
            value=RHYTHM_UNIT_LABELS.get(segment.chord_grid_unit, RHYTHM_UNIT_LABELS[RHYTHM_QUARTER])
        )
        self.grid_status_var = ctk.StringVar(value="")
        self.line_arpeggiator = segment.chord_arpeggiator
        self.measure_arpeggiators = list(segment.effective_measure_arpeggiators)
        self.grid_arpeggiators = list(segment.effective_grid_arpeggiators) if segment.effective_chord_mode == CHORD_MODE_GRID else []

        mode = segment.effective_chord_mode
        if mode == CHORD_MODE_GRID:
            self.chord_mode = CHORD_MODE_GRID
            self.grid_chord_vars = [ctk.StringVar(value=value or "") for value in segment.grid_chords]
        elif mode == CHORD_MODE_MEASURE:
            self.chord_mode = CHORD_MODE_MEASURE
            self.measure_chord_vars = [
                ctk.StringVar(value=symbol or "") for symbol in segment.measure_chords
            ]
        elif mode == CHORD_MODE_LINE:
            self.chord_mode = CHORD_MODE_LINE

        self._build_widgets()
        self.measures_var.trace_add("write", self._on_timing_changed)
        self.numerator_var.trace_add("write", self._on_timing_changed)
        self.denominator_var.trace_add("write", self._on_timing_changed)
        for variable in (
            self.bpm_var,
            self.numerator_var,
            self.denominator_var,
            self.measures_var,
            self.chord_symbol_var,
            self.chord_instrument_var,
            self.chord_grid_unit_var,
        ):
            self._register_history_var(variable)
        for variable in self.measure_chord_vars + self.grid_chord_vars:
            self._register_history_var(variable)

        if mode == CHORD_MODE_GRID:
            self.show_grid_chord_area()
        elif mode == CHORD_MODE_MEASURE:
            self.show_measure_chord_area()
        elif mode == CHORD_MODE_LINE:
            self.show_line_chord_area()

    def _notify_change(self) -> None:
        """Notify the application that the project state changed."""
        self.on_change()

    def _register_history_var(self, variable: ctk.Variable) -> None:
        """Attach a history notification to a Tk variable."""
        variable.trace_add("write", lambda *_args: self._notify_change())

    def to_history_state(self) -> dict:
        """Return an unvalidated, JSON-like snapshot of the editable row state."""
        return validate_row_history_state(
            {
                "bpm": self.bpm_var.get(),
                "numerator": self.numerator_var.get(),
                "denominator": self.denominator_var.get(),
                "measures": self.measures_var.get(),
                "chord_mode": self.chord_mode,
                "chord_symbol": self.chord_symbol_var.get(),
                "chord_instrument_label": self.chord_instrument_var.get(),
                "chord_grid_unit_label": self.chord_grid_unit_var.get(),
                "measure_chords": [variable.get() for variable in self.measure_chord_vars],
                "grid_chords": [variable.get() for variable in self.grid_chord_vars],
                "line_arpeggiator": self.line_arpeggiator.to_dict(),
                "measure_arpeggiators": [settings.to_dict() for settings in self.measure_arpeggiators],
                "grid_arpeggiators": [settings.to_dict() for settings in self.grid_arpeggiators],
            }
        )

    def apply_history_state(self, state: dict) -> None:
        """Restore a snapshot created by :meth:`to_history_state`."""
        self.bpm_var.set(str(state.get("bpm", "120")))
        self.numerator_var.set(str(state.get("numerator", "4")))
        self.denominator_var.set(str(state.get("denominator", "4")))
        self.measures_var.set(str(state.get("measures", "4")))
        self.chord_symbol_var.set(str(state.get("chord_symbol", "")))
        self.chord_instrument_var.set(
            str(state.get("chord_instrument_label", "Piano"))
        )
        self.chord_grid_unit_var.set(
            str(state.get("chord_grid_unit_label", RHYTHM_UNIT_LABELS[RHYTHM_QUARTER]))
        )

        self.measure_chord_vars = []
        for value in state.get("measure_chords", []):
            variable = ctk.StringVar(value=str(value or ""))
            self._register_history_var(variable)
            self.measure_chord_vars.append(variable)

        self.grid_chord_vars = []
        for value in state.get("grid_chords", []):
            variable = ctk.StringVar(value=str(value or ""))
            self._register_history_var(variable)
            self.grid_chord_vars.append(variable)

        self.line_arpeggiator = ArpeggiatorSettings.from_dict(
            state.get("line_arpeggiator")
        )
        self.measure_arpeggiators = [
            ArpeggiatorSettings.from_dict(payload)
            for payload in state.get("measure_arpeggiators", [])
        ]
        self.grid_arpeggiators = [
            ArpeggiatorSettings.from_dict(payload)
            for payload in state.get("grid_arpeggiators", [])
        ]
        self.line_arpeggiator_button.configure(
            text=_arpeggiator_button_text(self.line_arpeggiator)
        )

        self.chord_mode = str(state.get("chord_mode", CHORD_MODE_NONE))
        self._hide_all_chord_frames()
        if self.chord_mode == CHORD_MODE_LINE:
            self.show_line_chord_area()
        elif self.chord_mode == CHORD_MODE_MEASURE:
            self.show_measure_chord_area()
        elif self.chord_mode == CHORD_MODE_GRID:
            self.show_grid_chord_area()
        else:
            self.chord_mode = CHORD_MODE_NONE

    def _build_widgets(self) -> None:
        """Create and place row widgets."""
        for col in range(13):
            self.grid_columnconfigure(col, weight=1 if col in {1, 3, 5, 7} else 0)

        ctk.CTkLabel(self, text="BPM").grid(row=0, column=0, padx=(8, 4), pady=8)
        ctk.CTkEntry(self, textvariable=self.bpm_var, width=70).grid(
            row=0, column=1, padx=4, pady=8
        )
        ctk.CTkLabel(self, text="Signature").grid(
            row=0, column=2, padx=(12, 4), pady=8
        )
        ctk.CTkEntry(self, textvariable=self.numerator_var, width=55).grid(
            row=0, column=3, padx=(4, 2), pady=8
        )
        ctk.CTkLabel(self, text="/").grid(row=0, column=4, padx=0, pady=8)
        ctk.CTkEntry(self, textvariable=self.denominator_var, width=55).grid(
            row=0, column=5, padx=(2, 4), pady=8
        )
        ctk.CTkLabel(self, text="Mesures").grid(
            row=0, column=6, padx=(12, 4), pady=8
        )
        ctk.CTkEntry(self, textvariable=self.measures_var, width=70).grid(
            row=0, column=7, padx=4, pady=8
        )
        ctk.CTkButton(self, text="+", width=34, command=lambda: self.on_add_after(self)).grid(
            row=0, column=8, padx=(8, 2), pady=8
        )
        ctk.CTkButton(self, text="−", width=34, command=lambda: self.on_remove(self)).grid(
            row=0, column=9, padx=(2, 2), pady=8
        )
        ctk.CTkButton(
            self,
            text="D",
            width=34,
            command=lambda: self.on_duplicate(self),
        ).grid(row=0, column=10, padx=(2, 2), pady=8)
        ctk.CTkButton(self, text="☰", width=38, command=self.toggle_menu).grid(
            row=0, column=11, padx=(2, 2), pady=8
        )
        self.drag_handle = ctk.CTkLabel(
            self,
            text="⠿",
            width=34,
            height=28,
            corner_radius=6,
            fg_color=("gray82", "gray28"),
            font=ctk.CTkFont(size=19, weight="bold"),
        )
        self.drag_handle.grid(row=0, column=12, padx=(2, 8), pady=8)
        self.drag_handle.bind(
            "<ButtonPress-1>", lambda event: self.on_drag_start(self, event)
        )
        self.drag_handle.bind(
            "<B1-Motion>", lambda event: self.on_drag_motion(self, event)
        )
        self.drag_handle.bind(
            "<ButtonRelease-1>", lambda event: self.on_drag_end(self, event)
        )

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            self.menu_frame,
            text="Menu de ligne",
            font=ctk.CTkFont(weight="bold"),
        ).grid(row=0, column=0, padx=(10, 8), pady=8, sticky="w")
        ctk.CTkButton(
            self.menu_frame,
            text="Accord → Accord au début de chaque ligne",
            command=self.show_line_chord_area,
        ).grid(row=0, column=1, padx=8, pady=(8, 4), sticky="ew")
        ctk.CTkButton(
            self.menu_frame,
            text="Accord → Accord au début de chaque mesure",
            command=self.show_measure_chord_area,
        ).grid(row=1, column=1, padx=8, pady=4, sticky="ew")
        ctk.CTkButton(
            self.menu_frame,
            text="Accord → Accords selon une subdivision rythmique",
            command=self.show_grid_chord_area,
        ).grid(row=2, column=1, padx=8, pady=4, sticky="ew")
        ctk.CTkButton(
            self.menu_frame,
            text="Accord → Désactiver les accords",
            command=self.disable_chords,
        ).grid(row=3, column=1, padx=8, pady=4, sticky="ew")
        ctk.CTkButton(self.menu_frame, text="Masquer", width=80, command=self.hide_menu).grid(
            row=0, column=2, rowspan=4, padx=(8, 10), pady=8
        )

        self._build_line_chord_frame()
        self._build_measure_chord_frame()
        self._build_grid_chord_frame()

    def _build_line_chord_frame(self) -> None:
        self.line_chord_frame = ctk.CTkFrame(self)
        self.line_chord_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.line_chord_frame, text="Accord pour toute la ligne").grid(
            row=0, column=0, padx=(10, 6), pady=(8, 4), sticky="w"
        )
        ctk.CTkEntry(
            self.line_chord_frame,
            textvariable=self.chord_symbol_var,
            placeholder_text="Ex.: C, Cm7, Dadd11, G#m7(b13)",
        ).grid(row=0, column=1, padx=6, pady=(8, 4), sticky="ew")
        self.line_arpeggiator_button = ctk.CTkButton(
            self.line_chord_frame,
            text=_arpeggiator_button_text(self.line_arpeggiator),
            width=38,
            command=self._edit_line_arpeggiator,
        )
        self.line_arpeggiator_button.grid(row=1, column=1, padx=6, pady=(0, 4), sticky="w")
        ctk.CTkLabel(self.line_chord_frame, text="Instrument").grid(
            row=0, column=2, padx=(10, 6), pady=(8, 4)
        )
        ctk.CTkOptionMenu(
            self.line_chord_frame,
            variable=self.chord_instrument_var,
            values=list(INSTRUMENT_LABEL_TO_VALUE.keys()),
            width=150,
        ).grid(row=0, column=3, padx=6, pady=(8, 4))
        ctk.CTkButton(
            self.line_chord_frame, text="⌃", width=38, command=self.hide_line_chord_area
        ).grid(row=0, column=4, padx=(6, 10), pady=(8, 4))
        examples = ", ".join(SUPPORTED_CHORD_EXAMPLES[:12]) + ", ..."
        ctk.CTkLabel(
            self.line_chord_frame,
            text=f"Saisir un symbole d’accord A–G. Exemples : {examples}",
            font=ctk.CTkFont(size=11),
        ).grid(row=2, column=0, columnspan=5, padx=10, pady=(0, 8), sticky="w")

    def _build_measure_chord_frame(self) -> None:
        self.measure_chord_frame = ctk.CTkFrame(self)
        self.measure_chord_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            self.measure_chord_frame,
            text="Accords au début de chaque mesure",
            font=ctk.CTkFont(weight="bold"),
        ).grid(row=0, column=0, padx=(10, 8), pady=(8, 4), sticky="w")
        ctk.CTkLabel(self.measure_chord_frame, text="Instrument").grid(
            row=0, column=1, padx=(10, 6), pady=(8, 4), sticky="e"
        )
        ctk.CTkOptionMenu(
            self.measure_chord_frame,
            variable=self.chord_instrument_var,
            values=list(INSTRUMENT_LABEL_TO_VALUE.keys()),
            width=150,
        ).grid(row=0, column=2, padx=6, pady=(8, 4))
        ctk.CTkButton(
            self.measure_chord_frame,
            text="⌃",
            width=38,
            command=self.hide_measure_chord_area,
        ).grid(row=0, column=3, padx=(6, 10), pady=(8, 4))
        self.measure_chord_entries_frame = ctk.CTkFrame(
            self.measure_chord_frame, fg_color="transparent"
        )
        self.measure_chord_entries_frame.grid(
            row=1, column=0, columnspan=4, padx=8, pady=(4, 4), sticky="ew"
        )
        for column in range(4):
            self.measure_chord_entries_frame.grid_columnconfigure(column, weight=1)
        ctk.CTkLabel(
            self.measure_chord_frame,
            text="Une case vide produit une mesure sans accord. Chaque accord dure une mesure complète.",
            font=ctk.CTkFont(size=11),
        ).grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="w")

    def _build_grid_chord_frame(self) -> None:
        self.grid_chord_frame = ctk.CTkFrame(self)
        self.grid_chord_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            self.grid_chord_frame,
            text="Grille rythmique d’accords",
            font=ctk.CTkFont(weight="bold"),
        ).grid(row=0, column=0, padx=(10, 8), pady=(8, 4), sticky="w")
        ctk.CTkLabel(self.grid_chord_frame, text="Subdivision").grid(
            row=0, column=1, padx=(8, 4), pady=(8, 4), sticky="e"
        )
        ctk.CTkOptionMenu(
            self.grid_chord_frame,
            variable=self.chord_grid_unit_var,
            values=list(RHYTHM_LABEL_TO_UNIT.keys()),
            command=lambda _value: self._on_grid_unit_changed(),
            width=180,
        ).grid(row=0, column=2, padx=4, pady=(8, 4))
        ctk.CTkLabel(self.grid_chord_frame, text="Instrument").grid(
            row=0, column=3, padx=(8, 4), pady=(8, 4)
        )
        ctk.CTkOptionMenu(
            self.grid_chord_frame,
            variable=self.chord_instrument_var,
            values=list(INSTRUMENT_LABEL_TO_VALUE.keys()),
            width=150,
        ).grid(row=0, column=4, padx=4, pady=(8, 4))
        ctk.CTkButton(
            self.grid_chord_frame,
            text="⌃",
            width=38,
            command=self.hide_grid_chord_area,
        ).grid(row=0, column=5, padx=(6, 10), pady=(8, 4))

        self.grid_chord_entries_frame = ctk.CTkFrame(
            self.grid_chord_frame, fg_color="transparent"
        )
        self.grid_chord_entries_frame.grid(
            row=1, column=0, columnspan=6, padx=8, pady=(4, 4), sticky="ew"
        )
        for column in range(6):
            self.grid_chord_entries_frame.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            self.grid_chord_frame,
            textvariable=self.grid_status_var,
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=2, column=0, columnspan=6, padx=10, pady=(2, 0), sticky="w")
        ctk.CTkLabel(
            self.grid_chord_frame,
            text=(
                "Saisir un accord pour le jouer, une virgule (,) pour prolonger l’accord précédent "
                "sans nouvelle attaque (et avec le même arpégiateur), ou laisser vide pour produire un silence. "
                "Le bouton A sous chaque accord ouvre ses réglages d’arpégiateur."
            ),
            font=ctk.CTkFont(size=11),
            wraplength=920,
            justify="left",
        ).grid(row=3, column=0, columnspan=6, padx=10, pady=(0, 8), sticky="w")


    def _edit_line_arpeggiator(self) -> None:
        def save(settings: ArpeggiatorSettings) -> None:
            self.line_arpeggiator = settings
            self.line_arpeggiator_button.configure(text=_arpeggiator_button_text(settings))
            self._notify_change()

        ArpeggiatorDialog(self, self.line_arpeggiator, save)

    def _edit_measure_arpeggiator(self, index: int, button) -> None:
        self._ensure_measure_arpeggiators(index + 1)

        def save(settings: ArpeggiatorSettings) -> None:
            self.measure_arpeggiators[index] = settings
            button.configure(text=_arpeggiator_button_text(settings))
            self._notify_change()

        ArpeggiatorDialog(self, self.measure_arpeggiators[index], save)

    def _edit_grid_arpeggiator(self, index: int, button) -> None:
        self._ensure_grid_arpeggiators(index + 1)

        def save(settings: ArpeggiatorSettings) -> None:
            self.grid_arpeggiators[index] = settings
            button.configure(text=_arpeggiator_button_text(settings))
            self._notify_change()

        ArpeggiatorDialog(self, self.grid_arpeggiators[index], save)

    def toggle_menu(self) -> None:
        if self.menu_visible:
            self.hide_menu()
        else:
            self.menu_frame.grid(row=1, column=0, columnspan=12, padx=8, pady=(0, 6), sticky="ew")
            self.menu_visible = True

    def hide_menu(self) -> None:
        self.menu_frame.grid_forget()
        self.menu_visible = False

    def _hide_all_chord_frames(self) -> None:
        self.line_chord_frame.grid_forget()
        self.measure_chord_frame.grid_forget()
        self.grid_chord_frame.grid_forget()
        self.line_chord_visible = False
        self.measure_chord_visible = False
        self.grid_chord_visible = False

    def show_line_chord_area(self) -> None:
        changed = self.chord_mode != CHORD_MODE_LINE
        self.chord_mode = CHORD_MODE_LINE
        self._hide_all_chord_frames()
        self.line_chord_frame.grid(row=2, column=0, columnspan=12, padx=8, pady=(0, 8), sticky="ew")
        self.line_chord_visible = True
        self.hide_menu()
        if changed:
            self._notify_change()

    def hide_line_chord_area(self) -> None:
        self.line_chord_frame.grid_forget()
        self.line_chord_visible = False

    def show_measure_chord_area(self) -> None:
        changed = self.chord_mode != CHORD_MODE_MEASURE
        self.chord_mode = CHORD_MODE_MEASURE
        self._hide_all_chord_frames()
        self._rebuild_measure_chord_inputs()
        self.measure_chord_frame.grid(row=2, column=0, columnspan=12, padx=8, pady=(0, 8), sticky="ew")
        self.measure_chord_visible = True
        self.hide_menu()
        if changed:
            self._notify_change()

    def hide_measure_chord_area(self) -> None:
        self.measure_chord_frame.grid_forget()
        self.measure_chord_visible = False

    def show_grid_chord_area(self) -> None:
        changed = self.chord_mode != CHORD_MODE_GRID
        self.chord_mode = CHORD_MODE_GRID
        self._hide_all_chord_frames()
        self._rebuild_grid_chord_inputs()
        self.grid_chord_frame.grid(row=2, column=0, columnspan=12, padx=8, pady=(0, 8), sticky="ew")
        self.grid_chord_visible = True
        self.hide_menu()
        if changed:
            self._notify_change()

    def hide_grid_chord_area(self) -> None:
        self.grid_chord_frame.grid_forget()
        self.grid_chord_visible = False

    def disable_chords(self) -> None:
        changed = self.chord_mode != CHORD_MODE_NONE
        self.chord_mode = CHORD_MODE_NONE
        self._hide_all_chord_frames()
        self.hide_menu()
        if changed:
            self._notify_change()

    def _measure_count(self) -> int | None:
        try:
            count = int(self.measures_var.get())
        except ValueError:
            return None
        return count if count > 0 else None

    def _ensure_measure_chord_vars(self, count: int) -> None:
        while len(self.measure_chord_vars) < count:
            variable = ctk.StringVar(value="")
            self._register_history_var(variable)
            self.measure_chord_vars.append(variable)

    def _ensure_measure_arpeggiators(self, count: int) -> None:
        while len(self.measure_arpeggiators) < count:
            self.measure_arpeggiators.append(ArpeggiatorSettings())

    def _rebuild_measure_chord_inputs(self) -> None:
        count = self._measure_count()
        if count is None:
            return
        self._ensure_measure_chord_vars(count)
        self._ensure_measure_arpeggiators(count)
        for widget in self.measure_chord_entries_frame.winfo_children():
            widget.destroy()
        for index in range(count):
            cell = ctk.CTkFrame(self.measure_chord_entries_frame)
            row, column = divmod(index, 4)
            cell.grid(row=row, column=column, padx=4, pady=4, sticky="ew")
            cell.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(cell, text=f"Mesure {index + 1}", font=ctk.CTkFont(size=11)).grid(
                row=0, column=0, padx=6, pady=(5, 1), sticky="w"
            )
            ctk.CTkEntry(
                cell,
                textvariable=self.measure_chord_vars[index],
                placeholder_text="Ex.: C, Am7, F#",
            ).grid(row=1, column=0, padx=6, pady=(1, 6), sticky="ew")
            arp_button = ctk.CTkButton(
                cell,
                text=_arpeggiator_button_text(self.measure_arpeggiators[index]),
                width=34,
            )
            arp_button.configure(
                command=lambda idx=index, btn=arp_button: self._edit_measure_arpeggiator(idx, btn)
            )
            arp_button.grid(row=2, column=0, padx=6, pady=(0, 6), sticky="w")

    def _grid_values(self):
        try:
            numerator = int(self.numerator_var.get())
            denominator = int(self.denominator_var.get())
            measures = int(self.measures_var.get())
        except ValueError:
            return None
        unit = RHYTHM_LABEL_TO_UNIT.get(self.chord_grid_unit_var.get(), RHYTHM_QUARTER)
        try:
            durations = chord_grid_durations(numerator, denominator, measures, unit)
        except ValueError:
            return None
        return numerator, denominator, measures, unit, durations

    def _ensure_grid_chord_vars(self, count: int) -> None:
        while len(self.grid_chord_vars) < count:
            variable = ctk.StringVar(value="")
            self._register_history_var(variable)
            self.grid_chord_vars.append(variable)

    def _ensure_grid_arpeggiators(self, count: int) -> None:
        while len(self.grid_arpeggiators) < count:
            self.grid_arpeggiators.append(ArpeggiatorSettings())

    def _rebuild_grid_chord_inputs(self) -> None:
        for widget in self.grid_chord_entries_frame.winfo_children():
            widget.destroy()
        values = self._grid_values()
        if values is None:
            self.grid_status_var.set("Saisissez une signature et un nombre de mesures valides.")
            return
        numerator, denominator, _measures, unit, durations = values
        self._ensure_grid_chord_vars(len(durations))
        self._ensure_grid_arpeggiators(len(durations))
        nominal = RHYTHM_UNIT_DURATIONS[unit]
        one_measure = measure_duration(numerator, denominator)
        elapsed = 0
        for index, duration in enumerate(durations):
            cell = ctk.CTkFrame(self.grid_chord_entries_frame)
            row, column = divmod(index, 6)
            cell.grid(row=row, column=column, padx=3, pady=3, sticky="ew")
            cell.grid_columnconfigure(0, weight=1)
            measure_number = int(elapsed // one_measure) + 1
            adjusted = " · fin ajustée" if duration != nominal else ""
            ctk.CTkLabel(
                cell,
                text=f"Case {index + 1} · M{measure_number}{adjusted}",
                font=ctk.CTkFont(size=10),
            ).grid(row=0, column=0, padx=5, pady=(4, 1), sticky="w")
            ctk.CTkEntry(
                cell,
                textvariable=self.grid_chord_vars[index],
                placeholder_text="C / , / vide",
                width=110,
            ).grid(row=1, column=0, padx=5, pady=(1, 5), sticky="ew")
            arp_button = ctk.CTkButton(
                cell,
                text=_arpeggiator_button_text(self.grid_arpeggiators[index]),
                width=34,
            )
            arp_button.configure(
                command=lambda idx=index, btn=arp_button: self._edit_grid_arpeggiator(idx, btn)
            )
            arp_button.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="w")
            elapsed += duration
        self.grid_status_var.set(
            f"{len(durations)} case(s) · subdivision {RHYTHM_UNIT_LABELS[unit]} · "
            f"durée nominale LilyPond {lilypond_duration(nominal)}"
        )

    def _on_grid_unit_changed(self) -> None:
        if self.chord_mode == CHORD_MODE_GRID:
            self.after_idle(self._rebuild_grid_chord_inputs)

    def _on_timing_changed(self, *_args) -> None:
        if self.chord_mode == CHORD_MODE_MEASURE:
            self.after_idle(self._rebuild_measure_chord_inputs)
        elif self.chord_mode == CHORD_MODE_GRID:
            self.after_idle(self._rebuild_grid_chord_inputs)

    def to_segment(self) -> Segment:
        """Read the row fields and return a validated Segment."""
        chord_symbol: str | None = None
        measure_chords: tuple[str | None, ...] = ()
        grid_chords: tuple[str | None, ...] = ()
        chord_arpeggiator = ArpeggiatorSettings()
        measure_arpeggiators: tuple[ArpeggiatorSettings, ...] = ()
        grid_arpeggiators: tuple[ArpeggiatorSettings, ...] = ()
        chord_instrument = INSTRUMENT_LABEL_TO_VALUE.get(
            self.chord_instrument_var.get(), CHORD_INSTRUMENT_PIANO
        )
        chord_grid_unit = RHYTHM_LABEL_TO_UNIT.get(
            self.chord_grid_unit_var.get(), RHYTHM_QUARTER
        )

        try:
            bpm = int(self.bpm_var.get())
            numerator = int(self.numerator_var.get())
            denominator = int(self.denominator_var.get())
            measures = int(self.measures_var.get())

            if self.chord_mode == CHORD_MODE_LINE:
                chord_symbol = self.chord_symbol_var.get().strip() or None
                if chord_symbol:
                    chord_symbol_to_lilypond_chord(chord_symbol)
                chord_arpeggiator = self.line_arpeggiator

            elif self.chord_mode == CHORD_MODE_MEASURE:
                if measures > 0:
                    self._ensure_measure_chord_vars(measures)
                normalized: list[str | None] = []
                for measure_index in range(max(measures, 0)):
                    symbol = self.measure_chord_vars[measure_index].get().strip() or None
                    if symbol:
                        try:
                            chord_symbol_to_lilypond_chord(symbol)
                        except ChordParseError as exc:
                            raise ValidationError(f"Mesure {measure_index + 1}: {exc}") from exc
                    normalized.append(symbol)
                measure_chords = tuple(normalized)
                self._ensure_measure_arpeggiators(max(measures, 0))
                measure_arpeggiators = tuple(self.measure_arpeggiators[:max(measures, 0)])

            elif self.chord_mode == CHORD_MODE_GRID:
                durations = chord_grid_durations(
                    numerator, denominator, measures, chord_grid_unit
                )
                self._ensure_grid_chord_vars(len(durations))
                normalized_grid: list[str | None] = []
                for cell_index in range(len(durations)):
                    value = self.grid_chord_vars[cell_index].get().strip() or None
                    if value and value != ",":
                        try:
                            chord_symbol_to_lilypond_chord(value)
                        except ChordParseError as exc:
                            raise ValidationError(f"Case {cell_index + 1}: {exc}") from exc
                    normalized_grid.append(value)
                grid_chords = tuple(normalized_grid)
                self._ensure_grid_arpeggiators(len(durations))
                grid_arpeggiators = tuple(self.grid_arpeggiators[:len(durations)])

            segment = Segment(
                bpm=bpm,
                numerator=numerator,
                denominator=denominator,
                measures=measures,
                chord_symbol=chord_symbol,
                chord_instrument=chord_instrument,
                chord_mode=self.chord_mode,
                measure_chords=measure_chords,
                chord_grid_unit=chord_grid_unit,
                grid_chords=grid_chords,
                chord_arpeggiator=chord_arpeggiator,
                measure_arpeggiators=measure_arpeggiators,
                grid_arpeggiators=grid_arpeggiators,
            )
        except (ChordParseError, ArpeggiatorError) as exc:
            raise ValidationError(str(exc)) from exc
        except ValueError as exc:
            raise ValidationError("Tous les champs numériques doivent contenir des entiers.") from exc
        segment.validate()
        return segment


class TrackGeneratorApp(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("1120x720")
        self.minsize(940, 560)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.rows: list[SegmentRow] = []
        self.soundfont_var = ctk.StringVar(value="")
        self.click_track_enabled_var = ctk.BooleanVar(value=True)
        self.history: UndoHistory[dict] = UndoHistory(max_entries=100)
        self._history_suspended = True
        self._history_after_id: str | None = None
        self._dragged_row: SegmentRow | None = None
        self._drag_original_index: int | None = None

        self._build_menu()
        self._build_layout()
        self.soundfont_var.trace_add("write", lambda *_args: self._schedule_history_record())
        self.click_track_enabled_var.trace_add(
            "write", lambda *_args: self._schedule_history_record()
        )
        self.add_row(
            defaults=Segment(bpm=120, numerator=4, denominator=4, measures=4),
            record_history=False,
        )
        self._history_suspended = False
        self.history.reset(self._capture_history_snapshot())
        self._update_history_controls()
        self.bind_all("<Control-z>", self.undo)
        self.bind_all("<Command-z>", self.undo)
        self.bind_all("<Control-y>", self.redo)
        self.bind_all("<Control-Shift-z>", self.redo)
        self.bind_all("<Control-Shift-Z>", self.redo)
        self.bind_all("<Command-Shift-z>", self.redo)
        self.bind_all("<Command-Shift-Z>", self.redo)

    def _build_menu(self) -> None:
        """Create the standard Edit menu with Undo and Redo support."""
        self.menu_bar = tk.Menu(self)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.edit_menu.add_command(
            label="Annuler",
            accelerator="Ctrl+Z",
            command=self.undo,
            state="disabled",
        )
        self.edit_menu.add_command(
            label="Rétablir",
            accelerator="Ctrl+Y / Ctrl+Maj+Z",
            command=self.redo,
            state="disabled",
        )
        self.menu_bar.add_cascade(label="Édition", menu=self.edit_menu)
        self.configure(menu=self.menu_bar)

    def _capture_history_snapshot(self) -> dict:
        """Capture raw GUI values, including temporarily invalid input."""
        return build_project_history_snapshot(
            soundfont=self.soundfont_var.get(),
            click_track_enabled=bool(self.click_track_enabled_var.get()),
            rows=[row.to_history_state() for row in self.rows],
        )

    def _schedule_history_record(self) -> None:
        """Debounce keyboard edits so one typed value becomes one undo step."""
        if self._history_suspended:
            return
        if self._history_after_id is not None:
            self.after_cancel(self._history_after_id)
        self._history_after_id = self.after(450, self._commit_history_snapshot)

    def _commit_history_snapshot(self) -> None:
        """Commit the current GUI state to the bounded undo history."""
        if self._history_after_id is not None:
            try:
                self.after_cancel(self._history_after_id)
            except tk.TclError:
                pass
            self._history_after_id = None
        if self._history_suspended:
            return
        self.history.record(self._capture_history_snapshot())
        self._update_history_controls()

    def _flush_pending_history(self) -> None:
        if self._history_after_id is not None:
            self._commit_history_snapshot()

    def _update_history_controls(self) -> None:
        """Synchronize Undo/Redo buttons and menu entries with both stacks."""
        undo_state = "normal" if self.history.can_undo else "disabled"
        redo_state = "normal" if self.history.can_redo else "disabled"
        if hasattr(self, "undo_button"):
            self.undo_button.configure(state=undo_state)
        if hasattr(self, "redo_button"):
            self.redo_button.configure(state=redo_state)
        if hasattr(self, "edit_menu"):
            self.edit_menu.entryconfigure(0, state=undo_state)
            self.edit_menu.entryconfigure(1, state=redo_state)

    def _restore_history_snapshot(self, snapshot: dict) -> None:
        """Replace the GUI state without creating another history entry."""
        snapshot = validate_project_history_snapshot(snapshot)
        self._history_suspended = True
        try:
            for row in self.rows:
                row.destroy()
            self.rows.clear()
            self.soundfont_var.set(str(snapshot.get("soundfont", "")))
            self.click_track_enabled_var.set(
                bool(snapshot.get("click_track_enabled", True))
            )
            for row_state in snapshot.get("rows", []):
                row = self.add_row(record_history=False)
                row.apply_history_state(row_state)
            if not self.rows:
                self.add_row(
                    defaults=Segment(bpm=120, numerator=4, denominator=4, measures=4),
                    record_history=False,
                )
            self._refresh_rows_grid()
        finally:
            self._history_suspended = False

    def undo(self, _event=None):
        """Restore the previous project state and handle ``Ctrl+Z``."""
        self._flush_pending_history()
        snapshot = self.history.undo()
        if snapshot is None:
            self.bell()
            self._update_history_controls()
            return "break"
        self._restore_history_snapshot(snapshot)
        self._update_history_controls()
        return "break"

    def redo(self, _event=None):
        """Restore the next project state and handle Redo shortcuts."""
        self._flush_pending_history()
        snapshot = self.history.redo()
        if snapshot is None:
            self.bell()
            self._update_history_controls()
            return "break"
        self._restore_history_snapshot(snapshot)
        self._update_history_controls()
        return "break"

    def _build_layout(self) -> None:
        """Build all static parts of the GUI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=0)

        title = ctk.CTkLabel(
            self,
            text="GNU TrackGenerator",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(row=0, column=0, padx=18, pady=(18, 4), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Générateur programmable de click track — accords symboliques → LilyPond → MIDI → WAV",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, padx=18, pady=(0, 12), sticky="w")

        self.rows_frame = ctk.CTkScrollableFrame(self, label_text="Séquence musicale")
        self.rows_frame.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")
        self.rows_frame.grid_columnconfigure(0, weight=1)

        soundfont_frame = ctk.CTkFrame(self)
        soundfont_frame.grid(row=3, column=0, padx=18, pady=(8, 6), sticky="ew")
        soundfont_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(soundfont_frame, text="SoundFont (.sf2/.sf3, utilisé par TiMidity/FluidSynth)").grid(
            row=0, column=0, padx=(12, 8), pady=10
        )
        ctk.CTkEntry(soundfont_frame, textvariable=self.soundfont_var).grid(
            row=0, column=1, padx=8, pady=10, sticky="ew"
        )
        ctk.CTkButton(soundfont_frame, text="Parcourir", command=self.browse_soundfont).grid(
            row=0, column=2, padx=(8, 12), pady=10
        )
        self.click_track_switch = ctk.CTkSwitch(
            soundfont_frame,
            text="Click track du projet",
            variable=self.click_track_enabled_var,
            onvalue=True,
            offvalue=False,
        )
        self.click_track_switch.grid(
            row=1, column=0, columnspan=3, padx=12, pady=(0, 10), sticky="w"
        )

        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=4, column=0, padx=18, pady=(6, 6), sticky="ew")
        log_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            log_frame,
            text="Journal de génération — commandes LilyPond / TiMidity / FluidSynth",
            font=ctk.CTkFont(weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=(10, 4), sticky="w")
        self.command_log_text = ctk.CTkTextbox(log_frame, height=150, wrap="none")
        self.command_log_text.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="ew")
        self.command_log_text.insert(
            "end",
            "Les commandes exécutées apparaîtront ici pendant la génération.\n"
            "Un fichier .commands.txt sera aussi écrit dans le dossier de sortie.\n",
        )
        self.command_log_text.configure(state="disabled")

        actions = ctk.CTkFrame(self)
        actions.grid(row=5, column=0, padx=18, pady=(6, 18), sticky="ew")
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        actions.grid_columnconfigure(2, weight=1)
        actions.grid_columnconfigure(3, weight=1)
        actions.grid_columnconfigure(4, weight=2)

        self.undo_button = ctk.CTkButton(
            actions,
            text="Annuler (Ctrl+Z)",
            command=self.undo,
            state="disabled",
        )
        self.undo_button.grid(row=0, column=0, padx=8, pady=12, sticky="ew")
        self.redo_button = ctk.CTkButton(
            actions,
            text="Rétablir (Ctrl+Y)",
            command=self.redo,
            state="disabled",
        )
        self.redo_button.grid(row=0, column=1, padx=8, pady=12, sticky="ew")
        ctk.CTkButton(actions, text="Sauvegarder le projet", command=self.save_project_dialog).grid(
            row=0, column=2, padx=8, pady=12, sticky="ew"
        )
        ctk.CTkButton(actions, text="Charger un projet", command=self.load_project_dialog).grid(
            row=0, column=3, padx=8, pady=12, sticky="ew"
        )
        ctk.CTkButton(
            actions,
            text="Générer",
            height=46,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.generate_dialog,
        ).grid(row=0, column=4, padx=8, pady=12, sticky="ew")

    def add_row(
        self,
        after: SegmentRow | None = None,
        defaults: Segment | None = None,
        *,
        record_history: bool = True,
    ) -> SegmentRow:
        """Add a row, optionally directly after another row."""
        if record_history:
            self._flush_pending_history()
        row = SegmentRow(
            self.rows_frame,
            on_add_after=lambda current: self.add_row(after=current),
            on_remove=self.remove_row,
            on_duplicate=self.duplicate_row,
            on_drag_start=self._start_row_drag,
            on_drag_motion=self._drag_row,
            on_drag_end=self._end_row_drag,
            on_change=self._schedule_history_record,
            defaults=defaults,
        )

        if after and after in self.rows:
            index = self.rows.index(after) + 1
            self.rows.insert(index, row)
        else:
            self.rows.append(row)
        self._refresh_rows_grid()
        if record_history:
            self._commit_history_snapshot()
        return row

    def remove_row(self, row: SegmentRow) -> None:
        """Remove a row while keeping at least one row in the project."""
        if len(self.rows) <= 1:
            messagebox.showinfo(APP_NAME, "Le projet doit contenir au moins une rangée.")
            return
        self._flush_pending_history()
        self.rows.remove(row)
        row.destroy()
        self._refresh_rows_grid()
        self._commit_history_snapshot()

    def duplicate_row(self, row: SegmentRow) -> None:
        """Duplicate a row with all editable values and insert it below."""
        if row not in self.rows:
            return
        self._flush_pending_history()
        state = duplicate_row_state(row.to_history_state())
        self._history_suspended = True
        try:
            duplicate = self.add_row(after=row, record_history=False)
            duplicate.apply_history_state(state)
            self._refresh_rows_grid()
        finally:
            self._history_suspended = False
        self._commit_history_snapshot()

    def _start_row_drag(self, row: SegmentRow, _event=None):
        """Begin a drag-and-drop row reorder operation."""
        if row not in self.rows:
            return "break"
        self._flush_pending_history()
        self._dragged_row = row
        self._drag_original_index = self.rows.index(row)
        row.configure(border_width=2)
        return "break"

    def _drag_row(self, row: SegmentRow, _event=None):
        """Move the dragged row to the position nearest the pointer."""
        if self._dragged_row is not row or row not in self.rows:
            return "break"
        self.update_idletasks()
        pointer_y = self.winfo_pointery()
        target_index = min(
            range(len(self.rows)),
            key=lambda index: abs(
                pointer_y
                - (
                    self.rows[index].winfo_rooty()
                    + max(self.rows[index].winfo_height(), 1) / 2
                )
            ),
        )
        current_index = self.rows.index(row)
        if target_index != current_index:
            move_item(self.rows, current_index, target_index)
            self._refresh_rows_grid()
            self.update_idletasks()
        return "break"

    def _end_row_drag(self, row: SegmentRow, _event=None):
        """Finish drag-and-drop and store one history step if order changed."""
        if self._dragged_row is not row:
            return "break"
        row.configure(border_width=0)
        original_index = self._drag_original_index
        final_index = self.rows.index(row) if row in self.rows else None
        self._dragged_row = None
        self._drag_original_index = None
        if original_index is not None and final_index != original_index:
            self._commit_history_snapshot()
        else:
            self._update_history_controls()
        return "break"

    def _refresh_rows_grid(self) -> None:
        """Re-grid rows after add, remove, duplicate, or reorder operations."""
        for index, row in enumerate(self.rows):
            row.grid(row=index, column=0, padx=8, pady=6, sticky="ew")

    def browse_soundfont(self) -> None:
        """Let the user pick a SoundFont for TiMidity/FluidSynth rendering."""
        path = filedialog.askopenfilename(
            title="Choisir un SoundFont",
            filetypes=[("SoundFont", "*.sf2 *.sf3"), ("Tous les fichiers", "*.*")],
        )
        if path:
            self.soundfont_var.set(path)

    def collect_project(self) -> ProjectData:
        """Collect and validate the full GUI state."""
        segments = []
        for index, row in enumerate(self.rows, start=1):
            try:
                segments.append(row.to_segment())
            except ValidationError as exc:
                raise ValidationError(f"Rangée {index}: {exc}") from exc

        soundfont = self.soundfont_var.get().strip() or None
        project = ProjectData(
            segments=segments,
            soundfont_path=soundfont,
            click_track_enabled=bool(self.click_track_enabled_var.get()),
        )
        project.validate()
        return project

    def save_project_dialog(self) -> None:
        """Save the current GUI state as .gen."""
        try:
            project = self.collect_project()
        except ValidationError as exc:
            messagebox.showerror("Validation", str(exc))
            return

        path = filedialog.asksaveasfilename(
            title="Sauvegarder le projet",
            defaultextension=".gen",
            filetypes=[("GNU TrackGenerator", "*.gen"), ("JSON", "*.json"), ("Tous les fichiers", "*.*")],
        )
        if not path:
            return

        try:
            save_project(project, path)
        except OSError as exc:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le projet:\n{exc}")
            return
        messagebox.showinfo(APP_NAME, f"Projet sauvegardé:\n{path}")

    def load_project_dialog(self) -> None:
        """Load a .gen project and replace the current rows."""
        path = filedialog.askopenfilename(
            title="Charger un projet",
            filetypes=[("GNU TrackGenerator", "*.gen"), ("JSON", "*.json"), ("Tous les fichiers", "*.*")],
        )
        if not path:
            return

        try:
            project = load_project(path)
        except Exception as exc:  # JSON errors, validation errors, OS errors.
            messagebox.showerror("Erreur", f"Impossible de charger le projet:\n{exc}")
            return

        self._history_suspended = True
        try:
            for row in self.rows:
                row.destroy()
            self.rows.clear()
            self.soundfont_var.set(project.soundfont_path or "")
            self.click_track_enabled_var.set(project.click_track_enabled)
            for segment in project.segments:
                self.add_row(defaults=segment, record_history=False)
        finally:
            self._history_suspended = False
        self.history.reset(self._capture_history_snapshot())
        self._update_history_controls()

    def clear_command_log(self) -> None:
        """Clear the visible generation log."""
        self.command_log_text.configure(state="normal")
        self.command_log_text.delete("1.0", "end")
        self.command_log_text.configure(state="disabled")

    def append_command_log(self, message: str) -> None:
        """Append one line to the visible generation log."""
        self.command_log_text.configure(state="normal")
        self.command_log_text.insert("end", message + "\n")
        self.command_log_text.see("end")
        self.command_log_text.configure(state="disabled")
        self.update_idletasks()

    def generate_dialog(self) -> None:
        """Ask output options and run the local generation pipeline."""
        try:
            project = self.collect_project()
        except ValidationError as exc:
            messagebox.showerror("Validation", str(exc))
            return

        output_dir = filedialog.askdirectory(title="Choisir le répertoire de sortie")
        if not output_dir:
            return

        dialog = ctk.CTkInputDialog(
            title="Nom du fichier",
            text="Nom de base des fichiers générés:",
        )
        base_name = dialog.get_input() or "gnu_trackgenerator_click"

        self.clear_command_log()
        self.append_command_log("Démarrage de la génération...")

        try:
            result = generate_project(
                project,
                Path(output_dir),
                base_name=base_name,
                on_log=self.append_command_log,
            )
        except GenerationError as exc:
            messagebox.showerror("Erreur de génération", str(exc))
            return
        except OSError as exc:
            messagebox.showerror("Erreur système", str(exc))
            return

        messagebox.showinfo(
            APP_NAME,
            "Génération terminée:\n"
            f"• {result.gen_path}\n"
            f"• {result.lilypond_path}\n"
            f"• {result.midi_path}\n"
            f"• {result.wav_path}\n"
            f"• Journal: {result.command_log_path}",
        )


def main() -> None:
    """Application entry point."""
    app = TrackGeneratorApp()
    app.mainloop()
