int ldrPin   = A0;
int ledPin[] = {3,4,5,6,7};
int valorLDR = 0;
int umbral = 300;

bool modoManual = false;
unsigned long tiempoUltimoComando = 0;
unsigned long timeoutManual = 10000;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) {
    pinMode(ledPin[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available()) {
    char comando = Serial.read();

    if (comando == '1') {
      encenderLeds();
      modoManual = true;
      tiempoUltimoComando = millis();
    } else if (comando == '0') {
      apagarLeds();
      modoManual = true;
      tiempoUltimoComando = millis();
    }
  }

  if (modoManual && millis() - tiempoUltimoComando > timeoutManual) {
    modoManual = false;
  }

  if (!modoManual) {
    valorLDR = analogRead(ldrPin);
    Serial.print("L,");
    Serial.println(valorLDR);

    if (valorLDR < umbral) {
      encenderLeds();
    } else {
      apagarLeds();
    }
  }

  delay(100);
}

void encenderLeds() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(ledPin[i], HIGH);
  }
}

void apagarLeds() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(ledPin[i], LOW);
  }
}
