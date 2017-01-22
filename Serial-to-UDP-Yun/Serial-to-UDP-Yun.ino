/*!
 * Serial-to-UDP-Yun
 * 
 * Converts a serial stream into a UDP stream.
 *
 * Version 1.0
 * Date: January 22, 2017
 * Github repository: http://www.github.com/timsee/Serial-to-UDP-Yun
 * License: MIT-License, LICENSE provided in root of git repo
 */

#include <SoftwareSerial.h>
#include <Bridge.h>

SoftwareSerial input(10, 11); // RX, TX

// used for communication over the Bridge Library
const uint8_t buffer_size = 50;
char char_buffer[buffer_size];

// set to 1 to send all packets over serial as well.
const uint8_t SERIAL_DEBUG = 0;

// delimiter used in serial stream. This character is not
// sent over UDP.
const char delimiter = ';';

void setup() {
  if (SERIAL_DEBUG) {
    Serial.begin(9600);  
  }
  
  // set up software serial
  input.begin(9600);
  
  // set up the bridge. This may take a few seconds...
  Bridge.begin();
}



void loop() {
  // check for input from the serial stream
  // send to python processor, if any input is found
  serialToUDP();

  // check for input from the python script
  // send over serial, if any input is found
  UDPToSerial();
  
  delay(100);
}

/*
 * Checks if any data was received over serial. If any was
 * then it gets processed and sent over UDP.
 */
void serialToUDP() {
  if (input.available()) { 
    String response = input.readStringUntil(delimiter);
    // remove any whitespace
    response.trim(); 
    Bridge.put("from_arduino", response);
    if (SERIAL_DEBUG) {
      Serial.print("Serial->UDP: ");
      Serial.println(response); 
    }
  }
}



/*
 * Checks if any data was received over UDP. If any was
 * then it gets processed and sent over serial.
 */
void UDPToSerial() {
  Bridge.get("from_udp", char_buffer, buffer_size);
  // convert char buffer to string
  String currentPacket = String(char_buffer);

  // check string isn't empty
  if (currentPacket != "") {
    currentPacket += delimiter;
    input.print(currentPacket);
    // place an empty string on the from_udp key
    // in order to signal that the packet is read.
    Bridge.put("from_udp", "");

    if (SERIAL_DEBUG) {
      Serial.print("UDP->Serial: ");
      Serial.println(currentPacket); 
    }
  }
}

