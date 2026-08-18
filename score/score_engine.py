WEIGHTS={"trend_aligned":12,"mtf_confluence_confirmed":10,"pullback_confirmed":7,"bos_confirmed":7,"choch_confirmed":5,"mss_confirmed":7,"premium_discount_confirmed":6,"liquidity_pool_confirmed":5,"liquidity_sweep":5,"fvg_confirmed":5,"order_block_confirmed":5,"supply_demand_confirmed":4,"price_action_confirmed":5,"support_resistance_confirmed":3,"ema_slope_confirmed":4,"rsi_confirmed":4,"spread_confirmed":3,"atr_confirmed":3}
assert sum(WEIGHTS.values()) == 100

def calculate_score(checks, minimum=60):
    normalized={name:bool(checks.get(name,False)) for name in WEIGHTS}; value=sum(WEIGHTS[k] for k,v in normalized.items() if v)
    rating="EXCELLENT" if value>=85 else "GOOD" if value>=70 else "ACCEPTABLE" if value>=60 else "WEAK"
    return {"score":value,"rating":rating,"passed":value>=minimum,"failed_checks":[k for k,v in normalized.items() if not v],"checks":normalized}
