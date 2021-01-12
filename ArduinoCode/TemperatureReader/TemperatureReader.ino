#include <Adafruit_MAX31855.h>
#include <SPI.h>

String data = "Hello From Arduino!";

//1
int maxSO1 = 52;
int maxCS1 = 53;
int maxSCK1 = 50;
//Create a MAX31855 reference and tell it what pin does what
Adafruit_MAX31855 kTC1(maxSCK1, maxCS1, maxSO1);

//2
int maxSO2 = 51;
int maxCS2 = 48;
int maxSCK2 = 49;
//Create a MAX31855 reference and tell it what pin does what
Adafruit_MAX31855 kTC2(maxSCK2, maxCS2, maxSO2);

//3
int maxSO3 = 46;
int maxCS3 = 47;
int maxSCK3 = 44;
//Create a MAX31855 reference and tell it what pin does what
Adafruit_MAX31855 kTC3(maxSCK3, maxCS3, maxSO3);

//4
int maxSO4 = 45;
int maxCS4 = 42;
int maxSCK4 = 43;
//Create a MAX31855 reference and tell it what pin does what
Adafruit_MAX31855 kTC4(maxSCK4, maxCS4, maxSO4);

//5
int maxSO5 = 40;
int maxCS5 = 41;
int maxSCK5 = 38;
//Create a MAX31855 reference and tell it what pin does what
Adafruit_MAX31855 kTC5(maxSCK5, maxCS5, maxSO5);

//6
int maxSO6 = 37;
int maxCS6 = 36;
int maxSCK6 = 39;
//Create a MAX31855 reference and tell it what pin does what
Adafruit_MAX31855 kTC6(maxSCK6, maxCS6, maxSO6);

//7
int maxSO7 = 32;
int maxCS7 = 35;
int maxSCK7 = 34;
//Create a MAX31855 reference and tell it what pin does what
Adafruit_MAX31855 kTC7(maxSCK7, maxCS7, maxSO7);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500);

}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("C = "); 
  //Serial.println(kTC.readCelsius());
  // delay so it doesn't scroll too fast.
  //delay(1000);
  
  //Serial.println(data);//data that is being Sent
  //delay(200);

  double t1 = kTC1.readCelsius();
  double t2 = kTC2.readCelsius();
  double t3 = kTC3.readCelsius();
  double t4 = kTC4.readCelsius();
  double t5 = kTC5.readCelsius();
  double t6 = kTC6.readCelsius();
  double t7 = kTC7.readCelsius();
/*
  int t1 = 11;
  int t2 = 12;
  int t3 = 13;
  int t4 = 14;
  int t5 = 15;
  int t6 = 16;
  int t7 = 17;*/

  String s1 = "Temp1:";
  s1 += t1;
  s1 += "-Temp2:";
  s1 += t2;
  s1 += "-Temp3:";
  s1 += t3;
  s1 += "-Temp4:";
  s1 += t4;
  s1 += "-Temp5:";
  s1 += t5;
  s1 += "-Temp6:";
  s1 += t6;
  s1 += "-Temp7:";
  s1 += t7;


  //String dataStrng = "Temp1:%d-Temp2:%d-Temp3:%d-Temp4:%d-Temp5:%d-Temp6:%d-Temp7:%d",t1,t2,t3,t4,t5,t6,t7;
  Serial.println(s1);
  delay(1000);

}
