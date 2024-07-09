#include "Servo.h"

// yankee doodle

Servo fingerServo;
Servo controlServo;

//                      c    d    e   f   g   a   b   C
int controlAngles[] = {135, 110, 95, 77, 66, 55, 43, 30};

int noteToControlAngle(char note) {
    switch(note) {
        case 'c': return 130;
        case 'd': return 112;
        case 'e': return 93;
        case 'f': return 79;
        case 'g': return 69;
        case 'a': return 57;
        case 'b': return 47;
        case 'C': return 30;
        default: 
          Serial.print("[NTCA] Error: Invalid input char {");
          Serial.print(note);
          Serial.println("}");
          return 128; // Return -1 for invalid input
    }
}

struct Note {
  int octave;
  char note;
  int duration;
  bool terminator;
  Note(int o = 3, char n = 'c', int d = 500, bool t = false) : octave(o), note(n), duration(d), terminator(t) {}
};

Note song[99] = {
  {3, 'c', 250},  // C
  {3, 'd', 250},  // D
  {3, 'e', 250},  // E
  {3, 'f', 250},  // F
  {3, 'g', 250},  // G
  {3, 'a', 250},  // A
  {3, 'b', 250},  // B
  {3, 'C', 250}   // High C (extra key)
};

void up() {
  fingerServo.write(105);
}

void setup() {
  // put your setup code here, to run once:
  // controlServo.read()
  controlServo.attach(9);
  fingerServo.attach(6);
  
  up();
  controlServo.write(130);
  
  Serial.begin(9600);
  delay(50);
}

char buffer[100];
void loop() {
  // put your main code here, to run repeatedly:
  up();

  while (Serial.available() == 0) {
    delay(50);
  }
  String j = Serial.readStringUntil('|');
  if (j.length() < 2) return;
  j.replace("\\n", "\n");
   String f = "3,c,200\n3,b,150\n5,c,250";
  Serial.println("=========");
  Serial.println(j);
   Serial.println(f);
   Serial.println("===========");
  int songIndex = 0;
  int stringIndex = 0;
  while (stringIndex < j.length()) {
    int commaIndex = j.indexOf(',', stringIndex);
    int octave = j.substring(stringIndex, commaIndex).toInt();
    
    stringIndex = commaIndex + 1;
    commaIndex = j.indexOf(',', stringIndex);
    char note = j.charAt(stringIndex);
    
    stringIndex = commaIndex + 1;
    int newlineIndex = j.indexOf('\n', stringIndex);
    if (newlineIndex == -1) newlineIndex = j.length();
    int duration = j.substring(stringIndex, newlineIndex).toInt();
    
    song[songIndex++] = Note(octave, note, duration);
    
    stringIndex = newlineIndex + 1;
  }
  song[songIndex++] = Note(3,'c',500,true);
  Serial.println("SongIndexSize: ");
  Serial.println(songIndex);

  for (int i = 0; i < sizeof(song) / sizeof(Note); i++) {
    Note currentNote = song[i];
    if (currentNote.terminator) {
      return;
    }
    int controlServoAngle = noteToControlAngle(currentNote.note);
    sprintf(buffer, "Index: %d, Note: %c, Duration: %d, Octave: %d, CAngle: %d", i, currentNote.note, currentNote.duration, currentNote.octave, controlServoAngle);
    Serial.println(buffer);
    controlServo.write(controlServoAngle);
    delay(250);
    fingerServo.write(70);
    delay(currentNote.duration);
    up();
    delay(0);
  }
  
  delay(10000);
}
