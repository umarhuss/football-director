## Session 1 — 14/05/2026

### What I did:
Set up the initial project structure with a hybrid
Rust/Python architecture.

### Key decisions made and why:
- Rust for data processing engine — performance and learning
- Python for ML and dashboard — ecosystem and industry standard
- REST API as communication layer — clean separation of concerns
- uv over pip — modern standard, faster, reproducible
- Separate rust-engine and python-brain folders — two teams, two rooms

### Concepts I learned:
- cargo init vs cargo new
- uv init for Python project setup
- .gitignore and what to exclude and why
- Conventional commits — feat/fix/chore/docs
- mkdir -p for nested folders

### How I'd explain this to someone:
I created a separate file structures for my python brain and rust engine this allows there to be separation of concerns and
coding languages making it cleaner to develop. I utilised the uv python package manager as it allows me to have replace pip,virtual environments etc
with one tool making it more efficient, cleaner and modern. I also incorporated the equivalent package in rust which is cargo.



## Session 2 — 15/05/2026

### What I did:
Cloned Statsbomb data from github and saved it in raw data file.
Explored the data using notebook.
Made decisions about the direction of the project based on the data.

### Key decisions made and why:
- Focus on creating player vectors as data is not as extensive as i had hoped but i can still get good insights.
- I will have to scrape further data in V2 of the project to get certain information.
- Decided to use La liga and UCL data as this has a good length of continuous data and the worlds best players were in these leagues at the time.

### Concepts I learned:
- Path and file navigation
- Data exploration and extraction

### How I'd explain this to someone:
I created a notebook in order to explore the data. I navigated the paths to and accessed
the data to assess the data quality. Once I did this it was clear to see that i would need to do more in V2 to get the project to where i wanted
it in the end. I accessed the UCL and la liga data that i think will be the cornerstone of the the player vectors and plan to chose an initial
season to start with.

### What I'm still unsure about:
- Which season to start with for building
  the first player vectors

## Session 3 — 21/05/2026

### What I did:
Explored the UCL 2019 final event data in detail.
Identified all event types available in the data.
Built pass metrics extractor to get per player pass statistics.

### Key decisions made and why:
- Used a hash map (dictionary) for player metrics — O(1) lookup vs O(n) nested loop
- Used a set for incomplete pass outcomes — O(1) lookup vs O(n) list search
- Separated successful pass check into a helper function — single responsibility
- Decided to process all event types atomically rather than one at a time

### Concepts I learned:
- Hash map pattern for efficient player lookups
- Running average calculation without storing all values
- O(1) vs O(n) tradeoffs — time vs space complexity
- Idempotency — processing a match twice shouldn't corrupt data
- Atomic operations — all metrics save or nothing saves

### How I'd explain this to someone:
I loaded the UCL 2019 final events which contained 3165 individual actions. I filtered these by event type and built a per player pass metrics dictionary. For each player I tracked total passes, successful passes, average pass length and average pass angle. I used a running average calculation so I didn't need to store every individual pass value. The result was 890 total passes across 28 players which matched my earlier sanity check.

### What I'm still unsure about:
- How to handle edge cases in other event types
- Whether the running average calculation handles all scenarios correctly

---

## Session 4 — 5/06/2026

### What I did:
Refactored the pass metrics extractor into a proper Python package.
Created the module structure under src/football_director/extractors/.
Tested the module imports correctly and returns the same results.

### Key decisions made and why:
- Moved code from notebook into src/ — notebooks are for exploration only, src/ is for production code
- Created helper.py for successful_pass_check — single responsibility, reusable across extractors
- Used relative imports with . — correct way for modules to import from the same package
- Created __init__.py in each folder — required for Python to recognise them as packages

### Concepts I learned:
- Python package structure — src/package/module layout
- Relative imports — from .helper import function
- __init__.py — makes a folder a Python package
- sys.path — telling Python where to find your modules in notebooks
- Single responsibility principle — each function does one thing only

