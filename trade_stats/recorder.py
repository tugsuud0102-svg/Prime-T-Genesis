from datetime import datetime,timezone
from trade_stats.database import connect,initialize_database,COLUMNS
def open_trade_exists(position_id):
    initialize_database()
    with connect() as db:return db.execute("SELECT 1 FROM trades WHERE position_id=? AND status='OPEN' LIMIT 1",(position_id,)).fetchone() is not None
def insert_open_trade(**trade):
    initialize_database(); trade.setdefault("status","OPEN"); trade.setdefault("entry_time",datetime.now(timezone.utc).isoformat()); allowed={k:v for k,v in trade.items() if k in COLUMNS and k!="id"}
    with connect() as db:
        cur=db.execute(f"INSERT INTO trades ({','.join(allowed)}) VALUES ({','.join('?' for _ in allowed)})",tuple(allowed.values())); return cur.lastrowid
def update_closed_trade(position_id,**values):
    initialize_database(); values.setdefault("status","CLOSED"); values.setdefault("exit_time",datetime.now(timezone.utc).isoformat()); allowed={k:v for k,v in values.items() if k in COLUMNS and k not in ("id","position_id")}
    with connect() as db:return db.execute(f"UPDATE trades SET {','.join(k+'=?' for k in allowed)} WHERE position_id=? AND status='OPEN'",tuple(allowed.values())+(position_id,)).rowcount
