import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci 

#eq of motions 
# F = M*a = M*z"  z : altitude 
# // the notations are as follows : 
# a' means the first derivative of the value wrt time and a" means the double derivative 
# i will add the eq as we need to add in the sims but will show in comments the actual ways they are being used 
mass = 1

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
    F_g = -9.81*mass
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

tout = np.linspace(0,50,1000)  # np.linespace(start ,end , n) : this function allows you to make an array with the starting and ending points with n no of points in between including the endpoints 
z0 = 0.0 #m
velz_0 = 164 #m/s
stateinitial = np.asarray([z0,velz_0])
stateout = sci.odeint(derivatives ,stateinitial , tout)
zout = stateout[:,0]
velz_out = stateout[:,1]
fig ,(alt , speed) = plt.subplots(2,1,sharex = True); 
fig.suptitle("Output")

alt.plot(tout, zout )
speed.plot(tout,velz_out)
plt.show()