### How I'd explain this to someone:
I took the working pass extractor code from the notebook and turned it into a proper importable Python module. This involved creating the correct folder structure with __init__.py files, fixing imports to use relative paths, and testing that the function returns identical results when imported. This is the transition from exploration code to production code.

### What I'm still unsure about:
- How sys.path will be handled when we move to the full pipeline
- Whether the module structure is correct for when uv manages dependencies


## Session 6 — 03/07/2026

### What I did:
Built three player metric extractors — passes, carries and shots.
Refactored pass extractor to use shared helper functions.
Created helper.py with reusable functions across all extractors.
Tested each extractor with sanity checks against known match results.

### Key decisions made and why:
- Separation of concerns — each extractor handles one event type only
- Helper functions for shared logic — DRY principle, calculate_distance reused across carries and shots
- Defensive .get() on all data access — data pipelines must handle missing fields gracefully
- Functions over classes — extractors are pure transformations, no state needed
- Failed files table alongside processed files table — if a file fails processing log it separately
- PostgreSQL with pgvector confirmed — not Qdrant, one database for both relational and vector data
- Python extractors are reference implementation — Rust will reimplement same logic for production

### Concepts I learned:
- Defensive .get() — use when a field might be missing to avoid crashes
- Reference semantics in Python — modifying a dictionary through a variable changes the original, no need to reassign
- Running average formula — calculate without storing all values
- Sanity checks — verify output against known facts (Liverpool won 2-0, total goals must be 2)
- Pythagoras theorem applied to pitch coordinates — calculate_distance helper
- Progressive carries — end_x minus start_x >= 10 means the ball moved significantly forward
- StatsBomb pitch dimensions — 120 x 80, normalised across all grounds regardless of actual size
- When to use class vs function — class when state persists across calls, function when transforming input to output

### How I'd explain this to someone:
I built individual extractor functions for passes, carries and shots. Each takes a list of match events and returns a dictionary of per player metrics. I used a hash map pattern for O(1) player lookups and a running average formula so I never need to store all individual values. I extracted the shared maths into helper functions so the same distance calculation works for both carries and shots. I verified each extractor by checking the output against known facts — the UCL 2019 final finished 2-0 to Liverpool so my shot extractor must return exactly 2 goals.

### Architecture decisions locked in:
- PostgreSQL with pgvector — one database for relational data and vector similarity search
- Atomic processing — all extractors run on a match or none commit to the database
- Idempotency — processed_matches table prevents double processing
- Failed files table — log failures separately for debugging
- Python extractors are reference implementation for future Rust rewrite

### What I'm still unsure about:
- When to use helper functions vs a class — understood conceptually but need more practice
- How sys.path will be handled when the full pipeline is built
- Best way to structure the remaining extractors efficiently


## Session 7 — 23/07/2026

### What I did:
Completed all 13 player metric extractors for the football director project.
Used the UCL 2019 final as the initial exploration base and cross referenced
with La Liga 2020/2021 across 35 matches to ensure robustness of field names
and metric definitions.
Created a comprehensive helper.py with reusable functions across all extractors.
Tested each extractor in notebook 2 with sanity checks against known results.
Merged feat/player-metrics-extractors branch into main.

### Key decisions made and why:
- Cross referenced multiple competitions before building — one match is not
  enough to confirm all possible field values
- Helper functions for shared logic — DRY principle, reusable across all 13 extractors
- Defensive .get() throughout — external data is never guaranteed to have every field
- Separate extractors per event type — single responsibility principle
- Temporary dictionary ledger for V1 — database comes in V2
- JSON files for processed/failed match ledger in V1 — simple, effective,
  no database overhead yet

### Concepts I learned:
- Importance of exploring data across multiple matches not just one
- Order of operations — update counts before calculating percentages
- Reference semantics — modifying dictionary through variable changes original
- Atomic thinking — all extractors succeed or nothing saves
- Idempotency — processed matches ledger prevents double processing
- Failed files logging — separate ledger for failed extractions

