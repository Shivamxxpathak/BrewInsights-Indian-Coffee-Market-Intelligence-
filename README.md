# Indian Coffee Market Dashboard

This dashboard is the presentation layer for the coffee market project.

## Design
The UI follows the supplied Earthy Minimal reference:
- Primary: #2E3A2F
- Secondary: #6B7F5B
- Tertiary: #D9C9B2
- Accent: #C96F4F
- Background: #F8F6EE

## Sections
- Overview
- Consumer Analytics
- Customer Segments
- Brand Adoption
- Spending Prediction
- City Intelligence
- Demand Forecast
- 3 Corações Partnership Test
- Data Explorer
- Methodology

The original project notebook is kept unchanged. This dashboard reads the existing cleaned data and saved project outputs.

## Run

From the project root:

```powershell
& "C:\Users\Aman\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install -r requirements_dashboard.txt
& "C:\Users\Aman\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run dashboard\app.py
```

If Python is available normally, this also works:

```powershell
python -m streamlit run dashboard\app.py
```

Then open the Local URL shown by Streamlit, normally http://localhost:8501.
