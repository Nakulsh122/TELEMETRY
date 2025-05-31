import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

# Constants
G = 6.6743e-11         # Gravitational constant (m^3 kg^-1 s^-2)
M_e = 5.972e24         # Mass of Earth (kg)
Rplanet = 6378e3       # Radius of Earth (m)
mass = 1               # Mass of object (kg)
maxThrust = 50         # Force in newtons (N)

# Gravity function
def gravity(x, y):
    r = np.sqrt(x**2 + y**2)
    if r < Rplanet:
        return np.asarray([0.0, 0.0])
    factor = G * M_e / r**3
    return np.asarray([factor * x, factor * y])

# Thrust function
def thrust(t):
    global maxThrust
    if t < 5:
        thrust_f = maxThrust
    else:
        thrust_f = 0.0
    theta = 0.0  # Thrust direction: along x-axis
    thrust_X = thrust_f * np.cos(theta)
    thrust_Y = thrust_f * np.sin(theta)
    return np.asarray([thrust_X, thrust_Y])

# Derivatives
def derivatives(state, t):
    global mass
    x, y, vx, vy = state
    dxdt = vx
    dydt = vy
    F_gravity = -gravity(x, y)
    F_thrust = thrust(t)
    F_aero = np.asarray([0.0, 0.0])  # No drag in this sim
    Total_F = F_aero + F_gravity + F_thrust
    ax, ay = Total_F / mass
    return [dxdt, dydt, ax, ay]

# Initial Conditions
x0 = Rplanet
y0 = 0.0
velx_0 = 0.0
vely_0 = 0.0
stateinitial = [x0, y0, velx_0, vely_0]

# Time Settings
tout = np.linspace(0, 40, 1000)

# Integrate ODE
stateout = sci.odeint(derivatives, stateinitial, tout)

# Extract values
xout = stateout[:, 0]
yout = stateout[:, 1]
velx_out = stateout[:, 2]
vely_out = stateout[:, 3]
altitude = np.sqrt(xout**2 + yout**2) - Rplanet
velocity = np.sqrt(velx_out**2 + vely_out**2)

# Compute acceleration
accel_x = np.gradient(velx_out, tout) # makes the acceleration graph from the plots of the vels
accel_y = np.gradient(vely_out, tout)
accel_mag = np.sqrt(accel_x**2 + accel_y**2)

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Rocket Simulation", fontsize=16)

# 1. Trajectory plot
theta = np.linspace(0, 2 * np.pi, 360)
xplanet = Rplanet * np.cos(theta)
yplanet = Rplanet * np.sin(theta)
axs[0, 0].plot(xplanet, yplanet, 'b', label="Earth")
axs[0, 0].plot(xout, yout, 'r', label="Trajectory")
axs[0, 0].set_aspect('equal')
axs[0, 0].set_title("Trajectory")
axs[0, 0].set_xlabel("X (m)")
axs[0, 0].set_ylabel("Y (m)")
axs[0, 0].legend()
axs[0, 0].grid()

# 2. Altitude vs Time
axs[0, 1].plot(tout, altitude, 'g')
axs[0, 1].set_title("Altitude vs Time")
axs[0, 1].set_xlabel("Time (s)")
axs[0, 1].set_ylabel("Altitude (m)")
axs[0, 1].grid()

# 3. Velocity vs Time
axs[1, 0].plot(tout, velocity, 'orange')
axs[1, 0].plot(tout, velx_out, 'red')
axs[1, 0].plot(tout, vely_out, 'blue')
axs[1, 0].set_title("Velocity vs Time")
axs[1, 0].set_xlabel("Time (s)")
axs[1, 0].set_ylabel("Velocity (m/s)")
axs[1, 0].grid()

# 4. Acceleration vs Time
axs[1, 1].plot(tout, accel_mag, 'purple')
axs[1, 1].set_title("Acceleration vs Time")
axs[1, 1].set_xlabel("Time (s)")
axs[1, 1].set_ylabel("Acceleration (m/s²)")
axs[1, 1].grid()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
