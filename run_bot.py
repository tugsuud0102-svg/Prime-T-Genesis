import time
from main import main

print("=" * 50)
print("Prime T Genesis Live Bot Started")
print("=" * 50)

while True:
    try:
        print("\nChecking market...")
        main()

    except Exception as e:
        print("ERROR:", e)

    print("\nSleeping 30 seconds...")
    time.sleep(30)