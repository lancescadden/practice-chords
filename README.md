# Chord Trainer 🎸

A terminal-based guitar chord training app with visual diagrams, tab notation, and practice modes.

## Features

- **30+ chords** - Open, 7th, sus, barre, and add chords
- **Dual views** - Vertical chord diagram + horizontal tab notation
- **Practice modes** - Free browse, timed drill, chord progressions, song mode
- **Audio playback** - Hear chords and use metronome (optional)

## Installation

```bash
# With pip
pip install chord-trainer

# With pipx (recommended)
pipx install chord-trainer

# With audio support
pip install chord-trainer[audio]
```

## Usage

```bash
# Launch interactive mode
chord-trainer

# Quick chord lookup
chord-trainer --chord G
chord-trainer --chord Am7

# Timed practice (5 seconds per chord)
chord-trainer --practice --pacing 5

# Practice a progression
chord-trainer --progression pop

# With metronome
chord-trainer --metronome 80
```

## Practice Modes

### Browse Chords
Navigate through all chords with arrow keys. See the diagram, tab notation, and finger positions.

### Timed Practice
Chords cycle automatically with a countdown timer. Great for building muscle memory.

### Chord Progressions
Practice common patterns:
- **Pop** (I-V-vi-IV): G → D → Em → C
- **Rock** (I-IV-V-I): G → C → D → G
- **Blues** (12-bar): A → D → E progression
- **Sad** (vi-IV-I-V): Am → F → C → G
- **Jazz** (ii-V-I): Dm7 → G7 → Cmaj7

### Song Mode
Learn real songs by their chord progressions:
- Wonderwall (Oasis)
- Let It Be (Beatles)
- Knocking on Heaven's Door (Bob Dylan)
- No Woman No Cry (Bob Marley)
- And more!

## Keyboard Controls

| Key | Action |
|-----|--------|
| `←` `→` | Previous/Next chord |
| `Space` | Play chord sound |
| `m` | Toggle metronome |
| `q` | Back/Quit |
| `1-4` | Select menu option |

## Development

```bash
# Clone and install in dev mode
git clone https://github.com/yourusername/chord-trainer
cd chord-trainer
pip install -e ".[audio]"

# Run
chord-trainer
```

## License

MIT
