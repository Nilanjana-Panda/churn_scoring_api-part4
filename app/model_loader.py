import joblib


MODEL_PATH = "models/model.pkl"


def load_model():
    """
    Load trained churn model.
    """

    model = joblib.load(
        MODEL_PATH
    )

    return model