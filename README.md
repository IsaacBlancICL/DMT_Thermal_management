# DMT - Thermal management

We need to [read the 8 DS18B20 temperature sensors](https://lastminuteengineers.com/multiple-ds18b20-arduino-tutorial/) in the PCM case, using an Arduino. The Arduino must do two things with the data. Firstly, it must decide which valves need to be open and shut. Secondly, it must send this data to a laptop, where it'll be saved and graphed in real time.

## Sensor addresses

The sensors all have unique addresses. The Arduino OneWire library uses these addresses so it knows which sensors its reading data from. Finding the addresses required plugging in each sensor one-by-one and running the [Address_finder](https://github.com/IsaacBlancICL/DMT_Thermal_management/blob/main/Address_finder/Address_finder.ino) script. I've labelled the sensors with masking tape and written the addresses below.

Sensor 1 : 0x28, 0xA2, 0x50, 0x93, 0x31, 0x21, 0x03, 0x42
