/*
I'm following a tutorial (link below) on interfacing multiple DS18B20 temperature sensors
with an Arduino. The code is copied from there with no changes other than this comment and
the sensor addresses.

https://lastminuteengineers.com/multiple-ds18b20-arduino-tutorial/
*/

#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

// Addresses of 3 DS18B20s
uint8_t sensor1[8] = { 0x28, 0x08, 0x7D, 0xAB, 0x31, 0x21, 0x03, 0x91 };
uint8_t sensor2[8] = { 0x28, 0xA2, 0x50, 0x93, 0x31, 0x21, 0x03, 0x42 };
uint8_t sensor3[8] = { 0x28, 0xEB, 0x5B, 0x88, 0x31, 0x21, 0x03, 0x7D };

void setup(void)
{
  Serial.begin(9600);
  sensors.begin();
}

void loop(void)
{
  sensors.requestTemperatures();
  
  Serial.print("Sensor 1: ");
  printTemperature(sensor1);
  
  Serial.print("Sensor 2: ");
  printTemperature(sensor2);
  
  Serial.print("Sensor 3: ");
  printTemperature(sensor3);
  
  Serial.println();
  delay(1000);
}

void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  Serial.print(tempC);
  Serial.print((char)176);
  Serial.print("C  |  ");
  Serial.print(DallasTemperature::toFahrenheit(tempC));
  Serial.print((char)176);
  Serial.println("F");
}
