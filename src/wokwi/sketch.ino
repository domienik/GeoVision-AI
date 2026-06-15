#include "DHTesp.h"

#define DHT_PIN 15
#define LED_ALERTA 26

DHTesp dhtSensor;

void setup() {
  Serial.begin(115200);

  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  pinMode(LED_ALERTA, OUTPUT);

  Serial.println("GeoSensor Fire Alert iniciado");
}

void loop() {
  TempAndHumidity data = dhtSensor.getTempAndHumidity();

  float temperatura = data.temperature;
  float umidadeAr = data.humidity;

  bool riscoQueimada = temperatura > 35 || umidadeAr < 35;

  if (riscoQueimada) {
    digitalWrite(LED_ALERTA, HIGH);
  } else {
    digitalWrite(LED_ALERTA, LOW);
  }

  Serial.println("----- Leitura ambiental -----");
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" C");

  Serial.print("Umidade do ar: ");
  Serial.print(umidadeAr);
  Serial.println(" %");

  Serial.print("Status: ");
  Serial.println(riscoQueimada ? "RISCO DE QUEIMADA" : "NORMAL");

  Serial.println("-----------------------------");

  delay(2000);
}