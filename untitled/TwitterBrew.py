'''
Created on Oct 9, 2016

@author: cheavzy
'''
import time
from time import sleep
from TwitterAPI import TwitterAPI
from serial import Serial
import struct
import os
import http.client
from http.client import IncompleteRead
import requests
import socket

#Twitter credentials should be entered here
consumer_key = "2Rh95pJy8VNOPS6azkZ463lrz"
consumer_secret = "pploiYfMFHyb7yvZ7FvgjfKdNqfVw2lCd64UijTOfvFj7kR5MU"
access_token = "780057267592921088-JAfo28nhnNuqyEOklZbOtqKaTPXNWaq"
access_secret = "KzI80D02GPdni7iuTbQ94QEkimOmZYOTQQwOFaB1FCiwH"

#additional variables
TweetHashtoTrack = "motor123456" #place hashtag to track inside quotes
UserToTrack = "" #place @user to track inside quotes
availableArduino = True
TestSerial = False
arduinoPort = "COM5"
arduinoBaud = "9600"
arduinoWait = 3

# Arduino Serial Port Comms Establishment
if availableArduino:
    ser = Serial(arduinoPort, arduinoBaud, timeout = 3)

sleep (arduinoWait)

if TestSerial:
    print("Serial Testing is On")
    ser.write(bytes(1))
    sleep(arduinoWait)
    print("Serial Testing is now Off")
    ser.write(bytes(0))
    sleep(arduinoWait)
else:
    print("Initialization of Twitter connection OK")
    print("Twitter Stream API Authorizing!")
    try:
    #Twitter API connection setup
        api = TwitterAPI(consumer_key, consumer_secret, access_token, access_secret)

        r = api.request('statuses/filter', {'track':TweetHashtoTrack})

        for item in r.get_iterator():
            if 'text' in item:
                print (item['user']['screen_name'] + ' tweeted: ' + item['text'])  # Print screen name and the tweet text

                #if availableArduino:
                print("Arduino turning on the LED")
                ser.write(bytes(1))  # The command is a simple byte intepretation of the integer 1
                sleep(arduinoWait)  # Wait before sending next command
                ser.write(bytes(0))
                sleep(arduinoWait)  # Wait before sending next command
    except IncompleteRead:
            # Oh well, reconnect and keep trucking
        print("IncompleteRead occurred")
    except KeyboardInterrupt:
        # Or however you want to exit this loop
        api.disconnect()
        print("Disconnecting from Twitter")
        exit()
