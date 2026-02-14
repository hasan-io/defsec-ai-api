import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load model and features
model = joblib.load(os.path.join(BASE_DIR, "models", "random_forest_model.pkl"))
original_features = joblib.load(os.path.join(BASE_DIR, "models", "features.pkl"))

# Sanitize feature names to be valid Python identifiers
def sanitize(name):
    return name.replace(" ", "_").replace("/", "_").replace("-", "_").replace(".", "_")

feature_map = {sanitize(f): f for f in original_features}
sanitized_features = list(feature_map.keys())

# FastAPI app
app = FastAPI(title="Cyber Attack Detection API")

# Dynamic request model
class FeatureRequest(BaseModel):
    __annotations__ = {
        feature.replace(" ", "_")
               .replace("/", "_")
               .replace(".", "_"): float
        for feature in features
    }

@app.get("/")
def root():
    return {"message": "API is running. Use /predict endpoint with POST."}

@app.post("/predict")
def predict(request: FeatureRequest):
    try:
        # Convert request to dict
        request_dict = request.dict()

        # Map back to original feature names
        corrected_dict = {}

        for feature in features:
            safe_name = (
                feature.replace(" ", "_")
                       .replace("/", "_")
                       .replace(".", "_")
            )
            corrected_dict[feature] = request_dict[safe_name]

        df = pd.DataFrame([corrected_dict])

        prediction = model.predict(df)[0]

        return {"prediction": prediction}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))