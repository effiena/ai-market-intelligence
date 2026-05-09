import requests
import time

COINS_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano"
}

# CACHE
cached_prices = {}
last_fetch = 0

def get_live_prices():

    global cached_prices
    global last_fetch

    # cache for 30 seconds
    if time.time() - last_fetch < 30 and cached_prices:
        return cached_prices

    ids = ",".join(COINS_MAP.values())

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd"
    )

    try:
        response = requests.get(
            url,
            headers={
                "accept": "application/json",
                "user-agent": "Mozilla/5.0"
            },
            timeout=10
        )

        data = response.json()

        print("COINGECKO RESPONSE:", data)

        # rate limit protection
        if "status" in data:
            print("RATE LIMITED — USING CACHE")
            return cached_prices

        prices = {}

        for symbol, coin_id in COINS_MAP.items():

            if coin_id in data:
                prices[symbol] = data[coin_id].get("usd", 0)
            else:
                prices[symbol] = 0

        cached_prices = prices
        last_fetch = time.time()

        return prices

    except Exception as e:
        print("PRICE ERROR:", e)

        return cached_prices
