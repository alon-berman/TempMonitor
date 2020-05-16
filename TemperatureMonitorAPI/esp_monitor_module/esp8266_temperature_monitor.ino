#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHTesp.h>
#include <stdlib.h>


DHTesp dht;
WiFiClient espClient;
PubSubClient client;

#define BUFFER_SIZE 100

#define wifi_ssid "BezeqWiFiX23T"
#define wifi_password "a8kmx23t"

#define mqtt_server "soldier.cloudmqtt.com"
#define mqtt_port 17125
#define mqtt_user "lnacmzld"
#define mqtt_password "ad9LXazYZ4Za"

#define in_topic "/temperature/in"
#define out_topic "/temperature/out"
// Replace by 2 if you aren't enable to use Serial Monitor... Don't forget to Rewire R1 to GPIO2!
#define in_led 0

unsigned long previousMillis = 0;
const long interval = 10000;   
//const int DELAY = 1000*300; // miliseconds
const int SleepTimeSec = 60*0.5;
int read;
float humidity, temp_c;  // Values read from sensor

void setup() {
  // Initialize MQTT & WiFi
  Serial.begin(115200);
  setup_wifi();
  client.setClient(espClient);
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Initialize DHT sensor 
  dht.setup(4, DHTesp::DHT22); // Connect DHT sensor to GPIO 17

  
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(in_led, OUTPUT);
  digitalWrite(in_led, HIGH);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(wifi_ssid);

  WiFi.begin(wifi_ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // If you do not want to use a username and password, change next line to
    // if (client.connect("ESP8266Client")) {
    if (client.connect("ESP8266Client", mqtt_user, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
 Serial.print("Message arrived [");
 Serial.print(topic);
 Serial.print("] ");
 for (int i = 0; i < length; i++) {
  char receivedChar = (char)payload[i];
  Serial.print(receivedChar);
  if (receivedChar == '0')
   digitalWrite(in_led, LOW);
  if (receivedChar == '1')
   digitalWrite(in_led, HIGH);
 }
 Serial.println();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis >= interval) {  // checks if 10 delay is over
  // save the last time you read the sensor 
  previousMillis = currentMillis;   
  humidity = dht.getHumidity();
  temp_c = dht.getTemperature();
  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temp_c)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
    Serial.print("Temparture-sensor"); 
    Serial.print(temp_c);
  }
  char temp_c_char[8];
  dtostrf(temp_c, 6, 2, temp_c_char);
  
  client.publish(out_topic,temp_c_char, true);
//  delay(DELAY);
  client.subscribe(in_topic);
//  delay(DELAY);
  // Sleep
  Serial.println("ESP8266 in sleep mode");
  ESP.deepSleep(SleepTimeSec);
}
}
