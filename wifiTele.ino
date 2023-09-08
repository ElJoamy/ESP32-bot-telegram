#include <WiFi.h>
#include <AsyncEventSource.h>
#include <AsyncJson.h>
#include <AsyncWebSocket.h>
#include <AsyncWebSynchronization.h>
#include <ESPAsyncWebSrv.h>
#include <SPIFFSEditor.h>
#include <StringArray.h>
#include <WebAuthentication.h>
#include <WebHandlerImpl.h>
#include <WebResponseImpl.h>

const char *ssid = "EL NOMBRE DE LA RED DE WIFI A LA QUE TE CONECTARÁS";
const char *password = "LA CONTRASEÑA DE LA RED DE WIFI A LA QUE TE CONECTARÁS";

int ledPin = 13; // Pin del LED
bool isBlinking = false; // Variable para controlar el estado del parpadeo

AsyncWebServer server(80); // el puerto 80 es el puerto por defecto para HTTP

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP()); // Imprime la dirección IP asignada por el router

  server.on("/encender", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(ledPin, HIGH);
    request->send(200, "text/plain", "LED encendido");
  });

  server.on("/apagar", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(ledPin, LOW);
    request->send(200, "text/plain", "LED apagado");
  });

  server.on("/parpadear", HTTP_GET, [](AsyncWebServerRequest *request){
    isBlinking = true;
    request->send(200, "text/plain", "LED parpadeando");
  });

  server.on("/alto", HTTP_GET, [](AsyncWebServerRequest *request){
    isBlinking = false;
    digitalWrite(ledPin, LOW); // Detener el parpadeo apagando el LED
    request->send(200, "text/plain", "Parpadeo detenido");
  });

  server.begin();
}

void loop() {
  if (isBlinking) {
    digitalWrite(ledPin, !digitalRead(ledPin)); // Invierte el estado del LED
    delay(500); // Pausa de 500 ms (medio segundo) entre cambios de estado
  }
}
