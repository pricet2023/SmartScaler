from asyncio import streams
from signal import SIGILL
import time
import os

import docker
import matplotlib.pyplot as plt
from setuptools import sic


# Use headless backend
plt.switch_backend("Agg")

CONTAINER_NAME = "cpu_max_test"
IMAGE_NAME = "gradual_mem_leak"
DURATION_SECONDS = 10
SAMPLE_INTERVAL = 0.5
OUTPUT_PLOT = "container_resource_plot.png"

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

def calculate_mem_usage(stat):
    mem_usage = stat["memory_stats"]["usage"]
    mem_limit = stat["memory_stats"]["limit"]
    mem_percent = (mem_usage / mem_limit) * 100.0 if mem_limit else 0.0
    return mem_percent, mem_usage, mem_limit

def get_io_bytes(stat):
    print(stat["blkio_stats"])
    io_stats = stat.get("blkio_stats", {}).get("io_service_bytes_recursive", [])
    read_bytes = sum(x["value"] for x in io_stats if x["op"] == "Read")
    write_bytes = sum(x["value"] for x in io_stats if x["op"] == "Write")
    return read_bytes, write_bytes

def get_network_bytes(stat):
    networks = stat.get("networks", {})
    rx = sum(net["rx_bytes"] for net in networks.values())
    tx = sum(net["tx_bytes"] for net in networks.values())
    return rx, tx

def main():
    client = docker.from_env()

    host_directory = "/home/top/vol_dump"
    container_directory = "/data"

    print(f"[INFO] Starting container '{CONTAINER_NAME}'...")
    container = client.containers.run(
        IMAGE_NAME,
        name=CONTAINER_NAME,
        detach=True,
        remove=True,
        volumes={host_directory: {'bind': container_directory, 'mode': 'rw'}}
    )

    cpu_data = []
    mem_percent_data = []
    io_write_data = []
    io_read_data = []
    net_recv_data = []
    net_send_data = []
    timestamps = []

    print("[INFO] Collecting stats for 10 seconds...")
    stat = container.stats(stream=False)
    start_time = time.time()

    try:
        # Skip first stat (precpu_stats often empty)
        # first_stat = next(stats)
        time.sleep(SAMPLE_INTERVAL)

        while time.time() - start_time < DURATION_SECONDS:
            # stat = next(stats)
            stat = container.stats(stream=False)
            elapsed = time.time() - start_time
            cpu_percent = calculate_cpu_percent(stat)
            mem_percent = calculate_mem_usage(stat)[0]
            [io_read, io_write] = get_io_bytes(stat)
            [net_recv, net_send] = get_network_bytes(stat)

            timestamps.append(elapsed)
            cpu_data.append(cpu_percent)
            mem_percent_data.append(mem_percent)
            io_write_data.append(io_write)
            io_read_data.append(io_read)
            net_recv_data.append(net_recv)
            net_send_data.append(net_send)

            print(f"{elapsed:.1f}s - CPU: {cpu_percent:.2f}%")
            print(f"{elapsed:.1f}s - IO write: {io_write} Bytes")
            time.sleep(SAMPLE_INTERVAL)

    finally:
        print("[INFO] Stopping container...")
        container.stop(timeout=0)

    print(f"[INFO] Saving plot to '{OUTPUT_PLOT}'...")
    fig, axs = plt.subplots(4, 1, figsize=(10,5))   
    
    # cpu plot
    axs[0].plot(timestamps, cpu_data, marker='o')
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("CPU Usage (%)")
    axs[0].set_xlim(0, 12)
    axs[0].set_ylim(0, 110)
    axs[0].grid(True)

    # mem % plot
    axs[1].plot(timestamps, mem_percent_data, marker='o')
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("Mem Usage (%)")
    axs[1].set_xlim(0, 12)
    axs[1].grid(True)

    # io plot
    axs[2].plot(timestamps, io_read_data, marker='o', label="Read")
    axs[2].plot(timestamps, io_write_data, marker='x', label="Write")
    axs[2].legend()
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("IO (Bytes)")
    axs[2].set_xlim(0, 12)
    axs[2].grid(True)

    # network plot
    axs[3].plot(timestamps, net_recv_data, marker='o', label="Recv")
    axs[3].plot(timestamps, net_send_data, marker='x', label="Send")
    axs[3].legend()
    axs[3].set_xlabel("Time (s)")
    axs[3].set_ylabel("Net (Bytes)")
    axs[3].set_xlim(0, 12)
    axs[3].grid(True)

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)
    print("[DONE] Plot saved successfully.")

if __name__ == "__main__":
    main()