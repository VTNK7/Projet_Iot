// Import required libraries
#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Variables for temperature and humidity
float t = 0.0;
float h = 0.0;

void setup() {
  // Serial port for debugging purposes
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  delay(10000)

  float newT = dht.readTemperature();
  if (isnan(newT)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    t = newT;
    Serial.print("Temperature: ");
    Serial.print(t);
    Serial.println("°C");
  }

  // Read Humidity
  float newH = dht.readHumidity();
  if (isnan(newH)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    h = newH;
    Serial.print("Humidity: ");
    Serial.print(h);
    Serial.println("%");
  }
}