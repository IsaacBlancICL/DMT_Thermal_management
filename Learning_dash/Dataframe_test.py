'''
this is just me experimenting with two libraries: 'pandas' and 'time' so that I can work out
how I'll use them before writing stuff in main code. This file will never actually be used
'''

# importing libraries
import numpy as np
import pandas as pd
import time
import serial
import Calculations as calc

# DOMAIN
# domain size is from the CAD and in mm
# the +1 is because np.arange is an exclusive (ie: not inclusive) range
stepsize = 5
X,Y,Z = np.meshgrid(np.arange(0,427+1,stepsize), # domain X axis
                    np.arange(0,294+1,stepsize), # domain Y axis
                    np.arange(0,168+1,stepsize), # domain Z axis
                    indexing='ij')


# SENSOR LOCATIONS
x = np.array([60,  60, 140, 140, 220, 220, 300, 300])
y = np.array([72, 177, 124, 229,  72, 177, 124, 229])
z = np.array([49,  49,  97,  97,  49,  49,  97,  97])

# make dataframe
df = pd.DataFrame(columns = ['Time', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Solid fraction', 'Liquid fraction', 'Stored'])

# setup pyserial
ser = serial.Serial('COM3', baudrate=9600, timeout=None) # setup serial. Python waits to recieve \n before reading from serial buffer. Beware that I have not set a timeout value, so it might wait forever

while(1):
    # reading serial to list
    serialLine = ser.readline().decode('ascii').rstrip().split(',')
    sensor_list = list(map(int,serialLine))
    sensor_vals = np.array(sensor_list).transpose()
    
    # calculating stuff
    interp_vals = calc.domain_interp(X,Y,Z, x,y,z, sensor_vals)
    calcs_list = calc.SoC(interp_vals)
    
    # putting calculation results in DataFrame
    df.loc[len(df.index)] = [time.strftime("%H:%M:%S", time.localtime())] + sensor_list + calcs_list
    
    # saving DataFrame to csv
    filename = 'filename.csv'
    df.to_csv(filename, index=False)
    
    time.sleep(1.9)