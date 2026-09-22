<div align="center">

# ☕ BrewInsights
### Indian Coffee Market Intelligence

**Consumer analytics · Customer segmentation · Machine learning · City intelligence · Demand trends · Interactive dashboard**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

**11,072 survey responses** · **10 analytical views** · **5 consumer clusters** · **22 cities scored**

</div>

---

## 🧭 What is BrewInsights?

**BrewInsights** is an end-to-end data analytics and machine learning project built to understand coffee consumers and market opportunities in India.

The project turns survey data into a connected decision-support workflow:

> **Raw survey → Cleaning → EDA → Segmentation → Prediction → City Intelligence → Demand Trends → Dashboard**

It combines behavioral analysis with transparent modeling so that the final dashboard can be traced back to the underlying data and saved outputs.

---

## ✨ Explore the Project

| Area | What it answers |
|---|---|
| ☕ **Consumer Analytics** | Who drinks coffee, what they prefer, where they buy, and how much they spend |
| 🧩 **Customer Segmentation** | What distinct consumer groups appear in the survey? |
| 📈 **Brand Adoption** | Which factors are associated with willingness to buy a new coffee brand? |
| 💰 **Spending Prediction** | Can coffee spending be estimated from consumer features? |
| 🗺️ **City Intelligence** | Which cities show stronger signals for market-entry analysis? |
| 📊 **Demand Forecast** | What trends appear across the ordered survey periods? |
| 🧪 **Partnership Test** | How could a future partnership experiment be structured? |
| 🔎 **Data Explorer** | How do the underlying records and derived outputs look? |
| 📚 **Methodology** | What assumptions, transformations, and limitations sit behind the results? |

---

## 🎯 Project Highlights

- **11,072-response consumer survey** covering demographics, coffee habits, preferences, spending, brands, purchase behavior, price sensitivity, willingness to try, and purchase intention.
- **K-Means customer segmentation** with exported cluster assignments and profiles.
- **Brand adoption and spending model experiments** with model evaluation retained from the original analysis.
- **City-level intelligence** combining consumer signals with city features into an explicit market-entry scoring framework.
- **Demand trend analysis and forecast outputs** using ordered survey periods.
- **Sensitivity analysis** showing how market-entry rankings change when score weights change.
- **Partnership experiment template** for future treatment/control data collection.
- **Interactive Streamlit dashboard** designed as the presentation layer for the complete analysis.

---

## 🗂️ Repository Structure

```text
BrewInsights-Indian-Coffee-Market-Intelligence/
│
├── 📊 data/
│   ├── indian-coffee-all-responses final dataset.csv
│   ├── external_city_data.csv
│   ├── coffee_demand_by_period.csv
│   ├── coffee_demand_forecast.csv
│   ├── coffee_demand_model_comparison.csv
│   └── modules/
│       └── city_scores.csv
│
├── 📓 notebooks/
│   └── BrewInsights_Analysis.ipynb
│
├── 🖥️ dashboard/
│   ├── app.py
│   └── README.md
│
├── 📦 outputs/
│   ├── datasets/
│   │   ├── consumer_cluster_assignments.csv
│   │   ├── consumer_cluster_profiles.csv
│   │   ├── city_opportunity_scores.csv
│   │   ├── market_entry_ranking.csv
│   │   ├── recommendation_sensitivity.csv
│   │   └── partnership_experiment_template.csv
│   └── diagrams/
│       ├── consumer_segments.png
│       └── city_market_entry_score.png
│
├── 📝 docs/
│   └── PROJECT_COMPLETION_NOTES.md
│
├── requirements.txt
├── requirements_dashboard.txt
├── run_dashboard.py
└── README.md
```

---

## ⚙️ Run the Dashboard Locally

### 1. Clone the repository

```bash
git clone https://github.com/Shivamxxpathak/BrewInsights-Indian-Coffee-Market-Intelligence-.git
cd BrewInsights-Indian-Coffee-Market-Intelligence-
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements_dashboard.txt
```

### 4. Launch BrewInsights

```bash
streamlit run dashboard/app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

`http://localhost:8501`

> **Windows shortcut:** `run_dashboard.bat` is included in the repository for a quicker local launch.

---

