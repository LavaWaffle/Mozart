// #include "Servo.h"
#include <VarSpeedServo.h>

#define speed 30

VarSpeedServo octaveServo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  octaveServo.attach(9);
  octaveServo.write(19);
  pinMode(13, OUTPUT);
}

bool on = false;
void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Ready");
  while (Serial.available() == 0) {}
  String res = Serial.readStringUntil('\n');
  Serial.println(res);
  res.trim();
  if (res[0] != 'C') {
    return;
  }
  Serial.println(res);
  if (res == "CUP") {
    octaveServo.write(13, speed, true);
    Serial.println("GOING UP");
    // delay(100);
    octaveServo.write(19, speed, true);
  } else if (res == "CDOWN") {
    octaveServo.write(25, speed, true);
    Serial.println("GOIND DOWN");
    // delay(100);
    octaveServo.write(19, speed, true);
  }
  delay(50);
  if (on) {
    digitalWrite(13, LOW);
  } else {
    digitalWrite(13, HIGH);
  }
  on = !on;
}
