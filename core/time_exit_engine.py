from datetime import datetime,timezone
def evaluate_time_exit(position,max_hours=24.0,minimum_profit=0.0,now=None):
    now=now or datetime.now(timezone.utc); opened=datetime.fromtimestamp(position.time,timezone.utc); hours=(now-opened).total_seconds()/3600
    return {"exit":hours>=max_hours and position.profit<=minimum_profit,"hours_open":hours,"reason":f"Open {hours:.1f}h with profit {position.profit:.2f}"}
