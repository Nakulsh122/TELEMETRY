
import csv
import random
import time

x_value = 0
total_1 = 1000
total_2 = 1000

fieldnames = ["timestamp", "roll", "pitch","yaw","altitude"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "timestamp": time.time(),
            "roll":random.randint(-180,180),
            "pitch": random.randint(-180,180),
            "yaw" : random.randint(-180,180),
            "altitude" : x_value
        }

        csv_writer.writerow(info)
        x_value += 1

    time.sleep(0.4)