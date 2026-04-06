import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# API Settings
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
USER_CITY = os.getenv("USER_CITY", "Vellore, Tamil Nadu")

# Process settings
CONFIDENCE_THRESHOLD = int(os.getenv("CONFIDENCE_THRESHOLD", 70))

# Path settings
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
CACHE_PATH = "data/cache/merchant_cache.csv"

# Logging configuration
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
