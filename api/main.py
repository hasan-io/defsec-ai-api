import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load AI model and features
model = joblib.load(os.path.join(BASE_DIR, "models", "random_forest_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "models", "features.pkl"))

app = FastAPI(title="Cyber Attack Detection API")

# Define request model dynamically based on features
class FeatureRequest(BaseModel):
    __annotations__ = {feature.replace(" ", "_"): float for feature in features}

@app.get("/")
def root():
    return {"message": "API is running. Use /predict endpoint with POST."}

# --- Custom rule logic for attacks ---
def apply_custom_rules(data: pd.DataFrame) -> str:
    """
    Check for known attack patterns and return attack label if matched.
    Rules are examples, adjust thresholds based on your dataset.
    """
    row = data.iloc[0]

    # Rule for DoS (example: extremely high Flow_Packets/s)
    if row["Flow_Packets/s"] > 5000:
        return "DoS"

    # Rule for BruteForce (example: very high SYN count in small flow)
    if row["SYN_Flag_Count"] > 50 and row["Total_Fwd_Packets"] < 100:
        return "BruteForce"

    # Rule for XSS (example: high Bwd_Packets/s but small payload)
    if row["Bwd_Packets/s"] > 500 and row["Avg_Bwd_Segment_Size"] < 100:
        return "XSS"

    # Add more rules here if needed for other attacks

    return None  # No rule matched

@app.post("/predict")
def predict(request: FeatureRequest):
    # Convert request to DataFrame
    data_dict = {feature: getattr(request, feature.replace(" ", "_")) for feature in features}
    df = pd.DataFrame([data_dict])

    # First, try custom rules
    attack_label = apply_custom_rules(df)
    if attack_label:
        return {"prediction": attack_label, "method": "custom rule"}

    # Otherwise, fallback to AI model
    try:
        prediction = model.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"prediction": prediction, "method": "AI model"}
