# Football Director

A data-driven football player scouting and similarity engine.
Built out of a genuine love for football and a desire to apply
concepts from my masters degree to a real project.

## What it does

Football Director helps identify players with similar playing styles
to any player in the database. Search for a player, see their
statistical profile across passing, carrying, shooting and defending,
and find the top 10 most similar players globally ranked by similarity score.

The idea came from wanting to build a tool that could answer questions like:
- Who plays like Rodri but is under 23?
- What type of player does this team need based on their gaps?
- Which players from smaller leagues have profiles matching elite players?

## How it works

- **13 custom metric extractors** process StatsBomb event data — every pass,
  carry, shot, press, tackle and more across 9037 players
- **PCA** reduces 83 metrics to 53 components capturing 95% of variance
- **Cosine similarity** finds players with the closest playing style vectors
- **Streamlit dashboard** for search, player profiles and radar charts

## Data

Uses StatsBomb open data — event level data from multiple competitions
and seasons including the UCL and La Liga featuring some of the greatest
players of the last 20 years.

*StatsBomb data used under their open data licence.*

## Live Demo (V1 — Early Prototype)

**http://13.42.78.189:8501**

Note: V1 is a proof of concept. Data is limited to StatsBomb open data
which covers select competitions and seasons. V2 will incorporate
current player data via scraping and a Rust data processing engine.

## Run locally

```bash
git clone https://github.com/umarhuss/football-director.git
cd football-director/python-brain
uv sync
uv run streamlit run src/football_director/dashboard/app.py
```

## Stack

- **Python** — data pipeline, feature engineering, ML
- **Polars** — fast data processing
- **scikit-learn** — PCA and cosine similarity
- **Streamlit** — dashboard
- **AWS EC2** — deployment
- **StatsBomb** — event data

## Roadmap

**V2 (in progress)**
- Rust data processing engine
- PostgreSQL with pgvector
- FBref scraping for current players
- Docker containerisation
- GitHub Actions CI/CD

**V3**
- TypeScript frontend
- Heat maps with deck.gl
- Full AWS infrastructure
