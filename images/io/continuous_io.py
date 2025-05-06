import os
import time

def continuous_io():
    data = os.urandom(1024 * 1024)  # 1MB
    i = 0
    while True:
        with open(f"/tmp/cont_file_{i % 10}.bin", "wb") as f:
            f.write(data)
        i += 1
        time.sleep(0.1)  # Small pause to avoid locking up system

if __name__ == "__main__":
    continuous_io()