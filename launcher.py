import time
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RUN_BOT = BASE_DIR / "run_bot.py"

print("=" * 50)
print("Prime T Genesis Auto Restart Launcher")
print("=" * 50)

while True:
    print("\nStarting run_bot.py...")

    subprocess.run([sys.executable, str(RUN_BOT)], cwd=BASE_DIR)

    print("\nBot stopped or crashed.")
    print("Restarting in 10 seconds...")

    time.sleep(10)
