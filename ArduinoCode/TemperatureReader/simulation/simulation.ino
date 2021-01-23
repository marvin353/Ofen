#include <Adafruit_MAX31855.h>
#include <SPI.h>

String data = "Hello From Arduino!";

unsigned long lastMillis;
int t = 0;

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
  Serial1.begin(9600);
  delay(500);

}

/*
int[] simulateTemp() {
  int temps[7] = {0,0,0,0,0,0,0};
  temps[0] = temps[0] + random(-10, 10);
  temps[1] = temps[1] + random(-10, 10);
  temps[2] = temps[2] + random(-10, 10);
  temps[3] = temps[3] + random(-10, 10);
  temps[4] = temps[4] + random(-10, 10);
  temps[5] = temps[5] + random(-10, 10);
  temps[6] = temps[6] + random(-10, 10);
  return;
}

int* simulateTemp2() {
  int temps[7] = {0,0,0,0,0,0,0};
  temps[0] = random(0, 400);
  temps[1] = random(0, 400);
  temps[2] = random(0, 400);
  temps[3] = random(0, 400);
  temps[4] = random(0, 400);
  temps[5] = random(0, 400);
  temps[6] = random(0, 400);

  return temps;
}*/

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("C = "); 
  //Serial.println(kTC.readCelsius());
  // delay so it doesn't scroll too fast.
  //delay(1000);
  
  //Serial.println(data);//data that is being Sent
  //delay(200);

  if (millis() - lastMillis >= 1000UL) {
    lastMillis = millis();
    /*
    double t1 = kTC1.readCelsius();
    double t2 = kTC2.readCelsius();
    double t3 = kTC3.readCelsius();
    double t4 = kTC4.readCelsius();
    double t5 = kTC5.readCelsius();
    double t6 = kTC6.readCelsius();
    double t7 = kTC7.readCelsius();
    */
    int temps[7] = {0,0,0,0,0,0,0};
    temps[0] = t + random(-5, 5);
    temps[1] = t + random(-50, 50);
    temps[2] = t + random(-50, 50);
    temps[3] = t + random(-50, 50);
    temps[4] = t + random(-50, 50);
    temps[5] = t + random(-50, 50);
    temps[6] = t + random(-50, 50);

    if (t < 320) {
      t = t + random(2,5);
    } else {
      t = t + random(-5,5);
    }
  
    int t1 = temps[0];
    int t2 = temps[1];
    int t3 = temps[2];
    int t4 = temps[3];
    int t5 = temps[4];
    int t6 = temps[5];
    int t7 = temps[6];
  
    char buf[200];
    String s1 = "######T:";
    s1 += t1;
    s1 += "-";
    s1 += t2;
    s1 += "-";
    s1 += t3;
    s1 += "-";
    s1 += t4;
    s1 += "-";
    s1 += t5;
    s1 += "-";
    s1 += t6;
    s1 += "-";
    s1 += t7;

    if(temps[0] == 4) {
      Serial1.print("lessWood");
    }
  

    //String dataStrng = "Temp1:%d-Temp2:%d-Temp3:%d-Temp4:%d-Temp5:%d-Temp6:%d-Temp7:%d",t1,t2,t3,t4,t5,t6,t7;
    Serial.println(s1);
    s1.toCharArray(buf,200);//Serial.read();
    Serial1.print(buf);
  }

  String s;

  if (Serial1.available()) {
    s = Serial1.readString();
    String sub = s.substring(0,1);
    // D Drosselklappe
    // L Lüftung
    // G Gebläse
    // A Automode
    // F Fastheatup
    // H temp2hold
    
    if (sub == "D" || sub == "A" || sub == "F" || sub == "G" || sub == "L" || sub == "H") {
      Serial.println(s) ;
    }
  }
  
  //delay(1000);

}
