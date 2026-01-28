"""Chord data and rendering functions."""

from dataclasses import dataclass
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Console, Group


@dataclass
class Chord:
    """Guitar chord with fret positions and finger assignments."""
    name: str
    category: str
    frets: tuple[int | None, ...]  # (E, A, D, G, B, e) - None = muted, 0 = open
    fingers: tuple[int | None, ...]  # Finger numbers (1=index, 2=middle, 3=ring, 4=pinky)
    barre: int | None = None  # Fret number if barre chord

    @property
    def tab_notation(self) -> list[str]:
        """Return tab notation strings."""
        strings = ['e', 'B', 'G', 'D', 'A', 'E']
        lines = []
        for i, string in enumerate(strings):
            fret = self.frets[5 - i]  # Reverse order for tab
            if fret is None:
                val = 'x'
            else:
                val = str(fret)
            lines.append(f"{string} ──{val:^3}──")
        return lines


# Circled numbers for finger display
FINGER_CIRCLES = {1: '①', 2: '②', 3: '③', 4: '④', None: ' '}


def render_chord_diagram(chord: Chord) -> str:
    """Render a vertical chord diagram."""
    lines = []

    # Header with string names and open/muted indicators
    header = "    E A D G B e"
    open_muted = "    "
    for fret in chord.frets:
        if fret is None:
            open_muted += "× "
        elif fret == 0:
            open_muted += "○ "
        else:
            open_muted += "  "

    lines.append(header)
    lines.append(open_muted)

    # Determine starting fret for display
    non_zero_frets = [f for f in chord.frets if f and f > 0]
    if non_zero_frets:
        min_fret = min(non_zero_frets)
        max_fret = max(non_zero_frets)
        if max_fret <= 4:
            start_fret = 1
        else:
            start_fret = min_fret
    else:
        start_fret = 1

    # Nut or position indicator
    if start_fret == 1:
        lines.append("    ╒═╤═╤═╤═╤═╕")
    else:
        lines.append(f" {start_fret}  ┌─┬─┬─┬─┬─┐")

    # Frets
    for fret_num in range(start_fret, start_fret + 4):
        # Show fret number on left (skip 1 when at nut)
        if start_fret == 1:
            fret_label = str(fret_num) if fret_num > 0 else ' '
        else:
            fret_label = str(fret_num)
        fret_line = f" {fret_label} "

        # Build the fret positions
        positions = []
        for i, (fret, finger) in enumerate(zip(chord.frets, chord.fingers)):
            if fret == fret_num:
                positions.append(FINGER_CIRCLES.get(finger, '●'))
            else:
                positions.append(' ')

        # Handle barre chords
        if chord.barre and fret_num == chord.barre:
            barre_positions = []
            for i, (fret, finger) in enumerate(zip(chord.frets, chord.fingers)):
                if fret == chord.barre and finger == 1:
                    barre_positions.append('━')
                elif fret == fret_num:
                    barre_positions.append(FINGER_CIRCLES.get(finger, '●'))
                elif fret is not None and chord.barre <= fret_num:
                    barre_positions.append(' ')
                else:
                    barre_positions.append(' ')
            positions = barre_positions

        fret_line += "│" + "│".join(positions) + "│"
        lines.append(fret_line)

        # Fret separator
        if fret_num < start_fret + 3:
            lines.append("    ├─┼─┼─┼─┼─┤")

    lines.append("    └─┴─┴─┴─┴─┘")

    return "\n".join(lines)


def render_chord_panel(chord: Chord, console_width: int = 50, show_big: bool = True) -> Panel:
    """Render a complete chord panel with diagram, tab, and big ASCII name."""
    from .bigtext import render_big_text

    # Create the diagram
    diagram = render_chord_diagram(chord)

    # Create tab notation
    tab_lines = chord.tab_notation

    # Create big text (6 lines)
    big_lines = render_big_text(chord.name) if show_big else [""] * 6

    # Combine diagram and tab side by side
    diagram_lines = diagram.split('\n')

    # Build combined display: diagram | tab | big name
    # Pad all to same length
    max_lines = max(len(diagram_lines), len(tab_lines), len(big_lines))
    while len(diagram_lines) < max_lines:
        diagram_lines.append("")
    while len(tab_lines) < max_lines:
        tab_lines.insert(0, "")
    while len(big_lines) < max_lines:
        big_lines.append("")

    # Combine with spacing
    combined_lines = []
    for i, (d_line, t_line) in enumerate(zip(diagram_lines, tab_lines)):
        big_part = big_lines[i] if i < len(big_lines) else ""
        combined_lines.append(f"{d_line:<22} {t_line:<14} {big_part}")

    # Add finger info
    finger_str = "-".join(
        str(f) if f else 'x' if chord.frets[i] is None else '0'
        for i, f in enumerate(chord.fingers)
    )
    combined_lines.append("")
    combined_lines.append(f"{'':22} Fingers: {finger_str}")

    content = "\n".join(combined_lines)

    return Panel(
        content,
        title=f"[bold cyan]{chord.name}[/]",
        subtitle=f"[dim]{chord.category}[/]",
        border_style="blue",
        padding=(1, 2),
    )


