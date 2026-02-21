# Project Guidelines: Memory Game

## Code Style
- **Python Version**: 3.10+
- **Formatting**: Follow PEP 8 with type hints where possible
- **Imports**: Use `from module import Class` style, organize by standard library → third-party → local
- **Type Hints**: All functions should have input and return type annotations (use `|` for unions, not `Union`)
- **docstrings**: Use triple-quote docstrings for all classes and public methods with description + Args/Returns format
- **Class Names**: PascalCase (e.g., `GameUI`), exception classes end in `Error` or `Exception`
- **File organization**: Core logic in `src/`, UI in `src/ui.py`, storage in `src/storage.py`

## Architecture
The game follows a clean separation of concerns with four main components:

**Core Game Engine** (`src/game.py`):
- `Card`: Low-level card representation with state management (HIDDEN, REVEALED, MATCHED)
- `Game`: Orchestrates game logic—card shuffling, matching, win detection
- Uses `CardState` enum for type-safe state transitions
- No direct UI coupling; returns data for presentation layer

**Player Management** (`src/player.py`):
- `Player`: Represents a game participant with scores, pairs found, turn tracking
- Data validation via Pydantic (name length, non-negative scores)
- Methods like `add_score()` and `reset()` for clean state management

**Persistence Layer** (`src/storage.py`):
- `GameStorage`: Handles JSON-based leaderboard and game history
- Automatic file creation if missing
- Updates leaderboard rankings after each game
- Supports per-player statistics aggregation

**User Interface** (`src/ui.py`):
- `GameUI`: Wraps Rich library for terminal rendering
- Displays board state, player info, leaderboard
- Handles all user input (IntPrompt, Prompt)
- No game logic—purely presentation
- Single responsibility: render state and capture input

**Game Controller** (`main.py`):
- `MemoryGameController`: Orchestrates game flow (menu → setup → play → save → menu)
- Manages player instances and passes them through game lifecycle
- Delegates to Game, GameUI, and GameStorage

**Data Flow**: User selects action → Controller routes to appropriate module → Module updates state → UI renders result

## Build and Test
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run the game
python main.py
```

- **Test files**: Mirror `src/` structure in `tests/` with `test_*.py` naming
- **Coverage target**: >80% for game logic (`game.py`, `player.py`, `storage.py`)
- **UI testing**: Manual (Rich library interactions difficult to mock)

## Project Conventions
- **Game difficulty**: 4, 8, 12, 16 pairs (easy to expert)
- **Scoring**: +10 points per matched pair in your turn
- **Turn switching**: After failed match, turn goes to next player (circular)
- **Card reveal sequence**: Pick 1st → display → pick 2nd → display → check match → hide or mark matched
- **Leaderboard storage**: JSON in `data/leaderboard.json` with game history and per-player aggregates
- **Theme support**: Pre-defined emoji sets (animals, fruits, emojis); easy to add more via `Game.THEMES` dict

## Integration Points
- **Rich library**: All console output/input uses Rich (Panel, Table, Prompt, IntPrompt)
- **Pydantic**: Player validation and data serialization
- **JSON storage**: Flat file in `data/` directory; no database required
- **No external APIs**: Fully self-contained, works offline

## Security
- **Input validation**: Player names length-checked by Pydantic range, positions validated against board size
- **File handling**: Uses `pathlib.Path` with safe parent creation, no shell injection vectors
- **No sensitive data**: Game scores/names only; no authentication or secrets
