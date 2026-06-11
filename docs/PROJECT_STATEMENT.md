# Capstone Project: D2C Customer Churn Intelligence & Retention API

# Business Context

A D2C personal-care brand wants to reduce customer churn using data-driven retention strategies instead of giving discounts to all customers.

The company wants a system that can:

1. Understand customer behavior
2. Identify churn-risk patterns
3. Prioritize customers for retention campaigns
4. Provide churn predictions through an internal API

---

# Dataset Context

The project includes multiple datasets related to:

- Customer profiles
- Orders and transactions
- Support tickets
- Web/app activity
- Retention campaigns
- Churn labels

Important dataset definitions and leakage rules are available in:

```text
docs/data_dictionary.md
```

---

# Important Leakage Rule

Only data available on or before the snapshot date should be used for analysis and model features.

Post-snapshot information must NOT be used as model input.

---

# Submission Structure

The capstone project is divided into four separate GitHub repositories.

Each repository must:
- be independently runnable
- contain a proper README
- include required outputs
- include setup instructions
- avoid private/local-only paths

---

# Part 1 — Data Audit, EDA & Business Understanding

## Objective

Audit the raw data and understand customer churn behavior before building any model.

## Main Tasks

- Load and inspect all datasets
- Perform data-quality analysis
- Conduct exploratory data analysis (EDA)
- Identify churn-risk hypotheses
- Write business recommendations

## Required Outputs

- `eda_audit.ipynb`
- `data_quality_report.md`
- `business_memo.md`
- Minimum 6 meaningful charts/tables

---

# Part 2 — RFM Segmentation & Retention Strategy

## Objective

Create customer segments and recommend targeted retention actions.

## Main Tasks

- Build RFM features
- Create customer segments
- Use additional behavioral signals
- Recommend retention strategies
- Prioritize campaign budgets

## Required Outputs

- `rfm_segmentation.ipynb`
- `segments.csv`
- `retention_strategy.md`
- `manual_review_cases.md`

---

# Part 3 — Churn Prediction Model & Model Card

## Objective

Build a machine-learning model to predict customer churn.

## Main Tasks

- Prepare modeling features
- Prevent target leakage
- Train baseline and advanced models
- Evaluate model performance
- Perform error analysis
- Create model documentation

## Required Outputs

- `churn_model.ipynb`
- `model.pkl`
- `metrics.json`
- `error_analysis.md`
- `model_card.md`

---

# Part 4 — FastAPI Churn Scoring Service

## Objective

Deploy the churn model as a FastAPI prediction service.

## Main Tasks

- Create FastAPI endpoints
- Load trained model
- Add validation and testing
- Create reproducible workflow
- Add monitoring and responsible-use plan

## Required Outputs

- `app/main.py`
- API test files
- Model artifact
- Monitoring plan
- README with API instructions

---

# Overall Evaluation Focus

Evaluation will focus on:

- Data understanding
- Leakage prevention
- Business reasoning
- EDA quality
- Modeling correctness
- API functionality
- Reproducibility
- Documentation quality

---

# Important Notes

- Use dataset-backed reasoning
- Avoid generic AI-generated explanations
- Keep repositories public and runnable
- Do not expose private credentials or local paths
- Prevent future-data leakage in all modeling workflows