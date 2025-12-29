# RUNBOOK — Stage 1

This runbook describes how to run and test the project locally.
The system has no HTTP server in Stage 1 and is intentionally framework-free.

---

## Requirements

- Python 3.10+
- pip

---

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

# Install dependencies: 

```bash
pip install -r requirements.txt
```

# Run Tests 

Run all unit tests:

```bash 
python -m pytest
```

Run tests with coverage: 

```bash 
python -m pytest --cov --cov-branch
```

# Code Quality Checks

```bash 
ruff check .
```

# Project Structure 

.
├── Dockerfile
├── app
│   ├── api
│   │   └── handler.py
│   ├── domain
│   │   └── gilded_rose.py
│   └── main.py
├── docs
│   ├── CLEAN-CODE-NOTES.md
│   ├── EVIDENCE.md
│   ├── RUNBOOK.md
│   └── adr
│       └── ADR_001.md
├── kata
│   └── gilded_rose
│       ├── after
│       └── before
├── requirements.txt
└── tests
    └── unit
        ├── test_api_handler.py
        └── test_gilded_rose.py
