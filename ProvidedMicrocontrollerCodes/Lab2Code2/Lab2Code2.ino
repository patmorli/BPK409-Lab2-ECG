/*
 * This code measures an analog signal with a given sampling frequency
 * and logs it to a micro SD in the SparkFun Qwiic OpenLog
 * Created by Patrick Mayerhofer June 2020
 */

volatile unsigned int ADC_Value = 0;    //ADC current value


//*** added these lines for logging
#include <Wire.h>
#include "SparkFun_Qwiic_OpenLog_Arduino_Library.h"
OpenLog myLog; //Create instance
char filename[] = "ECGdata.txt";
//***

void setup() {
  Wire.begin();
  myLog.begin(); //Open connection to OpenLog (no pun intended)
  delay(500);
  myLog.append(filename);
  
}

void loop() {
        ADC_Value = analogRead(A0);
        myLog.append(filename);
        myLog.print(ADC_Value);  
        myLog.print('\t');        
        myLog.print(millis());
        myLog.println();
        
}
