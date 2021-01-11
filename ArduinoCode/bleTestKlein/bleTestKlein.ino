#include <SoftwareSerial.h>

SoftwareSerial ble_device(7,8);

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  ble_device.begin(9600);

}

void loop() {
/*delay(2000);
  float f = 12.3;
  char f_str[6];

  dtostrf(f,3,1,f_str);
  ble_device.write(f_str);*/

  char c;
  
  if (Serial.available()) {
    c = Serial.read();
    ble_device.print(c);
  }
  if (ble_device.available()) {
    c = ble_device.read();
    Serial.print(c);
  }

}
