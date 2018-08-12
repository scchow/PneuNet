const int PIN_COUNT = 4;
const int PINS[] = {5,6,7,8};

int pin;
int prescaler = 256; // set this to match whatever prescaler value you set in CS registers below
int pwmFreq = 30;

int dCycles[4];

void setup() {

  Serial.begin(9600);
  Serial.setTimeout(1);

  pinMode(LED_BUILTIN, OUTPUT);

  // output pins for valve PWM
  for (int i = 0; i < PIN_COUNT; i++) {
    pinMode(PINS[i], OUTPUT);
  }
  
  int eightOnes = 255;  // this is 11111111 in binary
  TCCR3A &= ~eightOnes;   // this operation (AND plus NOT), set the eight bits in TCCR registers to 0 
  TCCR3B &= ~eightOnes;
  TCCR4A &= ~eightOnes;
  TCCR4B &= ~eightOnes;

  // set waveform generation to frequency and phase correct, non-inverting PWM output
  TCCR3A = _BV(COM3A1) | _BV(COM3B1);
  TCCR3B = _BV(WGM33) | _BV(CS32);
  
  TCCR4A = _BV(COM4A1) | _BV(COM4B1);
  TCCR4B = _BV(WGM43) | _BV(CS42);
}

void setPWM(float pin1, float pin2, float pin3, float pin4) {

  // set PWM frequency by adjusting ICR (top of triangle waveform)
  ICR3 = F_CPU / (prescaler * pwmFreq * 2);
  ICR4 = F_CPU / (prescaler * pwmFreq * 2);
  
  // set duty cycles
  OCR3A = (ICR4) * (pin1 / 255);
  OCR4A = (ICR4) * (pin2 / 255);
  OCR4B = (ICR4) * (pin3 / 255);
  OCR3B = (ICR4) * (pin4 / 255);
}

// tells controlling computer to stop waiting
void acknowledge() {
  //delay(600); // to test checking for acknowledgement

  // 'r' for received
  Serial.write('r');
  Serial.flush();
}

void abort_all() {
  setPWM(0,0,0,0);
  
  flush_input();
  acknowledge();
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

void flush_input() {
  while (Serial.read() != -1) {}
}

void loop() {
  
  if (Serial.available()) {
    
    pin = 0;
    dCycles[0] = 0;
    dCycles[1] = 0;
    dCycles[2] = 0;
    dCycles[3] = 0;
    
    // if not abort, must be pin commands
    while (Serial.available()) {
      
      // if 'a' is ever received, abort
      if (Serial.peek() == 'a') {
        abort_all();
        return;
      }

      // end of stream check
      if (Serial.peek() == -1)
        break;
        
      // if there's a value, set it aside for later
      dCycles[pin] = Serial.parseInt();

      // next time around, set the next pin
      pin = pin + 1;
      
      // too many commands. ignore extras.
      if (pin >= PIN_COUNT)
        flush_input();
        break;
      
      // loop to get the next pin value
    } // end while available

    // update PWM output based on the above values
    setPWM(dCycles[0],dCycles[1],dCycles[2],dCycles[3]);
    
    // send a 'received' acknowledgement
    acknowledge();

    delay(100);  
  } else { // if not available
    // fast blink status light while waiting
    digitalWrite(LED_BUILTIN, LOW);
    delay(80);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(20);
  }
}
