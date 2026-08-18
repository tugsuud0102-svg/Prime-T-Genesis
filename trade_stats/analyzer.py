from trade_stats.database import connect,initialize_database
SETUPS=("bos","choch","mss","fvg","order_block","supply_demand","liquidity","mtf")
def build_performance_summary():
    initialize_database()
    with connect() as db:
        db.row_factory=__import__("sqlite3").Row; rows=db.execute("SELECT * FROM trades WHERE status='CLOSED'").fetchall()
    if not rows:return {"message":"No closed trades recorded yet.","total_trades":0}
    vals=[float(r["net_profit"] or 0) for r in rows]; wins=[v for v in vals if v>0]; losses=[v for v in vals if v<0]
    symbols={s:sum(float(r["net_profit"] or 0) for r in rows if r["symbol"]==s) for s in {r["symbol"] for r in rows}}
    setups={s:sum(float(r["net_profit"] or 0) for r in rows if r[s]) for s in SETUPS}; avg=lambda k:sum(float(r[k] or 0) for r in rows)/len(rows)
    return {"total_trades":len(rows),"wins":len(wins),"losses":len(losses),"breakeven":len(rows)-len(wins)-len(losses),"win_rate":len(wins)/len(rows)*100,"net_profit":sum(vals),"gross_profit":sum(wins),"gross_loss":sum(losses),"profit_factor":sum(wins)/abs(sum(losses)) if losses else float("inf"),"average_profit":sum(vals)/len(rows),"average_rr":avg("rr"),"average_score":avg("score"),"best_symbol":max(symbols,key=symbols.get),"best_setup":max(setups,key=setups.get)}
def format_performance_summary(s=None):
    s=s or build_performance_summary()
    if s.get("message"):return s["message"]
    return f"Prime T Genesis v4.1.3 Performance\nTrades: {s['total_trades']} | W/L/BE: {s['wins']}/{s['losses']}/{s['breakeven']}\nWin rate: {s['win_rate']:.1f}%\nNet: ${s['net_profit']:.2f} | PF: {s['profit_factor']:.2f}\nAvg profit: ${s['average_profit']:.2f} | Avg RR: {s['average_rr']:.2f} | Avg score: {s['average_score']:.1f}\nBest symbol: {s['best_symbol']} | Best setup: {s['best_setup']}"
if __name__=="__main__":print(format_performance_summary())
