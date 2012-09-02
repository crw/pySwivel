#include <Servo.h> 
#define numberOfBytes 2

char command;
byte value;

Servo pan; 
Servo tilt;

void setup() 
{ 
  // Attach servos to physical hardware
  pan.attach(9);
  tilt.attach(10);

  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  establishContact();  // send a byte to establish contact until receiver responds 
} 
 
void loop() 
{ 
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    serialRX();
    if (command == 'p') {
      pan.write(value);
      logAction("pan", value);
    } else if (command = 't') {
      tilt.write(value);
      logAction("tilt", value);
    }
  }
}

void serialRX() {
  if (Serial.available() > numberOfBytes) {
    if (Serial.read() == 0x00) { //send a 0 before your string as a start byte
      command = Serial.read();
      value = Serial.read();
    }
    logCommandValue();
  }
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print("A\n");   // send a capital A
    delay(300);
  }
}

void logCommandValue() {
    Serial.print("Recv: Command: ");
    Serial.print(command);
    Serial.print(", ");
    Serial.print("Value: ");
    Serial.print(value);
    Serial.print("\n");
}

void logAction(char* action, byte angle) {
    Serial.print("Set ");
    Serial.print(action);
    Serial.print(" to ");
    Serial.print(angle);
    Serial.print("\n");
}  
