import os
import pandas as pd


RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/cleaned_data.csv"


def load_data():
    all_files = [
        os.path.join(RAW_DATA_PATH, f)
        for f in os.listdir(RAW_DATA_PATH)
        if f.endswith(".csv")
    ]

    df_list = []
    for file in all_files:
        print(f"Loading {file}")
        df = pd.read_csv(file)
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    print("All files merged successfully.")
    print("Combined Shape:", combined_df.shape)
    return combined_df


def clean_data(df):
    print("Initial Shape:", df.shape)

    df.columns = df.columns.str.strip()

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove columns with only one unique value
    nunique = df.nunique()
    cols_to_drop = nunique[nunique <= 1].index
    df = df.drop(columns=cols_to_drop)

    # Handle infinite values
    df.replace([float("inf"), -float("inf")], pd.NA, inplace=True)

    # Fill missing values instead of dropping rows
    df = df.fillna(0)

    print("Shape After Cleaning:", df.shape)
    return df


def map_labels(df):

    # Normalize label text
    df["Label"] = df["Label"].str.strip().str.lower()

    def map_attack(label):

        if "benign" in label:
            return "Normal"

        elif "dos" in label:
            return "DoS"

        elif "patator" in label:
            return "BruteForce"

        elif "brute force" in label:
            return "BruteForce"

        elif "xss" in label:
            return "XSS"

        else:
            return None

    df["Label"] = df["Label"].apply(map_attack)

    # Drop rows that don't match our target classes
    df = df.dropna(subset=["Label"])

    print("Label Mapping Done.")
    print(df["Label"].value_counts())

    return df


def save_processed_data(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print("Processed data saved successfully.")


if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    df = map_labels(df)
    save_processed_data(df)
