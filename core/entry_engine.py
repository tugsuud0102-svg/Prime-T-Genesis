from dataclasses import dataclass
from config import settings
from score.score_engine import calculate_score

@dataclass
class TradeDecision:
    signal:str; entry:float; sl:float|None; tp:float|None; score:int; rating:str; reasons:list; confirmations:dict

def evaluate_entry(s):
    direction=s.bias; last=s.latest_completed_candle; prev=s.previous_candle
    aligned=lambda item:item.get("direction")==direction
    pullback=(direction=="BULLISH" and last.low<=last.EMA20 and last.close>last.EMA20) or (direction=="BEARISH" and last.high>=last.EMA20 and last.close<last.EMA20)
    confirmation=(direction=="BULLISH" and last.close>last.open and last.close>prev.high) or (direction=="BEARISH" and last.close<last.open and last.close<prev.low)
    pd_ok=(direction=="BULLISH" and s.premium_discount["zone"] in ("DISCOUNT","EQUILIBRIUM")) or (direction=="BEARISH" and s.premium_discount["zone"] in ("PREMIUM","EQUILIBRIUM"))
    pool_ok=(direction=="BULLISH" and s.liquidity_pools["buy_side_liquidity"] and s.liquidity_pools["buy_side_liquidity"]>s.entry) or (direction=="BEARISH" and s.liquidity_pools["sell_side_liquidity"] and s.liquidity_pools["sell_side_liquidity"]<s.entry)
    near=lambda item:item.get("inside_zone") or (item.get("distance") is not None and item["distance"]<=.5*s.atr)
    pa=s.price_action; pa_ok=any(x.get("detected") and x.get("direction",direction)==direction for x in (pa["pin_bar"],pa["engulfing"]))
    sr=s.support_resistance; sr_ok=(sr["support_distance"] if direction=="BULLISH" else sr["resistance_distance"]); sr_ok=sr_ok is not None and sr_ok<=s.atr
    checks={"trend_aligned":direction!="NONE","mtf_confluence_confirmed":s.mtf_confluence["confirmed"],"pullback_confirmed":pullback or confirmation,"bos_confirmed":aligned(s.bos),"choch_confirmed":aligned(s.choch),"mss_confirmed":aligned(s.mss),"premium_discount_confirmed":pd_ok,"liquidity_pool_confirmed":bool(pool_ok),"liquidity_sweep":aligned(s.liquidity_sweep),"fvg_confirmed":aligned(s.fvg) and near(s.fvg),"order_block_confirmed":aligned(s.order_block) and near(s.order_block),"supply_demand_confirmed":aligned(s.supply_demand) and near(s.supply_demand),"price_action_confirmed":pa_ok,"support_resistance_confirmed":sr_ok,"ema_slope_confirmed":s.ema_slope["direction"]==direction,"rsi_confirmed":settings.BUY_RSI_MIN<=s.rsi<=settings.BUY_RSI_MAX if direction=="BULLISH" else settings.SELL_RSI_MIN<=s.rsi<=settings.SELL_RSI_MAX if direction=="BEARISH" else False,"spread_confirmed":s.spread is not None and s.spread<=settings.MAX_SPREAD,"atr_confirmed":settings.MIN_ATR<=s.atr<=settings.MAX_ATR}
    scored=calculate_score(checks,settings.MIN_SIGNAL_SCORE); blockers=[]
    if direction=="NONE":blockers.append("No aligned EMA trend")
    if s.mtf_confluence["blocked"]:blockers.append("Opposite H4 trend")
    if s.choch["detected"] and s.choch["direction"]!=direction:blockers.append("Opposite CHoCH")
    if s.mss["detected"] and s.mss["direction"]!=direction:blockers.append("Opposite MSS")
    if not pd_ok:blockers.append("Wrong premium/discount value zone")
    if not scored["passed"]:blockers.append("Score below minimum")
    signal="BUY" if direction=="BULLISH" and not blockers else "SELL" if direction=="BEARISH" and not blockers else "NO_TRADE"
    sl=s.entry-s.atr*settings.SL_ATR_MULTIPLIER if signal=="BUY" else s.entry+s.atr*settings.SL_ATR_MULTIPLIER if signal=="SELL" else None
    tp=s.entry+s.atr*settings.TP_ATR_MULTIPLIER if signal=="BUY" else s.entry-s.atr*settings.TP_ATR_MULTIPLIER if signal=="SELL" else None
    return TradeDecision(signal,s.entry,sl,tp,scored["score"],scored["rating"],blockers+scored["failed_checks"],checks)
