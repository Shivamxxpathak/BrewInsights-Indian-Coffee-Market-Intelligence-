# PPT / Documentation Alignment

This file is the canonical factual reference for the BrewInsights presentation.

## Dataset
- 11,072 survey responses.
- 21 source columns.
- Public processed data excludes `email` and `respondentId`.
- The survey is consumer-response data, not a historical sales database.

## Customer segmentation
- K-Means is the saved customer-segmentation result.
- Hierarchical/agglomerative clustering was evaluated but is not the saved final segmentation output.
- City clustering silhouette: **0.628752** with the full city feature set.
- City clustering silhouette without city tier: **0.594685**.

## New-brand adoption
| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6051 | 0.6051 | 1.0000 | 0.7540 | 0.7838 |
| Decision Tree | 0.6390 | — | — | — | — |
| Random Forest | 0.7183 | 0.7179 | 0.8802 | 0.7909 | 0.7560 |
| XGBoost | 0.7500 | — | — | — | — |
| Gradient Boosting | 0.7609 | 0.7756 | 0.8510 | 0.8116 | 0.7990 |

Decision Tree and XGBoost were reported with accuracy only in the executed notebook.

## Coffee spending
- Linear Regression MAE: **137.8497**
- RMSE: **188.2792**
- R²: **0.6442**

## Demand analysis
| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 0.024208 | 0.027240 | -2.555373 |
| Random Forest | 0.026703 | 0.028985 | -3.025425 |
| Gradient Boosting | 0.027106 | 0.031199 | -3.663876 |

The demand series is constructed from ordered survey periods because the source survey does not contain genuine historical monthly sales. Present it as a survey-based demonstration/trend estimate, not an official Indian coffee sales forecast.

## Market-entry analysis
The market-entry score is a project-level analytical index combining adoption, spending, city strength and trend under an equal-weight baseline. Sensitivity analysis is provided in `outputs/datasets/recommendation_sensitivity.csv`. Do not describe the score as guaranteed commercial performance or a validated market-size estimate.

## Partnership experiment
The partnership section is an experiment template. The supplied survey contains no treatment/control observation for a partnership intervention, so no partnership effect should be reported as measured.

## Consistency rule
Any final PPT should preserve the same dataset size, model metrics, segmentation method, demand limitation, market-entry definition and partnership limitation. Any different number must be traceable to a clearly identified dashboard calculation.