# Claw Buddy

Terminal-based virtual pet with persistence, personality, and local LLM-powered interaction.

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Built with OpenClaw](https://img.shields.io/badge/Built%20with-OpenClaw-blue)](#)

## Live Demo

- Repository: `https://github.com/tylerdotai/claw-buddy`
- Architecture doc: `docs/ARCHITECTURE.md`

## About

Claw Buddy is a CLI-native virtual pet designed to feel more alive than a simple stat tracker. It combines persistence, mood and need management, ASCII interaction, and optional local LLM chat to create a pet that lives in your terminal and remembers your history over time.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python |
| Storage | SQLite |
| LLM | Ollama |
| Validation / Reliability | Logging and structured checks |
| Interface | Terminal CLI |

## Features

### Pet Experience
- Adopt multiple pet types with names and persistent state
- Feed, play, sleep, walk, and inspect status
- ASCII-driven CLI interaction
- Mood, needs, tricks, and achievements

### System Design
- Five-phase architecture split across `src/`
- SQLite-backed persistence
- Health checks and reliability helpers
- Optional LLM-powered chat

## Project Structure

```text
src/main.py               CLI entrypoint
src/data/                 Input and external transport layer
src/storage/              Persistence and memory
src/logic/                State and action handling
src/model/                LLM interaction layer
src/reliability/          Health checks and error handling
docs/ARCHITECTURE.md      Architecture breakdown
requirements.txt          Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.11+
- `pip`
- Ollama if you want local LLM chat

### Installation

```bash
git clone https://github.com/tylerdotai/claw-buddy.git
cd claw-buddy
pip install -r requirements.txt
```

## Deployment

Claw Buddy is designed for local terminal use rather than hosted deployment.

- Repository: `https://github.com/tylerdotai/claw-buddy`

## Usage

```bash
python -m src.main adopt cat Buddy
python -m src.main status
python -m src.main chat "Hello!"
```

## Current Limitations

- The dependency list is still very minimal relative to the broader architecture
- LLM chat depends on a local Ollama setup
- The project ships as a local CLI rather than a packaged installable application

## Roadmap

- Package the CLI more formally for installation and updates
- Expand pet behaviors and personality depth
- Improve local model integration and fallback behavior
- Continue refining the layered architecture documentation

## License

MIT - see `LICENSE` for details.
