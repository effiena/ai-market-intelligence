import requests
import pandas as pd

BASE_URL = "https://api.coingecko.com/api/v3"


def get_coin_data(coin="bitcoin"):
    url = f"{BASE_URL}/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": coin
    }

    response = requests.get(url, params=params)

    data = response.json()

    if not data:
        return {
            "error": "Coin not found"
        }

    coin_data = data[0]

    return {
        "name": coin_data["name"],
        "symbol": coin_data["symbol"],
        "price": coin_data["current_price"],
        "market_cap": coin_data["market_cap"],
        "volume": coin_data["total_volume"],
        "change_24h": coin_data["price_change_percentage_24h"]
    }

def get_historical_data(coin="bitcoin", days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

    params = {
        "vs_currency": "usd",
        "days": days
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = data.get("prices", [])

    if not prices:
        return {"error": "No data found"}

    df = pd.DataFrame(prices, columns=["timestamp", "price"])

    highest = df["price"].max()
    lowest = df["price"].min()

    growth = ((df["price"].iloc[-1] - df["price"].iloc[0]) / df["price"].iloc[0]) * 100

    volatility = df["price"].pct_change().std() * 100

    return {
        "coin": coin,
        "days": days,
        "highest_price": round(highest, 2),
        "lowest_price": round(lowest, 2),
        "growth_percent": round(growth, 2),
        "volatility": round(volatility, 2)
    }
