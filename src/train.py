import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


def load_data():
    path = os.path.join("data", "processed", "cleaned_data.csv")
    df = pd.read_csv(path)
    return df


def train():
    print("Loading processed dataset...")
    df = load_data()

    # Separate features and label
    X = df.drop("Label", axis=1)
    y = df["Label"]

    # Save the feature names for API usage
    features = X.columns.tolist()

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save model and feature list
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "random_forest_model.pkl")
    features_path = os.path.join("models", "features.pkl")

    joblib.dump(model, model_path)
    joblib.dump(features, features_path)

    print(f"\nModel saved at: {model_path}")
    print(f"Feature list saved at: {features_path}")


if __name__ == "__main__":
    train()
