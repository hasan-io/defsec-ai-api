import os
import pandas as pd
import joblib
import numpy as np

from sklearn.utils import resample

MODEL_PATH = os.path.join("models", "random_forest_model.pkl")
DATA_PATH = os.path.join("data", "processed", "cleaned_data.csv")


def load_model():
    print("Loading model...")
    return joblib.load(MODEL_PATH)


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def generate_heavy_attack_dataset(df):
    """
    Memory-safe stress-test dataset:
    - Oversample attacks moderately
    - Keep Normal intact
    """
    print("Generating memory-safe heavy attack dataset...")

    # Separate by label
    df_normal = df[df["Label"] == "Normal"].sample(n=50000, random_state=42)
    df_dos = df[df["Label"] == "DoS"].sample(n=5000, replace=True, random_state=42)
    df_brute = df[df["Label"] == "BruteForce"].sample(n=5000, replace=True, random_state=42)
    df_xss = df[df["Label"] == "XSS"].sample(n=500, replace=True, random_state=42)

    stress_df = pd.concat([df_normal, df_dos, df_brute, df_xss])
    stress_df = stress_df.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"Stress dataset shape: {stress_df.shape}")
    print(stress_df["Label"].value_counts())

    X = stress_df.drop("Label", axis=1)
    y = stress_df["Label"]

    return X, y


def stress_test():
    df = load_data()
    model = load_model()

    X, y = generate_heavy_attack_dataset(df)

    print("Predicting on stress dataset...")
    y_pred = model.predict(X)

    from sklearn.metrics import classification_report
    print("\nStress Test Classification Report:\n")
    print(classification_report(y, y_pred))


if __name__ == "__main__":
    stress_test()
