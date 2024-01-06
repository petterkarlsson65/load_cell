#include <HX711.h>

const int LOADCELL_DOUT_PIN = 6;
const int LOADCELL_SCK_PIN = 7;

HX711 scale;

void setup() {
 Serial.begin(115200);
 scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}

void loop() {
  Serial.println(scale.get_units(), 4); // Visar vikten med två decimaler
  delay(50);
}
