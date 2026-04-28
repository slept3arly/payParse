import os
import sys
import logging
import pandas as pd

# Ensure the root directory is in the path if run directly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.core import settings
from app.utils.google_maps import query_google_places, score_match, map_types_to_category

logger = logging.getLogger(__name__)

def load_cache():
    """Load merchant categorization cache."""
    cache_file = settings.CACHE_PATH
    if os.path.exists(cache_file):
        return pd.read_csv(cache_file)
    
    return pd.DataFrame(columns=[
        "merchant_name", "city", "place_id", "name",
        "formatted_address", "types", "confidence_score", "category"
    ])

def save_cache(cache_df):
    """Save merchant categorization cache."""
    os.makedirs(os.path.dirname(settings.CACHE_PATH), exist_ok=True)
    cache_df.to_csv(settings.CACHE_PATH, index=False)

def categorize_merchant(merchant, cache_df, city=settings.USER_CITY):
    """High-level categorization logic with caching and Google API fallback."""
    # Check cache first
    existing = cache_df[(cache_df["merchant_name"] == merchant) & (cache_df["city"] == city)]
    if not existing.empty:
        return existing.iloc[0]["category"], cache_df

    # Query API
    result = query_google_places(merchant, city)
    if not result:
        return "Uncategorized", cache_df

    score = score_match(merchant, result, city)
    category = "Uncategorized"
    
    if score >= settings.CONFIDENCE_THRESHOLD:
        types = result.get("types", [])
        category = map_types_to_category(types)

    entry = {
        "merchant_name": merchant,
        "city": city,
        "place_id": result.get("place_id", ""),
        "name": result.get("name", ""),
        "formatted_address": result.get("formatted_address", ""),
        "types": ",".join(result.get("types", [])),
        "confidence_score": score,
        "category": category
    }

    cache_df = pd.concat([cache_df, pd.DataFrame([entry])], ignore_index=True)
    return category, cache_df

def run_enrichment_flow():
    """Main flow to enrich transactions with categories."""
    input_file = os.path.join(settings.PROCESSED_DATA_PATH, "transactions_cleaned.csv")
    output_file = os.path.join(settings.PROCESSED_DATA_PATH, "enriched_transactions.csv")

    if not os.path.exists(input_file):
        logger.error(f"Data not found: {input_file}")
        return

    df = pd.read_csv(input_file)
    cache_df = load_cache()

    merchants = df["merchant"].unique()
    categorization_map = {}

    logger.info(f"Processing {len(merchants)} unique merchants...")
    for idx, m in enumerate(merchants):
        category, cache_df = categorize_merchant(m, cache_df)
        categorization_map[m] = category
        if (idx + 1) % 10 == 0:
            logger.info(f"Processed {idx + 1}/{len(merchants)}...")
            save_cache(cache_df)  # Save periodically

    save_cache(cache_df)
    df["category"] = df["merchant"].map(categorization_map)
    
    df.to_csv(output_file, index=False)
    logger.info(f"Enriched data saved to {output_file}")

if __name__ == "__main__":
    from app.core.settings import setup_logging
    setup_logging()
    run_enrichment_flow()
