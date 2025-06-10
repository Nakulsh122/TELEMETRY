import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

# Constants
G = 6.6743e-11         # Gravitational constant (m^3 kg^-1 s^-2)
M_e = 5.972e24         # Mass of Earth (kg)
Rplanet = 6378e3 
w_tons = 5.3      # Radius of Earth (m)
mass_0 = w_tons*2000/2.2       # Mass of object (kg) - increased for more realistic rocket
maxThrust = 167970.0   # Force in newtons (N) - increased proportionally
ISP1 = 250    
ISP2 = 400          # Specific impulse (s)
tMECO = 38   
tsep1 = 2.0
mass1tons  = 0.2   
mass1 = mass1tons*2000/2.2
t2start = 261.0    # Main Engine Cut-Off time (s)
tSECO = t2start + 10
ve1 = ISP1 * 9.81
ve2 = ISP2*9.81
# Gravity function - returns force per unit mass (acceleration)
def gravity(x, y):
    r = np.sqrt(x**2 + y**2)
    if r < Rplanet:
        return np.asarray([0.0, 0.0])
    # Return gravitational acceleration pointing toward center
    factor = -G * M_e / r**3  # Negative because force points toward center
    return np.asarray([factor * x, factor * y])

# Thrust function
def propulsion(t):
    if t < tMECO:
        theta = 10 * np.pi / 180
        thrust_f = maxThrust
        mdot = -thrust_f / ve1
    elif t < (tMECO + tsep1):
        theta = 0.0
        thrust_f = 0.0
        mdot = -mass1 / tsep1
    elif t < t2start:
        theta = 0.0
        thrust_f = 0.0
        mdot = 0.0
    elif t <= tSECO:
        theta = 90.0 * np.pi / 180
        thrust_f = maxThrust
        mdot = -thrust_f / ve2
    else:
        theta = 0.0
        thrust_f = 0.0
        mdot = 0.0

    thrust_X = thrust_f * np.cos(theta)
    thrust_Y = thrust_f * np.sin(theta)
    return np.asarray([thrust_X, thrust_Y]), mdot


# Derivatives
def derivatives(state, t):
    x, y, vx, vy, mass = state
    dxdt = vx
    dydt = vy
    
    # Get gravitational acceleration
    a_gravity = gravity(x, y)
    
    # Get thrust force and mass flow rate
    F_thrust, mdot = propulsion(t)
    
    # Calculate thrust acceleration
    if mass > 0:
        a_thrust = F_thrust / mass
    else:
        a_thrust = np.asarray([0.0, 0.0])
        mdot = 0.0
    
    # Total acceleration
    ax = a_gravity[0] + a_thrust[0]
    ay = a_gravity[1] + a_thrust[1]
    
    return [dxdt, dydt, ax, ay, mdot]

# Initial Conditions
x0 = Rplanet
y0 = 0.0
velx_0 = 0.0
vely_0 = 0.0
stateinitial = [x0, y0, velx_0, vely_0, mass_0]

# Time Settings
tout = np.linspace(0, 2000, 1000)

# Integrate ODE
stateout = sci.odeint(derivatives, stateinitial, tout)

# Extract values
xout = stateout[:, 0]
yout = stateout[:, 1]
velx_out = stateout[:, 2]
vely_out = stateout[:, 3]
massOut = stateout[:, 4]
altitude = np.sqrt(xout**2 + yout**2) - Rplanet
velocity = np.sqrt(velx_out**2 + vely_out**2)

# Calculate accelerations from velocity gradients
accel_total_x = np.gradient(velx_out, tout)  # d(vx)/dt
accel_total_y = np.gradient(vely_out, tout)  # d(vy)/dt
accel_total_mag = np.sqrt(accel_total_x**2 + accel_total_y**2)

# Calculate individual acceleration components by recomputing forces
# (This is more accurate than trying to separate from total acceleration)
accel_gravity_x = []
accel_gravity_y = []
accel_thrust_x = []
accel_thrust_y = []

for i in range(len(tout)):
    x, y, vx, vy, m = stateout[i]
    
    # Gravitational acceleration
    a_grav = gravity(x, y)
    accel_gravity_x.append(a_grav[0])
    accel_gravity_y.append(a_grav[1])
    
    # Thrust acceleration
    F_thrust, _ = propulsion(tout[i])
    if m > 0:
        a_thrust = F_thrust / m
    else:
        a_thrust = np.asarray([0.0, 0.0])
    
    accel_thrust_x.append(a_thrust[0])
    accel_thrust_y.append(a_thrust[1])

# Convert to arrays
accel_gravity_x = np.array(accel_gravity_x)
accel_gravity_y = np.array(accel_gravity_y)
accel_thrust_x = np.array(accel_thrust_x)
accel_thrust_y = np.array(accel_thrust_y)

# Calculate magnitudes
accel_gravity_mag = np.sqrt(accel_gravity_x**2 + accel_gravity_y**2)
accel_thrust_mag = np.sqrt(accel_thrust_x**2 + accel_thrust_y**2)
accel_total_mag = np.sqrt(accel_total_x**2 + accel_total_y**2)

