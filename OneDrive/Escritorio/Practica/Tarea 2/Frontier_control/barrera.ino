#include <Stepper.h>

#define STEPS 48

Stepper stepper(STEPS, 8, 9, 10, 11);

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(13, OUTPUT); // Set pin 13 as an output
  stepper.setSpeed(180); // Set the speed in degrees per second
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read a single character from serial
    if (command == '1') {
      stepper.step(STEPS); // Move forward by 48 steps
      delay(5000);
      stepper.step(-STEPS); // Move backward by 48 steps
    
  }
}
}
