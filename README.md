# python-ai-automation-suite

A small, production-style Python automation demo: input → workflow → output, with logging, retries, and clean configuration.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.app.main
cat output/report.json
```

## Tests
```bash
pytest -q
```