### How I'd explain this to someone:
I built 13 individual extractor functions each responsible for one event type.
For each I first explored the data shape in a notebook to understand all possible
fields, then built the extractor using a hash map pattern for O(1) player lookups
and running averages to avoid storing all raw values. I cross referenced field names
across multiple competitions to ensure robustness. Each extractor returns a dictionary
of per player metrics which will be combined in the pipeline into a full player profile.

### What I'm still unsure about:
- Exact timing of when to introduce PostgreSQL for the pipeline
- How to handle players who appear across multiple seasons —
  same player ID but potentially different teams
- Best way to combine metrics from all 13 extractors into one player vector

## Session 8 — 24/07/2026

### What I did:
Built the player profile pipeline function that orchestrates all 13 extractors.
Fixed defensive .get() issues across multiple extractors discovered during pipeline testing.
Standardised player_id and player_name keys across all extractors.
Successfully processed 9037 player profiles across all competitions and seasons in the dataset.

### Key decisions made and why:
- Pipeline takes Path objects as parameters — clean, reusable, not hardcoded
- Try/except block around all extractors — if any fail the match is skipped entirely
- Nested loop structure for now — competitions → seasons → matches → events
- Will flatten into separate functions in V2 for cleaner code
- Deferred idempotency ledger to V2 — JSON ledger for processed/failed files not yet implemented
- Parquet storage next — V1 persistence layer before PostgreSQL in V2

### Concepts I learned:
- Running a pipeline across an entire dataset surfaces bugs that single match testing misses
- Defensive .get() is essential for any data pipeline — never assume fields exist
- Consistent naming conventions across modules matter — player name vs player_name breaks downstream code
- Stale kernel causes — always restart after changing module code
- Relative imports with .. to navigate up package levels

### How I'd explain this to someone:
I built a pipeline function that walks through every competition, season and match in the StatsBomb dataset. For each match it loads the events file and passes it through all 13 extractors. If any extractor fails the match is skipped and logged. The results from all extractors are merged into a single dictionary per player using their player ID as the key. Running this across the full dataset revealed two bugs — missing defensive .get() calls in carries and clearances, and inconsistent key naming across extractors. After fixing both the pipeline ran cleanly producing 9037 complete player profiles.

### What I'm still unsure about:
- Best way to implement the processed/failed match ledger in V1
- How to handle players who appear across multiple seasons — currently metrics accumulate which may skew averages
- Whether 9037 is the right number or if some players are being missed

### Additional — Parquet storage:
Converted 9037 player profiles to a Polars DataFrame and saved to
data/processed/player_profiles.parquet. Used fill_null(0) to handle
missing metrics for players who didn't appear in certain event types.
Result: 9037 rows, 87 columns, ready for PCA.


## Session 9 — 25/07/2026

### What I did:
Implemented PCA and cosine similarity engine on 9037 player profiles.
Standardised 83 numeric metrics using StandardScaler before running PCA.
Reduced 83 dimensions to 53 components explaining 95% of variance.
Built player similarity search function using cosine similarity.
Saved player vectors to data/processed/player_vectors.parquet.

### Key decisions made and why:
- StandardScaler before PCA — without it PCA would be dominated by metrics
  with larger numerical ranges regardless of actual importance
- 95% variance threshold — industry standard, captures signal while removing noise
- 53 components — higher than expected, reflects genuine complexity of player data
  across 83 diverse metrics
- Cosine similarity over euclidean distance — measures style angle not volume,
  so number of games played doesn't inflate similarity scores

### Concepts I learned:
- PCA doesn't remove original metrics — it creates new components that are
  weighted combinations of all original metrics
- Each component captures a direction of maximum variance in the data
- Eigenvalues tell you how much variance each component explains
- Cosine similarity measures angle between vectors not distance
- numpy argmax on cumulative variance to find optimal number of components
- reshape(1, -1) to convert a 1D vector to 2D for sklearn compatibility

