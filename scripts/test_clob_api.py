import requests
import time
import json

def test_api():
    token_id = "42334954850219754195241248003172889699504912694714162671145392673031415571339"
    url = "https://clob.polymarket.com/prices-history"

    start_ts = 1735689600 # Jan 1 2025
    end_ts = 1735776000 # Jan 2 2025

    params = {
        "market": token_id,
        "startTs": start_ts,
        "endTs": end_ts
    }

    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        print(f"URL: {response.url}")
        if response.status_code == 200:
            data = response.json()
            history = data.get('history', [])
            print(f"Data length: {len(history)}")
            if len(history) > 0:
                print(f"First item: {history[0]}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
