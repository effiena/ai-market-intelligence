from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import asyncio

from market import get_coin_data, get_historical_data
from cycle_ai import detect_cycle
from sentiment_ai import analyze_sentiment
from health_ai import calculate_health_score
from get_prices import get_live_prices



app = FastAPI()

# -----------------------------
# CORS CONFIG
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# COINS LIST
# -----------------------------
COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA"]


# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "AI Market Intelligence Layer Running"
    }


# -----------------------------
# COIN INFO
# -----------------------------
@app.get("/coin/{coin_name}")
def coin(coin_name: str):
    return get_coin_data(coin_name)


# -----------------------------
# HISTORY
# -----------------------------
@app.get("/history/{coin_name}")
def history(coin_name: str, days: int = 365):
    return get_historical_data(coin_name, days)


# -----------------------------
# CYCLE ANALYSIS
# -----------------------------
@app.get("/cycle/{coin_name}")
def cycle(coin_name: str, days: int = 365):
    history_data = get_historical_data(coin_name, days)

    if "error" in history_data:
        return history_data

    result = detect_cycle(history_data)

    return {
        "coin": coin_name,
        "history": history_data,
        "cycle_analysis": result
    }


# -----------------------------
# SENTIMENT
# -----------------------------
class SentimentRequest(BaseModel):
    text: str = ""


@app.post("/sentiment")
def sentiment(data: SentimentRequest):
    return analyze_sentiment(data.text)


# -----------------------------
# HEALTH ANALYSIS
# -----------------------------
class HealthRequest(BaseModel):
    text: str = "Bitcoin market update"


@app.post("/health/{coin}")
def health(coin: str, request: HealthRequest):

    valid_coins = ["bitcoin", "ethereum", "solana"]

    if coin not in valid_coins:
        return {"error": "Unsupported coin"}

    history_data = get_historical_data(coin)
    cycle = detect_cycle(history_data)
    sentiment = analyze_sentiment(request.text)

    result = calculate_health_score(cycle, sentiment, history_data)

    return {
        "coin": coin,
        "health_analysis": result
    }


# -----------------------------
# MARKET OVERVIEW (AI RANKING)
# -----------------------------
@app.post("/market/overview")
def market_overview(req: dict):

    results = []

    for coin in COINS:
        history = get_historical_data(coin)

        if not history:
            results.append({
                "coin": coin,
                "health_score": 0,
                "status": "no data",
                "risk": "unknown"
            })
            continue

        cycle = detect_cycle(history)

        results.append({
            "coin": coin,
            "health_score": cycle.get("signal_strength", 0),
            "status": cycle.get("cycle_phase", "unknown"),
            "risk": cycle.get("risk_level", "unknown")
        })

    return {"ranking": results}


# -----------------------------
# LIVE PRICES (NEW FIXED)
# -----------------------------
@app.get("/market/prices")
def market_prices():

    prices = get_live_prices()

    return {
        "prices": prices
    }


# -----------------------------
# WEBSOCKET LIVE MARKET STREAM
# -----------------------------
@app.websocket("/ws/market")
async def market_ws(websocket: WebSocket):
    await websocket.accept()

    while True:
        results = []

        for coin in COINS:
            history = get_historical_data(coin)
            cycle = detect_cycle(history)

            results.append({
                "coin": coin,
                "health_score": cycle.get("signal_strength", 0),
                "status": cycle.get("cycle_phase", "unknown"),
                "risk": cycle.get("risk_level", "unknown")
            })

        await websocket.send_json({
            "ranking": results
        })

        await asyncio.sleep(3)


