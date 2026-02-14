import os
import pandas as pd
import joblib
import random

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


MODEL_PATH = os.path.join("models", "random_forest_model.pkl")
DATA_PATH = os.path.join("data", "processed", "cleaned_data.csv")


def load_model():
    return joblib.load(MODEL_PATH)


def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df.drop("Label", axis=1)
    y = df["Label"]
    return X, y


def test_model():
    print("Loading model...")
    model = load_model()

    print("Loading data...")
    X, y = load_data()

    # Same split as training
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("\nEvaluating on test set only:\n")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Random sample testing
    print("\nRandom Sample Predictions:\n")
    for _ in range(5):
        idx = random.randint(0, len(X_test) - 1)
        sample = X_test.iloc[idx:idx+1]
        true_label = y_test.iloc[idx]
        prediction = model.predict(sample)[0]

        print(f"True: {true_label} | Predicted: {prediction}")

    # Focused XSS testing
    print("\nXSS Sample Testing:\n")
    xss_indices = y_test[y_test == "XSS"].index

    if len(xss_indices) > 0:
        for idx in xss_indices[:5]:
            sample = X_test.loc[[idx]]
            prediction = model.predict(sample)[0]
            print(f"True: XSS | Predicted: {prediction}")
    else:
        print("No XSS samples found in test set.")


if __name__ == "__main__":
    test_model()
