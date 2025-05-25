import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

# Create figure for roll, pitch, yaw with 3 subplots
fig_attitude, (ax_roll, ax_pitch, ax_yaw) = plt.subplots(3, 1, sharex=True, figsize=(8, 8))
fig_attitude.suptitle('Attitude Measurements (Roll, Pitch, Yaw)')

# Create separate figure for altitude
fig_altitude, ax_altitude = plt.subplots()
fig_altitude.suptitle('Altitude vs Time')

def animate(i):
    data = pd.read_csv('data.csv')
    timestamp = data['timestamp']
    roll = data['roll']
    pitch = data['pitch']
    yaw = data['yaw']
    altitude = data['altitude']

    # Roll subplot
    ax_roll.cla()
    ax_roll.plot(timestamp, roll, color='red', label='Roll')
    ax_roll.set_ylabel('Roll (°)')
    ax_roll.legend(loc='upper left')
    ax_roll.grid(True)

    # Pitch subplot
    ax_pitch.cla()
    ax_pitch.plot(timestamp, pitch, color='green', label='Pitch')
    ax_pitch.set_ylabel('Pitch (°)')
    ax_pitch.legend(loc='upper left')
    ax_pitch.grid(True)

    # Yaw subplot
    ax_yaw.cla()
    ax_yaw.plot(timestamp, yaw, color='blue', label='Yaw')
    ax_yaw.set_ylabel('Yaw (°)')
    ax_yaw.set_xlabel('Time')
    ax_yaw.legend(loc='upper left')
    ax_yaw.grid(True)

    # Altitude plot
    ax_altitude.cla()
    ax_altitude.plot(timestamp, altitude, color='orange', label='Altitude')
    ax_altitude.set_xlabel('Time')
    ax_altitude.set_ylabel('Altitude')
    ax_altitude.legend(loc='upper left')
    ax_altitude.grid(True)

# Set up animations
ani_attitude = FuncAnimation(fig_attitude, animate, interval=100)
ani_altitude = FuncAnimation(fig_altitude, animate, interval=100)

plt.show()
