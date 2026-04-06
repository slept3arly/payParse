import os
import shutil
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config.settings import setup_logging, RAW_DATA_PATH, PROCESSED_DATA_PATH
import pandas as pd

# Import our processing flows
from scripts.run_parse import run_parse_flow
from scripts.run_clean import run_clean_flow
from scripts.run_analyze import run_enrichment_flow

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="payParse API", version="1.0.0")

# CORS Configuration - Broaden for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # More permissive for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "payParse API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload Google Activity HTML file."""
    if not file.filename.endswith(".html"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an HTML file.")
    
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    target_path = os.path.join(RAW_DATA_PATH, "My Activity.html")
    
    try:
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File uploaded successfully: {file.filename}")
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_data():
    """Trigger the full processing pipeline."""
    try:
        logger.info("Starting pipeline execution via API...")
        
        # Step 1: Parse
        run_parse_flow()
        
        # Step 2: Clean
        run_clean_flow()
        
        # Step 3: Analyze (Enrich)
        run_enrichment_flow()
        
        logger.info("Pipeline execution completed successfully.")
        return {"message": "Processing completed successfully"}
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/transactions")
async def get_transactions():
    """Return the final enriched transaction data."""
    processed_file = os.path.join(PROCESSED_DATA_PATH, "enriched_transactions.csv")
    
    if not os.path.exists(processed_file):
        # Fallback to cleaned transactions if enrichment hasn't run or failed
        processed_file = os.path.join(PROCESSED_DATA_PATH, "transactions_cleaned.csv")
        
    if not os.path.exists(processed_file):
        raise HTTPException(status_code=404, detail="No processed data found. Please run processing first.")
    
    try:
        df = pd.read_csv(processed_file)
        # Handle NaN values specifically for JSON compatibility
        df = df.fillna("")
        data = df.to_dict(orient="records")
        return {"data": data, "count": len(data)}
    except Exception as e:
        logger.error(f"Error reading processed data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
