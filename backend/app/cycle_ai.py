import numpy as np

def get_historical_data(coin):
    return {
        "prices": [100, 110, 120],
        "volatility": 3,
        "growth_percent": 5
    }

def detect_cycle(historical_data):
    prices = historical_data.get("prices", [])
    volatility = historical_data.get("volatility", 0)

    if len(prices) >= 2:
        growth = ((prices[-1] - prices[0]) / prices[0]) * 100
    else:
        growth = historical_data.get("growth_percent", 0)

    if growth > 200:
        cycle = "bull market expansion"
    elif growth > 50:
        cycle = "early recovery"
    elif growth > 0:
        cycle = "accumulation"
    else:
        cycle = "bear market"

    if volatility > 8:
        risk = "high"
    elif volatility > 4:
        risk = "medium"
    else:
        risk = "low"

    signal_strength = max(0, min(100, int(growth / 3 + (10 - volatility) * 5)))

    return {
        "cycle_phase": cycle,
        "risk_level": risk,
        "signal_strength": signal_strength,
        "growth": growth,
        "volatility": volatility
    }
