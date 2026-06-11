# Customer Churn Scoring API

## Project Overview

This project provides a FastAPI-based prediction service for customer churn risk assessment.

The API loads a trained Logistic Regression churn model and exposes endpoints that allow CRM systems or internal business tools to request churn-risk predictions for individual customers or batches of customers.

The service returns:

* Churn probability
* Predicted churn class
* Risk level
* Risk explanation

The model was trained using historical customer behavior, engagement, support, and purchase-related features.

---

## Repository Structure

churn-scoring-api/
│
├── app/
│ ├── init.py
│ ├── main.py
│ ├── schemas.py
│ ├── model_loader.py
│ └── risk_explainer.py
│
├── data/
│ └── sample_payloads/
│ ├── single_customer.json
│ └── batch_customers.json
│
├── docs/
│ ├── DATA_DICTIONARY.md
│ └── PROJECT_STATEMENT.md
│
├── models/
│ └── model.pkl
│
├── tests/
│ ├── init.py
│ └── test_api.py
│
├── reports/
│ └── MONITORING_PLAN.md
│
├── requirements.txt
├── README.md
├── Dockerfile
└── .gitignore

---

## Model Information

Model Type:

* Logistic Regression

Preprocessing:

* ColumnTransformer
* OneHotEncoder
* Scikit-learn Pipeline

Target Variable:

* churn_next_60d

The saved model artifact includes both preprocessing and prediction logic.

---

## Installation

### Clone Repository

git clone <repository-url>
cd churn-scoring-api

### Create Virtual Environment

python -m venv venv


### Activate Environment

Windows:

venv\Scripts\activate


### Install Dependencies

pip install -r requirements.txt

---

## Running the API

Start the FastAPI application:

uvicorn app.main:app --reload


The API will be available at:

http://127.0.0.1:8000


Interactive API documentation:

http://127.0.0.1:8000/docs


---

# API Endpoints

## GET /health

Health-check endpoint used to verify that the API is running.

### Example Response
{
  "status": "ok"
}

---

## POST /predict

Returns churn prediction for a single customer.

### Sample Request

{
  "recency_days": 15,
  "frequency_180d": 8,
  "monetary_180d": 450.5,
  "return_rate_180d": 0.12,
  "avg_discount_pct_180d": 18.5,
  "avg_rating_180d": 4.3,
  "category_diversity_180d": 4,
  "ticket_count_90d": 2,
  "negative_ticket_rate_90d": 0.25,
  "avg_resolution_hours_90d": 24,
  "days_since_signup": 800,
  "sessions_30d": 12,
  "product_views_30d": 45,
  "cart_adds_30d": 8,
  "wishlist_adds_30d": 3,
  "abandoned_carts_30d": 2,
  "email_opens_30d": 6,
  "campaign_clicks_30d": 2,
  "last_visit_days_ago": 4,
  "city_tier": "Tier_1",
  "age_group": "25-34",
  "acquisition_channel": "Organic",
  "loyalty_tier": "Gold",
  "preferred_category": "Fragrance",
  "marketing_consent": "Yes"
}


### Sample Response

{
  "churn_probability": 0.9853,
  "predicted_class": 1,
  "risk_level": "high",
  "risk_explanation": "Customer shows a high likelihood of churn based on historical behavior."
}

---

## POST /batch_predict

Returns churn predictions for multiple customers.

### Sample Request

See:

data/sample_payloads/batch_customers.json

### Sample Response

{
  "predictions": [
    {
      "churn_probability": 0.9853,
      "predicted_class": 1,
      "risk_level": "high",
      "risk_explanation": "Customer shows a high likelihood of churn based on historical behavior."
    }
  ]
}

---

## Input Validation

Request validation is implemented using Pydantic models.

Validation ensures:

* Required fields are present
* Data types are correct
* Invalid requests return descriptive validation errors

---

## Running Tests

Execute the API test suite:

pytest

Expected result:

3 passed

Test coverage includes:

1. Health endpoint
2. Single prediction endpoint
3. Batch prediction endpoint

---

## Docker Support

Build Docker image:

docker build -t churn-scoring-api .

Run container:

docker run -p 8000:8000 churn-scoring-api

---

## Monitoring Plan

See:

reports/monitoring_plan.md

The monitoring plan covers:

* Data drift
* Prediction distribution
* Business outcomes
* API errors
* Retraining triggers
* Responsible use guidelines

---

## Source Data Notes

The prediction model was developed using customer-level churn modeling data generated during earlier project stages.

Features include:

* Purchase behavior
* Customer support activity
* Product returns
* Website engagement
* Marketing engagement
* Loyalty information

The API uses a previously trained and saved model artifact ('model.pkl') to generate predictions.

---

## Conclusion

This FastAPI service provides a production-style interface for customer churn prediction. It supports both single-customer and batch scoring workflows while maintaining input validation, automated testing, monitoring guidance, and reproducible deployment configuration.
