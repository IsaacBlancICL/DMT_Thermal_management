'''
functions for inter/extrapolating temperature distribution throughout
PCM and using this to calculate useful things like solid volume fraction,
liquid volume fraction, state of charge etc...
'''


# IMPORTING LIBRARIES
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


# MAKING DEMO READINGS
readings = [4,5,7,2,4,6,5,7]


# DECLARING FUNCTION
def domain_interp(readings):
    
    # DOMAIN
    # domain size is from the CAD and in mm
    X = np.arange(0,427,1)
    Y = np.arange(0,294,1)
    Z = np.arange(0,168,1)
    domain_points = np.meshgrid(X,Y,Z)
    
    # SENSORS
    # locations for all 8 sensors stored as coordinates [x,y,z]
    sensor_locs = np.array( [[ 60,  72,  49],
                             [ 60, 177,  49],
                             [140, 124,  97],
                             [140, 229,  97],
                             [220,  72,  49],
                             [220, 177,  49],
                             [300, 124,  97],
                             [300, 229,  97]] )
    # values from all 8 sensors
    sensor_vals = np.array(readings).transpose()
    
    # PLOTTING SENSOR LOCATIONS
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(sensor_locs[:,0], sensor_locs[:,1], sensor_locs[:,2])
    ax.set_title('Temperature sensor locations')
    ax.set_xlim(left=0,right=427)
    ax.set_ylim(bottom=0,top=294)
    ax.set_zlim(bottom=0,top=168)
    
    # INTERPOLATION
    

# TESTING FUNCTIONS
domain_interp(readings)