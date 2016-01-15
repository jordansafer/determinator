#include <Wire.h>
#include "Arduino.h"

#include <FIMU_ADXL345.h>
#define FIMU_ACC_ADDR ADXL345_ADDR_ALT_LOW // SDO connected to GND
#include <FIMU_ITG3200.h>


#ifndef FreeSixIMU_h
#define FreeSixIMU_h


#define FIMU_BMA180_DEF_ADDR BMA180_ADDRESS_SDO_LOW
#define FIMU_ITG3200_DEF_ADDR ITG3200_ADDR_AD0_LOW // AD0 connected to GND
// HMC5843 address is fixed so don't bother to define it


#define twoKpDef  (2.0f * 0.5f) // 2 * proportional gain
#define twoKiDef  (2.0f * 0.1f) // 2 * integral gain

#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif

class FreeSixIMU
{
  public:
    FreeSixIMU();
    void init();
    void init(bool fastmode);
    void init(int acc_addr, int gyro_addr, bool fastmode);
    void getRawValues(int * raw_values);
    void getValues(float * values);
    void getQ(float * q);
    void getEuler(float * angles);
    void getYawPitchRoll(float * ypr);
    void getAngles(float * angles);
    
    
	ADXL345 acc;
    ITG3200 gyro;
    
    int* raw_acc, raw_gyro, raw_magn;
    
  private:
    void AHRSupdate(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz);
    //float q0, q1, q2, q3; // quaternion elements representing the estimated orientation
    float iq0, iq1, iq2, iq3;
    float exInt, eyInt, ezInt;  // scaled integral error
    volatile float twoKp;      // 2 * proportional gain (Kp)
    volatile float twoKi;      // 2 * integral gain (Ki)
    volatile float q0, q1, q2, q3; // quaternion of sensor frame relative to auxiliary frame
    volatile float integralFBx,  integralFBy, integralFBz;
    unsigned long lastUpdate, now; // sample period expressed in milliseconds
    float sampleFreq; // half the sample period expressed in seconds
    int startLoopTime;
};

float invSqrt(float number);

#endif // FreeSixIMU_h
