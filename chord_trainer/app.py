"""Main application logic for Chord Trainer."""

import sys
import time
import threading
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table

from .chords import CHORDS, get_chord_list, render_chord_panel, Chord
from .data import PROGRESSIONS, SONGS, Progression, Song
from .audio import AUDIO_AVAILABLE, play_chord, Metronome, stop_all


class Mode(Enum):
    MENU = "menu"
    BROWSE = "browse"
    PRACTICE = "practice"
    PROGRESSIONS = "progressions"
    SONGS = "songs"
    SETTINGS = "settings"


class ChordTrainer:
    """Main application class."""

    def __init__(self):
        self.console = Console()
        self.mode = Mode.MENU
        self.running = True

        # Chord navigation
        self.chord_list = get_chord_list()
        self.chord_index = 0

        # Practice settings
        self.pacing = 6  # seconds per chord
        self.metronome = Metronome(80)

        # State
        self.current_progression: Progression | None = None
        self.current_song: Song | None = None
        self.progression_index = 0

    @property
    def current_chord(self) -> Chord:
        return self.chord_list[self.chord_index]

    def run(self):
        """Main application loop."""
        try:
            while self.running:
                if self.mode == Mode.MENU:
                    self.show_menu()
                elif self.mode == Mode.BROWSE:
                    self.browse_chords()
                elif self.mode == Mode.PRACTICE:
                    self.timed_practice()
                elif self.mode == Mode.PROGRESSIONS:
                    self.progression_practice()
                elif self.mode == Mode.SONGS:
                    self.song_mode()
                elif self.mode == Mode.SETTINGS:
                    self.settings_menu()
        except KeyboardInterrupt:
            pass
        finally:
            self.metronome.stop()
            stop_all()
            self.console.print("\n[dim]Thanks for practicing![/]")

    def show_menu(self):
        """Display the main menu."""
        self.console.clear()

        # Header
        header = Panel(
            Text("CHORD TRAINER\n♪ ═══════════════ ♪", justify="center", style="bold cyan"),
            border_style="blue",
        )
        self.console.print(header)
        self.console.print()

        # Menu options
        options = [
            ("1", "Browse Chords", f"{len(self.chord_list)} chords"),
            ("2", "Timed Practice", f"Random chords, {self.pacing}s each"),
            ("3", "Chord Progressions", f"{len(PROGRESSIONS)} patterns"),
            ("4", "Song Mode", f"{len(SONGS)} songs"),
            ("5", "Settings", f"Pacing: {self.pacing}s"),
            ("q", "Quit", ""),
        ]

        for key, label, desc in options:
            if desc:
                self.console.print(f"  [bold cyan]{key}[/]. {label}  [dim]({desc})[/]")
            else:
                self.console.print(f"  [bold cyan]{key}[/]. {label}")

        self.console.print()

        # Audio status
        if AUDIO_AVAILABLE:
            self.console.print("[dim]Audio: ✓ Available[/]")
        else:
            self.console.print("[dim]Audio: ✗ Install [cyan]pip install chord-trainer[audio][/] for sound[/]")

        # Get input
        self.console.print()
        choice = self.console.input("[bold]Select option: [/]").strip().lower()

        if choice == '1':
            self.mode = Mode.BROWSE
        elif choice == '2':
            self.mode = Mode.PRACTICE
        elif choice == '3':
            self.mode = Mode.PROGRESSIONS
        elif choice == '4':
            self.mode = Mode.SONGS
        elif choice == '5':
            self.mode = Mode.SETTINGS
        elif choice == 'q':
            self.running = False

    def browse_chords(self):
        """Browse through chords with keyboard navigation."""
        while True:
            self.console.clear()
            self.console.print(f"[bold]Browse Chords[/]  [{self.chord_index + 1}/{len(self.chord_list)}]")
            self.console.print()

            panel = render_chord_panel(self.current_chord)
            self.console.print(panel)

            self.console.print()
            self.console.print("[dim]n[/]=next  [dim]p[/]=prev  [dim]space[/]=play  [dim]q[/]=back  [dim]or type chord name[/]")
            choice = self.console.input("> ").strip()

            if choice.lower() == 'q':
                self.mode = Mode.MENU
                return
            elif choice == '' or choice.lower() == 'n':
                self.chord_index = (self.chord_index + 1) % len(self.chord_list)
            elif choice.lower() == 'p':
                self.chord_index = (self.chord_index - 1) % len(self.chord_list)
            elif choice == ' ':
                if AUDIO_AVAILABLE:
                    play_chord(self.current_chord.frets)
            else:
                # Try to find chord by name
                for i, chord in enumerate(self.chord_list):
                    if chord.name.lower() == choice.lower():
                        self.chord_index = i
                        if AUDIO_AVAILABLE:
                            play_chord(chord.frets)
                        break

    def timed_practice(self):
        """Timed chord practice with countdown."""
        self.console.print("[bold]Starting timed practice...[/]")
        self.console.print(f"[dim]Each chord displays for {self.pacing} seconds. Press Ctrl+C to stop.[/]")
        time.sleep(1)

        try:
            while True:
                # Pick next chord (cycle through)
                self.chord_index = (self.chord_index + 1) % len(self.chord_list)
                chord = self.current_chord

                # Play chord immediately
                if AUDIO_AVAILABLE:
                    play_chord(chord.frets)

                # Countdown with live display
                for remaining in range(self.pacing, 0, -1):
                    self.console.clear()

                    # Progress bar
                    progress_pct = (self.pacing - remaining) / self.pacing
                    bar_width = 30
                    filled = int(bar_width * progress_pct)
                    bar = "█" * filled + "░" * (bar_width - filled)

                    self.console.print(f"[bold]Timed Practice[/]  {bar}  [cyan]{remaining}s[/]")
                    self.console.print()

                    panel = render_chord_panel(chord)
                    self.console.print(panel)

                    self.console.print("\n[dim]Press Ctrl+C to stop[/]")

                    time.sleep(1)

        except KeyboardInterrupt:
            self.console.print("\n[dim]Practice stopped.[/]")
            time.sleep(0.5)

        self.mode = Mode.MENU

    def progression_practice(self):
        """Practice chord progressions."""
        self.console.clear()

        # Show progression list
        self.console.print("[bold]Chord Progressions[/]\n")

        prog_list = list(PROGRESSIONS.items())
        for i, (key, prog) in enumerate(prog_list, 1):
            chords_str = " → ".join(prog.chords[:4])
            if len(prog.chords) > 4:
                chords_str += " ..."
            self.console.print(f"  [cyan]{i}[/]. [bold]{prog.name}[/] ({prog.numerals})")
            self.console.print(f"      [dim]{chords_str}[/]")

        self.console.print(f"\n  [cyan]q[/]. Back to menu")
        self.console.print()

        choice = self.console.input("[bold]Select progression: [/]").strip().lower()

        if choice == 'q':
            self.mode = Mode.MENU
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(prog_list):
                key, prog = prog_list[idx]
                self._auto_play_sequence(prog.chords, f"{prog.name} Progression")
        except ValueError:
            pass

    def song_mode(self):
        """Practice songs by their chord progressions."""
        self.console.clear()

        self.console.print("[bold]Song Mode[/]\n")

        for i, song in enumerate(SONGS, 1):
            chords_str = " → ".join(song.chords)
            self.console.print(f"  [cyan]{i}[/]. [bold]{song.title}[/] - {song.artist}")
            self.console.print(f"      [dim]{chords_str}[/]")

        self.console.print(f"\n  [cyan]q[/]. Back to menu")
        self.console.print()

        choice = self.console.input("[bold]Select song: [/]").strip().lower()

        if choice == 'q':
            self.mode = Mode.MENU
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(SONGS):
                song = SONGS[idx]
                self._auto_play_sequence(song.chords, f"{song.title} by {song.artist}")
        except ValueError:
            pass

    def _auto_play_sequence(self, chord_names: list[str], title: str):
        """Auto-play a sequence of chords with timing."""
        # Build chord list for this sequence
        seq_chords = []
        for name in chord_names:
            if name in CHORDS:
                seq_chords.append(CHORDS[name])
            else:
                self.console.print(f"[yellow]Warning: Chord '{name}' not found[/]")

        if not seq_chords:
            return

        self.console.clear()
        self.console.print(f"[bold]{title}[/]")
        self.console.print(f"[dim]Chords cycle every {self.pacing}s. Press Ctrl+C to stop.[/]")
        self.console.print()

        # Show all chords in sequence
        chord_names_display = " → ".join(c.name for c in seq_chords)
        self.console.print(f"[cyan]{chord_names_display}[/]")
        self.console.print()
        time.sleep(1)

        seq_index = 0

        try:
            while True:
                chord = seq_chords[seq_index]

                # Play chord sound
                if AUDIO_AVAILABLE:
                    play_chord(chord.frets)

                # Display with countdown
                for remaining in range(self.pacing, 0, -1):
                    self.console.clear()

                    self.console.print(f"[bold]{title}[/]")
                    self.console.print()

                    # Show chord sequence with current highlighted
                    seq_display = []
                    for i, c in enumerate(seq_chords):
                        if i == seq_index:
                            seq_display.append(f"[bold cyan][{c.name}][/]")
                        else:
                            seq_display.append(f"[dim]{c.name}[/]")
                    self.console.print(" → ".join(seq_display))

                    # Progress bar
                    progress_pct = (self.pacing - remaining) / self.pacing
                    bar_width = 20
                    filled = int(bar_width * progress_pct)
                    bar = "█" * filled + "░" * (bar_width - filled)
                    self.console.print(f"\n{bar}  [cyan]{remaining}s[/]")
                    self.console.print()

                    # Show current chord
                    panel = render_chord_panel(chord)
                    self.console.print(panel)

                    self.console.print("\n[dim]Ctrl+C to stop[/]")

                    time.sleep(1)

                # Move to next chord (loop)
                seq_index = (seq_index + 1) % len(seq_chords)

        except KeyboardInterrupt:
            self.console.print("\n[dim]Stopped.[/]")
            time.sleep(0.5)

    def settings_menu(self):
        """Settings menu."""
        while True:
            self.console.clear()
            self.console.print("[bold]Settings[/]\n")

            self.console.print(f"  [cyan]1[/]. Pacing: [bold]{self.pacing}[/] seconds per chord")
            self.console.print(f"  [cyan]2[/]. Metronome BPM: [bold]{self.metronome.bpm}[/]")
            self.console.print(f"  [cyan]3[/]. Toggle metronome: [bold]{'ON' if self.metronome.is_running else 'OFF'}[/]")
            self.console.print()
            self.console.print(f"  [cyan]q[/]. Back to menu")
            self.console.print()

            choice = self.console.input("[bold]Select option: [/]").strip().lower()

            if choice == 'q':
                self.mode = Mode.MENU
                return
            elif choice == '1':
                try:
                    val = int(self.console.input("Seconds per chord (2-30): "))
                    self.pacing = max(2, min(30, val))
                except ValueError:
                    pass
            elif choice == '2':
                try:
                    val = int(self.console.input("BPM (40-200): "))
                    self.metronome.set_bpm(val)
                except ValueError:
                    pass
            elif choice == '3':
                if self.metronome.is_running:
                    self.metronome.stop()
                else:
                    self.metronome.start()


def show_single_chord(chord_name: str):
    """Display a single chord and exit."""
    console = Console()

    # Try exact match first
    chord = CHORDS.get(chord_name)

    # Try case-insensitive
    if not chord:
        for name, c in CHORDS.items():
            if name.lower() == chord_name.lower():
                chord = c
                break

    if not chord:
        console.print(f"[red]Chord '{chord_name}' not found.[/]")
        console.print("[dim]Available chords:[/]", ", ".join(CHORDS.keys()))
        return

    panel = render_chord_panel(chord)
    console.print(panel)

    if AUDIO_AVAILABLE:
        play_chord(chord.frets)
        time.sleep(2)


def quick_practice(pacing: int = 6):
    """Start quick practice mode."""
    app = ChordTrainer()
    app.pacing = pacing
    app.mode = Mode.PRACTICE
    app.run()


def quick_progression(name: str):
    """Start a specific progression."""
    console = Console()
    prog = PROGRESSIONS.get(name.lower())

    if not prog:
        console.print(f"[red]Progression '{name}' not found.[/]")
        console.print("[dim]Available progressions:[/]", ", ".join(PROGRESSIONS.keys()))
        return

    app = ChordTrainer()
    app._auto_play_sequence(prog.chords, f"{prog.name} Progression")
