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
- I will have to scrape further dat in V2 of the project to get certain information.
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
