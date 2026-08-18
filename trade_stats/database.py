from pathlib import Path
import sqlite3
DB_PATH=Path("data/statistics.db")
COLUMNS={"id":"INTEGER PRIMARY KEY AUTOINCREMENT","ticket":"INTEGER","deal":"INTEGER","order_id":"INTEGER","position_id":"INTEGER","symbol":"TEXT","signal":"TEXT","status":"TEXT DEFAULT 'OPEN'","entry_time":"TEXT","exit_time":"TEXT","entry_price":"REAL","exit_price":"REAL","volume":"REAL","sl":"REAL","tp":"REAL","profit":"REAL DEFAULT 0","commission":"REAL DEFAULT 0","swap":"REAL DEFAULT 0","net_profit":"REAL DEFAULT 0","rr":"REAL","score":"REAL","rating":"TEXT","bos":"INTEGER","choch":"INTEGER","mss":"INTEGER","fvg":"INTEGER","order_block":"INTEGER","supply_demand":"INTEGER","liquidity":"INTEGER","mtf":"INTEGER","rsi":"REAL","atr":"REAL","spread":"REAL","exit_reason":"TEXT"}
def connect():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True); return sqlite3.connect(DB_PATH)
def initialize_database():
    with connect() as db:
        db.execute("CREATE TABLE IF NOT EXISTS trades (id INTEGER PRIMARY KEY AUTOINCREMENT)")
        existing={r[1] for r in db.execute("PRAGMA table_info(trades)")}
        for name,kind in COLUMNS.items():
            if name not in existing and name!="id":db.execute(f"ALTER TABLE trades ADD COLUMN {name} {kind}")
        db.execute("CREATE INDEX IF NOT EXISTS idx_trades_position_id ON trades(position_id)"); db.execute("CREATE INDEX IF NOT EXISTS idx_trades_status ON trades(status)")
    return DB_PATH
if __name__=="__main__":print(f"Statistics database ready: {initialize_database()}")
