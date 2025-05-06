import threading

def burn_cpu():
    while True:
        pass  # Infinite loop keeps the CPU busy

if __name__ == "__main__":
    threads = []
    num_threads = 1  # Adjust this to the number of CPU cores you want to max out

    for _ in range(num_threads):
        t = threading.Thread(target=burn_cpu)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()