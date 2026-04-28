import re
import pandas as pd

def normalize_timestamp(raw_timestamp):
    """Clean and normalize timestamp strings."""
    cleaned = re.sub(r"[^\x00-\x7F]+", " ", raw_timestamp)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned.replace("Sept", "Sep")

def extract_merchant_and_type(first_line):
    """Determine transaction type and merchant name from Google activity line."""
    merchant = None
    txn_type = None
    fl = first_line.lower()

    if fl.startswith("paid"):
        txn_type = "Paid"
        if "to " in first_line:
            merchant = first_line.split("to ")[1].split(" using")[0]

    elif fl.startswith("sent"):
        txn_type = "Sent"
        merchant = "Bank Transfer"

    elif fl.startswith("received"):
        txn_type = "Received"
        if "from " in first_line:
            merchant = first_line.split("from ")[1].split(" using")[0]

    elif "added to" in fl:
        txn_type = "Top-up"
        merchant = "Wallet Top-up"

    elif fl.startswith("refunded"):
        txn_type = "Refunded"
        if "from " in first_line:
            merchant = first_line.split("from ")[1].split(" using")[0]
        else:
            merchant = "Refund"

    # Fallbacks
    if txn_type is None:
        txn_type = "Other"
    if merchant is None:
        if txn_type == "Sent":
            merchant = "Bank Transfer"
        elif txn_type == "Top-up":
            merchant = "Wallet Top-up"
        elif txn_type == "Refunded":
            merchant = "Refund"
        else:
            merchant = "Unknown"
    
    return txn_type, merchant

def parse_amount(first_line):
    """Extract numeric amount from the first line."""
    amount_match = re.search(r"₹\s*([\d,]+\.?\d*)", first_line)
    return float(amount_match.group(1).replace(",", "")) if amount_match else None
