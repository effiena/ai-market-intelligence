def calculate_health_score(cycle, sentiment, history):

    score = 50  # neutral base

    # -------------------------
    # CYCLE (FIXED BALANCE)
    # -------------------------
    cycle_phase = cycle["cycle_phase"]

    if cycle_phase == "bull market expansion":
        score += 30
    elif cycle_phase == "early recovery":
        score += 20
    elif cycle_phase == "accumulation":
        score += 10
    else:
        score -= 10   # NOT -20 (was too harsh)

    # -------------------------
    # SENTIMENT (STRONGER IMPACT)
    # -------------------------
    sentiment_type = sentiment["sentiment"]

    if sentiment_type == "bullish":
        score += 25
    elif sentiment_type == "bearish":
        score -= 25

    # -------------------------
    # VOLATILITY (SOFTENED)
    # -------------------------
    volatility = history["volatility"]

    if volatility > 10:
        score -= 10
    elif volatility < 3:
        score += 5

    # -------------------------
    # FINAL CLAMP
    # -------------------------
    score = max(0, min(100, score))

    # -------------------------
    # STATUS
    # -------------------------
    if score >= 75:
        status = "strong bullish"
    elif score >= 60:
        status = "bullish recovery"
    elif score >= 40:
        status = "neutral"
    else:
        status = "bearish"

    # -------------------------
    # RISK
    # -------------------------
    if volatility > 10:
        risk = "high"
    elif volatility > 6:
        risk = "medium"
    else:
        risk = "low"

    return {
        "health_score": score,
        "status": status,
        "risk_level": risk,
        "summary": f"Market shows {status} conditions with {risk} risk."
    }
