#!/usr/bin/python

#------------------------------------------------------------
# Arduino Yun UDP Echo Server
#------------------------------------------------------------
# Version 1.0
# January 22, 2017
# MIT License (in root of git repo)
# by Tim Seemann
#
#
# Takes UDP datagram packets at its UDP_PORT as input and
# echoes them to the Arduino Yun's ATmega32U4 processor. 
# This script takes a lot of elements from the [Yun's 
# Bridge client](https://github.com/arduino/YunBridge/blob/master/bridge/bridgeclient.py)
# but does not use it directly. Instead, we interact with
# the TSPJSONClient directly and manage our own sockets. 
# This adds a significant speed increase over the Bridge 
# Client's implementation. 
#
# [Check here for setup instructions](https://github.com/timsee/Serial-to-UDP-Yun)
#
#------------------------------------------------------------

#-----
# imports

import socket
from time import sleep

import sys
# Adds a yun specific-library to the sys path
sys.path.insert(0, '/usr/lib/python2.7/bridge')
# imports the yun specific library
from bridgeclient import BridgeClient

#-----
# config

# port for the UDP connection to bind to
UDP_PORT = 10008


#-----
# bridge setup

# set up the serial port for communication with
# the yun's microprocessor
print "Setup the Arduino bridge..."
bridge = BridgeClient()
# Very important! Without this comannd, communication will work
# but will be significantly slower, since it will open and close
# sockets in each function.
bridge.begin() 
addr = None
#-----

print "Setup the UDP Socket..."
# set up UDP server. Python can do a simple server
# in just a few lines..
sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(("", UDP_PORT))
sock.settimeout(1.0)

#-----
# loop

#repeats ad nauseam
while True:
    # check if theres packets from serial, send if they are available
    arduino_data = bridge.get('from_arduino')
    if arduino_data and addr:
        #print "received %r with size %r" % (arduino_data, len(arduino_data))
        sock.sendto(arduino_data, (addr[0], UDP_PORT))
        bridge.put('from_arduino', "")
    # waits to receive data, timeout
    try:
        udp_data, addr = sock.recvfrom(512)
        #print "received %r from %r" % (udp_data, addr)
        if udp_data:
            bridge.put('from_udp', udp_data)
    except socket.timeout as err:
        pass
