const int pinX = 0;
const int pinY = 1;
const int push = 12;

void setup() {
  pinMode(pinX, INPUT);
  pinMode(pinY, INPUT);
  pinMode(push, INPUT);
  Serial.begin(19200);
}

void loop() {
  int x, y, p;
  x = analogRead(pinX);
  y = analogRead(pinY);
  p = digitalRead(push);

  Serial.print(x);
  Serial.print(" ");
  Serial.print(y);
  Serial.print(" ");
  Serial.print(p);
  Serial.print(" ");
  Serial.println();

  delay(15);
}
