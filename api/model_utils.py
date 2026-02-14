import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join("..", "models", "random_forest_model.pkl")

print("Loading model...")
model = joblib.load(MODEL_PATH)
print("Model loaded.")

def predict_attack(data: dict):
    """
    data: dictionary with all features
    returns: predicted attack label
    """
    df = pd.DataFrame([data])  # Single row
    # You can add any preprocessing here if needed
    pred = model.predict(df)
    return pred[0]
