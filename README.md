# DMT - Thermal management

We need to [read the 8 DS18B20 temperature sensors](https://lastminuteengineers.com/multiple-ds18b20-arduino-tutorial/) in the PCM case, using an Arduino. The Arduino must do two things with the data. Firstly, it must decide which valves need to be open and shut. Secondly, it must send this data to a laptop, where it'll be saved and graphed in real time. In the end, I only ended up doing the second part of that. We may do the first part using pseudocode or something for speed.

## Sensor addresses

The sensors all have unique addresses. The Arduino OneWire library uses these addresses so it knows which sensors its reading data from. Finding the addresses required plugging in each sensor one-by-one and running the [Address_finder.ino](https://github.com/IsaacBlancICL/DMT_Thermal_management/blob/main/Address_finder/Address_finder.ino) script. I've labelled the sensors with masking tape and written the addresses below.

Updated after all the labels got removed:

Sensor 1: 0x28, 0xBD, 0x51, 0x88, 0x31, 0x21, 0x03, 0x5C <br>
Sensor 2: 0x28, 0x8C, 0xA2, 0x8B, 0x31, 0x21, 0x03, 0xE6 <br>
Sensor 3: 0x28, 0x85, 0x87, 0x94, 0x31, 0x21, 0x03, 0xF8 <br>
Sensor 4: 0x28, 0x3D, 0x41, 0x9D, 0x31, 0x21, 0x03, 0x73 <br>
Sensor 5: 0x28, 0x08, 0x7D, 0xAB, 0x31, 0x21, 0x03, 0x91 <br>
Sensor 6: 0x28, 0xEB, 0x5B, 0x88, 0x31, 0x21, 0x03, 0x7D <br>
Sensor 7: 0x28, 0x87, 0x7C, 0x97, 0x31, 0x21, 0x03, 0xC8 <br>
Sensor 8: 0x28, 0x58, 0x8A, 0x99, 0x31, 0x21, 0x03, 0x07 <br>

Spare two sensors still in main DMT box:

0x28, 0xA2, 0x50, 0x93, 0x31, 0x21, 0x03, 0x42 <br>
0x28, 0x28, 0x58, 0x8A, 0x31, 0x21, 0x03, 0xF2 <br>
