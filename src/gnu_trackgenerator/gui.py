# SPDX-FileCopyrightText: 2026 Steve Prud'Homme and GNU TrackGenerator contributors
# SPDX-License-Identifier: GPL-3.0-only

"""CustomTkinter GUI for GNU TrackGenerator."""

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk
except ImportError as exc:  # Friendly failure when launched without dependency.
    raise SystemExit(
        "CustomTkinter n'est pas installé. Exécutez: pip install -r requirements.txt"
    ) from exc

from .generator import GenerationError, generate_project
from .models import APP_NAME, APP_VERSION, ProjectData, Segment, ValidationError
from .project_io import load_project, save_project


class SegmentRow(ctk.CTkFrame):
    """One editable musical segment row in the scrollable list."""

    def __init__(
        self,
        master: ctk.CTkFrame,
        on_add_after,
        on_remove,
        defaults: Segment | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self.on_add_after = on_add_after
        self.on_remove = on_remove

        segment = defaults or Segment(bpm=120, numerator=4, denominator=4, measures=4)
        self.bpm_var = ctk.StringVar(value=str(segment.bpm))
        self.numerator_var = ctk.StringVar(value=str(segment.numerator))
        self.denominator_var = ctk.StringVar(value=str(segment.denominator))
        self.measures_var = ctk.StringVar(value=str(segment.measures))

        self._build_widgets()

    def _build_widgets(self) -> None:
        """Create and place row widgets."""
        for col in range(9):
            self.grid_columnconfigure(col, weight=1 if col in {1, 3, 5, 7} else 0)

        ctk.CTkLabel(self, text="BPM").grid(row=0, column=0, padx=(8, 4), pady=8)
        ctk.CTkEntry(self, textvariable=self.bpm_var, width=70).grid(row=0, column=1, padx=4, pady=8)

        ctk.CTkLabel(self, text="Signature").grid(row=0, column=2, padx=(12, 4), pady=8)
        ctk.CTkEntry(self, textvariable=self.numerator_var, width=55).grid(row=0, column=3, padx=(4, 2), pady=8)
        ctk.CTkLabel(self, text="/").grid(row=0, column=4, padx=0, pady=8)
        ctk.CTkEntry(self, textvariable=self.denominator_var, width=55).grid(row=0, column=5, padx=(2, 4), pady=8)

        ctk.CTkLabel(self, text="Mesures").grid(row=0, column=6, padx=(12, 4), pady=8)
        ctk.CTkEntry(self, textvariable=self.measures_var, width=70).grid(row=0, column=7, padx=4, pady=8)

        ctk.CTkButton(self, text="+", width=34, command=lambda: self.on_add_after(self)).grid(
            row=0, column=8, padx=(8, 2), pady=8
        )
        ctk.CTkButton(self, text="−", width=34, command=lambda: self.on_remove(self)).grid(
            row=0, column=9, padx=(2, 8), pady=8
        )

    def to_segment(self) -> Segment:
        """Read the row fields and return a validated Segment."""
        try:
            segment = Segment(
                bpm=int(self.bpm_var.get()),
                numerator=int(self.numerator_var.get()),
                denominator=int(self.denominator_var.get()),
                measures=int(self.measures_var.get()),
            )
        except ValueError as exc:
            raise ValidationError("Tous les champs doivent contenir des entiers.") from exc
        segment.validate()
        return segment


class TrackGeneratorApp(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("980x640")
        self.minsize(860, 520)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.rows: list[SegmentRow] = []
        self.soundfont_var = ctk.StringVar(value="")

        self._build_layout()
        self.add_row(defaults=Segment(bpm=120, numerator=4, denominator=4, measures=4))

    def _build_layout(self) -> None:
        """Build all static parts of the GUI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        title = ctk.CTkLabel(
            self,
            text="GNU TrackGenerator",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(row=0, column=0, padx=18, pady=(18, 4), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Générateur programmable de click track — LilyPond → MIDI → WAV",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, padx=18, pady=(0, 12), sticky="w")

        self.rows_frame = ctk.CTkScrollableFrame(self, label_text="Séquence musicale")
        self.rows_frame.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")
        self.rows_frame.grid_columnconfigure(0, weight=1)

        soundfont_frame = ctk.CTkFrame(self)
        soundfont_frame.grid(row=3, column=0, padx=18, pady=(8, 6), sticky="ew")
        soundfont_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(soundfont_frame, text="SoundFont (.sf2/.sf3)").grid(
            row=0, column=0, padx=(12, 8), pady=10
        )
        ctk.CTkEntry(soundfont_frame, textvariable=self.soundfont_var).grid(
            row=0, column=1, padx=8, pady=10, sticky="ew"
        )
        ctk.CTkButton(soundfont_frame, text="Parcourir", command=self.browse_soundfont).grid(
            row=0, column=2, padx=(8, 12), pady=10
        )

        actions = ctk.CTkFrame(self)
        actions.grid(row=4, column=0, padx=18, pady=(6, 18), sticky="ew")
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        actions.grid_columnconfigure(2, weight=2)

        ctk.CTkButton(actions, text="Sauvegarder le projet", command=self.save_project_dialog).grid(
            row=0, column=0, padx=8, pady=12, sticky="ew"
        )
        ctk.CTkButton(actions, text="Charger un projet", command=self.load_project_dialog).grid(
            row=0, column=1, padx=8, pady=12, sticky="ew"
        )
        ctk.CTkButton(
            actions,
            text="Générer",
            height=46,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.generate_dialog,
        ).grid(row=0, column=2, padx=8, pady=12, sticky="ew")

    def add_row(self, after: SegmentRow | None = None, defaults: Segment | None = None) -> None:
        """Add a row, optionally directly after another row."""
        row = SegmentRow(
            self.rows_frame,
            on_add_after=lambda current: self.add_row(after=current),
            on_remove=self.remove_row,
            defaults=defaults,
        )

        if after and after in self.rows:
            index = self.rows.index(after) + 1
            self.rows.insert(index, row)
        else:
            self.rows.append(row)
        self._refresh_rows_grid()

    def remove_row(self, row: SegmentRow) -> None:
        """Remove a row while keeping at least one row in the project."""
        if len(self.rows) <= 1:
            messagebox.showinfo(APP_NAME, "Le projet doit contenir au moins une rangée.")
            return
        self.rows.remove(row)
        row.destroy()
        self._refresh_rows_grid()

    def _refresh_rows_grid(self) -> None:
        """Re-grid rows after add/remove operations."""
        for index, row in enumerate(self.rows):
            row.grid(row=index, column=0, padx=8, pady=6, sticky="ew")

    def browse_soundfont(self) -> None:
        """Let the user pick a SoundFont for FluidSynth rendering."""
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
        project = ProjectData(segments=segments, soundfont_path=soundfont)
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

        for row in self.rows:
            row.destroy()
        self.rows.clear()
        self.soundfont_var.set(project.soundfont_path or "")
        for segment in project.segments:
            self.add_row(defaults=segment)

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

        try:
            result = generate_project(project, Path(output_dir), base_name=base_name)
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
            f"• {result.wav_path}",
        )


def main() -> None:
    """Application entry point."""
    app = TrackGeneratorApp()
    app.mainloop()
