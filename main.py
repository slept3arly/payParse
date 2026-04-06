import argparse
import sys
import os

# Ensure the root directory is in the path for modular imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.run_parse import run_parse_flow
from scripts.run_clean import run_clean_flow
from scripts.run_analyze import run_enrichment_flow

def main():
    parser = argparse.ArgumentParser(description="payParse - Data Processing Pipeline")
    parser.add_argument("--step", choices=["parse", "clean", "analyze", "all"], default="all",
                      help="Specific step to run (default: all)")
    
    args = parser.parse_args()

    if args.step in ["parse", "all"]:
        print("\n--- [Step 1] Parsing HTML Export ---")
        run_parse_flow()

    if args.step in ["clean", "all"]:
        print("\n--- [Step 2] Cleaning and Preprocessing ---")
        run_clean_flow()

    if args.step in ["analyze", "all"]:
        print("\n--- [Step 3] Categorizing Merchants (Google API) ---")
        run_enrichment_flow()

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()