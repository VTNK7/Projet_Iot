#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <Arduino.h>


#define DHTTYPE DHT11
#define DHTPIN 5

DHT dht(DHTPIN, DHTTYPE);

// Var for temperature and humidity
float t = 0.0;
float h = 0.0;

// Informations Wi-Fi
const char* ssid = "iPhone de Victor";
const char* password = "aaaaaaaa";

// Adresse IP et port du serveur
const char* serverUrl = "http:/172.22.224.105:5001/data";

WiFiClient client; // Créez une instance de WiFiClient

void setup() {  
  Serial.begin(115200);
  delay(1000);

  // Connexion au Wi-Fi
  Serial.println("Connexion au Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnecté au Wi-Fi !");
  dht.begin();
}

void loop() {
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

  String jsonPayload = "{\"temperature\": " + String(t) + ", \"humidity\": " + String(h) + "}";


  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Commencer la requête avec WiFiClient
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Envoyez la requête POST
    int httpResponseCode = http.POST(jsonPayload);

    // Vérifiez la réponse
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);
    } else {
      Serial.println("Erreur dans la requête : " + String(httpResponseCode));
    }

    // Terminez la requête
    http.end();
  } else {
    Serial.println("Wi-Fi non connecté !");
  }
  delay(4000); // Attendre avant la prochaine requête
}