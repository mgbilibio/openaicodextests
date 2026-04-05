# CLAUDE.md

This file provides guidance for AI assistants (Claude Code and similar tools) working in this repository.

## Repository Overview

**Name:** openaicodextests  
**Remote:** mgbilibio/openaicodextests  
**Stack:** Python · PySide6  
**Purpose:** Testing and experimentation with AI coding tools (OpenAI Codex, Claude Code, etc.).

## Repository Structure

```
openaicodextests/
├── CLAUDE.md                   # AI assistant guidance (this file)
├── requirements.txt            # Python dependencies
├── main.py                     # Application entry point (thin launcher only)
├── docs/
│   ├── codeinstructions.html   # Developer/AI documentation (always kept current)
│   ├── usersmanual.html        # End-user operation manual (always kept current)
│   └── versions.html           # Full change history with user requests + explanations
├── app/                        # All application source code
│   ├── __init__.py
│   ├── core/                   # Business logic, data access, utilities
│   │   └── paths.py            # BASE_DIR, DATA_DIR, and subfolder constants
│   ├── ui/                     # PySide6 panels and main window
│   │   ├── main_window.py      # QMainWindow, dock setup, layout save/restore
│   │   └── panels/             # One file per QDockWidget panel
│   └── manager.py              # Top-level coordinator / app entry point logic
└── data/                       # Runtime subfolder (auto-created, git-ignored)
    ├── config/                 # Saved dock/panel layouts and app settings (JSON)
    ├── db/                     # SQLite or other local databases
    ├── tmp/                    # Temporary / working files
    └── results/                # Output and export files
```

> **Root is kept lean.** Only `main.py`, `requirements.txt`, and `CLAUDE.md` live
> at the root. Everything else goes inside `app/`, `docs/`, or `data/`.
>
> All accessory files (config, databases, temp, results) live inside `data/`
> adjacent to `main.py`. The app creates this structure on first run.

## Development Workflow

### Branch Strategy

- **Feature branches:** `claude/<description>` or `feature/<description>`
- **Default development branch:** `main`
- Never commit directly to `main`.

### Git Conventions

- Imperative mood: `Add feature X`, `Fix bug Y`, `Update docs`
- One logical change per commit
- Push with tracking: `git push -u origin <branch-name>`

### Setting Up

```bash
git clone https://github.com/mgbilibio/openaicodextests.git
cd openaicodextests
pip install -r requirements.txt
python main.py
```

### Linting / Formatting

```bash
ruff check .        # linting
ruff format .       # formatting (PEP 8)
```

## AI Assistant Guidelines

### General Principles

- **Read before editing.** Always read a file with the Read tool before modifying it.
- **Edit, never Write.** Use the Edit tool (targeted line replacement) instead of
  rewriting whole files. Only use Write when creating a brand-new file.
- **Minimal changes.** Only change what the task requires — no extra refactors,
  no speculative abstractions, no added error handling for impossible cases.
- **Security first.** No command injection, SQL injection, XSS, or other
  OWASP Top-10 vulnerabilities.

### File Size Limit — 150 lines per file (hard rule)

- **No source file may exceed 150 lines.** If a file would exceed this limit,
  stop, explain why more lines are needed, and ask before proceeding.
- When a module grows beyond 150 lines, split it into a package folder with a
  `manager.py` (or equivalent coordinator) that imports and exposes the parts.
- Example split: `panels/toolbar.py` → `panels/toolbar/manager.py` +
  `panels/toolbar/actions.py` + `panels/toolbar/style.py`.

### Documentation Files (mandatory — always update after changes)

Three HTML files in `docs/` must be created and kept current at all times:

| File | Purpose |
|------|---------|
| `docs/codeinstructions.html` | Developer reference: architecture, module map, class/function index, patterns used, extension guide |
| `docs/usersmanual.html` | End-user guide: how to use every panel and feature, screenshots/descriptions |
| `docs/versions.html` | Full change log: every user request verbatim + explanation + what changed + date |

- After **every** set of changes, update all three files.
- `versions.html` must record the user's original request (quoted), the
  rationale given, the files changed, and the date (ISO 8601).
- These files are committed alongside the code changes they document.

### Python Code Style (PEP 8 — mandatory)

- **Imports:** all at the top of the file, at module root level.
  No `import` inside functions, classes, or `try/except` blocks.
- **No bare `try/except` around imports.** Never use try-except to guard imports.
- **Docstrings:** every module, class, and public function/method must have a
  complete Google-style or NumPy-style docstring. Never leave them partial.
- **Inline comments:** add explanatory inline comments for every non-trivial
  block or logic step so the intent is immediately clear.
