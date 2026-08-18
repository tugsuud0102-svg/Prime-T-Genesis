from pathlib import Path
import math
import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5
from config.settings import PARTIAL_CLOSE_ENABLED,PARTIAL_CLOSE_TRIGGER_R,PARTIAL_CLOSE_PERCENT
from core.mt5_actions import own_positions,close_position
from core.telegram_alert import send_telegram
STATE=Path("data/partial_close")
def manage_partial_close():
    if not PARTIAL_CLOSE_ENABLED or not initialize_mt5():return 0
    STATE.mkdir(parents=True,exist_ok=True); count=0
    for p in own_positions():
        marker=STATE/f"{p.ticket}.done"
        if marker.exists() or not p.sl:continue
        tick=mt5.symbol_info_tick(p.symbol); info=mt5.symbol_info(p.symbol)
        if not tick or not info:continue
        price=tick.bid if p.type==mt5.POSITION_TYPE_BUY else tick.ask; risk=abs(p.price_open-p.sl); r=((price-p.price_open) if p.type==mt5.POSITION_TYPE_BUY else (p.price_open-price))/risk
        step=info.volume_step or .01; close=math.floor((p.volume*PARTIAL_CLOSE_PERCENT)/step)*step; close=round(close,8); remaining=round(p.volume-close,8)
        if r>=PARTIAL_CLOSE_TRIGGER_R and close>=info.volume_min and remaining>=info.volume_min:
            result=close_position(p,close,"Prime T partial close")
            if result:marker.write_text(str(result.deal),encoding="utf-8"); count+=1; send_telegram(f"✂️ Partial close completed\n{p.symbol} #{p.ticket}\nVolume: {close}")
    mt5.shutdown(); return count
