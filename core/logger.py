from datetime import datetime
from pathlib import Path

def write_log(message):
    Path("logs").mkdir(exist_ok=True)
    with open("logs/signals.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
