# data_processor.py
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging

class DataAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def convert_to_dataframe(self, raw_data):
        try:
            self.logger.info("Converting raw data to DataFrame")
            df = pd.DataFrame(raw_data)
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('datetime', inplace=True)
            self.logger.info(f"Created DataFrame with {len(df)} rows")
            return df
        except Exception as e:
            self.logger.error(f"Error converting data to DataFrame: {e}")
            raise

    def _convert_numpy_types(self, obj):
        """Convert numpy types to Python native types"""
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._convert_numpy_types(item) for item in obj]
        return obj

    def calculate_price_statistics(self, df):
        try:
            self.logger.info("Calculating price statistics")
            stats = {
                'highest_price': {
                    'value': float(df['avgHighPrice'].max()),
                    'timestamp': df['avgHighPrice'].idxmax().strftime('%Y-%m-%d %H:%M')
                },
                'lowest_price': {
                    'value': float(df['avgLowPrice'].min()),
                    'timestamp': df['avgLowPrice'].idxmin().strftime('%Y-%m-%d %H:%M')
                },
                'average_price': float(df['avgHighPrice'].mean()),
                'price_volatility': float(df['avgHighPrice'].std()),
                'typical_daily_range': float(df.groupby(df.index.date)['avgHighPrice'].agg(lambda x: x.max() - x.min()).mean())
            }
            return self._convert_numpy_types(stats)
        except Exception as e:
            self.logger.error(f"Error calculating price statistics: {e}")
            raise

    def calculate_volume_statistics(self, df):
        try:
            self.logger.info("Calculating volume statistics")
            stats = {
                'average_daily_volume': float(df.groupby(df.index.date)['highPriceVolume'].sum().mean()),
                'peak_volume': {
                    'value': int(df['highPriceVolume'].max()),
                    'timestamp': df['highPriceVolume'].idxmax().strftime('%Y-%m-%d %H:%M')
                },
                'total_volume': int(df['highPriceVolume'].sum())
            }
            return self._convert_numpy_types(stats)
        except Exception as e:
            self.logger.error(f"Error calculating volume statistics: {e}")
            raise

    def analyze_trading_patterns(self, df):
        try:
            self.logger.info("Analyzing trading patterns")
            df['price_change'] = df['avgHighPrice'].diff()
            patterns = {
                'average_5min_movement': float(df['price_change'].abs().mean()),
                'positive_movements': int((df['price_change'] > 0).sum()),
                'negative_movements': int((df['price_change'] < 0).sum())
            }
            return self._convert_numpy_types(patterns)
        except Exception as e:
            self.logger.error(f"Error analyzing trading patterns: {e}")
            raise

    def generate_analysis_report(self, df):
        try:
            self.logger.info("Generating complete analysis report")
            report = {
                'price_statistics': self.calculate_price_statistics(df),
                'volume_statistics': self.calculate_volume_statistics(df),
                'trading_patterns': self.analyze_trading_patterns(df)
            }
            return self._convert_numpy_types(report)
        except Exception as e:
            self.logger.error(f"Error generating analysis report: {e}")
            raise