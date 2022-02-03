/*
This script is for finding the addresses of the DS18B20 temperature sensors.
It won't actually be used in the final project, but I need to use it now so that
I know what addresses to use in the actual project code.

I'm following a tutorial (link below) on interfacing multiple DS18B20 temperature sensors
with an Arduino. The code is copied from there with no changes other than this comment.

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

// variable to hold device addresses
DeviceAddress Thermometer;

int deviceCount = 0;

void setup(void)
{
  // start serial port
  Serial.begin(9600);

  // Start up the library
  sensors.begin();

  // locate devices on the bus
  Serial.println("Locating devices...");
  Serial.print("Found ");
  deviceCount = sensors.getDeviceCount();
  Serial.print(deviceCount, DEC);
  Serial.println(" devices.");
  Serial.println("");
  
  Serial.println("Printing addresses...");
  for (int i = 0;  i < deviceCount;  i++)
  {
    Serial.print("Sensor ");
    Serial.print(i+1);
    Serial.print(" : ");
    sensors.getAddress(Thermometer, i);
    printAddress(Thermometer);
  }
}

void loop(void)
{}

void printAddress(DeviceAddress deviceAddress)
{ 
  for (uint8_t i = 0; i < 8; i++)
  {
    Serial.print("0x");
    if (deviceAddress[i] < 0x10) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
    if (i < 7) Serial.print(", ");
  }
  Serial.println("");
}
