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
