# fake_arduino.py
import serial
import time

ser = serial.Serial('COM7', 9600)
while True:
    ser.write(b"TEMP:23.5\n")
    time.sleep(1)
    print("sending")
