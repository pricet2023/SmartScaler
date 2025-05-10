import os
import time
import random

def random_io():
    i = 0
    while True:
        op = random.choice(["read", "write"])
        size_kb = random.randint(4, 1024)  # 4KB to 1MB
        path = f"/data/random_file_{i % 10}.bin"

        if op == "write":
            with open(path, "wb") as f:
                f.write(os.urandom(size_kb * 1024))
            print(f"Wrote {size_kb}KB to {path}")
        else:
            try:
                with open(path, "rb") as f:
                    _ = f.read()
                print(f"Read from {path}")
            except FileNotFoundError:
                pass  # Skip if file doesn't exist yet

        i += 1
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    random_io()