const int PIN_COUNT = 6;
const int PINS[] = {3, 5, 6, 9, 10, 11};

// pre-allocate
int pin;
int amplitude;

// runs at start. setup serial and pins
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  // all commands are sent at once, so no timeout is needed

  // set all pins to OUTPUT mode
  for (int i = 0; i < PIN_COUNT; i++) {
    pinMode(PINS[i], OUTPUT);
  }
  pinMode(LED_BUILTIN, OUTPUT);
}

// tells controlling computer to stop waiting
void acknowledge() {
  //delay(600); // to test checking for acknowledgement

  // 'r' for received
  Serial.write('r');
  Serial.flush();
}

// turns all pins off, blinks LED for visual indication
void abort_all() {
    for (int i = 0; i < PIN_COUNT; i++)
      digitalWrite(PINS[i], 0);

    flush_input();
    acknowledge();

    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}

// clears out command queue just in case
void flush_input() {
    // double while structure enables fast clearing without
    //   risking returning before a stream is complete.
    while (Serial.available()){
      while (Serial.read() != -1) {}
      delay(5);
    }
}

// runs indefinitely
void loop() {
  // if there is data to read
  if (Serial.available()) {

    // reset counter so first pin is always pin 0
    pin = 0;

    // while there is data to read
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

      // next time through, set the next pin
      pin = pin + 1;

      // if too many commands. ignore extras.
      if (pin >= PIN_COUNT) {
        flush_input();
        break;
      }
    }

    // pins not set are set to 0
    for (int i = pin; i < PIN_COUNT; i++) {
      analogWrite(PINS[i], 0);
    }

    // send a 'received' acknowledgement
    acknowledge();

  } else {
    // fast blink status light while waiting
    digitalWrite(LED_BUILTIN, LOW);
    delay(80);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(20);
  }
}

