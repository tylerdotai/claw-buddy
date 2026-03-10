# Claw Buddy 🦞

> A terminal-based virtual pet with LLM-powered personality.

Built with ❤️ using OpenClaw. Part of the Hal Stack 🦞

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![OpenClaw](https://img.shields.io/badge/Built%20with-OpenClaw-blue)
![Hal Stack](https://img.shields.io/badge/Part%20of-Hal%20Stack%20🦞-red)

## The Problem

Virtual pets are either:
- Too simple (stat bars go up/down)
- No persistence (lose progress)
- No real personality (scripted responses)

## Our Solution

Claw Buddy is:**

- **Part of the Hal Stack** 🦞 — Built with OpenClaw
- **Your CLI companion** — Lives in your terminal
- **Never forgets** — SQLite persistence
- **Actually smart** — LLM-powered personality
- **Alive** — Moods, needs, evolution

## Architecture

Built using the 5-phase agent hierarchy:

```
├── src/
│   ├── data/        # Phase 1: Data Transport (CLI, HTTP)
│   ├── storage/     # Phase 2: Storage & Memory (SQLite)
│   ├── logic/       # Phase 3: Logic & State (State machine)
│   ├── model/       # Phase 4: Model Layer (LLM prompts)
│   └── reliability/ # Phase 5: Reliability (Validation, logging)
├── tests/
└── config/
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed breakdown.

## Quick Start

```bash
git clone https://github.com/tylerdotai/claw-buddy.git
cd claw-buddy

# Install
pip install -r requirements.txt

# Run
python -m src.main adopt cat Buddy
python -m src.main status
python -m src.main chat "Hello!"
```

## Features

- [x] Adopt pets (Cat, Dog, Hamster, Fox)
- [x] Stats system (Happiness, Hunger, Energy, Health)
- [x] ASCII art visuals
- [x] Actions: Pet, Feed, Play, Sleep, Walk
- [x] LLM-powered chat
- [x] Trick system
- [x] Achievements
- [x] Persistent storage (SQLite)
- [x] Input validation
- [x] Structured logging
- [x] Graceful error handling

## Commands

| Command | Action |
|---------|--------|
| `adopt <type> <name>` | Adopt a new pet |
| `status` | Check pet stats |
| `pet` | Pet your animal |
| `feed` | Feed your pet |
| `play` | Play with your pet |
| `sleep` | Put pet to sleep |
| `walk` | Take pet for a walk |
| `chat <message>` | Talk to your pet |
| `trick <name>` | Teach/perform trick |
| `achievements` | View badges |

## Tech Stack

| Layer | Technology |
|-------|------------|
| Data | Python, requests |
| Storage | SQLite |
| Logic | State machine |
| Model | Ollama (local LLM) |
| Reliability | Pydantic, logging |

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai) (optional, for LLM chat)

## LLM Setup

```bash
ollama pull llama3.2
```

## Reliability Features

- Input validation on all commands
- Structured logging (step, outcome, duration)
- Graceful degradation when LLM unavailable
- Retry logic for API calls
- Health check endpoint

## License

MIT
