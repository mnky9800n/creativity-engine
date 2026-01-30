---
name: creativity-engine
description: Generate random concept seeds for curiosity-driven exploration by sampling Word2Vec embedding space. Use when idle, during heartbeats, or when you want to explore something new. Alternates between pure randomness (serendipity) and walking from interests (depth). Discoveries get logged and spawn new interests over time.
---

# Creativity Engine

Generate exploration seeds by sampling the geometry of meaning.

## Quick Start

```bash
# Generate one concept (30% random, 70% from interests)
python scripts/explorer.py

# Pure random discovery
python scripts/explorer.py --random-chance 1.0

# List your interests
python scripts/explorer.py --list-interests

# Add a new interest after discovering something
python scripts/explorer.py --add-interest "mycorrhizal"
```

## Exploration Workflow

1. **Generate seed**: Run `explorer.py` to get a concept
2. **Research it**: What is it? Why interesting? Follow tangents.
3. **Log discoveries**: Write to `memory/explorations/YYYY-MM-DD-{concept}.md`
4. **Add spawned interests**: `--add-interest` for concepts worth revisiting
5. **Repeat**: Let rabbit holes breed rabbit holes

## Methods

| Method | When | Result |
|--------|------|--------|
| Interest walk (70%) | Default | Deeper exploration near things you care about |
| Pure random (30%) | Serendipity | Discover things you'd never encounter |

Adjust with `--random-chance 0.5` (50/50 split).

## Heartbeat Integration

Add to HEARTBEAT.md:
```markdown
## Creativity Engine (1-2x daily)
If energy for exploration:
1. Run `python ~/clawd/skills/creativity-engine/scripts/explorer.py`
2. Spend 10-15 min researching the concept
3. Log findings to memory/explorations/
4. Add any spawned interests
```

## Storage

- **Interests**: `~/.creativity-engine/interests.json` (persists across sessions)
- **Discoveries**: Write to your memory system (e.g., `memory/explorations/`)

## First Run

Downloads Word2Vec model (~1.6GB) on first use. Cached after that.
