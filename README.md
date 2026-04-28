# PayParse

Transaction parsing and merchant enrichment pipeline for Google Pay data.

---

## Overview

PayParse is an early-stage prototype focused on processing raw payment history and transforming it into structured, analyzable data.

The project emphasizes:

- Data parsing and cleaning
- Feature extraction from transaction records
- Merchant enrichment using external APIs
- Preparing a foundation for future machine learning workflows

---

## Current Capabilities

- Parse Google Pay transaction history exports
- Clean and normalize raw transaction data
- Extract time-based features (hour, day, month)
- Enrich merchant data using Google Places API
- Perform heuristic-based categorization

---

## Tech Stack

- Python
- FastAPI (backend structure)
- Google Places API
- RapidFuzz (string matching)

---

## Project Status

⚠️ **Prototype / In Progress**

This project currently focuses on **data processing and enrichment**.  
It does **not yet include a trained ML model or predictive system**.

Planned improvements:

- Introduce a defined prediction task (e.g., spending classification or forecasting)
- Build training and evaluation pipeline
- Add model-based recommendations
- Improve generalization beyond single-user data

---

## Architecture (Current)

- Data ingestion → parsing and cleaning
- Feature engineering → timestamp-based features
- Merchant enrichment → API + fuzzy matching
- Output → structured dataset for analysis

---

## Limitations

- No machine learning model yet
- Limited dataset scope
- Depends on external API for enrichment
- No authentication or production deployment

---

## Purpose

- Explore financial data processing pipelines
- Serve as a base for future ML experimentation
- Understand real-world data cleaning and enrichment challenges

---

## Notes

This is an experimental project and is actively being improved.