# main.py
import logging
from pathlib import Path
import json
from config import *
from api_client import RunescapeAPI
from data_processor import DataAnalyzer
from visualizer import PriceVisualizer
import sys
import traceback

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def save_data(data, filepath):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Error saving data to {filepath}: {e}")
        return False

def main():
    logger = setup_logging()
    logger.info("Starting historical data analysis")

    try:
        # Initialize components
        api_client = RunescapeAPI()
        analyzer = DataAnalyzer()
        visualizer = PriceVisualizer()

        # Fetch data
        logger.info(f"Fetching historical data for item {ITEM_ID}")
        raw_data = api_client.fetch_full_year_data(ITEM_ID)
        if not raw_data:
            logger.error("Failed to fetch data")
            return

        # Save raw data
        logger.info("Saving raw data")
        if not save_data(raw_data, RAW_DATA_FILE):
            logger.error("Failed to save raw data")
            return

        # Process data
        logger.info("Processing data")
        df = analyzer.convert_to_dataframe(raw_data)
        
        # Generate analysis
        logger.info("Generating analysis report")
        analysis_report = analyzer.generate_analysis_report(df)
        
        # Save analysis report
        logger.info("Saving analysis report")
        if not save_data(analysis_report, ANALYSIS_REPORT_FILE):
            logger.error("Failed to save analysis report")
            return

        # Create visualizations
        logger.info("Generating visualizations")
        fig = visualizer.create_price_chart(df)
        visualizer.save_plot()

        logger.info("Analysis complete")
        logger.info(f"Raw data saved to: {RAW_DATA_FILE}")
        logger.info(f"Analysis report saved to: {ANALYSIS_REPORT_FILE}")
        logger.info(f"Chart saved to: {CHART_FILE}")

    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()