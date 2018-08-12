const int PIN_COUNT = 6;
const int PINS[] = {3, 5, 6, 9, 10, 11};

// pre-allocate
int pin;
int amplitude;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  // all commands are sent at once, so no timeout is needed.
  // Also, parseInt() relies on timeout being short
  
  for (int i = 0; i < PIN_COUNT; i++) {
    pinMode(PINS[i], OUTPUT);
  }
  pinMode(LED_BUILTIN, OUTPUT);
}

void abort_all() {
    for (int i = 0; i < PIN_COUNT; i++)
      digitalWrite(PINS[i], 0);

    flush_input();

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
        
      // if there's a value, set the pin with it
      amplitude = Serial.parseInt();
        
      analogWrite(PINS[pin], amplitude);

      // no need to flush input buffer, since the
      // next numbers are still in there.
      
      pin = pin + 1;
      
      // too many commands. ignore extras.
      if (pin >= PIN_COUNT)
        break;
    }

    //others are 0.
    for (int i = pin; i < PIN_COUNT; i++) {
      analogWrite(PINS[i], 0);
    }

    // send a 'received' acknowledgement if new pin data acquired
    //delay(600); // to test checking for acknowledgement
    Serial.write('r');
    Serial.flush();
    
  } else {
    // fast blink status light while waiting
    digitalWrite(LED_BUILTIN, LOW);
    delay(80);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(20);
  }
}
