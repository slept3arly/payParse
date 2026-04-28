import os
import sys
import logging
import pandas as pd

# Ensure the root directory is in the path if run directly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.core import settings

logger = logging.getLogger(__name__)

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
        logger.error(f"Input file not found: {input_file}")
        return

    logger.info(f"Loading data from {input_file}")
    df = pd.read_csv(input_file, parse_dates=["timestamp"])
    df_cleaned = clean_transaction_data(df)
    
    df_cleaned.to_csv(output_file, index=False)
    logger.info(f"Saved cleaned data to {output_file} with {len(df_cleaned)} rows.")

if __name__ == "__main__":
    from app.core.settings import setup_logging
    setup_logging()
    run_clean_flow()
