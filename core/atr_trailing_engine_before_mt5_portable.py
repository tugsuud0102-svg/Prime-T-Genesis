import MetaTrader5 as mt5
from config.settings import ATR_TRAILING_MULTIPLIER
from core.mt5_actions import own_positions,modify_sl
from core.telegram_alert import send_telegram
from core.data_loader import get_candles
from indicators.atr import calculate_atr
def manage_atr_trailing():
    if not mt5.initialize():return 0
    count=0
    for p in own_positions():
        # Break-even is active only when SL protects entry.
        active=(p.type==mt5.POSITION_TYPE_BUY and p.sl>=p.price_open) or (p.type!=mt5.POSITION_TYPE_BUY and p.sl and p.sl<=p.price_open)
        if not active:continue
        tick=mt5.symbol_info_tick(p.symbol)
        try:d=get_candles(p.symbol,count=50); atr=float(calculate_atr(d).iloc[-2])
        except Exception:continue
        if not mt5.initialize():
            continue
        tick=mt5.symbol_info_tick(p.symbol)
        if not tick:
            continue
        candidate=(tick.bid-atr*ATR_TRAILING_MULTIPLIER) if p.type==mt5.POSITION_TYPE_BUY else (tick.ask+atr*ATR_TRAILING_MULTIPLIER)
        tighter=(p.type==mt5.POSITION_TYPE_BUY and candidate>p.sl) or (p.type!=mt5.POSITION_TYPE_BUY and candidate<p.sl)
        if tighter and modify_sl(p,candidate,"Prime T ATR trail"):count+=1; send_telegram(f"📈 ATR trail updated\n{p.symbol} #{p.ticket}\nSL: {candidate}")
    mt5.shutdown(); return count
