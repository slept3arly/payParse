import re
import pandas as pd
from bs4 import BeautifulSoup

file_path = r"Assets/My Activity.html"

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

        # Normalize timestamp string
        cleaned_timestamp = re.sub(r"[^\x00-\x7F]+", " ", raw_timestamp)
        cleaned_timestamp = re.sub(r"\s+", " ", cleaned_timestamp).strip()

        # Fix non-standard month abbreviation
        cleaned_timestamp = cleaned_timestamp.replace("Sept", "Sep")

        # Amount
        amount_match = re.search(r"₹\s*([\d,]+\.?\d*)", first_line)
        amount = float(amount_match.group(1).replace(",", "")) if amount_match else None

        # Transaction type + merchant
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

        # Transaction ID and Status
        txn_id = None
        status = None
        for line in lines:
            if line.startswith("Details:"):
                txn_id = line.replace("Details:", "").strip()
            if "Completed" in line:
                status = "Completed"

        transactions.append([cleaned_timestamp, txn_type, merchant, amount, txn_id, status])

    except Exception as e:
        print("Skipping block due to error:", e)

# Build DataFrame
df = pd.DataFrame(
    transactions,
    columns=["timestamp", "transaction_type", "merchant", "amount", "transaction_id", "status"]
)

# Parse timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Add separate date and time columns
df["date"] = df["timestamp"].dt.date
df["time"] = df["timestamp"].dt.time

# Clean amount
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Drop rows with no amount
df = df.dropna(subset=["amount"]).reset_index(drop=True)



csv_path = r"Assets/transactions.csv"
df.to_csv(csv_path, index=False)
print("Saved", len(df), "transactions to transactions.csv")