#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>
#include <WiFiUdp.h>
#include <SPI.h>

// Debuging variables
int const DEBUG = 0; // Test LED without Serial feedback

// Wifi Portion of code //
char ssid[] = "";     //  your network SSID (name) 
char pass[] = "";  // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status

byte mac[] ={ 0x02, 0x0F, 0xB5, 0x01, 0xA0, 0x9A}; //Assign mac address
IPAddress ip(192, 168, 0, x); //Assign the IP Adress - typical IP address a home network router assigns
unsigned int localPort = 2390; // listening port for wifishield
char packetBuffer[255]; //dimensian a char array to hold our data packet
int packetSize; //Size of the packet
WiFiUDP Udp; // Create a UDP Object

// LED control
int ledPin = A1;

// Value sent from Python
int signalState;

void setup() {  
  pinMode(ledPin, OUTPUT); // Transistor pin connection on board

  // Enabling communication
  Serial.begin(9600);

  // Test breadboard setup to LED
  if (DEBUG) {
    tweetReceived();
  }

    // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present"); 
    // don't continue:
    while(true);
  }
  // attempt to connect to Wifi network:
  while ( status != WL_CONNECTED) { 
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:    
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }
    // you're connected now, so print out the data:
  Serial.print("You're connected to the network");
  printWifiData();
  Udp.begin(localPort); //Initialize Udp
  delay(1500); //delay
}

void loop() {
  if (!DEBUG) {
  
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print(packetSize); 
  // read the packet into packetBuffer
    int len = Udp.read(packetBuffer, 255);
       if (len > 0) {
        tweetReceived();
        packetBuffer[len] = 0;
       }
  }
 //   if (Serial.available()) {
 //     byte receivedValue = Serial.read() + byte(1);
 //     signalState = receivedValue;
 //     if (signalState == 1) {
 //       tweetReceived();
 //     }
 //     else if (signalState == 0) {
 //       ledToggle(false);
 //     }
 //     Serial.flush();
 //   }
  }
}

// Flash the light when tweet is received
void tweetReceived() {  
  for (int i = 0; i < 10; i++) {
    ledToggle(true);
    delay(100);
    ledToggle(false);
    delay(100);
  }
}

// turn LED on and off
void ledToggle(boolean value) {  
  if (value) {
    analogWrite(ledPin, 1023);
  } else {
    analogWrite(ledPin, 0);
  }
}
void printWifiData() {
  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
  Serial.println(ip);
  Serial.println(ip);
  
  // print your MAC address:
  byte mac[6];  
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[5],HEX);
  Serial.print(":");
  Serial.print(mac[4],HEX);
  Serial.print(":");
  Serial.print(mac[3],HEX);
  Serial.print(":");
  Serial.print(mac[2],HEX);
  Serial.print(":");
  Serial.print(mac[1],HEX);
  Serial.print(":");
  Serial.println(mac[0],HEX);
}

