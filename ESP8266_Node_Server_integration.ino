#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID "Radio Gnome"
#define STAPSK  "wakkawakkawakka"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.1.25";
const uint16_t port = 9999;

int count = 300000;

WiFiServer wifiServer(port-1);

void setup() {
  Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  wifiServer.begin();

  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(5000);
    return;
  }
  if (client.connected()) {
    String handshake_header = "IP:";
    IPAddress ip = WiFi.localIP();
    String handshake_ip = String(ip[0]);
    for (byte octet = 1; octet < 4; ++octet) {
      handshake_ip += '.' + String(ip[octet]);
    }

    String handshake = handshake_header + handshake_ip;
    client.println(handshake);
  }
  while (client.available()) {
    char ch = static_cast<char>(client.read());
    Serial.print(ch);
  }
  client.stop();
}

void loop() {
  if (count > 299999)
  {
    Serial.print("connecting to ");
    Serial.print(host);
    Serial.print(':');
    Serial.println(port);
    count = 0;
    WiFiClient client1;
    if (!client1.connect(host, port)) {
      Serial.println("connection failed");
      delay(5000);
      return;
    }
    Serial.println("sending data to server");
    if (client1.connected()) {
      client1.println("hello from ESP8266");
    }
    unsigned long timeout = millis();
    while (client1.available() == 0) {
      if (millis() - timeout > 5000) {
        Serial.println(">>> Client Timeout !");
        client1.stop();
        delay(60000);
        return;
      }
    }
    Serial.println("receiving from remote server");
    while (client1.available()) {
      char ch = static_cast<char>(client1.read());
      Serial.print(ch);
    }

    // Close the connection
    Serial.println();
    Serial.println("closing connection");
    client1.stop();
  }
  count++;
  delay(1);
  // delay(300000); // execute once every 5 minutes, don't flood remote service

  WiFiClient client2 = wifiServer.available();

  if (client2) {

    while (client2.connected()) {

      while (client2.available()>0) {
        char c = client2.read();
        Serial.write(c);
      }
      count += 10;
      delay(10);
    }

    client2.stop();
    Serial.println("Client disconnected");
  }
}
