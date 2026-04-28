from scripts.ingestion.run_parse import run_parse_flow
from scripts.cleaning.run_clean import run_clean_flow
from scripts.analysis.run_analyze import run_enrichment_flow


def run_full_pipeline():
    """Execute the full backend processing pipeline."""
    run_parse_flow()
    run_clean_flow()
    run_enrichment_flow()
