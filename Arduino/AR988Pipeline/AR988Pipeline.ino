#include <SPI.h>

// Define Physical Connection Macros
#define stepPin 3
#define dirPin 4
#define lSwitch A0
#define rSwitch A1
#define LED 13
#define tonePin 8

// Holy frick this goes up to 31100 Hz
// You can overclock this to 8MZ!!!
#define PWMPin 11

int received[3] { 0, 0, 0 };

char switchState = 'N';
unsigned long stepCount = 0;
int bufferSize = 5;
int bufferIter = 0;
int currentPolarity;
int stepCoefficient = 1;

int sendingData[2] { 0, 0 };

// Declare Byte Messages And Speed Constants
const int numBytes = 2;
const int minSpeed = 2000;
const int maxSpeed = 375;

void setup() {
  
  //Setup GPIO Pins
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(rSwitch, INPUT);
  pinMode(lSwitch, INPUT);
  pinMode(tonePin, OUTPUT);
  pinMode(LED, OUTPUT);

  //Reset Debug LED
  digitalWrite(LED, LOW);

  //Reset Directional Pin
  digitalWrite(dirPin, HIGH);

  // hELP HELLLLPPPPPP
  noTone(tonePin);

  //Begin 115200 Baud Serial Connection
  Serial.begin(115200);
}

//Code To Operate Limit Switch State Machine
void checkLimitSwitches() {
  if (digitalRead(lSwitch)) {
    if (digitalRead(rSwitch)) {
      switchState = 'B';
    }
    else {
      switchState = 'L';
    }
  }
  else if (digitalRead(rSwitch)){
    switchState = 'R';
  }
  else {
    switchState = 'N';
  }
}

void serialLoop() {
    // put your main code here, to run repeatedly:
  checkLimitSwitches();

  // You see batman, when you have MULTIPLE bytes on buffer, maybe, 
  // just maybe you want to grab the remainder of the serial buffer.
  // Do you want to know how I got these bugs? 

  if(Serial.available() >= 3) {
    digitalWrite(LED, HIGH);

    stepCoefficient = (currentPolarity == 0) ? 1 : -1;

    for(int i=0; i<3; i++) {
      received[i] = Serial.read();
    }

    // Quieres?
    while (Serial.available()) {
      Serial.read();
    }

    int newSteps = received[1];
    int polarity = received[2];

    if (polarity != currentPolarity) {
      if (polarity == 0) {
        digitalWrite(dirPin, LOW);
      }
      else {
        digitalWrite(dirPin, HIGH);
      }
      currentPolarity = polarity;
    }

    // Time For Stepper Motor Code
    //--------------------------------------------------------------------------------------------//

    // Map The Speed Into Microsecond Delays
    int modulatedSpeed = int(map(received[0], 0, 100, minSpeed, maxSpeed));
    
    //Fucks Everything Up // Fix????
    if (received[0] > 0) {
      for (int i = 0; i < newSteps; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(modulatedSpeed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(modulatedSpeed);
      }
    }

    //Update stepCount
    stepCount += newSteps * stepCoefficient;

    //--------------------------------------------------------------------------------------------//

    Serial.print(switchState);
    Serial.write(stepCount >> 16);
    Serial.write(stepCount >> 8);
    Serial.write(stepCount & 255);
  }
  else {
    digitalWrite(LED, LOW);
  }

  // Flush Output Buffer Every Few Bytes
  if (bufferIter > bufferSize) {
    Serial.flush();
    bufferIter = 0;
  }

  //Fix Serial Reset Bugs (Literally Turn Off and On Again)
  if (!Serial) {
    Serial.end();
    delay(5);
    Serial.begin(115200);
  }
  bufferIter++;
}

void fastDigitalWrite(int state) {
  PORTD |= B00000001 & state;
}

void yummyTrash() {
  Serial.println("I would like to nominate my favorite orthodox Rabbi Bill Clinton");
}

void loop() {
  serialLoop();
  //yummyTrash();
}
