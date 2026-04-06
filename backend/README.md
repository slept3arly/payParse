# payParse

A Python tool to parse, clean, and categorize transactions from Google Pay activity exports.

## Features
- **Security-First**: Environment variables for API keys and data isolation.
- **Automated Categorization**: Uses Google Places API to identify merchant types.
- **Fast Processing**: Caching mechanism to avoid redundant API calls.
- **Modular Design**: Separate parsing, cleaning, and analysis steps.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_PLACES_API_KEY
   ```

## Usage
Run the full pipeline:
```bash
python main.py
```
Run specific steps:
```bash
python main.py --step parse
python main.py --step clean
python main.py --step analyze
```

## Project Structure
- `config/`: Application settings.
- `data/`: Storage for raw and processed data (ignored by git).
- `src/`: Core logic and utilities.
- `scripts/`: Implementation scripts forEach stage.
- `main.py`: Entry point for the application.

## Security
This project uses `.env` for managing secrets. Ensure `.env` is never committed to source control.
