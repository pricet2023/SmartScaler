import time

if __name__ == "__main__":
    allocation_size_mb = 512  # Total memory to hold

    # Allocate and keep in memory
    memory_holder = bytearray(allocation_size_mb * 1024 * 1024)

    print(f"Allocated {allocation_size_mb}MB of memory.")
    while True:
        time.sleep(10)  # Just stay alive and hold the memory