## Session 1 — [DATE]

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
