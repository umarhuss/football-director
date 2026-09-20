# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All Python commands run from `python-brain/` using `uv`:

```bash
# Install dependencies
cd python-brain && uv sync

# Run the Streamlit dashboard
cd python-brain && uv run streamlit run src/football_director/dashboard/app.py

# Run the data pipeline (reprocesses StatsBomb JSON → Parquet)
cd python-brain && uv run python src/football_director/pipeline/process_matches.py

# Launch Jupyter for notebook exploration
cd python-brain && uv run jupyter lab

# Rust engine (fd_engine/) — currently scaffolded, no build steps yet
cd fd_engine && cargo build

# Run the tests to ensure the code works correctly
cd fd_engine && cargo test

# Run clippy to check if my code is idiomatic (is this good rust)
cd fd_engine && cargo clippy
```

Tests and clippy are available; no test suite written yet.

## Architecture

**Data flow:**
1. Raw StatsBomb JSON events in `data/raw/statsbomb/` (gitignored)
2. Pipeline (`pipeline/process_matches.py`) orchestrates 13 extractors → `data/processed/player_profiles.parquet` (83 metrics, ~9k players)
3. PCA reduces 83 metrics → 53 components → `data/processed/player_vectors.parquet`
4. Dashboard loads both Parquet files at startup; cosine similarity drives player search

**Extractors** (`src/football_director/extractors/`): one file per event type (passes, carries, shots, pressures, interceptions, clearances, blocks, ball_recovery, duels, fouls_won, fouls_committed, miscontrols, dispossessed). Each returns a Polars DataFrame. `helper.py` holds shared utilities. The pipeline calls every extractor and joins results on `player_id`.

**Dashboard** (`src/football_director/dashboard/app.py`): single-file Streamlit app. Loads `player_profiles.parquet` and `player_vectors.parquet`, runs PCA/cosine similarity in-memory with scikit-learn, renders radar charts via Plotly.

**Rust engine** (`fd_engine/`): in-progress migration of extractors to Rust. `src/lib.rs` defines module structure mirroring the Python extractors. `schema.sql` defines the target PostgreSQL schema with pgvector (53-dimension embeddings). Rust and Python coexist by design — Rust takes ingestion, extractors, DB writes and the API; Python keeps PCA, cosine similarity and Streamlit. This split is intentional. Do not suggest porting the Python side to Rust.

## Key files

| Path | Purpose |
|------|---------|
| `python-brain/src/football_director/dashboard/app.py` | Streamlit UI — player search, profiles, similarity |
| `python-brain/src/football_director/pipeline/process_matches.py` | Pipeline orchestrator |
| `python-brain/src/football_director/extractors/` | 13 metric extractor modules |
| `fd_engine/src/lib.rs` | Rust module scaffolding |
| `fd_engine/schema.sql` | Target PostgreSQL + pgvector schema |
| `python-brain/pyproject.toml` | Python deps (Polars, Streamlit, scikit-learn, Plotly) |

## Tech notes

- **Polars** (not pandas) for all DataFrame work in Python
- **`uv`** manages the virtualenv at `python-brain/.venv/` — don't use pip directly
- Processed Parquet files are gitignored; re-run the pipeline to regenerate them
- The Rust crate uses `edition = "2024"` and is currently a library crate with no external dependencies

## How to work with me on this project

- I'm learning Rust. This is the whole point of the rebuild.
- Do NOT write Rust code for me unless I explicitly say "write this".
- When I'm stuck: explain the concept and give a hint. Never the full solution.
- I write: ownership, borrowing, traits, async, all core logic.
- You may draft: Cargo config, Docker, CI, test scaffolding — but explain it so I can defend every line.
- When reviewing my code, ask questions ("is this idiomatic? what would you change?") rather than rewriting it.
- Point me to the relevant Rust book chapter when a new concept comes up.
