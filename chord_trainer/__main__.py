"""Entry point for Chord Trainer."""

import argparse
import sys

from .app import ChordTrainer, show_single_chord, quick_practice, quick_progression
from .audio import AUDIO_AVAILABLE, Metronome


def main():
    parser = argparse.ArgumentParser(
        description="Terminal-based guitar chord trainer",
        prog="chord-trainer",
    )

    parser.add_argument(
        "--chord", "-c",
        metavar="NAME",
        help="Display a specific chord (e.g., G, Am7, Fmaj7)",
    )

    parser.add_argument(
        "--practice", "-p",
        action="store_true",
        help="Start timed practice mode",
    )

    parser.add_argument(
        "--pacing",
        type=int,
        default=5,
        metavar="SECONDS",
        help="Seconds per chord in practice mode (default: 5)",
    )

    parser.add_argument(
        "--progression",
        metavar="NAME",
        help="Practice a progression (pop, rock, blues, sad, jazz, folk)",
    )

    parser.add_argument(
        "--metronome", "-m",
        type=int,
        metavar="BPM",
        help="Start with metronome at given BPM",
    )

    parser.add_argument(
        "--list-chords",
        action="store_true",
        help="List all available chords",
    )

    parser.add_argument(
        "--list-progressions",
        action="store_true",
        help="List all available progressions",
    )

    args = parser.parse_args()

    # Handle list commands
    if args.list_chords:
        from .chords import get_chords_by_category
        from rich.console import Console
        console = Console()

        for category, chords in get_chords_by_category().items():
            console.print(f"\n[bold]{category}[/]")
            chord_names = [c.name for c in chords]
            console.print("  " + ", ".join(chord_names))
        return

    if args.list_progressions:
        from .data import PROGRESSIONS
        from rich.console import Console
        console = Console()

        console.print("\n[bold]Available Progressions[/]\n")
        for key, prog in PROGRESSIONS.items():
            console.print(f"  [cyan]{key}[/]: {prog.name} - {' → '.join(prog.chords)}")
        return

    # Handle single chord display
    if args.chord:
        show_single_chord(args.chord)
        return

    # Handle progression mode
    if args.progression:
        quick_progression(args.progression)
        return

    # Handle practice mode
    if args.practice:
        quick_practice(args.pacing)
        return

    # Interactive mode
    app = ChordTrainer()

    # Apply metronome setting
    if args.metronome and AUDIO_AVAILABLE:
        app.metronome.set_bpm(args.metronome)
        app.metronome.start()

    app.run()


if __name__ == "__main__":
    main()
