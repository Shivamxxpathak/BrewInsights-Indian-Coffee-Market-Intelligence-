# Reproducibility & Verification

## Environment
BrewInsights targets Python 3.10+.

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dashboard and QA:

```bash
pip install -r dashboard/requirements_dashboard.txt
python -m compileall -q dashboard src scripts tests
pytest -q
```

## Automated checks
`.github/workflows/quality.yml` runs on pushes and pull requests to `main`. It installs the declared dependencies on Python 3.11, compiles the source tree, validates required files and schemas, checks public-data identifiers are absent, checks key outputs are non-empty, and performs a Streamlit dependency import smoke test.

The workflow also starts the dashboard in headless mode and verifies that it responds over HTTP before the CI run is considered successful.

## End-to-end analytical verification
The original executed notebook remains the analytical source of truth. `scripts/run_pipeline.py` intentionally does not regenerate notebook outputs; it points users to the preserved workflow. This prevents a validation run from silently replacing the executed model results.

## Dashboard verification
The dashboard is launched with `streamlit run dashboard/app.py` and uses repository-relative paths derived from `dashboard/app.py` rather than machine-specific absolute paths.

## Reproducibility note
The dependency files declare the package set rather than a machine-specific `pip freeze` snapshot. CI validates that the declared environment installs and imports successfully. For exact environment reproduction, a release-specific lockfile can be captured from the validated CI environment.
