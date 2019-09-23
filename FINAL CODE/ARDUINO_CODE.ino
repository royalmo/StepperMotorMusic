#include <SoftwareSerial.h>
#include <MIDI.h>
#include "pitches.h"
#define stepPin_M1 2
#define stepPin_M2 3

unsigned long motorSpeeds[] = {0, 0, 0};
unsigned long prevStepMicros[] = {0, 0, 0};
bool disableSteppers = HIGH;

MIDI_CREATE_DEFAULT_INSTANCE();
SoftwareSerial mi(0, 1);

void setup() {
  pinMode(stepPin_M1, OUTPUT);
  pinMode(stepPin_M2, OUTPUT);
  pinMode(enPin, OUTPUT);

  mi.begin(31250);
  Serial.begin(9600);
  MIDI.begin(MIDI_CHANNEL_OMNI);
  MIDI.setHandleNoteOn(handleNoteOn);
  MIDI.setHandleNoteOff(handleNoteOff);
}

void loop() {
  if (mi.available()) {
    char c = mi.read();
    Serial.println(c);
  }
  MIDI.read();
  digitalWrite(enPin, disableSteppers);
  singleStep(1, stepPin_M1);
  singleStep(2, stepPin_M2);
}

void handleNoteOn(byte channel, byte pitch, byte velocity) {
  disableSteppers = LOW;
  motorSpeeds[channel] = pitchVals[pitch];
}

void handleNoteOff(byte channel, byte pitch, byte velocity) {
  motorSpeeds[channel] = 0;
}

void singleStep(byte motorNum, byte stepPin) {
  if ((micros() - prevStepMicros[motorNum] >= motorSpeeds[motorNum]) && (motorSpeeds[motorNum] != 0)) {
    prevStepMicros[motorNum] += motorSpeeds[motorNum];
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin, LOW);
  }
}