### How I'd explain this to someone:
I standardised all 83 player metrics to the same scale so PCA could fairly
compare them. PCA then found 53 underlying patterns in the data that together
explain 95% of the variation between players. Each player now has a vector of
53 numbers representing their playing style. To find similar players I use
cosine similarity which measures the angle between two vectors — meaning Messi
and Arjen Robben have similar angles because their overall action profiles are
similar, not just one specific attribute.

### What I'm still unsure about:
- Whether to filter by position before running similarity search
- How to handle women's players appearing in results for men's player searches
- Whether 53 components is too many or if 90% threshold would be better


## Session 10 — 30/07/2026

### What I did:
Built the V1 Streamlit dashboard with player search, profile display
and similarity engine.
Implemented selectbox search across 9037 players.
Built player profile card with passing, carrying, shooting and
defending metrics.
Built similar players section showing top 10 most similar players
using cosine similarity with cards in a 5x2 grid layout.

### Key decisions made and why:
- st.selectbox over st.text_input — built in filtering, simpler implementation
- st.cache_data for data loading — prevents reloading on every page refresh
- st.metric for stats display — clean card format built into Streamlit
- st.columns for layout — organises metrics into readable sections
- Calculated pass_completion_pct and shot_accuracy_pct on the fly
  in the dashboard — no need to change extractors

### Concepts I learned:
- Streamlit runs top to bottom and reruns on every interaction
- st.cache_data prevents expensive operations running on every rerun
- columns and containers for layout
- unsafe_allow_html for custom CSS — unreliable in Streamlit
- cosine_similarity needs 2D input hence reshape(1, -1)

### How I'd explain this to someone:
I built a Streamlit dashboard that loads player profiles and vectors
from Parquet files. When a player is selected the app filters their
row from the profiles DataFrame and displays key metrics. It then
finds their vector in the player vectors DataFrame, runs cosine
similarity against all 9037 players and displays the top 10 most
similar players in a card grid.

### What I'm still unsure about:
- How to handle players known by different names e.g. Pelé
- Whether to normalise stats per 90 minutes — decided to leave for V2
  as minutes played data not readily available
- CSS styling limitations in Streamlit

### Improvements identified for next session:
- Add radar chart with Plotly for visual player profile comparison
- Add position and club to player cards and similar player cards
- Consider per 90 normalisation in V2 with better data sources

## Session 11 — 07/07/2026

### What I did:
Deployed the Football Director app to AWS EC2.
Set up an Elastic IP for a permanent URL.
Configured systemd to keep the app running automatically.
App is now live at http://13.42.78.189:8501

### Key decisions made and why:
- Ubuntu over Amazon Linux — skills transfer to any cloud provider
- t3.micro — enough power for a Streamlit app, free tier eligible
- Elastic IP — so the URL stays the same when instance stops/starts
- systemd service — so I don't have to manually restart the app

### Concepts I learned:
- EC2 — renting a virtual computer from Amazon
- AMI — the operating system you install on it
- Instance types — hardware specs, chose based on what the app needs
- Key pairs — SSH authentication, more secure than passwords
- Security groups — firewall, nothing open by default, I opened ports 22, 80 and 8501
- Elastic IP — permanent IP address
- systemd — Linux service manager, keeps app running permanently

### How I'd explain this to someone:
I deployed my Streamlit app to an AWS EC2 instance running Ubuntu.
I configured the security group to open the ports my app needs,
connected via SSH using a key pair, cloned my repo onto the server,
transferred the Parquet data files, and set up a systemd service
so the app runs automatically and restarts if it ever crashes.

### What I'm still unsure about:
- Doing this from scratch without guidance — need to do it again
- Terminal commands becoming natural with more practice
- More advanced AWS for V2 — RDS, ECS, Docker
