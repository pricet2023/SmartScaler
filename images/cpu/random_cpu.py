import threading
import time
import random

def noisy_worker():
    while True:
        work_duration = random.uniform(0.05, 0.5)   # Do work for 50–500 ms
        sleep_duration = random.uniform(0.1, 1.0)   # Then rest for 100–1000 ms

        end_time = time.time() + work_duration
        while time.time() < end_time:
            pass  # Busy work

        time.sleep(sleep_duration)

if __name__ == "__main__":
    num_threads = 2  # Adjust based on how noisy you'd like it

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=noisy_worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()