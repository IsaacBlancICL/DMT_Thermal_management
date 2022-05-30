'''
A hastily reduced version of the file app.py

Just reads the data from the Arduino via serial and saves it, without doing any of the calculations or dash stuff in app.py
'''

# IMPORTING LIBRARIES
# data handling libraries
import numpy as np
import pandas as pd
import serial
import time


# DATA SETUP
ser = serial.Serial('COM3', baudrate=9600, timeout=None)
df = pd.DataFrame(columns = ['Time', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8'])

# reading serial to list
serialLine = ser.readline().decode('ascii').rstrip().split(',')
sensor_list = [float(item) for item in serialLine]
sensor_vals = np.array(sensor_list).transpose()

# putting calculation results in DataFrame
df.loc[len(df.index)] = [time.strftime("%H:%M:%S", time.localtime())] + sensor_list
# saving DataFrame to csv
filename = 'test_run_1.csv'
df.to_csv(filename, index=False)


# CLOSING SERIAL PORT
ser.close()