# DMT - Thermal management

We need to [read the 8 DS18B20 temperature sensors](https://lastminuteengineers.com/multiple-ds18b20-arduino-tutorial/#:~:text=Wiring%20Multiple%20DS18B20%20Sensors%20to,digital%20pin%202%20on%20arduino.) in the PCM case, using an Arduino. The Arduino must do two things with the data. Firstly, it must decide which valves need to be open and shut. Secondly, it must send this data to a laptop, where it'll be saved and graphed in real time.
