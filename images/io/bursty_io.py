import time
import os

def burst_io(burst_size=50, pause_time=5):
    data = os.urandom(1024 * 1024)  # 1MB of random data
    while True:
        for i in range(burst_size):
            with open(f"/data/burst_file_{i}.bin", "wb") as f:
                f.write(data)
        print(f"Wrote {burst_size} MB burst, pausing {pause_time}s")
        time.sleep(pause_time)

if __name__ == "__main__":
    burst_io()