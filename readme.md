# 🤖 DefSec AI API — Cyber Attack Detection Engine

> A Machine Learning-powered REST API that classifies network traffic as **Normal, DoS, BruteForce, or XSS** in real time — built to plug directly into the Guard IQ security platform.

---

## 📌 What is This?

The **DefSec AI API** is a standalone Python microservice that powers the intelligent attack detection layer of Guard IQ. It takes raw network flow features (packet counts, flow durations, TCP flags, byte sizes, etc.) as input and uses a trained **Random Forest classifier** to instantly predict whether the traffic is benign or a specific type of cyberattack.

This module is deployed separately from the main PHP dashboard and is called via HTTP POST requests. It was trained on a real-world network intrusion dataset (CICIDS-style) and is production-deployed on **Render**.

---

## 🚀 Live Deployment

```
Base URL:  https://defsec-ai-api-1.onrender.com
Endpoint:  POST /predict
Health:    GET  /
```

---

## 🎯 What It Detects

The model classifies every network flow into one of **4 categories**:

| Label | Description |
|---|---|
| `Normal` | Legitimate, benign traffic |
| `DoS` | Denial of Service attack (flood-based) |
| `BruteForce` | Credential stuffing / Patator-style attacks |
| `XSS` | Cross-Site Scripting attack traffic pattern |

---

## 🧠 Machine Learning Model

| Property | Detail |
|---|---|
| Algorithm | **Random Forest Classifier** |
| Library | scikit-learn |
| Estimators | 100 trees |
| Class Weighting | `balanced` (handles imbalanced attack vs. normal traffic) |
| Parallelism | `n_jobs=-1` (uses all CPU cores) |
| Train/Test Split | 80% / 20% (stratified) |
| Serialization | `joblib` (`.pkl` format) |
| Input Features | **71 numerical network flow features** |

### Model Artifacts (in `/models/`)
| File | Purpose |
|---|---|
| `random_forest_model.pkl` | Trained Random Forest model (~40MB) |
| `features.pkl` | Ordered list of 71 feature names expected by the model |
| `confusion_matrix.png` | Visual evaluation — actual vs. predicted labels |
| `feature_importance.png` | Top 20 most influential features identified by the model |

---

