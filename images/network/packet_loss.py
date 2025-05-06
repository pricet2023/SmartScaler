import subprocess
import time

target = "8.8.8.8"  # Google DNS (or use host.docker.internal for local testing)

print(f"[INFO] Starting ping test to {target} with simulated packet loss...")

while True:
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", target],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True)
        output = result.stdout.strip()
        if "1 received" in output:
            print("[SUCCESS] Ping successful")
        else:
            print("[FAIL] Ping failed or timed out")
    except Exception as e:
        print(f"[ERROR] {e}")
    time.sleep(1)