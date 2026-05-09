
from fastapi import FastAPI, WebSocket
from market import get_coin_data
from market import get_coin_data, get_historical_data
from cycle_ai import detect_cycle
from sentiment_ai import analyze_sentiment
from health_ai import calculate_health_score
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
import asyncio

app = FastAPI()
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

COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA"]

@app.get("/")
def home():
    return {
        "status": "AI Market Intelligence Layer Running"
    }


@app.get("/coin/{coin_name}")
def coin(coin_name: str):
    return get_coin_data(coin_name)


@app.get("/history/{coin_name}")
def history(coin_name: str, days: int = 365):
    return get_historical_data(coin_name, days)

@app.get("/cycle/{coin_name}")
def cycle(coin_name: str, days: int = 365):
    history = get_historical_data(coin_name, days)
    
    if "error" in history:
        return history

    result = detect_cycle(history)

    return {
        "coin": coin_name,
        "history": history,
        "cycle_analysis": result
    }

@app.post("/sentiment")
def sentiment(data: dict):
    text = data.get("text", "")
    return analyze_sentiment(text)

class HealthRequest(BaseModel):
    text: str = "Bitcoin market update"


@app.post("/health/{coin}")
def health(coin: str, request: HealthRequest):

    valid_coins = ["bitcoin", "ethereum", "solana"]

    if coin not in valid_coins:
        return {"error": "Unsupported coin"}

    # 1. Get history
    history = get_historical_data(coin)

    # 2. Cycle AI
    cycle = detect_cycle(history)

    # 3. Sentiment AI
    sentiment = analyze_sentiment(request.text)

    # 4. Health score
    result = calculate_health_score(cycle, sentiment, history)

    return {
        "coin": coin,
        "health_analysis": result
    }

@app.post("/market/overview")
def market_overview(req: dict):

    coins = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA"]

    results = []

    for coin in coins:
        history = get_historical_data(coin)

        # SAFE GUARD (prevents crashes)
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

        await asyncio.sleep(3)  # live update every 3s
