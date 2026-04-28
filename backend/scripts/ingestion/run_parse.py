import os
import sys
import logging
from bs4 import BeautifulSoup
import pandas as pd

# Ensure the root directory is in the path if run directly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.core import settings
from app.utils.cleaning import normalize_timestamp, extract_merchant_and_type, parse_amount

logger = logging.getLogger(__name__)

def parse_activity_html(file_path):
    """Main parsing function to convert Google Activity HTML to DataFrame."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    blocks = soup.find_all("div", class_="content-cell")
    transactions = []

    for block in blocks:
        try:
            lines = block.get_text(separator="\n").split("\n")
            lines = [l.strip() for l in lines if l.strip()]
            if len(lines) < 2:
                continue

            first_line = lines[0]
            raw_timestamp = lines[1]

            cleaned_timestamp = normalize_timestamp(raw_timestamp)
            txn_type, merchant = extract_merchant_and_type(first_line)
            amount = parse_amount(first_line)

            # Transaction ID and Status
            txn_id = None
            status = "Pending"  # Default if not found
            for line in lines:
                if line.startswith("Details:"):
                    txn_id = line.replace("Details:", "").strip()
                if "Completed" in line:
                    status = "Completed"

            transactions.append([cleaned_timestamp, txn_type, merchant, amount, txn_id, status])

        except Exception as e:
            logger.warning(f"Skipping block due to error: {e}")

    df = pd.DataFrame(
        transactions,
        columns=["timestamp", "transaction_type", "merchant", "amount", "transaction_id", "status"]
    )

    # Conversion logic
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["date"] = df["timestamp"].dt.date
    df["time"] = df["timestamp"].dt.time
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"]).reset_index(drop=True)
    
    return df

def run_parse_flow():
    """Execution flow wrapper."""
    input_file = os.path.join(settings.RAW_DATA_PATH, "My Activity.html")
    output_file = os.path.join(settings.PROCESSED_DATA_PATH, "transactions.csv")
    
    logger.info(f"Starting parsing: {input_file}")
    df = parse_activity_html(input_file)
    
    if df is not None:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        logger.info(f"Successfully saved {len(df)} transactions to {output_file}")
    else:
        logger.error("Parsing failed.")

if __name__ == "__main__":
    from app.core.settings import setup_logging
    setup_logging()
    run_parse_flow()
