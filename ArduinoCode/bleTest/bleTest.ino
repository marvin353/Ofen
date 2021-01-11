//////////////////////////////////////////////////
//
// Kleines interaktives Demo
// (c) 2016, Michael Stal
//  Nutzung:
//     Sketch auf Arduino laden
//     An Arduino HM-10 anschließen
//     
//     Über BLE App serielle Verbindung aufbauen,
//     "ein" oder "aus" ins Textfeld eingeben, 
//     und LED beobachten.
//
///////////////////////////////////////////////////


// Wir verwenden Software Serial
#define softserial

// Eingebaute LED nutzen:
const int LED  = 13;
const int LED_ext  = A0;


#ifdef softserial
  #include <SoftwareSerial.h>
  const int BTRX = 0;  // 11
  const int BTTX = 1;  // 10
  SoftwareSerial SerialBT(BTRX, BTTX);
#else 
  HardwareSerial SerialBT = Serial1;
#endif


// Die versendete Nachricht:
String msg; 

void setup() {
  //Serial.begin(9600);
  SerialBT.begin(9600);
  SerialBT.println("Bluetooth-Verbindung steht");
  //pinMode(LED, OUTPUT);
}

///////////////////////////////////////////////////
//
// loop
//    In jeder Iteration auf Nachricht warten,
//    Nachricht analysieren,
//    Aktion auslösen (LED ein/aus)
//
///////////////////////////////////////////////////

void loop() {
  delay(2000);
  SerialBT.println("Blue");
  if (SerialBT.available()){      // Daten liegen an
     msg = SerialBT.readString(); // Nachricht lesen
     if (msg == "ein") {
         //digitalWrite(LED, HIGH);
         //digitalWrite(LED_ext, HIGH);
         SerialBT.print("LED an Pin ");
         SerialBT.print(LED);
         SerialBT.println(" ist eingeschaltet!");
      } 
      else
      if (msg == "aus") {
         //digitalWrite(LED, LOW);
         //digitalWrite(LED_ext, LOW);
         SerialBT.print("LED an Pin ");
         SerialBT.print(LED);
         SerialBT.println(" ist ausgeschaltet!");
      }
      else {
         SerialBT.print("Kommando <");
         SerialBT.print(msg);
         SerialBT.println("> nicht bekannt");
      }
    }
}                                          
