#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <Wire.h>
#include "SparkFunMPL3115A2.h"


float angles[3]; // yaw pitch roll

// Set the FreeSixIMU object
FreeSixIMU sixDOF = FreeSixIMU();
MPL3115A2 myPressure;
float q[4];

void setup() { 
  Serial.begin(9600);
  Wire.begin();
  
  myPressure.begin(); // Get sensor online
  myPressure.setModeAltimeter();
  myPressure.setOversampleRate(7);
  myPressure.enableEventFlags();
  delay(5);
  sixDOF.init(); //begin the IMU
  delay(5);
}

void loop() { 
  
  float altitude = myPressure.readAltitudeFt();
  Serial.print(" Altitude(ft):");
  Serial.print(altitude, 2);
  float temperature = myPressure.readTempF();
  Serial.print(" Temp(f):");
  Serial.print(temperature, 2);
  Serial.print(" | "); 

  sixDOF.getQ(q);
  Serial.print("Q values: ");
  Serial.print(q[0]);
  Serial.print(" | ");
  Serial.print(q[1]);
  Serial.print(" | ");
  Serial.print(q[2]);
  Serial.print(" | ");
  Serial.print(q[3]);
  Serial.print(" | ");
  Serial.print(""); //line break

  
  sixDOF.getEuler(angles);
  Serial.print("Euler angles: ");
  Serial.print(angles[0]);
  Serial.print(" | ");  
  Serial.print(angles[1]);
  Serial.print(" | ");
  Serial.println(angles[2]);
  
  delay(100); 
}

