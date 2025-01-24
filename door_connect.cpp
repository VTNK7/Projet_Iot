#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define lights D4 // Led in NodeMCU at pin GPIO16 (D0).
#define sensor D3 // Led in NodeMCU at pin GPIO16 (D0).

const char* ssid = "iPhone de Victor";
const char* password = "aaaaaaaa";

// Adresse IP et port du serveur
const char* serverUrl = "http://172.20.10.8:5001/data";

WiFiClient client; // Crée une instance de WiFiClient
String jsonOld="";

void setup() {

  Serial.begin(115200);
  pinMode(sensor, INPUT_PULLDOWN_16);
  pinMode(lights, OUTPUT);
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

  if(WiFi.status()==WL_CONNECTED){

    String jsonPayload;

    if (digitalRead(sensor)) {
      digitalWrite(lights, HIGH);
      jsonPayload = "{\"id\": 1,\"door\": 1}";
    } else {
      digitalWrite(lights, LOW);
      jsonPayload = "{\"id\": 1,\"door\": 0}";
    }
    Serial.println(jsonPayload);


    // Envoyez la requête POST
    if(jsonPayload!=jsonOld){
      Serial.println(jsonPayload);
      HTTPClient http;

      // Commencez la requête avec WiFiClient
      http.begin(client, serverUrl);
      http.addHeader("Content-Type", "application/json");

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
    }

    jsonOld=jsonPayload;

  } else {
    Serial.println("Wi-Fi non connecté !");
  }


  delay(500);
}