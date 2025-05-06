import socket
import time

TARGET_HOST = "host.docker.internal"
TARGET_PORT = 9999

def bursty_sender():
    data = b"x" * 1024 * 1024  # 1MB
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TARGET_HOST, TARGET_PORT))

    while True:
        for _ in range(10):  # Send burst
            sock.sendall(data)
        print("Burst sent, pausing")
        time.sleep(5)

if __name__ == "__main__":
    bursty_sender()