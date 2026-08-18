from indicators.swing_points import detect_swing_points

def detect_liquidity_pools(df, atr, tolerance_atr=.15):
    swings = detect_swing_points(df)
    price, tolerance = float(df.iloc[-1]["close"]), max(float(atr or 0)*tolerance_atr, 1e-9)
    def cluster(items):
        best=[]
        for item in items:
            group=[x for x in items if abs(x["level"]-item["level"]) <= tolerance]
            if len(group)>len(best): best=group
        return best
    eh, el = cluster(swings["highs"]), cluster(swings["lows"])
    buy = sum(x["level"] for x in eh)/len(eh) if len(eh)>=2 else None
    sell = sum(x["level"] for x in el)/len(el) if len(el)>=2 else None
    candidates=[("BUY_SIDE",buy), ("SELL_SIDE",sell)]
    candidates=[x for x in candidates if x[1] is not None]
    nearest=min(candidates,key=lambda x:abs(x[1]-price)) if candidates else ("NONE",None)
    return {"equal_highs_detected": buy is not None, "equal_lows_detected": sell is not None, "buy_side_liquidity": buy, "sell_side_liquidity": sell, "equal_high_touches": len(eh) if buy else 0, "equal_low_touches": len(el) if sell else 0, "equal_high_distance": abs(buy-price) if buy else None, "equal_low_distance": abs(sell-price) if sell else None, "nearest_pool": nearest[0], "nearest_pool_level": nearest[1]}
