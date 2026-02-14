import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "models", "random_forest_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "models", "features.pkl"))

app = FastAPI(title="Cyber Attack Detection API")

# Define request model dynamically based on features
class FeatureRequest(BaseModel):
    __annotations__ = {feature.replace(" ", "_"): float for feature in features}

@app.get("/")
def root():
    return {"message": "API is running. Use /predict endpoint with POST."}

@app.post("/predict")
def predict(request: FeatureRequest):
    # Convert request to DataFrame
    data_dict = {feature: getattr(request, feature.replace(" ", "_")) for feature in features}
    df = pd.DataFrame([data_dict])

    # Predict
    try:
        prediction = model.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"prediction": prediction}
