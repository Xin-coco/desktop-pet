# Desktop Pet

A desktop pet for macOS built with Python + Pygame. Your character floats on top of all windows, walks around, and interacts with you.

## Features

- **Always on top** — pet floats above all windows with transparent background
- **Custom characters** — drag any character PNG into `assets/sprites/` and run the generator
- **Multiple states** — idle, walk, sleep, eat, play with pixel-art animations
- **Status system** — hunger, mood, and energy decay over time
- **Interactions** — drag to move, click to pet, right-click for menu
- **Reminders** — set timed reminders, pet shows speech bubble when it's time

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# If you have a custom character image:
python generate_sprites.py  # edit SRC path in the script first

# Run
python main.py
```

Press `Esc` or `Cmd+Q` to quit.

## Custom Sprites

1. Place your character image somewhere (e.g. `~/Downloads/character.jpg`)
2. Edit the `SRC` path at the top of `generate_sprites.py`
3. Run `python generate_sprites.py`
4. Start the pet: `python main.py`

Or manually: add PNG frames to `assets/sprites/<state>/`:

| Folder | Frames | Description |
|--------|--------|-------------|
| `idle/` | `idle_01.png`, `idle_02.png` | Breathing idle animation |
| `walk/` | `walk_01.png` ... `walk_04.png` | Walking animation |
| `sleep/` | `sleep_01.png`, `sleep_02.png` | Sleeping with Zzz |
| `eat/` | `eat_01.png`, `eat_02.png` | Eating animation |
| `play/` | `play_01.png`, `play_02.png` | Playful bounce |

## Requirements

- macOS
- Python 3.10+
- SDL2 (`brew install sdl2`)

## Controls

| Action | How |
|--------|-----|
| Move pet | Drag with mouse |
| Pet | Click the pet |
| Context menu | Right-click the pet |
| Quit | `Esc` or `Cmd+Q` |
