from dataclasses import dataclass
from typing import Any
import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5
from core.data_loader import get_candles
from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr
from indicators.bos import detect_bos
from indicators.choch import detect_choch
from indicators.mss import detect_mss
from indicators.liquidity import detect_liquidity_sweep
from indicators.liquidity_pools import detect_liquidity_pools
from indicators.fvg import detect_fvg
from indicators.order_block import detect_order_block
from indicators.supply_demand import detect_supply_demand
from indicators.support_resistance import detect_support_resistance
from indicators.price_action import detect_price_action
from indicators.premium_discount import detect_premium_discount
from indicators.ema_slope import detect_ema_slope
from core.mtf_confluence import evaluate_mtf_confluence

@dataclass
class MarketSnapshot:
    symbol:str; dataframe:Any; completed_candles:Any; latest_completed_candle:Any; previous_candle:Any; entry:float; atr:float; rsi:float; spread:float|None; h1_trend:str; h4_trend:str; bias:str; bos:dict; choch:dict; mss:dict; premium_discount:dict; liquidity_sweep:dict; liquidity_pools:dict; fvg:dict; order_block:dict; supply_demand:dict; support_resistance:dict; price_action:dict; ema_slope:dict; mtf_confluence:dict

def _trend(symbol,timeframe,count=250):
    if not initialize_mt5(): return "NONE"
    rates=mt5.copy_rates_from_pos(symbol,timeframe,0,count); mt5.shutdown()
    if rates is None or len(rates)<201:return "NONE"
    import pandas as pd
    d=pd.DataFrame(rates); e50=d.close.ewm(span=50,adjust=False).mean().iloc[-2]; e200=d.close.ewm(span=200,adjust=False).mean().iloc[-2]
    return "BULLISH" if e50>e200 else "BEARISH" if e50<e200 else "NEUTRAL"

def build_market_snapshot(symbol):
    df=get_candles(symbol,count=300).copy()
    for n in (20,50,200):df[f"EMA{n}"]=calculate_ema(df,n)
    df["RSI"]=calculate_rsi(df); df["ATR"]=calculate_atr(df)
    completed=df.iloc[:-1].dropna().copy()
    if len(completed)<205: raise RuntimeError("Insufficient completed candle history")
    last,prev=completed.iloc[-1],completed.iloc[-2]; atr=float(last.ATR); price=float(last.close)
    bias="BULLISH" if last.close>last.EMA20>last.EMA50>last.EMA200 else "BEARISH" if last.close<last.EMA20<last.EMA50<last.EMA200 else "NONE"
    h1=_trend(symbol,mt5.TIMEFRAME_H1); h4=_trend(symbol,mt5.TIMEFRAME_H4)
    if not initialize_mt5(): spread=None
    else:
        tick=mt5.symbol_info_tick(symbol); spread=abs(tick.ask-tick.bid) if tick else None; mt5.shutdown()
    bos=detect_bos(completed); choch=detect_choch(completed,bias); mss=detect_mss(completed,bias,atr)
    return MarketSnapshot(symbol,df,completed,last,prev,price,atr,float(last.RSI),spread,h1,h4,bias,bos,choch,mss,detect_premium_discount(completed),detect_liquidity_sweep(completed),detect_liquidity_pools(completed,atr),detect_fvg(completed,atr),detect_order_block(completed,atr),detect_supply_demand(completed,atr),detect_support_resistance(completed),detect_price_action(completed),detect_ema_slope(completed),evaluate_mtf_confluence(bias,h1,h4))
