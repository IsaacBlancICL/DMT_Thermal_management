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

// Addresses of 8 DS18B20 sensors
uint8_t sensor1[8] = { 0x28, 0xA2, 0x50, 0x93, 0x31, 0x21, 0x03, 0x42 };
uint8_t sensor2[8] = { 0x28, 0x08, 0x7D, 0xAB, 0x31, 0x21, 0x03, 0x91 };
uint8_t sensor3[8] = { 0x28, 0xEB, 0x5B, 0x88, 0x31, 0x21, 0x03, 0x7D };
uint8_t sensor4[8] = { 0x28, 0x87, 0x7C, 0x97, 0x31, 0x21, 0x03, 0xC8 };
uint8_t sensor5[8] = { 0x28, 0x58, 0x8A, 0x99, 0x31, 0x21, 0x03, 0x07 };
uint8_t sensor6[8] = { 0x28, 0x85, 0x87, 0x94, 0x31, 0x21, 0x03, 0xF8 };
uint8_t sensor7[8] = { 0x28, 0x3D, 0x41, 0x9D, 0x31, 0x21, 0x03, 0x73 };
uint8_t sensor8[8] = { 0x28, 0x8C, 0xA2, 0x8B, 0x31, 0x21, 0x03, 0xE6 };

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
  printTemperature(sensor3, true);
  printTemperature(sensor4, true);
  printTemperature(sensor5, true);
  printTemperature(sensor6, true);
  printTemperature(sensor7, true);
  printTemperature(sensor8, false);
  
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
