import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

# eq of motions
# F = M*a = M*y"  y : altitude
# // the notations are as follows :
# a' means the first derivative of the value wrt time and a" means the double derivative
# i will add the eq as we need to add in the sims but will show in comments the actual ways they are being used
G = 6.6743e-11
M_e = 5.972e24
Rplanet = 6378e3  # m
# here we will simulate the launch in 2D
mass = 1

#we will be using the yx plane as in the y axs is the y-axis and the x-axis is the same , 
# think of it as slicing the earth from the middle

# see y.png for diagram

def gravity(x,y):
    global G
    global M_e, Rplanet
    r = np.sqrt(x**2 + y**2)
    if r < Rplanet:
        accelX = 0
        accely = 0
        return np.asarray([accelX,accely])
    accelX = ((G*M_e)/r**3 )*x
    accely = ((G*M_e)/r**3 )*y
    return np.asarray([accelX,accely])


# second order differnetial
def derivatives(state, t):
    # state vector will have 2 rows
    y = state[0]
    x =state[1]
    vely = state[2]
    velx = state[3]
    global mass
    # compute ydot - Kinematic rel
    ydot = vely
    xdot = velx
    # Gravity
    GravityF = -gravity(x,y)*mass
    # Aerodynamic
    aero = np.asarray([0.0,0.0])
    # Thrust
    thrust = np.asarray([0.0,0.0])

    Forces = GravityF + aero + thrust

    # yddot
    ddot = Forces / mass

    # state' vector needs to be calculated
    statedot = np.asarray([ydot,xdot, ddot[1],ddot[0]])

    return statedot


## Main Script

#Input parmas 
x0 = Rplanet + 40000   
y0 = 0  # m
vely_0 = 8000 # m/s
velx_0 = 0 #m/s
r0 = np.sqrt(x0**2 + y0**2)
TimePeriod = 2*np.pi/np.sqrt(G*M_e/r0)
tout = np.linspace(
    0, TimePeriod, 1000
)  # np.linespace(start ,end , n) : this function allows you to make an array with the starting and ending points with n no of points in between including the endpoints
stateinitial = np.asarray([y0,x0,vely_0,velx_0])

# Outputs 
stateout = sci.odeint(derivatives, stateinitial, tout)
yout = stateout[:, 0]
xout = stateout[:, 1]
vely_out = stateout[:, 2]
velx_out = stateout[:, 3]
altitude = np.sqrt(xout**2 + yout**2) - Rplanet
vel_out = np.sqrt(velx_out**2 + vely_out**2)
# plottings 
theta = np.linspace(0,2*np.pi,360)
xplanet = Rplanet*np.sin(theta)
yplanet = Rplanet*np.cos(theta)
# plt.figure()
# plt.plot(altitude,tout)
# plt.title("Altitude")
# plt.grid()
# plt.show()

# plt.figure()
# plt.title("Speed")
# plt.plot(vel_out,tout)
# plt.grid()

plt.figure()
plt.plot(xplanet,yplanet)
plt.plot(xout,yout)

plt.grid()
plt.show()