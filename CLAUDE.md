# CLAUDE.md

This file provides guidance for AI assistants (Claude Code and similar tools) working in this repository.

## Repository Overview

**Name:** openaicodextests  
**Remote:** mgbilibio/openaicodextests  
**Status:** Newly initialized — no source files exist yet.  
**Purpose:** Testing and experimentation with AI coding tools (OpenAI Codex, Claude Code, etc.).

> When the project grows, update this file to reflect the actual tech stack, structure, and conventions.

## Repository Structure

```
openaicodextests/
└── CLAUDE.md          # This file
```

As files are added, document the structure here. For example:

```
openaicodextests/
├── CLAUDE.md
├── README.md
├── src/               # Source code
├── tests/             # Test files
├── package.json       # (or requirements.txt, Cargo.toml, etc.)
└── .env.example       # Environment variable template
```

## Development Workflow

### Branch Strategy

- **Feature branches:** `claude/<description>` or `feature/<description>`
- **Default development branch:** `main` (or `master`)
- Always develop on a dedicated branch; never commit directly to `main`.

### Git Conventions

- Write commit messages in the imperative mood: `Add feature X`, `Fix bug Y`, `Update docs`
- Keep commits focused and atomic — one logical change per commit
- Push with tracking: `git push -u origin <branch-name>`

### Setting Up (once source files exist)

```bash
# Clone the repo
git clone https://github.com/mgbilibio/openaicodextests.git
cd openaicodextests

# Install dependencies (update command once stack is known)
# npm install          # Node.js
# pip install -r requirements.txt  # Python
# cargo build          # Rust

# Copy environment variables
cp .env.example .env
```

### Running Tests (update once test framework is chosen)

```bash
# Examples — replace with actual commands
npm test              # Node.js / Jest / Vitest
pytest                # Python
cargo test            # Rust
```

### Linting / Formatting

```bash
# Examples — replace with actual commands
npm run lint          # ESLint
npm run format        # Prettier
ruff check .          # Python (ruff)
cargo fmt             # Rust
```

## AI Assistant Guidelines

### General Principles

- **Read before editing.** Always read a file before modifying it.
- **Minimal changes.** Only change what is required to complete the task.
- **No speculative additions.** Don't add features, abstractions, or error handling beyond what is asked.
- **No unnecessary files.** Don't create documentation, README files, or helpers unless explicitly requested.
- **Security first.** Never introduce command injection, XSS, SQL injection, or other OWASP top-10 vulnerabilities.

### Branching

- Develop on the designated feature branch (check the session instructions).
- Never push to `main` or `master` without explicit permission.

### Commits

- Commit with clear, descriptive messages.
- Stage specific files rather than `git add -A` to avoid accidentally including secrets or large binaries.
- Never commit `.env` files, credentials, or secrets.

### Testing

- Run the test suite after making changes (once tests exist).
- Do not mark a task complete if tests are failing.

### Code Style

Once a language and framework are chosen, document conventions here. For example:
- TypeScript: strict mode, ESLint + Prettier
- Python: ruff + black, type hints required
- Rust: `cargo fmt` + `cargo clippy`

## Environment Variables

Document required environment variables here once they are known. Example:

| Variable        | Description                  | Required |
|-----------------|------------------------------|----------|
| `API_KEY`       | External service API key     | Yes      |
| `DATABASE_URL`  | Database connection string   | Yes      |
| `DEBUG`         | Enable debug logging         | No       |

Copy `.env.example` to `.env` and fill in values before running the project.

## Key Decisions / ADRs

Document significant architectural decisions here as the project evolves.

- *(none yet — project is in initial setup)*

## Common Pitfalls

- *(none yet — add gotchas here as they are discovered)*
