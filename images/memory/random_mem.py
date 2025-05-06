import time
import random

if __name__ == "__main__":
    allocations = []

    while True:
        if random.random() < 0.5:
            # Allocate between 1MB and 20MB
            size_mb = random.randint(1, 20)
            allocations.append(bytearray(size_mb * 1024 * 1024))
            print(f"Allocated {size_mb}MB")
        else:
            if allocations:
                allocations.pop(random.randint(0, len(allocations) - 1))
                print("Freed some memory")
        time.sleep(random.uniform(0.5, 2.0))