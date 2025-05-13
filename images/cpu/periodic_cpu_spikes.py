import threading
import time
import random

def burn_cpu_for(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pass  # Busy wait

def spike_pattern(active_duration=5, idle_duration=5):
    while True:
        burn_cpu_for(active_duration)
        time.sleep(idle_duration)

if __name__ == "__main__":
    num_threads = random.randint(1, 2)  # One thread = ~one logical CPU core. Adjust as needed.
    active_duration = random.randint(5, 10)  # seconds
    idle_duration = random.randint(5 ,10)    # seconds

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=spike_pattern, args=(active_duration, idle_duration))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()