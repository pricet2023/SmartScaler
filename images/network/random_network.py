import socket
import time
import random

HOST = "host.docker.internal"  # or 172.17.0.1 on Linux
PORT = 9000

def random_send():
    while True:
        try:
            s = socket.create_connection((HOST, PORT), timeout=5)
            size = random.randint(100, 5000)  # Bytes
            data = bytes([random.randint(0, 255) for _ in range(size)])
            s.sendall(data)
            s.close()
            print(f"Sent {size} bytes")
        except Exception as e:
            print(f"Send failed: {e}")
        
        sleep_time = random.uniform(0.1, 2.0)  # Random pause between 100ms and 2s
        time.sleep(sleep_time)

if __name__ == "__main__":
    random_send()