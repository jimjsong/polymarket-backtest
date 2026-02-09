import requests
import json

def fetch_bitcoin_market():
    # Fetch events without filters first to avoid 422
    url = "https://gamma-api.polymarket.com/events?limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()
        events = response.json()

        for event in events:
            title = event.get("title", "")
            if "Bitcoin" in title or "BTC" in title:
                print(f"Event: {title}")
                for market in event.get("markets", []):
                     print(f"  Market: {market.get('question')}")
                     clob_token_ids = market.get('clobTokenIds')
                     print(f"  CLOB Token IDs: {clob_token_ids}")
                     if clob_token_ids and isinstance(clob_token_ids, list) and len(clob_token_ids) > 0:
                         # Usually 0 is YES, 1 is NO.
                         # But let's verify format. It seems to be a list of strings.
                         return clob_token_ids[0]
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return None

if __name__ == "__main__":
    token_id = fetch_bitcoin_market()
    if token_id:
        print(f"Found Token ID: {token_id}")
    else:
        print("No Bitcoin market found.")
