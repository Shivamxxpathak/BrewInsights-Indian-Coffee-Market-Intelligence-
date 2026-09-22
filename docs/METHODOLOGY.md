# BrewInsights Methodology

Raw survey → cleaning → feature engineering → EDA → analytical branches → saved outputs → Streamlit dashboard.

## Data preparation
Inspect shape, types, missingness and duplicates; standardize selected categorical values; convert modeling fields to numeric/encoded representations; exclude identifiers and metadata.

## Exploratory analysis
Analyze coffee frequency, coffee type, brands, spending, purchase mode/location, price sensitivity, taste, loyalty, willingness to try and purchase intention.

## Customer segmentation
Evaluate K-Means and hierarchical/agglomerative clustering with standardized features and silhouette scores. Saved consumer outputs use K-Means.

## New-brand adoption
Evaluate Logistic Regression, Decision Tree, Random Forest, XGBoost and Gradient Boosting. The notebook's final evaluation table contains Logistic Regression, Random Forest and Gradient Boosting with Accuracy, Precision, Recall, F1 and ROC-AUC.

## Coffee spending
Use a preprocessing pipeline and Linear Regression to estimate `Coffee_Spend`, reporting MAE, RMSE and R².

## Demand forecasting
Construct 24 ordered survey periods because the survey has no genuine monthly sales history. The demand indicator uses coffee frequency, purchase intention and monthly coffee spend. Evaluate Linear Regression, Random Forest Regression and Gradient Boosting Regression.

**Limitation:** this is a survey-based forecasting demonstration, not a forecast of actual monthly Indian coffee sales.

## City market analysis
Merge city-level consumer features with external city data, cluster cities with K-Means, evaluate silhouette separation, and calculate a normalized opportunity score from monthly coffee spend, café density and income index.

## Market-entry score
Combine adoption, spending, city strength and trend using an equal-weight baseline. Sensitivity scenarios vary the weights. This is a project-level decision aid, not a guarantee of commercial performance.
