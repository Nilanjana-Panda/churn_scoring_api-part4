def explain_risk(
    probability: float
):
    """
    Generate risk explanation.
    """

    if probability >= 0.70:

        return {

            "risk_level": "high",

            "risk_explanation":
            (
                "Customer shows a high "
                "likelihood of churn based "
                "on historical behavior."
            )

        }

    elif probability >= 0.40:

        return {

            "risk_level": "medium",

            "risk_explanation":
            (
                "Customer exhibits some "
                "churn-related signals and "
                "should be monitored."
            )

        }

    return {

        "risk_level": "low",

        "risk_explanation":
        (
            "Customer currently shows "
            "a relatively low risk "
            "of churn."
        )

    }