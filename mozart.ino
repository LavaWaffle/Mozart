// #include "Servo.h"
#include <VarSpeedServo.h>
#include <LiquidCrystal.h>
#include <SharpIR.h>

SharpIR distanceSensor(SharpIR::GP2Y0A41SK0F, A0);

const uint8_t rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
// yankee doodle

VarSpeedServo fingerServo;
VarSpeedServo controlServo;

//                      c    d    e   f   g   a   b   C
uint8_t controlAngles[] = {135, 110, 92, 77, 66, 55, 43, 30};

uint8_t noteToControlAngle(char note) {
    switch(note) {
        case 'c': return 131;
        case 'd': return 112;
        case 'e': return 94;
        case 'f': return 78;
        case 'g': return 63;
        case 'a': return 49;
        case 'b': return 37;
        case 'C': return 30;
        default: 
          Serial.print("[NTCA] Error: Invalid input char {");
          Serial.print(note);
          Serial.println("}");
          return 128; // Return -1 for invalid input
    }
}

struct Note {
  uint8_t octave;
  char note;
  int duration;
  bool terminator;
  Note(uint8_t o = 3, char n = 'c', int d = 500, bool t = false) : octave(o), note(n), duration(d), terminator(t) {}
};

Note song[60] = {
  {4, 'c', 250},  // C
  {4, 'd', 250},  // D
  {4, 'e', 250},  // E
  {4, 'f', 250},  // F
  {4, 'g', 250},  // G
  {4, 'a', 250},  // A
  {4, 'b', 250},  // B
  {4, 'C', 250}   // High C (extra key)
};

void up() {
  fingerServo.write(105);
}

void setup() {
  // put your setup code here, to run once:
  // controlServo.read()
  controlServo.attach(9);
  fingerServo.attach(10);
  
  up();
  controlServo.write(130,20);
  // controlServo.writeMicroseconds(int value)
  
  lcd.begin(16,2);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.write("Mozart");
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  delay(50);
}

char buffer[60];
char buffet[16];
int songIndex = 0;
int octave = 0;
char note = 'c';
int duration = 0;
int valueIndex = 0;
String currentValue = "";
bool dataStarted = false;
void loop() {
char incomingByte;
  // put your main code here, to run repeatedly:
  up();

  while (true) {
    if (Serial.available() > 0) {
      incomingByte = Serial.read();
      // lcd.clear();
      // lcd.write("GOT SMTHN");
      // lcd.setCursor(0,1);
      // // String owo = String(incomingByte);
      // // lcd.write(incomingByte, 2);
      // Serial.print("'");
      // Serial.print(incomingByte);
      // Serial.print("' ");
      // Serial.println(incomingByte == );
      // // lcd.write()
      // lcd.setCursor(0,0);

      // Start processing only when we see a digit or a valid note character
      if (!dataStarted && incomingByte == 'S') {
        dataStarted = true;
        lcd.clear();
        lcd.write("YAY");
        Serial.println("GOOD NEWS");
        continue;
      }

      if (!dataStarted) {
        continue;  // Skip this iteration if data hasn't started yet
      }

      if (incomingByte == '|') {  // End of transmission
        break;
      }

      if (incomingByte == ',' || incomingByte == '\n') {
        // Serial.print(valueIndex);
        // Serial.print(" : ");
        // Serial.println(currentValue);
        switch(valueIndex) {
          case 0:
            octave = currentValue.toInt();
            break;
          case 1:
            note = currentValue.charAt(0);
            break;
          case 2:
            duration = currentValue.toInt();
            // if (octave == )
            song[songIndex++] = Note(octave, note, duration);
            Serial.print("N: ");
            Serial.print(note);
            Serial.print(" O: ");
            Serial.print(octave);
            Serial.print(" DUR: ");
            Serial.println(duration);
            break;
        }
        valueIndex = (valueIndex + 1) % 3;
        currentValue = "";
      } else if (incomingByte != '\\') {  // Ignore backslashes
        currentValue += incomingByte;
      }
    }
  }

  song[songIndex++] = Note(4,'c',500,true);
  dataStarted=false;
  Serial.println("SongIndexSize: ");
  Serial.println(songIndex);

  int currentOctave = 4;

  toOctave(currentOctave, song[0].octave);
    currentOctave = song[0].octave; 

  for (int i = 0; i < sizeof(song) / sizeof(Note); i++) {
    lcd.clear();
    lcd.setCursor(0, 0);
    Note currentNote = song[i];
    if (currentNote.terminator) {
      toOctave(currentOctave, 4);
      lcd.write("Done!");
      return;
    }
    int controlServoAngle = noteToControlAngle(currentNote.note);
    lcd.write("I |N|O| A | Dur");
    lcd.setCursor(0, 1);
    sprintf(buffet, "%d|%c|%d|%d|%d", i, currentNote.note, currentNote.octave, controlServoAngle, currentOctave);
    lcd.write(buffet);
    sprintf(buffer, "Index: %d, Note: %c, Duration: %d, Octave: %d, CAngle: %d", i, currentNote.note, currentNote.duration, currentNote.octave, controlServoAngle);
    // Serial.println(buffer);
    unsigned long startTime = millis();  // Get the start time

    // Perform the servo write operation
    controlServo.write(controlServoAngle, 79);
    // Calculate how much time has passed
    toOctave(currentOctave, currentNote.octave);
    currentOctave = currentNote.octave; 
    while (controlServo.isMoving()) {
      delay(5);
    }

    unsigned long elapsedTime = millis() - startTime;
    // If less than 250ms has passed, wait the remainder
    if (elapsedTime < 350) {
        delay(350 - elapsedTime);
    }
    // Serial.print("OWO: ");
    // Serial.println(controlServo.read());
    fingerServo.write(69);
    delay(currentNote.duration);
    up();
    delay(0);
  }
  
  // toOctave(currentOctave, 4);

  // delay(10000);
}

void toOctave(int currentOctave, int desiredOctave) {
  int difference = currentOctave - desiredOctave;
  if (difference == 0) {
    return;
  }
  if (difference < 0) {
    // currentOctave < desiredOctave
    for (int i = 0; i < difference*-1; i++) {
      Serial.println("CUP");
    }
  } else if (difference > 0) {
    for (int i =0; i < difference; i++) {
      Serial.println("CDOWN");
    }
  }
}
