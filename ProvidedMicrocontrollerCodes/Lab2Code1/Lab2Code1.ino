
/*
 * This code measures an analog signal with a given sampling frequency
 * Created by Patrick Mayerhofer June 2020
 */

#define sf 1000 //change this for wanted sampling fq
int tc (1000/(sf));     // time constant

unsigned int ADC_Value = 0;    //ADC current value
unsigned long last_time = 0;
void setup() {
  Serial.begin(500000);
}


// the loop routine runs over and over again forever:
void loop() {

  if (millis() - last_time >= tc) {
    last_time = millis();
    ADC_Value = analogRead(A0);
    
    Serial.print(ADC_Value);
    Serial.print('\t');
    Serial.print(millis());
    Serial.println();
    }
}
