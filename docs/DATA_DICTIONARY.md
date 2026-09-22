# BrewInsights Data Dictionary

The supplied survey contains 11,072 responses and 21 columns. Identifier/metadata fields are excluded from modeling.

| Column | Meaning | Analytical role |
|---|---|---|
| respondentId | Respondent identifier | Excluded |
| source | Response source | Metadata |
| age | Respondent age | Feature |
| gender | Gender | Feature/EDA |
| city | Respondent city | Segmentation/market analysis |
| occupation | Occupation | Feature/EDA |
| monthlyIncome | Monthly income | Feature |
| coffeeFrequency | Coffee consumption frequency | Feature/demand |
| preferredCoffeeType | Preferred coffee type | Feature/EDA |
| preferredBrand | Preferred/current brand | Feature/market |
| monthlyCoffeeSpend | Monthly coffee spending | Target/feature |
| purchaseLocation | Purchase location | Feature/market |
| purchaseMode | Purchase mode | Feature/EDA |
| priceSensitivity | Price sensitivity | Feature |
| tastePreference | Taste preference | Feature/EDA |
| brandLoyalty | Brand loyalty | Feature |
| willingnessToTry | Willingness to try a new brand | Adoption signal |
| preferredPriceRange | Preferred price range | Feature |
| purchaseIntention | Purchase intention | Adoption/demand signal |
| email | Respondent email | Personal identifier; exclude from public data |
| createdAt | Response timestamp | Metadata; not a genuine sales time index |

## Privacy
Do not publish respondent-level contact information. The public-data workflow removes `email` and `respondentId`.
