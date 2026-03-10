# Claw Buddy Architecture 🦞

Built using the 5-phase agent architecture.

## Phase 1: Data Transport

**What:** CLI input parsing and HTTP client for Ollama

**Files:**
- `src/data/__init__.py`

**Responsibilities:**
- Parse CLI arguments
- Validate input
- HTTP calls to Ollama API

## Phase 2: Storage & Memory

**What:** SQLite database for pet state and conversation history

**Files:**
- `src/storage/__init__.py`

**Responsibilities:**
- Persist pet data
- Store conversations
- Log events
- Load/save state

## Phase 3: Logic & State

**What:** State machine for pet behavior

**Files:**
- `src/logic/__init__.py`

**Responsibilities:**
- Pet state management
- Action handlers
- Mood calculation
- Stat updates

## Phase 4: Model Layer

**What:** LLM integration for personality and chat

**Files:**
- `src/model/__init__.py`

**Responsibilities:**
- Ollama API calls
- Personality prompts
- Fallback responses when LLM unavailable

## Phase 5: Reliability

**What:** Validation, logging, error handling

**Files:**
- `src/reliability/__init__.py`

**Responsibilities:**
- Input validation
- Structured logging
- Error handling
- Health checks
- Graceful degradation

## Data Flow

```
User Input → CLI Parser → Action Handler → State Machine → Storage
                                    ↓
                              LLM (if chat)
                                    ↓
                              Response → User
```

## Key Design Decisions

1. **SQLite over file** — Structured queries, better than JSON files
2. **Fallback responses** — Works even without Ollama
3. **State machine** — Predictable behavior vs random
4. **Modular phases** — Each layer is independent
