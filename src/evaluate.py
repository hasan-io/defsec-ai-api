import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix, classification_report


MODEL_PATH = os.path.join("models", "random_forest_model.pkl")
DATA_PATH = os.path.join("data", "processed", "cleaned_data.csv")


def load_model():
    model = joblib.load(MODEL_PATH)
    return model


def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df.drop("Label", axis=1)
    y = df["Label"]
    return X, y


def evaluate():
    print("Loading model...")
    model = load_model()

    print("Loading dataset...")
    X, y = load_data()

    print("Generating predictions...")
    y_pred = model.predict(X)

    print("\nClassification Report:\n")
    print(classification_report(y, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y, y_pred, labels=model.classes_)

    plt.figure()
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        xticklabels=model.classes_,
        yticklabels=model.classes_
    )
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()

    os.makedirs("models", exist_ok=True)
    plt.savefig("models/confusion_matrix.png")
    plt.close()

    print("Confusion matrix saved at models/confusion_matrix.png")

    # Feature Importance
    importances = model.feature_importances_
    feature_names = X.columns

    feature_importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    top_features = feature_importance_df.head(20)

    plt.figure()
    plt.barh(top_features["Feature"], top_features["Importance"])
    plt.gca().invert_yaxis()
    plt.title("Top 20 Feature Importances")
    plt.tight_layout()

    plt.savefig("models/feature_importance.png")
    plt.close()

    print("Feature importance plot saved at models/feature_importance.png")


if __name__ == "__main__":
    evaluate()
