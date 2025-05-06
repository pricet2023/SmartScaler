#!/bin/bash

# Wait for networking to be ready (optional but safe)
sleep 1

# Add 10% packet loss to all outgoing packets on eth0
tc qdisc add dev eth0 root netem loss 10%

echo "[INFO] Simulated 10% packet loss on eth0"

# Keep the script running in the background
tail -f /dev/null