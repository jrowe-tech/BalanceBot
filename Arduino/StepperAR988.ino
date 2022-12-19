#include <SPI.h>

#define stepPin 3
#define dirPin 4
#define InterruptLED 13
#define PWMPin 11
#define tonePin 8

const int maxSpeed = 375; //375 is maximum possible speed
const int minSpeed = 2000; //1000-5000 is pretty slow
int rotationSpeed = 100;
int stepCount = 0;
//1 Is Clockwise, -1 is CounterClockwise
int cw = 1;

void setup() {
  // Sets Outputs / Serial BaudRate (Recommended <=115200 baud)
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(InterruptLED, OUTPUT);
  pinMode(tonePin, OUTPUT);
  digitalWrite(InterruptLED, LOW);
  noTone(tonePin);
  Serial.begin(115200);
}



void stepAmountSpeed(int steps, int speed) {
  //Takes Unlimited Step Count Int and Speed 1-100
  
  //Change Polarity Of Motor
  if (cw==1) {digitalWrite(dirPin, HIGH);}
  else {digitalWrite(dirPin, LOW);}

  //Map the speed and cache
  int modulatedSpeed = int(map(speed, 0, 100, minSpeed, maxSpeed));
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(modulatedSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(modulatedSpeed);
    stepCount += cw;
  }
}

void testStepper(int speed) {
  cw =! cw;
  stepAmountSpeed(400, speed);

  delay(500); // One second delay
  
  //changeDirection(false);

  digitalWrite(dirPin,LOW); //Changes the rotations direction
  
  cw =! cw;
  stepAmountSpeed(400, speed);

  delay(500);

  Serial.println("Speed: " + String(speed));
}

void amalogStepper() {
  //This is actual hell (Speed 0 - 100)
  int speed = 50;
  int modulatedSpeed = int(map(speed, 0, 100, 0, 255));
  analogWrite(PWMPin, modulatedSpeed);
  delay(5000);
  analogWrite(PWMPin, 0);
  delay(5000);
}

void tuneStepper() {
  tone(tonePin, 300000);
  delay(1000);
}


void loop() {
  //testStepper(100);
  //analogStepper();
  tuneStepper();
}