## 📡 API Reference

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{
  "message": "API is running. Use /predict endpoint with POST."
}
```

---

### `POST /predict`
Accepts 71 network flow features and returns the predicted attack class.

**Request Body** (`application/json`):
```json
{
  "Destination_Port": 443,
  "Flow_Duration": 5000,
  "Total_Fwd_Packets": 200,
  "Total_Backward_Packets": 5,
  "Total_Length_of_Fwd_Packets": 10000,
  "Total_Length_of_Bwd_Packets": 250,
  "Fwd_Packet_Length_Max": 60,
  "Fwd_Packet_Length_Min": 40,
  "Fwd_Packet_Length_Mean": 50,
  "Fwd_Packet_Length_Std": 5,
  "Bwd_Packet_Length_Max": 60,
  "Bwd_Packet_Length_Min": 40,
  "Bwd_Packet_Length_Mean": 50,
  "Bwd_Packet_Length_Std": 5,
  "Flow_Bytes_s": 2000,
  "Flow_Packets_s": 40,
  "Flow_IAT_Mean": 5,
  "Flow_IAT_Std": 2,
  "Flow_IAT_Max": 10,
  "Flow_IAT_Min": 1,
  "Fwd_IAT_Total": 500,
  "Fwd_IAT_Mean": 2,
  "Fwd_IAT_Std": 1,
  "Fwd_IAT_Max": 5,
  "Fwd_IAT_Min": 1,
  "Bwd_IAT_Total": 50,
  "Bwd_IAT_Mean": 10,
  "Bwd_IAT_Std": 2,
  "Bwd_IAT_Max": 15,
  "Bwd_IAT_Min": 5,
  "Fwd_PSH_Flags": 1,
  "Fwd_URG_Flags": 0,
  "Fwd_Header_Length": 40,
  "Bwd_Header_Length": 40,
  "Fwd_Packets_s": 35,
  "Bwd_Packets_s": 1,
  "Min_Packet_Length": 40,
  "Max_Packet_Length": 60,
  "Packet_Length_Mean": 50,
  "Packet_Length_Std": 5,
  "Packet_Length_Variance": 25,
  "FIN_Flag_Count": 0,
  "SYN_Flag_Count": 180,
  "RST_Flag_Count": 0,
  "PSH_Flag_Count": 5,
  "ACK_Flag_Count": 10,
  "URG_Flag_Count": 0,
  "CWE_Flag_Count": 0,
  "ECE_Flag_Count": 0,
  "Down_Up_Ratio": 0.025,
  "Average_Packet_Size": 50,
  "Avg_Fwd_Segment_Size": 50,
  "Avg_Bwd_Segment_Size": 50,
  "Fwd_Header_Length_1": 40,
  "Subflow_Fwd_Packets": 200,
  "Subflow_Fwd_Bytes": 10000,
  "Subflow_Bwd_Packets": 5,
  "Subflow_Bwd_Bytes": 250,
  "Init_Win_bytes_forward": 1024,
  "Init_Win_bytes_backward": 1024,
  "act_data_pkt_fwd": 180,
  "min_seg_size_forward": 40,
  "Active_Mean": 50,
  "Active_Std": 10,
  "Active_Max": 70,
  "Active_Min": 40,
  "Idle_Mean": 10,
  "Idle_Std": 2,
  "Idle_Max": 15,
  "Idle_Min": 5
}
```

**Response:**
```json
{
  "prediction": "DoS"
}
```

Possible prediction values: `"Normal"`, `"DoS"`, `"BruteForce"`, `"XSS"`

**Error Response (500):**
```json
{
  "detail": "error message here"
}
```

> **Note:** Feature names with spaces, slashes, hyphens, or dots are automatically sanitized to underscores in the API (e.g., `Flow Bytes/s` → `Flow_Bytes_s`). The model internally maps them back to their original names.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| API Framework | **FastAPI** |
| Server | **Uvicorn** (ASGI) |
| ML Library | **scikit-learn** |
| Data Processing | **pandas**, **numpy** |
| Model Serialization | **joblib** |
| Deployment | **Render** (via `Procfile`) |
| Language | **Python 3.x** |

---

## 📁 Project Structure

```
defsec-ai-api/
│
├── api/
│   ├── main.py              # FastAPI app — /predict endpoint, model loading, feature sanitization
│   ├── model_utils.py       # Utility: load model and predict from a dict input
│   └── test_api.py          # Quick local test script for the /predict endpoint
│
├── src/
│   ├── data_preprocessing.py  # Loads raw CSVs, cleans data, maps attack labels, saves processed CSV
│   ├── train.py               # Trains the Random Forest model, saves .pkl files
│   ├── evaluate.py            # Generates confusion matrix + top-20 feature importance plots
│   ├── test_model.py          # Evaluates model on test split + random sample predictions + XSS focus test
│   ├── stress_test.py         # Stress tests model with 60,500 samples (50k Normal + oversampled attacks)
│   ├── feature_engineering.py # (Reserved for future feature engineering)
│   └── utils.py               # (Reserved for shared utilities)
│
├── models/
│   ├── random_forest_model.pkl  # Trained model (~40MB)
│   ├── features.pkl             # Ordered list of 71 feature names
│   ├── confusion_matrix.png     # Model evaluation heatmap
│   └── feature_importance.png   # Top 20 features chart
│
├── payload.json             # Sample 71-feature JSON payload for testing
├── testt_api.py             # Tests the live Render-deployed API with payload.json
├── requirments.txt          # Python dependencies
├── Procfile                 # Render deployment command (uvicorn)
└── .gitignore               # Excludes data/, .pyc, .csv, .zip files
```

---

## ⚙️ Data Pipeline — How the Model Was Built

### Step 1: Data Collection
- Raw training data: **CICIDS-style network flow CSV files** (stored in `data/raw/`)
- Dataset contains labeled network traffic flows with 70+ numerical features per flow

### Step 2: Preprocessing (`src/data_preprocessing.py`)
- Loads and merges all CSV files from `data/raw/`
- Strips whitespace from column names
- Removes duplicate rows
- Drops constant columns (only 1 unique value — no information)
- Replaces `inf` / `-inf` with `NaN`, then fills `NaN` with `0`
- **Label mapping:**
  - `benign` → `Normal`
  - `dos*` → `DoS`
  - `patator` / `brute force` → `BruteForce`
  - `xss` → `XSS`
  - Anything else is dropped
- Saves cleaned data to `data/processed/cleaned_data.csv`

### Step 3: Training (`src/train.py`)
- Loads `cleaned_data.csv`
- Splits 80/20 with stratification to maintain class balance
- Trains `RandomForestClassifier` with:
  - 100 estimators
  - `class_weight="balanced"` for imbalanced classes
  - All CPU cores (`n_jobs=-1`)
- Saves `random_forest_model.pkl` and `features.pkl`

### Step 4: Evaluation (`src/evaluate.py`)
- Generates **confusion matrix** heatmap (seaborn) → saved as `models/confusion_matrix.png`
- Generates **Top 20 Feature Importances** bar chart → saved as `models/feature_importance.png`

### Step 5: Stress Testing (`src/stress_test.py`)
Model was stress-tested on a mixed dataset of **60,500 samples**:
- 50,000 Normal
- 5,000 DoS (oversampled)
- 5,000 BruteForce (oversampled)
- 500 XSS (oversampled)

---

## 🔌 Integration with Guard IQ

The DefSec AI API is called from the main Guard IQ PHP dashboard when network flow data is available. The integration flow is:

```
Guard IQ PHP Dashboard
        │
        │  POST /predict  (71 network features as JSON)
        ▼
DefSec AI API (Render)
        │
        │  Random Forest Classifier
        ▼
{ "prediction": "DoS" }
        │
        ▼
Guard IQ logs result → triggers alert if attack detected
```

---

## 🏃 Running Locally

### 1. Install dependencies
```bash
pip install -r requirments.txt
```

### 2. Start the API server
```bash
uvicorn api.main:app --reload
```

API will be live at: `http://127.0.0.1:8000`

### 3. Test locally
```bash
python api/test_api.py
```

### 4. Test the live deployed API
```bash
python testt_api.py
```

### 5. Interactive API docs (auto-generated by FastAPI)
```
http://127.0.0.1:8000/docs      ← Swagger UI
http://127.0.0.1:8000/redoc     ← ReDoc
```

---

## 🔁 Retraining the Model

To retrain from scratch with new data:

```bash
# Step 1 — Preprocess raw CSVs
python src/data_preprocessing.py

# Step 2 — Train the model
python src/train.py

# Step 3 — Evaluate performance
python src/evaluate.py

# Step 4 — Stress test
python src/stress_test.py
```

---

## ☁️ Deployment (Render)

The `Procfile` defines the startup command for Render:

```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

To deploy:
1. Push to GitHub
2. Connect repo to Render as a **Web Service**
3. Set build command: `pip install -r requirments.txt`
4. Render auto-detects the `Procfile` and runs the server

---

## 📦 Dependencies

```
fastapi
uvicorn
pandas
scikit-learn
joblib
numpy
```

---

## 📄 License

Built for the Guard IQ / DefSec hackathon project. All rights reserved © 2026 DefSec Security Solutions.
