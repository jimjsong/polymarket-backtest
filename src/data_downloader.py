import pandas as pd
import requests
import time
import os
from datetime import datetime

class DataDownloader:
    BASE_URL = "https://clob.polymarket.com/prices-history"

    def __init__(self):
        pass

    def fetch_candles(self, token_id, start_time, end_time):
        """
        Fetches historical trade data and converts it to a DataFrame.
        Args:
            token_id (str): The market token ID.
            start_time (int): Start timestamp (seconds).
            end_time (int): End timestamp (seconds).
        Returns:
            pd.DataFrame: DataFrame with columns [timestamp, price, size, side].
        """
        params = {
            "market": token_id,
            "startTs": int(start_time),
            "endTs": int(end_time)
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            history = data.get('history', [])
            if not history:
                print("No history found for the given range.")
                return pd.DataFrame(columns=['timestamp', 'price', 'size', 'side'])

            df = pd.DataFrame(history)
            # Ensure columns exist and are correct types
            # The API returns 't' (timestamp), 'p' (price), 's' (size), 'side' (side) usually.
            # Let's inspect the keys if we had data. Assuming standard CLOB format.
            # Based on similar APIs: t, p, s, side
            # Let's map them to more readable names if needed.

            # If the API returns dictionaries like {'t': ..., 'p': ...}
            # I will rename them if they match.
            rename_map = {'t': 'timestamp', 'p': 'price', 's': 'size'}
            df.rename(columns=rename_map, inplace=True)

            # Ensure timestamp is numeric
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_numeric(df['timestamp'])

            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()

class LiveRecorder:
    def __init__(self, token_id, output_file="live_data.csv"):
        self.token_id = token_id
        self.output_file = output_file
        self.recording = False

    def start_recording(self, duration_seconds=60, interval_seconds=5):
        """
        Simulates live recording by fetching order book snapshots.
        Since we can't easily get live trades without websocket,
        we'll use a snapshot endpoint or just simulate logging.
        The prompt says: "implement a 'Live Recorder' function that saves best-ask/bid snapshots to a CSV every 5 seconds."
        """
        self.recording = True
        start_time = time.time()

        # Check if file exists to write header
        file_exists = os.path.isfile(self.output_file)

        with open(self.output_file, 'a') as f:
            if not file_exists:
                f.write("timestamp,best_bid,best_ask\n")

            while time.time() - start_time < duration_seconds:
                snapshot = self._fetch_snapshot()
                if snapshot:
                    timestamp = int(time.time())
                    line = f"{timestamp},{snapshot['best_bid']},{snapshot['best_ask']}\n"
                    f.write(line)
                    f.flush()
                    print(f"Recorded snapshot at {timestamp}")

                time.sleep(interval_seconds)

    def _fetch_snapshot(self):
        # Fetch order book snapshot
        # https://clob.polymarket.com/book?token_id=...
        url = "https://clob.polymarket.com/book"
        params = {"token_id": self.token_id}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                # data structure: {'bids': [...], 'asks': [...]}
                bids = data.get('bids', [])
                asks = data.get('asks', [])

                best_bid = bids[0]['price'] if bids else 0
                best_ask = asks[0]['price'] if asks else 0

                return {'best_bid': best_bid, 'best_ask': best_ask}
            return None
        except Exception as e:
            print(f"Error fetching snapshot: {e}")
            return None

if __name__ == "__main__":
    # Test block
    downloader = DataDownloader()
    # Using the token ID from previous search
    token_id = "60720872908759207415849094365832344673404757243986952574612322985192917925291"
    start_ts = 1654100000
    end_ts = start_ts + 86400

    df = downloader.fetch_candles(token_id, start_ts, end_ts)
    print("Downloaded DataFrame:")
    print(df.head())

    # Test LiveRecorder
    print("Testing LiveRecorder...")
    recorder = LiveRecorder(token_id, output_file="test_live_data.csv")
    recorder.start_recording(duration_seconds=15, interval_seconds=5)
