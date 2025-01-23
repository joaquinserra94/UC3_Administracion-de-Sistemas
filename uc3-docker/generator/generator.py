import time
import random

def main():
    while True:
        num = random.randint(1, 10000)
        with open("/app-data/numbers.txt", "a") as f:
            f.write(f"{num}\n")
        time.sleep(1)

if __name__ == "__main__":
    main()
