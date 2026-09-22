# Reproducibility and Refactored Pipeline

BrewInsights now exposes reusable analytics functions under `src/` instead of keeping all executable logic inside the notebook.

## Run the refactored pipeline

From the repository root:

```bash
python scripts/run_pipeline_refactored.py
```

The runner reads `data/processed/coffee_cleaned.csv` and `data/external_city_data.csv`, executes cleaning, segmentation, adoption modeling, spending modeling, demand trend modeling, city clustering, and market-entry scoring, then writes fresh validation artifacts to `outputs/pipeline_validation/`.

Canonical notebook outputs are not overwritten.

## Verify the notebook

```bash
python scripts/verify_notebook.py
```

This checks that the notebook is readable, contains cells, reports executed cells, and references the canonical saved artifacts.

## Tests

```bash
pytest -q
```

The test suite covers cleaning, segmentation, adoption-target construction, spending regression, demand forecasting, and city/market-entry scoring.

## Analytical integrity

The refactor is intentionally non-destructive. Existing benchmark outputs and the original notebook remain the project record; the new modules provide reusable, testable implementations and a separate reproducibility path for future iterations.
