from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import pandas as pd

from app.model_loader import load_model
from app.schemas import (
    CustomerFeatures,
    BatchRequest
)
from app.risk_explainer import (
    explain_risk
)


# App Initialization

app = FastAPI(
    title="Customer Churn Scoring API",
    version="1.0.0"
)


# Load Model

model = load_model()

# Root Endpoint

@app.get("/", response_class=HTMLResponse)
def root():

    return """
    <html>
        <head>
            <title>Customer Churn Scoring API</title>
        </head>

        <body>

            <h1>Customer Churn Scoring API</h1>

            <p>Status: Running</p>

            <p>
                <a href="/health">
                    Health Check
                </a>
            </p>

            <p>
                <a href="/docs">
                    Open API Documentation
                </a>
            </p>

        </body>
    </html>
    """
# Health Check

@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }



# Single Prediction

@app.post("/predict")
def predict(
    customer: CustomerFeatures
):

    input_df = pd.DataFrame(
        [customer.model_dump()]
    )

    probability = float(
        model.predict_proba(
            input_df
        )[0][1]
    )

    prediction = int(
        model.predict(
            input_df
        )[0]
    )

    risk_info = explain_risk(
        probability
    )

    return {

        "churn_probability":
        round(probability, 4),

        "predicted_class":
        prediction,

        "risk_level":
        risk_info["risk_level"],

        "risk_explanation":
        risk_info["risk_explanation"]

    }

# Batch Prediction

@app.post("/batch_predict")
def batch_predict(
    request: BatchRequest
):

    customer_records = [

        customer.model_dump()

        for customer in request.customers

    ]

    input_df = pd.DataFrame(
        customer_records
    )

    probabilities = (
        model.predict_proba(
            input_df
        )[:, 1]
    )

    predictions = (
        model.predict(
            input_df
        )
    )

    results = []

    for probability, prediction in zip(
        probabilities,
        predictions
    ):

        risk_info = explain_risk(
            float(probability)
        )

        results.append({

            "churn_probability":
            round(
                float(probability),
                4
            ),

            "predicted_class":
            int(prediction),

            "risk_level":
            risk_info["risk_level"],

            "risk_explanation":
            risk_info[
                "risk_explanation"
            ]

        })

    return {
        "predictions": results
    }