#include <ArduinoJson.h>
#include <Sparki.h>
#include "pitches.h"

// Buffer for parsing JSON.
StaticJsonBuffer<200> jsonBuffer;

void playNotes(int notes[], int noteDurations[], int numberNotes) {
  for (int i = 0; i < numberNotes; i++) {
    // Calculate the note duration as 1 second divided by note type.
    // e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000 / noteDurations[i];
    sparki.beep(notes[i], noteDuration);

    // To distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    delay(noteDuration * 1.30);
    // stop the tone playing:
    sparki.noBeep();
  }
}

void setup() {
  // setup goes here.
}

void handleJsonRPC(const JsonObject& rpc) {
  const char* method = rpc["method"];
  Serial.print("Method: ");
  Serial.println(method);
  if (strcmp(method, "move") == 0) {
    double distanceCm = rpc["distance_mm"].as<double>() / 10.0;
    if (distanceCm > 0) {
      sparki.moveForward(distanceCm);
    } else {
      sparki.moveBackward(-distanceCm);
    }
  } else if (strcmp(method, "turn") == 0) {
    double angleDegrees = rpc["angle_radians"].as<double>() * (180.0/M_PI);
    Serial.println("TURNING!");
    Serial.println(angleDegrees);
    if (angleDegrees > 0) {
      sparki.moveRight(angleDegrees);
    } else {
      sparki.moveLeft(-angleDegrees);
    }
  } else if (strcmp(method, "open_gripper") == 0) {
    double widthCm = rpc["width_mm"].as<double>() / 10.0;
    sparki.gripperOpen(widthCm);
  } else if (strcmp(method, "close_gripper") == 0) {
    double widthCm = rpc["width_mm"].as<double>() / 10.0;
    sparki.gripperClose(widthCm);
  } else if (strcmp(method, "play_notes") == 0) {
    int notes[] = {NOTE_G4, NOTE_FS4, NOTE_DS3, NOTE_A3, NOTE_GS3, NOTE_E4, NOTE_GS4, NOTE_C5};
    int noteDurations[] = { 8, 6, 8, 6, 8, 8, 8, 4 };
    playNotes(notes, noteDurations, 8);
  }
}

void loop() {
  if (Serial.available()) {
    JsonObject& jsonMessage = jsonBuffer.parseObject(Serial);
    jsonMessage.prettyPrintTo(Serial);
    handleJsonRPC(jsonMessage);
    jsonBuffer.clear();
  };
  delay(150);
}