# Verification: Compare gradient-based vs force-based total acceleration
accel_force_based_x = accel_gravity_x + accel_thrust_x
accel_force_based_y = accel_gravity_y + accel_thrust_y
accel_force_based_mag = np.sqrt(accel_force_based_x**2 + accel_force_based_y**2)

# Plotting
fig, axs = plt.subplots(3, 2, figsize=(12, 10))
fig.suptitle("Fixed Rocket Simulation", fontsize=14)

# 1. Trajectory plot
theta = np.linspace(0, 2 * np.pi, 360)
xplanet = Rplanet * np.cos(theta)
yplanet = Rplanet * np.sin(theta)
axs[0, 0].plot(xplanet/1000, yplanet/1000, 'b', linewidth=2, label="Earth")
axs[0, 0].plot(xout/1000, yout/1000, 'r', linewidth=1, label="Trajectory")
axs[0, 0].set_aspect('equal')
axs[0, 0].set_title("Trajectory")
axs[0, 0].set_xlabel("X (km)")
axs[0, 0].set_ylabel("Y (km)")
axs[0, 0].legend()
axs[0, 0].grid(True, alpha=0.3)

# 2. Altitude vs Time
axs[0, 1].plot(tout, altitude/1000, 'g', linewidth=2)
axs[0, 1].axvline(x=tMECO, color='r', linestyle='--', alpha=0.7, label='Engine Cutoff')
axs[0, 1].set_title("Altitude vs Time")
axs[0, 1].set_xlabel("Time (s)")
axs[0, 1].set_ylabel("Altitude (km)")
axs[0, 1].legend()
axs[0, 1].grid(True, alpha=0.3)

# 3. Velocity vs Time
axs[1, 0].plot(tout, velocity, 'orange', linewidth=2, label="Total")
axs[1, 0].plot(tout, velx_out, 'red', alpha=0.7, label="Vx")
axs[1, 0].plot(tout, vely_out, 'blue', alpha=0.7, label="Vy")
axs[1, 0].axvline(x=tMECO, color='r', linestyle='--', alpha=0.7, label='Engine Cutoff')
axs[1, 0].set_title("Velocity vs Time")
axs[1, 0].set_xlabel("Time (s)")
axs[1, 0].set_ylabel("Velocity (m/s)")
axs[1, 0].legend()
axs[1, 0].grid(True, alpha=0.3)

# 4. Acceleration Components vs Time
axs[1, 1].plot(tout, accel_gravity_mag, 'blue', linewidth=2, label="Gravity")
axs[1, 1].plot(tout, accel_thrust_mag, 'red', linewidth=2, label="Thrust")
axs[1, 1].plot(tout, accel_total_mag, 'black', linewidth=1, alpha=0.7, label="Total")
axs[1, 1].axvline(x=tMECO, color='r', linestyle='--', alpha=0.7, label='Engine Cutoff')
axs[1, 1].set_title("Acceleration Components vs Time")
axs[1, 1].set_xlabel("Time (s)")
axs[1, 1].set_ylabel("Acceleration (m/s²)")
axs[1, 1].legend()
axs[1, 1].grid(True, alpha=0.3)

# 5. Mass vs Time
axs[2, 0].plot(tout, massOut, 'brown', linewidth=2)
axs[2, 0].axvline(x=tMECO, color='r', linestyle='--', alpha=0.7, label='Engine Cutoff')
axs[2, 0].set_title("Mass vs Time")
axs[2, 0].set_xlabel("Time (s)")
axs[2, 0].set_ylabel("Mass (kg)")
axs[2, 0].legend()
axs[2, 0].grid(True, alpha=0.3)

# 6. Detailed Acceleration (X and Y components)
axs[2, 1].plot(tout, accel_total_x, 'purple', linewidth=1, label="Total Acc X")
axs[2, 1].plot(tout, accel_total_y, 'green', linewidth=1, label="Total Acc Y")
axs[2, 1].plot(tout, accel_gravity_x, 'blue', alpha=0.5, linestyle=':', label="Gravity X")
axs[2, 1].plot(tout, accel_gravity_y, 'cyan', alpha=0.5, linestyle=':', label="Gravity Y")
axs[2, 1].axvline(x=tMECO, color='r', linestyle='--', alpha=0.7, label='Engine Cutoff')
axs[2, 1].set_title("Acceleration Components (X & Y)")
axs[2, 1].set_xlabel("Time (s)")
axs[2, 1].set_ylabel("Acceleration (m/s²)")
axs[2, 1].legend(fontsize=8)
axs[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print some diagnostics
print(f"\nDiagnostics:")
print(f"Final altitude: {altitude[-1]/1000:.2f} km")
print(f"Final velocity: {velocity[-1]:.2f} m/s")
print(f"Final mass: {massOut[-1]:.2f} kg")
print(f"Fuel consumed: {mass_0 - massOut[-1]:.2f} kg")
print(f"Maximum altitude: {np.max(altitude)/1000:.2f} km")
print(f"Maximum velocity: {np.max(velocity):.2f} m/s")