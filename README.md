# Tic Tac Toe

A two-player Tic Tac Toe game built with Pygame. Deployable as a web app (via Pygbag/WebAssembly) or as a standalone executable.

## Project structure

```
tic_tac_toe/
├── main.py          # Entry point (async, Pygbag-compatible)
├── game_state.py    # Game logic (board, win detection)
├── renderer.py      # All Pygame rendering
├── constants.py     # Shared constants
├── pictures/        # Game images (cover, X, O)
├── requirements.txt
└── pyproject.toml
```

## Local development

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python  main.py
```

## Web deployment (Pygbag)

Pygbag compiles the game to WebAssembly so it runs in any browser.

```bash
pip install pygbag
pygbag main.py
# Open http://localhost:8000
```

To build a static bundle for hosting (GitHub Pages, Netlify, etc.):

```bash
pygbag --build main.py
# Static files are generated in build/web/
```

## Standalone executable (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "pictures:pictures" main.py
# Executable is in dist/
```

## How to play

- The game starts with a cover screen (3 seconds or click to skip).
- Players take turns clicking a cell to place their mark (X goes first).
- The first player to align 3 marks in a row, column, or diagonal wins.
- After the result is shown (3 seconds), the game resets automatically.
