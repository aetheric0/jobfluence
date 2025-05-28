# JOBFLUENCE

## Setup
- Clone the repo and navigate into `jobfluence/`
- Copy `.env.local` to `.env` and fill in your keys
- Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
- Install dependencies: 
    ```bash
    pip install -r requirements
    ```
- Run the app locally:
    ```bash
    uvicorn app.main:app --reload
    ```

