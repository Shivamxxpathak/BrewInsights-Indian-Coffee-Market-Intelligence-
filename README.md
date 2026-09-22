<div align="center">

# ☕ BrewInsights
### Indian Coffee Market Intelligence

**Consumer Analytics • Customer Segmentation • Machine Learning • Demand Intelligence • Interactive Dashboard**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 🚀 What is BrewInsights?

BrewInsights is an end-to-end analytics project built to understand **coffee consumer behaviour in India** from survey data.

The project takes the analysis from:

**Raw Survey Data → Data Cleaning → EDA → Consumer Segmentation → Predictive Modeling → Demand Analysis → City Intelligence → Interactive Dashboard**

It combines analytical notebooks, reusable datasets, generated outputs, and a Streamlit dashboard into one portfolio-ready workflow.

---

## 🎯 Project Focus

| Area | What BrewInsights explores |
|---|---|
| ☕ Consumer Behaviour | Consumption habits, preferences and purchase behaviour |
| 💰 Spending | Coffee spending patterns and price sensitivity |
| 🧩 Segmentation | Behavioural customer groups using clustering |
| 🤖 Machine Learning | Predictive modelling and model comparison |
| 📈 Demand Intelligence | Period-level demand patterns and forecasting outputs |
| 🏙️ City Intelligence | City opportunity and market-entry analysis |
| 📊 Dashboard | Interactive presentation of analytical outputs |

---

## 🧭 Project Map

```text
                     ┌─────────────────────┐
                     │   Survey Responses  │
                     └──────────┬──────────┘
                                ↓
                    ┌───────────────────────┐
                    │ Cleaning & Preparation│
                    └──────────┬────────────┘
                               ↓
                     ┌────────────────────┐
                     │       EDA          │
                     └─────────┬──────────┘
                               ↓
               ┌───────────────┴───────────────┐
               ↓                               ↓
      ┌─────────────────┐             ┌─────────────────┐
      │  Segmentation   │             │ Predictive ML   │
      └────────┬────────┘             └────────┬────────┘
               ↓                               ↓
      ┌─────────────────┐             ┌─────────────────┐
      │ Consumer Profiles│             │ Demand Analysis │
      └────────┬────────┘             └────────┬────────┘
               └──────────────┬────────────────┘
                              ↓
                   ┌─────────────────────┐
                   │ City / Market Intel │
                   └──────────┬──────────┘
                              ↓
                   ┌─────────────────────┐
                   │ BrewInsights Dashboard│
                   └─────────────────────┘
```

---

## 📂 Repository Structure

```text
.
├── BrewInsights_Analysis.ipynb
├── app.py
├── run_dashboard.py
├── dashboard/run_dashboard.bat
├── dashboard/START_DASHBOARD.cmd
│
├── data/
│   ├── raw_survey.csv
│   ├── indian-coffee-survey.csv
│   ├── coffee_cleaned.csv
│   ├── external_city_data.csv
│   └── ...
│
├── outputs/
│   ├── consumer_cluster_assignments.csv
│   ├── consumer_cluster_profiles.csv
│   ├── city_opportunity_scores.csv
│   ├── market_entry_ranking.csv
│   ├── recommendation_sensitivity.csv
│   └── ...
│
├── assets/
│   ├── consumer_segments.png
│   └── city_market_entry_score.png
│
├── docs/
│   └── PROJECT_COMPLETION_NOTES.md
│
├── scripts/
│   └── missing_parts_added.py
│
├── requirements.txt
├── requirements_dashboard.txt
├── LICENSE
└── README.md
```

> The current GitHub branch contains the project's analysis notebook, dashboard app, datasets, analytical outputs, visual assets, documentation and launch helpers.

---

## ⚙️ Run the Analysis

### 1. Create an environment

```bash
python -m venv .venv
```

### 2. Activate it

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Open the analysis notebook

Open:

```text
notebooks/BrewInsights_Analysis.ipynb
```

---

## 🖥️ Launch the Dashboard

Install dashboard dependencies:

```bash
pip install -r dashboard/requirements_dashboard.txt
```

### Windows

Double-click:

```text
START_DASHBOARD.cmd
```

or:

```text
run_dashboard.bat
```

### Terminal

```bash
streamlit run dashboard/app.py
```

The dashboard must be launched with Streamlit; do not execute `dashboard/app.py` directly.

---

## 📊 Key Outputs

### Consumer Segmentation

![Consumer Segments](assets/figures/consumer_segments.png)

The repository includes cluster assignments and cluster profiles generated from the project's segmentation workflow.

### City Market Intelligence

![City Market Entry Score](assets/figures/city_market_entry_score.png)

City opportunity and market-entry outputs are provided as CSV files for reproducibility and dashboard use.

---

## 🧪 Analytical Components

### Exploratory Data Analysis
The notebook explores demographic, consumption, preference, spending and purchasing variables from the survey data.

### Customer Segmentation
Clustering outputs are used to identify groups of consumers with different behavioural characteristics.

### Predictive Modeling
The project includes model-comparison outputs and prediction-related datasets used in the analytical workflow.

### Demand Analysis
The repository contains:
- demand by period
- forecast output
- model comparison results

### Market Entry Intelligence
Supporting city data is combined with generated opportunity scores and market-entry outputs.

---

## 🗂️ Data Lineage

```text
Raw Survey
   ↓
Cleaning / Preprocessing
   ↓
Cleaned Analytical Dataset
   ↓
EDA / Feature Engineering
   ↓
Model & Segmentation Outputs
   ↓
Dashboard
```

The repository keeps the project's source and derived datasets distinguishable so the analytical workflow can be traced from input to output.

---

## 🧰 Tech Stack

**Python · Pandas · NumPy · Matplotlib · Seaborn · Scikit-learn · Plotly · Streamlit · Jupyter Notebook · Git/GitHub**

---

## 📌 Important Notes

- The repository preserves the project's existing analytical outputs.
- Model results are documented as generated by the project rather than being silently replaced.
- Raw and processed datasets are retained separately where available.
- The dashboard should be launched with **Streamlit**.

---

## 👤 Project

**Shivam Pathak**

GitHub: [@Shivamxxpathak](https://github.com/Shivamxxpathak)

---

<div align="center">

### ☕ BrewInsights
**Turning coffee survey data into market intelligence.**

</div>
