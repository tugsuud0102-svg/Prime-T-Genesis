import MetaTrader5 as mt5
from config.settings import BREAK_EVEN_ENABLED,BREAK_EVEN_TRIGGER_R,BREAK_EVEN_OFFSET_POINTS,BOT_MAGIC
from core.mt5_actions import own_positions,modify_sl
from core.telegram_alert import send_telegram
def manage_break_even():
    if not BREAK_EVEN_ENABLED or not mt5.initialize():return 0
    changed=0
    for p in own_positions():
        risk=abs(p.price_open-p.sl) if p.sl else 0
        tick=mt5.symbol_info_tick(p.symbol)
        if not risk or not tick:continue
        price=tick.bid if p.type==mt5.POSITION_TYPE_BUY else tick.ask; r=(price-p.price_open)/risk if p.type==mt5.POSITION_TYPE_BUY else (p.price_open-price)/risk
        point=(mt5.symbol_info(p.symbol).point or 0); candidate=p.price_open+(BREAK_EVEN_OFFSET_POINTS*point if p.type==mt5.POSITION_TYPE_BUY else -BREAK_EVEN_OFFSET_POINTS*point)
        protected=(p.type==mt5.POSITION_TYPE_BUY and (not p.sl or candidate>p.sl)) or (p.type!=mt5.POSITION_TYPE_BUY and (not p.sl or candidate<p.sl))
        if r>=BREAK_EVEN_TRIGGER_R and protected and p.magic==BOT_MAGIC and modify_sl(p,candidate,"Prime T break even"):
            changed+=1; send_telegram(f"🛡 Break-even active\n{p.symbol} #{p.ticket}\nSL: {candidate}")
    mt5.shutdown(); return changed
