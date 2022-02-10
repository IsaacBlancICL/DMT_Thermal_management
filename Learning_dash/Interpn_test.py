'''
playing around with interpn function

In the end, I realised this was the wrong function to use because
it requires data that is structured across the grid (ie: a datapoint
for every point in the grid). Instead, I found that griddata is the
right function to use, however I'm keeping this Python file because
it contains useful numbers describing the positions of the sensors
(from the CAD) and the PCM dimensions (also from the CAD).
'''

# IMPORTING LIBRARIES
import numpy as np
from scipy.interpolate import interpn


# SENSOR VALUES
readings = [4,5,7,2,4,6,5,7]

# making an array with the correct shape where every element is an NaN
sensor_values = np.empty((8,8,8))
sensor_values[:] = np.NaN
# filling the elements with sensor values
for i in range(0,len(readings)):
    sensor_values[i,i,i] = readings[i]


# SENSOR POINTS
x = [60,60,140,140,220,220,300,300]
y = [72,177,124,229,72,177,124,229]
z = [49,49,97,97,49,49,97,97]

sensor_points = np.meshgrid(x,y,z)

# not used for anything, but helpful for figuring out how these lists are working
def sensor_coord(num):
    print('Sensor', num, 'is at coord:')
    print('x = ', sensor_points[0][num,num,num])
    print('y = ', sensor_points[1][num,num,num])
    print('z = ', sensor_points[2][num,num,num])

# DOMAIN POINTS
# X = np.arange(0,427,1)
# Y = np.arange(0,294,1)
# Z = np.arange(0,168,1)

# domain_points = np.meshgrid(X,Y,Z)


# INTERPOLATION
