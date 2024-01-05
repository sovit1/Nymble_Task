#include <EEPROM.h>

#define BAUD_RATE 2400

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}

void loop() {
  int i = 0;
  
  // Write incoming data to EEPROM
  while (Serial.available() > 0 && i < EEPROM.length()) {
    char incomingByte = Serial.read();  // read the incoming byte
    EEPROM.write(i, incomingByte);  // write to EEPROM
    i++;
  }

  // Read data from EEPROM and send it back
  for (int j = 0; j < i; j++) {
    Serial.write(EEPROM.read(j));
  }
}
