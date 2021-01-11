void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //char c;
  String str = "T1:123-T2:234-T3:345-T4:456-T5:567-T6:678-T7:789";
  char buf[200];
  
  String s;
  
  //if (Serial.available()) {
    str.toCharArray(buf,200);//Serial.read();
    Serial1.print(buf);
  //}
  if (Serial1.available()) {
    s = Serial1.readString();
    String sub = s.substring(0,1);
    // D Drosselklappe
    // L Lüftung
    // G Gebläse
    // A Automode
    // F Fastheatup
    
    if (sub == "D" || sub == "A" || sub == "F" || sub == "G" || sub == "L") {
      Serial.println(s) ;
    }
  }

  delay(2000);
}

float strProcessAndToFloat(String str) {
  return str.toFloat()*100;
}

String FloatToString(float f) {
  char buf[10];
  dtostrf(f,10,2,buf);
  Serial.println("test2");
  String s = buf;
  Serial.println("test3");
  return s;
}

String test(String s) {
  Serial.println("test");
  return FloatToString(strProcessAndToFloat(s));
}

