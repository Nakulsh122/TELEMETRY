import serial
import time
import math
import threading
import random

# Configuration
PORT = 'COM7'
BAUD = 9600
NUM_CHANNELS = 4
SEND_INTERVAL = 0.2  # seconds between data packets

ser = serial.Serial(PORT, BAUD, timeout=1)
print(f"[Fake Arduino] Connected on {PORT} at {BAUD} baud")

sending_data = False

def generate_data(t):
    """Generate shifted sine wave + noise for each channel"""
    data = []
    for i in range(NUM_CHANNELS):
        val = math.sin(t + i) * 50 + 100 + random.uniform(-2, 2)
        data.append(f"{val:.2f}")
    return data

def sender_thread():
    t = 0.0
    while True:
        global sending_data
        if sending_data:
            data = generate_data(t)
            packet = "#D#" + "#".join(data) + "#\n"
            ser.write(packet.encode())
            print(f"[Sent] {packet.strip()}")
            t += SEND_INTERVAL
            time.sleep(SEND_INTERVAL)
        else:
            time.sleep(0.1)

# Start background thread for sending data
threading.Thread(target=sender_thread, daemon=True).start()

# Command listener
while True:
    try:
        cmd = ser.readline().decode().strip()
        if not cmd:
            continue

        print(f"[Received] {cmd}")

        if cmd == "#n#":
            ser.write(f"#N#{NUM_CHANNELS}\n".encode())

        elif cmd == "#s#":
            sending_data = True
            print("[Info] Data stream started.")

        elif cmd == "#st#":
            sending_data = False
            print("[Info] Data stream stopped.")

        else:
            print(f"[Warning] Unknown command: {cmd}")

    except Exception as e:
        print(f"[Error] {e}")
        break
