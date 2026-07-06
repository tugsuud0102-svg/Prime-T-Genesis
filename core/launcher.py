import time
import subprocess

print("=" * 50)
print("Prime T Genesis Auto Restart Launcher")
print("=" * 50)

while True:
    print("\nStarting run_bot.py...")

    process = subprocess.run(["python", "run_bot.py"])

    print("\nBot stopped or crashed.")
    print("Restarting in 10 seconds...")

    time.sleep(10)