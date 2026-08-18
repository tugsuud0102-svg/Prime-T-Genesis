from config.settings import SYMBOL,TRADING_MODE
from core.market_engine import build_market_snapshot
from core.entry_engine import evaluate_entry

def run_signal_cycle(symbol=SYMBOL):
    s=build_market_snapshot(symbol); d=evaluate_entry(s); l=s.latest_completed_candle
    print("="*62); print("Prime T Genesis v4.1.3 - MODULAR SIGNAL ENGINE"); print(f"Mode      : {TRADING_MODE}\nSymbol    : {symbol}\nClose     : {s.entry:.2f}\nEMA20     : {l.EMA20:.2f}\nEMA50     : {l.EMA50:.2f}\nEMA200    : {l.EMA200:.2f}\nRSI       : {s.rsi:.2f}\nATR       : {s.atr:.2f}\nSpread    : {s.spread if s.spread is not None else 'N/A'}\nH1 Trend  : {s.h1_trend}\nH4 Trend  : {s.h4_trend}\nBias      : {s.bias}"); print("-"*62)
    print(f"BOS       : {s.bos['direction']}\nCHoCH     : {s.choch['direction']}\nMSS       : {s.mss['direction']} ({s.mss['strength']})\nPremium   : {s.premium_discount['zone']} | EQ={s.premium_discount['equilibrium']:.2f} | Pos={s.premium_discount['position_percent']:.1f}%\nLiquidity : {s.liquidity_sweep['direction']}\nEQH/EQL   : H={s.liquidity_pools['equal_highs_detected']} L={s.liquidity_pools['equal_lows_detected']} | Nearest={s.liquidity_pools['nearest_pool']}\nPool Lvls : BUY={s.liquidity_pools['buy_side_liquidity']} | SELL={s.liquidity_pools['sell_side_liquidity']}\nFVG       : {s.fvg['direction']}\nOB        : {s.order_block['direction']}\nS/D       : {s.supply_demand['zone_type']}\nPin Bar   : {s.price_action['pin_bar']}\nEngulfing : {s.price_action['engulfing']}\nEMA Slope : {s.ema_slope['direction']}\nMTF       : {s.mtf_confluence['strength']} | H1={s.h1_trend} | H4={s.h4_trend} | Align={s.mtf_confluence['alignment_count']}/2\nScore     : {d.score}/100 | {d.rating}"); print("="*62); print(f"SIGNAL: {d.signal}")
    return s,d
