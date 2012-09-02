#include <Servo.h> 
#define numberOfBytes 2

char command;
byte value;
//char inByte0;         // incoming serial byte

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
  int angle = 0;
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    serialRX();
    angle = getAngle();
    if (command == 'p') {
      pan.write(angle);
      Serial.print("Set pan to ");
      Serial.print(angle);
      Serial.print("\n");
    } else if (command = 't') {
      angle = getAngle();
      tilt.write(angle);
      Serial.print("Set tilt to ");
      Serial.print(angle);
      Serial.print("\n");
    }    
  }
}

void serialRX() {
  while (Serial.available() > numberOfBytes) {
    if (Serial.read() == 0x00) { //send a 0 before your string as a start byte
      command = Serial.read();
      //for (byte i=0; i<numberOfBytes-1; i++)
      value = Serial.read();
    }
    Serial.print("Read Command: ");
    Serial.print(command);
    Serial.print("\n");
    Serial.print("Read Value  : ");
    Serial.print(value);
    Serial.print("\n");
  }
}

int getAngle() {
  return value;
  //return atoi(value);
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print("A\n");   // send a capital A
    delay(300);
  }
}


