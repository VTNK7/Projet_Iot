// Import required libraries
#include <Arduino.h>
#include <ESP8266WiFi.h>

// Replace with your network credentials
const char* ssid = "iPhone de Victor";
const char* password = "aaaaaaaa";

void setup() {

  // Serial port for debugging purposes
  Serial.begin(115200);
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println(".");
  }

  // Print ESP8266 Local IP Address
  Serial.println("Connected to WiFi");
  Serial.println("ESP8266 IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
}