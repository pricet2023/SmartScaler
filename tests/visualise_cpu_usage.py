import docker
import time
import matplotlib.pyplot as plt

# Use headless backend
plt.switch_backend("Agg")

CONTAINER_NAME = "cpu_spike_test"
IMAGE_NAME = "cpu-spike"
DURATION_SECONDS = 10
SAMPLE_INTERVAL = 0.5
OUTPUT_PLOT = "cpu_usage_plot.png"

def calculate_cpu_percent(stat):
    try:
        cpu_delta = stat["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    stat["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stat["cpu_stats"]["system_cpu_usage"] - \
                       stat["precpu_stats"]["system_cpu_usage"]

        cpu_count = len(stat["cpu_stats"]["cpu_usage"].get("percpu_usage", [])) or 1

        if cpu_delta > 0 and system_delta > 0:
            return (cpu_delta / system_delta) * cpu_count * 100.0
    except (KeyError, ZeroDivisionError):
        pass
    return 0.0

def main():
    client = docker.from_env()

    print(f"[INFO] Starting container '{CONTAINER_NAME}'...")
    container = client.containers.run(
        IMAGE_NAME,
        name=CONTAINER_NAME,
        detach=True,
        remove=True
    )

    cpu_data = []
    timestamps = []

    print("[INFO] Collecting stats for 10 seconds...")
    stats = container.stats(stream=True)
    start_time = time.time()

    try:
        # Skip first stat (precpu_stats often empty)
        first_stat = next(stats)
        time.sleep(SAMPLE_INTERVAL)

        while time.time() - start_time < DURATION_SECONDS:
            stat = next(stats)
            elapsed = time.time() - start_time
            cpu_percent = calculate_cpu_percent(stat)

            timestamps.append(elapsed)
            cpu_data.append(cpu_percent)

            print(f"{elapsed:.1f}s - CPU: {cpu_percent:.2f}%")
            time.sleep(SAMPLE_INTERVAL)

    finally:
        print("[INFO] Stopping container...")
        container.stop()

    print(f"[INFO] Saving plot to '{OUTPUT_PLOT}'...")
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_data, marker='o')
    plt.xlabel("Time (s)")
    plt.ylabel("CPU Usage (%)")
    plt.title("Bursty CPU Container Usage")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)
    print("[DONE] Plot saved successfully.")

if __name__ == "__main__":
    main()