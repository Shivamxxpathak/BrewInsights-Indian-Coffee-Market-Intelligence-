# BrewInsights Dashboard

The Streamlit dashboard presents saved survey KPIs, consumer segments, demand analysis, forecasts, city opportunity analysis, market-entry outputs and partnership-experiment preparation.

## Run

```bash
pip install -r requirements.txt
pip install -r dashboard/requirements_dashboard.txt
streamlit run dashboard/app.py
```

On Windows, use `dashboard/START_DASHBOARD.cmd` or `dashboard/run_dashboard.bat`.

Do not execute `dashboard/app.py` with Python directly; launch it through Streamlit.

The dashboard reads saved datasets from `data/` and `outputs/datasets/`.
