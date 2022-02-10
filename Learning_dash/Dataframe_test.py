'''
this is just me experimenting with two libraries: 'pandas' and 'time' so that I can work out
how I'll use them before writing stuff in main code. This file will never actually be used
'''

# importing libraries
import pandas as pd
import time

# make dataframe
df = pd.DataFrame(columns = ['Time', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Solid fraction', 'Liquid fraction', 'Stored'])







# reading serial to list
serialLine = ser.readline().decode('ascii')
sensor_list = # serialLine

# calculating stuff
interp_vals = domain_interp(domain, sensor_locs, readings)
calcs_list = SoC(interp_vals)

# putting calculation results in DataFrame
df.loc[len(df.index)] = [time.strftime("%H:%M:%S", time.localtime())] + sensor_list + calcs_list

# saving DataFrame to csv
filename = 'filename.csv'
df.to_csv(filename, index=False)