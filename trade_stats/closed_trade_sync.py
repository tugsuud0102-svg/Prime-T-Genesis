from datetime import datetime,timezone,timedelta
import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5
from config.settings import BOT_MAGIC
from trade_stats.database import connect,initialize_database
from trade_stats.recorder import update_closed_trade
def sync_closed_trades(days=30):
    initialize_database()
    with connect() as db: ids=[r[0] for r in db.execute("SELECT position_id FROM trades WHERE status='OPEN' AND position_id IS NOT NULL")]
    if not ids or not initialize_mt5():return 0
    deals=mt5.history_deals_get(datetime.now(timezone.utc)-timedelta(days=days),datetime.now(timezone.utc)) or []; mt5.shutdown(); count=0
    for pid in ids:
        matches=[d for d in deals if getattr(d,"position_id",None)==pid and getattr(d,"magic",None)==BOT_MAGIC and getattr(d,"entry",None) in (getattr(mt5,"DEAL_ENTRY_OUT",1),getattr(mt5,"DEAL_ENTRY_OUT_BY",3))]
        if matches:
            profit=sum(float(getattr(d,"profit",0)) for d in matches); commission=sum(float(getattr(d,"commission",0)) for d in matches); swap=sum(float(getattr(d,"swap",0)) for d in matches); last=max(matches,key=lambda d:d.time)
            count+=update_closed_trade(pid,exit_time=datetime.fromtimestamp(last.time,timezone.utc).isoformat(),exit_price=last.price,profit=profit,commission=commission,swap=swap,net_profit=profit+commission+swap,exit_reason=getattr(last,"comment","") or "MT5 close")
    return count
