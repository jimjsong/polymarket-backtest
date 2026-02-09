import requests
import json

def fetch_active_market():
    url = "https://gamma-api.polymarket.com/events?limit=20&active=true&closed=false&order=volume&ascending=false"
    try:
        response = requests.get(url)
        response.raise_for_status()
        events = response.json()

        for event in events:
            markets = event.get("markets", [])
            for market in markets:
                clob_token_ids_raw = market.get('clobTokenIds')
                if clob_token_ids_raw:
                    try:
                        if isinstance(clob_token_ids_raw, str):
                            clob_token_ids = json.loads(clob_token_ids_raw)
                        else:
                            clob_token_ids = clob_token_ids_raw

                        if isinstance(clob_token_ids, list) and len(clob_token_ids) > 0:
                            print(f"Market: {market.get('question')}")
                            print(f"CLOB Token ID: {clob_token_ids[0]}")
                            return clob_token_ids[0]
                    except Exception as e:
                        print(f"Error parsing token IDs: {e}")

    except Exception as e:
        print(f"Error fetching markets: {e}")
        return None

if __name__ == "__main__":
    token_id = fetch_active_market()
    if token_id:
        print(f"Found Active Token ID: {token_id}")
    else:
        print("No active market found.")
