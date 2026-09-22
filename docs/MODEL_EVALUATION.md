# Model Evaluation

## New Coffee Brand Adoption

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6051 | 0.6051 | 1.0000 | 0.7540 | 0.7838 |
| Decision Tree | 0.6390 | — | — | — | — |
| Random Forest | 0.7183 | 0.7179 | 0.8802 | 0.7909 | 0.7560 |
| XGBoost | 0.7500 | — | — | — | — |
| Gradient Boosting | 0.7609 | 0.7756 | 0.8510 | 0.8116 | 0.7990 |

Decision Tree and XGBoost are shown with accuracy only because the notebook reports those metrics separately rather than including them in its final evaluation DataFrame.

## Coffee Spending Prediction

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 137.8497 | 188.2792 | 0.6442 |

## Demand Forecasting

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 0.024208 | 0.027240 | -2.555373 |
| Random Forest | 0.026703 | 0.028985 | -3.025425 |
| Gradient Boosting | 0.027106 | 0.031199 | -3.663876 |

The demand model has negative R² values because the ordered survey series is not genuine historical sales time series; the notebook explicitly documents this limitation.

## City clustering

| Evaluation | Silhouette |
|---|---:|
| Full city features | 0.628752 |
| Without city tier | 0.594685 |