- **Type hints:** include type hints on all function signatures.
- **Line length:** 99 characters max.
- **No `messagebox` / dialog popups for logging.** All feedback goes to stdout
  via timestamped `print()`.

### Logging Convention (stdout only)

Use timestamped prints for all operational feedback — **no** GUI message boxes,
**no** modal dialogs for errors/info. Pattern:

```python
from datetime import datetime

def _log(msg: str) -> None:
    """Print a timestamped log line to stdout."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Usage
_log("START  load_data()")
_log("END    load_data() — 42 rows loaded")
_log("ERROR  load_data() — FileNotFoundError: data.csv")
```

Every significant operation must log **START**, **END**, and **ERROR** (when applicable).

### PySide6 UI Conventions

#### Dockable Panels (QDockWidget)

- **Every functional area is a `QDockWidget`** — never a fixed central widget
  (or if a central widget is needed, it should also be swappable/hidden).
- All dock widgets must be **freely movable and dockable** on any side
  (left, right, top, bottom) or floated into the centre of the window.
- Enable **tabification**: docks dropped onto each other become tabs.
- Docks are **non-modal** — the user can interact with all panels simultaneously.
- Every `QDockWidget` must show its own **minimize / maximize / close** buttons
  via a custom title bar or `DockWidgetFeatures` flags:

  ```python
  dock.setFeatures(
      QDockWidget.DockWidgetMovable
      | QDockWidget.DockWidgetFloatable
      | QDockWidget.DockWidgetClosable
  )
  ```

- The main window must call
  `setDockOptions(QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks)`
  so panels can be tabbed and freely nested.
- No dock widget may be hard-coded to a specific side at startup;
  use `addDockWidget` with a sensible default that the user can override.

#### Layout Persistence

- On close, serialize the full dock/panel layout with
  `QMainWindow.saveState()` and store it in `data/config/layout.json`
  (or via `QSettings` pointing to that directory).
- On start, restore the layout with `QMainWindow.restoreState()`.
- If no saved layout exists, apply a sensible default arrangement.

#### Style & Colours

- **Avoid blue as a primary/accent colour.** Use dark greens and dark reds as
  the main accent palette (e.g., `#2d5a27`, `#7a1c1c`, `#3b7a35`, `#a83232`).
- Each panel should have a **distinct accent colour** in its title bar to aid
  visual orientation (stylesheet applied per `QDockWidget` instance).
- Overall theme: clean, readable, visually friendly — soft/dark tones,
  never garish. White or light-grey backgrounds for content areas.

### File / Directory Helpers

Resolve the `data/` subfolder relative to the script's own location, not the
current working directory:

```python
import pathlib

# Base directory: folder that contains main.py (or the running script)
BASE_DIR = pathlib.Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

CONFIG_DIR = DATA_DIR / "config"
DB_DIR     = DATA_DIR / "db"
TMP_DIR    = DATA_DIR / "tmp"
RESULTS_DIR = DATA_DIR / "results"

# Create all subdirectories on first run
for _d in (CONFIG_DIR, DB_DIR, TMP_DIR, RESULTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)
```

### Branching

- Develop on the designated feature branch (check the session instructions).
- Never push to `main` without explicit permission.

### Commits

- Stage specific files by name — never `git add -A`.
- Never commit `.env` files, credentials, secrets, or the `data/` folder
  (add `data/` to `.gitignore`).

### Testing

- Run the test suite after changes once tests exist.
- Do not mark a task complete if tests are failing.

## Environment Variables

| Variable   | Description                | Required |
|------------|----------------------------|----------|
| *(none yet — add as the project grows)* | | |

## Key Decisions / ADRs

- **UI framework:** PySide6 (Qt for Python) — dockable, non-modal panels.
- **Colour palette:** dark greens + dark reds; no blue as primary accent.
- **File size:** hard 150-line limit per source file; split into packages when needed.
- **Documentation:** `docs/codeinstructions.html`, `docs/usersmanual.html`,
  `docs/versions.html` always updated alongside code.
- **Data locality:** all runtime artefacts under `data/` next to the app entry point.
- **Logging:** stdout-only with timestamps; no GUI message boxes.
- **Imports:** always at module root; no try-except import guards.
- **Root cleanliness:** only `main.py`, `requirements.txt`, `CLAUDE.md` at root.

## Common Pitfalls

- Forgetting to call `setDockOptions` on the `QMainWindow` — tabs won't work without it.
- Saving layout state before all dock widgets are added — always save on `closeEvent`.
- Using relative paths (`./data/`) instead of `__file__`-based paths — breaks when
  the app is launched from a different working directory.
- Letting a file grow past 150 lines without splitting — ask first if needed.
- Forgetting to update `docs/versions.html` after changes — it must record every
  user request verbatim with date and affected files.