# ============================================================================
# CHORD LIBRARY
# ============================================================================

CHORDS: dict[str, Chord] = {}

def _add(name: str, category: str, frets: tuple, fingers: tuple, barre: int | None = None):
    """Helper to add chord to library."""
    CHORDS[name] = Chord(name, category, frets, fingers, barre)


# Open Chords
_add("G", "Open Major", (3, 2, 0, 0, 0, 3), (2, 1, None, None, None, 3))
_add("C", "Open Major", (None, 3, 2, 0, 1, 0), (None, 3, 2, None, 1, None))
_add("D", "Open Major", (None, None, 0, 2, 3, 2), (None, None, None, 1, 3, 2))
_add("E", "Open Major", (0, 2, 2, 1, 0, 0), (None, 2, 3, 1, None, None))
_add("A", "Open Major", (None, 0, 2, 2, 2, 0), (None, None, 1, 2, 3, None))
_add("Em", "Open Minor", (0, 2, 2, 0, 0, 0), (None, 2, 3, None, None, None))
_add("Am", "Open Minor", (None, 0, 2, 2, 1, 0), (None, None, 2, 3, 1, None))
_add("Dm", "Open Minor", (None, None, 0, 2, 3, 1), (None, None, None, 2, 3, 1))

# 7th Chords
_add("G7", "7th", (3, 2, 0, 0, 0, 1), (3, 2, None, None, None, 1))
_add("C7", "7th", (None, 3, 2, 3, 1, 0), (None, 3, 2, 4, 1, None))
_add("D7", "7th", (None, None, 0, 2, 1, 2), (None, None, None, 2, 1, 3))
_add("A7", "7th", (None, 0, 2, 0, 2, 0), (None, None, 2, None, 3, None))
_add("E7", "7th", (0, 2, 0, 1, 0, 0), (None, 2, None, 1, None, None))
_add("Am7", "7th", (None, 0, 2, 0, 1, 0), (None, None, 2, None, 1, None))
_add("Em7", "7th", (0, 2, 0, 0, 0, 0), (None, 2, None, None, None, None))
_add("Dm7", "7th", (None, None, 0, 2, 1, 1), (None, None, None, 2, 1, 1))
_add("Cmaj7", "7th", (None, 3, 2, 0, 0, 0), (None, 3, 2, None, None, None))
_add("Fmaj7", "7th", (None, None, 3, 2, 1, 0), (None, None, 3, 2, 1, None))

# Sus Chords
_add("Dsus2", "Sus", (None, None, 0, 2, 3, 0), (None, None, None, 1, 3, None))
_add("Dsus4", "Sus", (None, None, 0, 2, 3, 3), (None, None, None, 1, 3, 4))
_add("Asus2", "Sus", (None, 0, 2, 2, 0, 0), (None, None, 1, 2, None, None))
_add("Asus4", "Sus", (None, 0, 2, 2, 3, 0), (None, None, 1, 2, 4, None))
_add("Esus4", "Sus", (0, 2, 2, 2, 0, 0), (None, 2, 3, 4, None, None))

# Barre Chords
_add("F", "Barre", (1, 3, 3, 2, 1, 1), (1, 3, 4, 2, 1, 1), barre=1)
_add("Bm", "Barre", (None, 2, 4, 4, 3, 2), (None, 1, 3, 4, 2, 1), barre=2)
_add("F#m", "Barre", (2, 4, 4, 2, 2, 2), (1, 3, 4, 1, 1, 1), barre=2)
_add("Bb", "Barre", (None, 1, 3, 3, 3, 1), (None, 1, 2, 3, 4, 1), barre=1)
_add("B", "Barre", (None, 2, 4, 4, 4, 2), (None, 1, 2, 3, 4, 1), barre=2)

# Add Chords
_add("Cadd9", "Add", (None, 3, 2, 0, 3, 0), (None, 2, 1, None, 3, None))
_add("Gadd9", "Add", (3, 2, 0, 2, 0, 3), (2, 1, None, 3, None, 4))

# Extra useful chords
_add("D6/9", "Add", (None, None, 0, 2, 0, 0), (None, None, None, 2, None, None))  # For Horse With No Name


def get_chords_by_category() -> dict[str, list[Chord]]:
    """Return chords grouped by category."""
    categories: dict[str, list[Chord]] = {}
    for chord in CHORDS.values():
        if chord.category not in categories:
            categories[chord.category] = []
        categories[chord.category].append(chord)
    return categories


def get_chord_list() -> list[Chord]:
    """Return all chords in a logical order."""
    order = ["Open Major", "Open Minor", "7th", "Sus", "Barre", "Add"]
    result = []
    by_cat = get_chords_by_category()
    for cat in order:
        if cat in by_cat:
            result.extend(by_cat[cat])
    return result
