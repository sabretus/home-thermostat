// ESP8266 DS18B20 ArduinoIDE Thingspeak IoT Example code
// http://vaasa.hacklab.fi
//
// https://github.com/milesburton/Arduino-Temperature-Control-Library
// https://gist.github.com/jeje/57091acf138a92c4176a

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#include <DHT.h>
#define DHTTYPE DHT22  //or DHT11
#define DHTPIN  2 // GPIO 2
#define REPORT_INTERVAL 30 //in sec

// Initialize DHT sensor - adafruit note
// NOTE: For working with a faster than ATmega328p 16 MHz Arduino chip, like an ESP8266,
// you need to increase the threshold for cycle counts considered a 1 or 0.
// You can do this by passing a 3rd parameter for this threshold.  It's a bit
// of fiddling to find the right value, but in general the faster the CPU the
// higher the value.  The default for a 16mhz AVR is a value of 6.  For an
// Arduino Due that runs at 84mhz a value of 30 works.
// This is for the ESP8266 processor on ESP-01
DHT dht(DHTPIN, DHTTYPE, 11); // 11 works fine for ESP8266

float humidity, temperature;  // Values read from sensor
unsigned long previousMillis = 0;        // will store last temp was read
const long interval = 2000;              // interval at which to read sensor

const char* host = "hgwx.hopto.org"; // Your domain  
String path = "/py-cgi/sender.py";
String sensorId = "?sensorid=esp8266_001"; // uniq sensor ID
String tempKey = "&temp=";
String humKey = "&hum=";

const char* ssid = "";
const char* pass = "";

void setup(void){
  Serial.begin(115200);
  Serial.println("");
  
  WiFi.begin(ssid, pass);
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  dht.begin();           // initialize temperature sensor
  Serial.println("\n\r \n\rDHT done");
  gettemperature();
  Serial.println(String(temperature));

  delay(2);
}

void gettemperature() {
  // Wait at least 2 seconds seconds between measurements.
  // if the difference between the current time and last time you read
  // the sensor is bigger than the interval you set, read the sensor
  // Works better than delay for things happening elsewhere also
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time you read the sensor
    previousMillis = currentMillis;

    // Reading temperature for humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (it's a very slow sensor)
    humidity = dht.readHumidity();          // Read humidity (percent)
    //temperature = dht.readTemperature(true);     // Read temperature as Fahrenheit
    temperature = dht.readTemperature();     // Read temperature as *C
    // Check if any reads failed and exit early (to try again).
    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
  }
}

void loop() {

  gettemperature();

  WiFiClient client;
  const int httpPort = 1334;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  client.print(String("GET ") + path + sensorId + tempKey + temperature + humKey + humidity + " HTTP/1.1\r\n" +
                "Host: " + host + "\r\n" + 
                "Connection: keep-alive\r\n\r\n");

  int cnt = REPORT_INTERVAL;  
  while(cnt--)
    delay(1000);
}
