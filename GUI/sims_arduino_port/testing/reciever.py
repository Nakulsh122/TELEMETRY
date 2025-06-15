import serial
import time

PORT = 'COM8'  # Connects to the fake Arduino's side of the com0com pair
BAUD = 9600
TIMEOUT = 2

ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
print(f"[MASTER] Connected to {PORT} at {BAUD} baud")

def send_command(cmd):
    ser.write((cmd + '\n').encode())
    print(f"[Sent] {cmd}")

def wait_for_response(prefix=None, timeout=3):
    start = time.time()
    while time.time() - start < timeout:
        line = ser.readline().decode().strip()
        if line:
            print(f"[Received] {line}")
            if prefix is None or line.startswith(prefix):
                return line
    print("[Timeout] No valid response")
    return None

# Step 1: Ask for number of channels
send_command("#n#")
resp = wait_for_response("#N#")
if resp and resp.startswith("#N#"):
    try:
        num_channels = int(resp.split("#")[2])
        print(f"[Info] Detected {num_channels} channels")
    except:
        print("[Error] Malformed response")
        ser.close()
        exit()
else:
    print("[Error] Failed to detect channels")
    ser.close()
    exit()

# Step 2: Start stream
send_command("#s#")
print("[MASTER] Started data stream. Listening for 10 packets...")

# Step 3: Read 10 data packets
packet_count = 0
while packet_count < 10:
    line = ser.readline().decode().strip()
    if line.startswith("#D#"):
        values = line.split("#")[2:-1]  # skip #D# and trailing #
        print(f"[Packet {packet_count + 1}] Data: {values}")
        if len(values) != num_channels:
            print("[Warning] Channel count mismatch!")
        packet_count += 1
    elif line:
        print(f"[Unrecognized] {line}")

# Step 4: Stop stream
send_command("#st#")
print("[MASTER] Stream stopped.")

ser.close()
print("[MASTER] Done.")
