/*
sends dummy serial data for testing with Python
*/

#define PERIOD 10000

// SETUP
void setup(void)
{
  Serial.begin(9600);
}


// MAIN LOOP
void loop(void)
{
  Serial.print("76,45,67,78,81,45,67,92");
  Serial.println();
  delay(PERIOD);

  Serial.print("60,51,64,68,82,78,45,78");
  Serial.println();
  delay(PERIOD);

  Serial.print("63,55,46,71,92,75,52,63");
  Serial.println();
  delay(PERIOD);
}
