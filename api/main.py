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

    data_dict = {feature: getattr(request, feature.replace(" ", "_")) for feature in features}

    # 🔥 -------- RULE-BASED DETECTION -------- 🔥

    # DoS
    if data_dict.get("Total_Fwd_Packets", 0) > 1000 and \
       data_dict.get("SYN_Flag_Count", 0) > 300 and \
       data_dict.get("Total_Backward_Packets", 0) < 50:
        return {"prediction": "DoS"}

    # BruteForce
    if data_dict.get("Destination_Port", 0) in [21, 22] and \
       data_dict.get("RST_Flag_Count", 0) > 20:
        return {"prediction": "BruteForce"}

    # XSS
    if data_dict.get("Destination_Port", 0) in [80, 443] and \
       data_dict.get("PSH_Flag_Count", 0) > 10:
        return {"prediction": "XSS"}

    # -----------------------------------------

    df = pd.DataFrame([data_dict])

    try:
        prediction = model.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"prediction": prediction}

