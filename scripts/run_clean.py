import pandas as pd
import os
from config import settings

def clean_transaction_data(df):
    """Apply cleaning transformations to transaction data."""
    if df is None:
        return None
        
    # Drop duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    # Fill missing merchant names
    df["merchant"] = df["merchant"].fillna("Unknown")

    # Normalize merchant names (strip spaces, title case)
    df["merchant"] = df["merchant"].astype(str).str.strip().str.title()

    # Feature engineering
    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["timestamp"].dt.day_name()
    df["hour"] = df["timestamp"].dt.hour
    df["month"] = df["timestamp"].dt.month_name()
    df["year"] = df["timestamp"].dt.year

    return df

def run_clean_flow():
    """Execution flow wrapper."""
    input_file = os.path.join(settings.PROCESSED_DATA_PATH, "transactions.csv")
    output_file = os.path.join(settings.PROCESSED_DATA_PATH, "transactions_cleaned.csv")

    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return

    df = pd.read_csv(input_file, parse_dates=["timestamp"])
    df_cleaned = clean_transaction_data(df)
    
    df_cleaned.to_csv(output_file, index=False)
    print(f"Saved cleaned data to {output_file} with {len(df_cleaned)} rows.")

if __name__ == "__main__":
    run_clean_flow()
