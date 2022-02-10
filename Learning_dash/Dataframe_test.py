'''
this is just me experimenting with two libraries: 'pandas' and 'time' so that I can work out
how I'll use them before writing stuff in main code. This file will never actually be used
'''

# importing libraries
import pandas as pd
import time

# make dataframe
df = pd.DataFrame(columns = ['Time', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Solid fraction', 'Liquid fraction', 'SoC'])

for i in range (0,5):
    # entering data
    sensor_list = [1,2,3,4,5,6,7,8]
    calcs_list = [1,2,3]
    df.loc[len(df.index)] = [time.strftime("%H:%M:%S", time.localtime())] + sensor_list + calcs_list
    
    # saving to csv
    filename = 'filename.csv'
    df.to_csv(filename, index=False)