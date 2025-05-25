import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci 

#eq of motions 
# F = M*a = M*z"  z : altitude 
# // the notations are as follows : 
# a' means the first derivative of the value wrt time and a" means the double derivative 
# i will add the eq as we need to add in the sims but will show in comments the actual ways they are being used 
G = 6.6743e-11
M_e = 5.972e24
Rplanet = 6378e3 #m
# here we will simulate newtonian gravity 
mass = 1
def gravity(z) :
    global G    
    global M_e,Rplanet
    r = np.sqrt(z**2)
    if r < Rplanet:
        return 0
    return (( G * M_e ) / r**3) * r 
# second order differnetial 
def derivatives (state,t) :
    #state vector will have 2 rows 
    z = state[0]
    velz = state[1]
    global mass;
    #compute zdot - Kinematic rel
    zdot = velz 
    #Total forces 

    #Gravity
    F_g = -gravity(z)*mass
    #Aerodynamic
    aero = 0
    #Thrust
    thrust = 0

    Forces = F_g + aero + thrust

    #zddot 
    zddot = Forces/mass

    #state' vector needs to be calculated 
    statedot = np.asarray([zdot ,zddot])

    return statedot

## Main Script 

tout = np.linspace(0,30000   ,1000)  # np.linespace(start ,end , n) : this function allows you to make an array with the starting and ending points with n no of points in between including the endpoints 
z0 = Rplanet #m
velz_0 = 16400#m/s
stateinitial = np.asarray([z0,velz_0])
stateout = sci.odeint(derivatives ,stateinitial , tout)
zout = stateout[:,0]
altitude = zout - Rplanet
velz_out = stateout[:,1]
fig ,(alt , speed) = plt.subplots(2,1,sharex = True); 
fig.suptitle("Output")

alt.plot(tout, altitude )
speed.plot(tout,velz_out)
plt.show()


