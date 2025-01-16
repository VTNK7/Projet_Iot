#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Informations Wi-Fi
const char* ssid = "iPhone de Victor";
const char* password = "aaaaaaaa";

// Adresse IP et port du serveur
const char* serverUrl = "http://172.20.10.8:5001/data";

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
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Commencez la requête avec WiFiClient
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Créez la charge utile JSON
    String jsonPayload = "{\"temperature\": 23.5, \"humidity\": 60}";

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
