# config.py
import os
from pathlib import Path

# API Configuration
API_BASE_URL = "https://prices.runescape.wiki/api/v1/osrs"
USER_AGENT = "Historical Analysis Bot - TalAslan"
ITEM_ID = 565  # Blood rune

# Time Configuration
TIMESTEP = "5m"
DAYS_TO_ANALYZE = 365

# Output Configuration
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
RAW_DATA_FILE = OUTPUT_DIR / "raw_data.json"
ANALYSIS_REPORT_FILE = OUTPUT_DIR / "analysis_report.json"
CHART_FILE = OUTPUT_DIR / "price_analysis.png"

# Logging Configuration
LOG_FILE = OUTPUT_DIR / "analysis.log"