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

void loop() {
  if (Serial.available()) {

    // abort
    if (Serial.peek() == 'a') {
      for (int i = 0; i < PIN_COUNT; i++)
        digitalWrite(PINS[i], 0);

      // flush out anything else
      while (Serial.read() != -1) {}

      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
      
      return;
    }

    // if not abort, must be pin commands
    while (Serial.available()) {
      // pin ID comes first
      pin = Serial.parseInt();
  
      // values must come in pairs. No pair = ignore
      if (Serial.peek() == -1)
        return;
      
      // if there's a second value, set the pin with it
      amplitude = Serial.parseInt();
      if (pin < PIN_COUNT)
        analogWrite(PINS[pin], amplitude);
  
      // no need to flush input buffer, since multiple
      // commands can come at the same time.
    }
    
  } else {
    // fast blink status light while waiting
    digitalWrite(LED_BUILTIN, LOW);
    delay(80);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(20);
  }
}
