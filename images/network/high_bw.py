import socket
import time

TARGET_HOST = "host.docker.internal"  # Replace with actual host or container IP
TARGET_PORT = 9000                    # Replace with your listener port

def high_bandwidth_sender():
    data = b"x" * 1024 * 1024  # 1MB payload
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TARGET_HOST, TARGET_PORT))

    while True:
        sock.sendall(data)
        time.sleep(0.01)  # Adjust to control bandwidth

if __name__ == "__main__":
    high_bandwidth_sender()