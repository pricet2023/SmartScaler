import time

leak = []

if __name__ == "__main__":
    allocation_size_kb = 1024  # 1MB per step
    delay = 1.0                # seconds between leaks

    while True:
        leak.append(bytearray(allocation_size_kb * 1024))  # Leak memory
        time.sleep(delay)