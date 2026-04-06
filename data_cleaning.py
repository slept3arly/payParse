import pandas as pd
import re

# Load parsed transactions
df = pd.read_csv("Assets/transactions.csv", parse_dates=["timestamp"])

# Drop duplicates
df = df.drop_duplicates().reset_index(drop=True)

# Fill missing merchant names
df["merchant"] = df["merchant"].fillna("Unknown")

# Normalize merchant names (strip spaces, title case)
df["merchant"] = df["merchant"].astype(str).str.strip().str.title()

# Add time-based features
df["date"] = df["timestamp"].dt.date
df["time"] = df["timestamp"].dt.time
df["weekday"] = df["timestamp"].dt.day_name()
df["hour"] = df["timestamp"].dt.hour
df["month"] = df["timestamp"].dt.month_name()
df["year"] = df["timestamp"].dt.year

# Optional: flag transactions with missing time
df["has_time"] = df["time"].astype(str) != "NaT"

# Optional: categorize merchants (customize this!)
merchant_map = {
    "Amazon I": "Shopping",
    "Google P": "Transfer",
    "Zomato": "Food",
    "Swiggy": "Food",
    "Bank Transfer": "Transfer",
    "Wallet Top-Up": "Top-up",
    "Refund": "Refund",
}
df["category"] = df["merchant"].map(merchant_map).fillna("Other")

# Save cleaned data
df.to_csv("Assets/transactions_cleaned.csv", index=False)
print("Saved cleaned data with", len(df), "rows.")