## 🧠 Analytical Workflow

### 01 · Data Preparation

The raw survey is cleaned by removing non-analytical identifiers, standardizing fields, converting selected ordinal/value ranges into numeric representations, handling missing values, and normalizing inconsistent categorical labels.

### 02 · Exploratory Data Analysis

The analysis examines demographic distributions, coffee frequency, preferred coffee types and brands, purchase channels, spending, price sensitivity, taste preferences, brand loyalty, willingness to try, and purchase intention.

### 03 · Customer Segmentation

Behavioral and demographic features are used to create consumer clusters. The cluster assignment and cluster-profile files are saved in `outputs/datasets/` so the dashboard can reuse the analytical results without rerunning the notebook.

### 04 · Predictive Modeling

The notebook contains model experiments for **new-brand adoption** and **coffee spending**, including evaluation metrics and model comparison.

### 05 · City Intelligence

Consumer-level signals are combined with city-level features such as city tier, cafe density, income index, competitor count, and e-commerce share. The resulting market-entry score is treated as a transparent project-level decision aid.

### 06 · Demand Analysis

Demand is analyzed across ordered survey periods, with comparison outputs and future-period forecast values stored separately for dashboard use.

### 07 · Decision Layer

The final outputs are surfaced through an interactive Streamlit dashboard with filtering, visual exploration, model views, city analysis, data inspection, and methodology notes.

---

## 🔍 Key Outputs

The repository intentionally stores the derived datasets used by the dashboard:

- `consumer_cluster_assignments.csv` — respondent-level cluster labels
- `consumer_cluster_profiles.csv` — cluster-level summary profiles
- `city_opportunity_scores.csv` — city-level component scores and combined score
- `market_entry_ranking.csv` — integrated city analysis table
- `recommendation_sensitivity.csv` — ranking sensitivity under alternative weights
- `partnership_experiment_template.csv` — template for future partnership testing
- `coffee_demand_by_period.csv` — observed survey-period demand trend
- `coffee_demand_forecast.csv` — forecasted future periods
- `coffee_demand_model_comparison.csv` — model error comparison

---

## ⚠️ Methodology & Interpretation Notes

### Demand forecasting

The available dataset does **not** contain a genuine historical monthly sales time series. The forecast therefore uses **ordered survey periods** and should be interpreted as a project-level demand-trend demonstration, not as historical Indian coffee sales forecasting.

### Market-entry score

The baseline market-entry score uses an **equal-weight framework across adoption, spending, city strength, and trend**. The sensitivity analysis is included to make the effect of alternative assumptions visible. The score is a documented analytical assumption, not a guaranteed market outcome.

### Partnership experiment

The partnership section is a **future experiment template**. The supplied survey does not contain treatment/control information that would support an observed causal partnership effect.

### Model results

Model metrics in this repository are preserved from the project analysis. They should be read in the context of the available survey features, preprocessing decisions, sample design, and the limitations of survey-based inference.

---

## 🧰 Tech Stack

**Python · Pandas · NumPy · Matplotlib · Seaborn · Plotly · Scikit-learn · Streamlit · Jupyter Notebook · Git · GitHub**

---

## 📸 Visual Story

The dashboard follows an earthy, minimal visual system designed around the BrewInsights brand and uses interactive Plotly/Streamlit views for exploration.

### Consumer Segments

![Consumer Segments](outputs/diagrams/consumer_segments.png)

### City Market Entry Score

![City Market Entry Score](outputs/diagrams/city_market_entry_score.png)

---

## 🚀 Why This Project Matters

BrewInsights demonstrates a complete analytics workflow rather than a standalone model:

**data quality → business questions → exploratory analysis → segmentation → prediction → market intelligence → decision support → presentation.**

That makes the repository useful as both a **technical portfolio project** and a practical example of how analytical outputs can be connected into an interactive product.

---

## 👤 Author

### Shivam Pathak

Computer Science Engineering · AI / Machine Learning · Data Analytics

[![GitHub](https://img.shields.io/badge/GitHub-Shivamxxpathak-181717?style=flat-square&logo=github)](https://github.com/Shivamxxpathak)

---

<div align="center">

### ☕ BrewInsights
**From coffee consumers to market intelligence.**

</div>
