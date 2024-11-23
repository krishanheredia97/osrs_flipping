# api_client.py
import requests
import logging
from datetime import datetime, timedelta
import time
from config import API_BASE_URL, USER_AGENT

class RunescapeAPI:
    def __init__(self):
        self.headers = {"User-Agent": USER_AGENT}
        
    def get_timeseries_data(self, item_id, timestep, timestamp=None):
        url = f"{API_BASE_URL}/timeseries"
        params = {
            "id": item_id,
            "timestep": timestep
        }
        if timestamp:
            params["timestamp"] = timestamp
            
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()['data']
        except requests.RequestException as e:
            logging.error(f"Error fetching timeseries data: {e}")
            return None

    def fetch_full_year_data(self, item_id):
        all_data = []
        current_timestamp = None
        
        while len(all_data) < (365 * 24 * 12):  # Approximate 5min intervals in a year
            data_chunk = self.get_timeseries_data(item_id, "5m", current_timestamp)
            
            if not data_chunk or len(data_chunk) == 0:
                break
                
            all_data.extend(data_chunk)
            current_timestamp = data_chunk[-1]['timestamp']
            time.sleep(1)  # Be nice to the API
            
        return all_data