/*
I'm following a tutorial (link below) on interfacing multiple DS18B20 temperature sensors
with an Arduino. The code is copied from there with no changes other than this comment and
the sensor addresses.

https://lastminuteengineers.com/multiple-ds18b20-arduino-tutorial/

Requires 'DallasTemperature' and 'OneWire' libraries, both of which can be installed by
going Sketch > Include Library > Manage Libararies and then typing in DallasTemperature.
Click instal and it'll ask if you want to instal OneWire as well. Click yes.

DallasTemperature documentation:
https://github.com/milesburton/Arduino-Temperature-Control-Library
*/

#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

// Define measurement time period in milliseconds - ie: how often the Arduino will make a new set of measurements
#define PERIOD 1000

// Addresses of 3 DS18B20s
uint8_t sensor1[8] = { 0x28, 0x08, 0x7D, 0xAB, 0x31, 0x21, 0x03, 0x91 };
uint8_t sensor2[8] = { 0x28, 0xA2, 0x50, 0x93, 0x31, 0x21, 0x03, 0x42 };
uint8_t sensor3[8] = { 0x28, 0xEB, 0x5B, 0x88, 0x31, 0x21, 0x03, 0x7D };


// SETUP
void setup(void)
{
  Serial.begin(9600);
  sensors.begin();
}


// MAIN LOOP
void loop(void)
{
  sensors.requestTemperatures();
  
  printTemperature(sensor1, true);
  printTemperature(sensor2, true);
  printTemperature(sensor3, false);
  
  Serial.println();
  delay(PERIOD);
}


// DEFINING FUNCTIONS
/*
function to read a given temperature sensor (in deg C) and print the result to serial.
If comma=true, then it will also print a comma after the number.
Therefore, repeated use of this function can give CSV output to the serial monitor.
*/
void printTemperature(DeviceAddress deviceAddress, boolean comma)
{
  float tempC = sensors.getTempC(deviceAddress);
  if(comma){Serial.print(String(tempC) + ',');}
  else     {Serial.print(tempC);}
}
