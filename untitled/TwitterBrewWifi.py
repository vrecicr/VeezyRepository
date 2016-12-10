'''
Created on Oct 9, 2016

@author: cheavzy
'''
import time
from time import sleep
import time
from TwitterAPI import TwitterAPI
from serial import Serial
import struct
import os
import http.client
from http.client import IncompleteRead
import requests
from socket import *

#Twitter credentials should be entered here
consumer_key = "2Rh95pJy8VNOPS6azkZ463lrz"
consumer_secret = "pploiYfMFHyb7yvZ7FvgjfKdNqfVw2lCd64UijTOfvFj7kR5MU"
access_token = "780057267592921088-JAfo28nhnNuqyEOklZbOtqKaTPXNWaq"
access_secret = "KzI80D02GPdni7iuTbQ94QEkimOmZYOTQQwOFaB1FCiwH"

#additional variables
TweetHashtoTrack = "motor123456" #place hashtag to track inside quotes
UserToTrack = "780057267592921088" #@cheavzy twitter ID
availableArduino = False
TestSerial = False
arduinoPort = "COM5"
arduinoBaud = "9600"
arduinoWait = 3

address = ("192.168.0.111", 2390) #Defind who you are talking to (must match arduino IP and port)
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.settimeout(1) #only wait 1 second for a resonse

# Arduino Serial Port Comms Establishment
#if availableArduino:
#    ser = Serial(arduinoPort, arduinoBaud, timeout = 3)

#sleep (arduinoWait)

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
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_secret)

    ######### Section of code to search for specific twitter hashtag
    r = api.request('statuses/filter', {'track': TweetHashtoTrack})
    for item in r.get_iterator():
        try:
            if 'text' in item:
                print(item['user']['screen_name'] + ' tweeted: ' + item['text'])  # Print screen name and the tweet text
            # if availableArduino:
                print("Arduino turning on the LED")
                data = "TweetObtained"  # Set data of packet to command
                client_socket.sendto(data.encode('utf-8'), address)  # send command to arduino
            # ser.write(bytes(1))  # The command is a simple byte intepretation of the integer 1
            # sleep(arduinoWait)  # Wait before sending next command
            # ser.write(bytes(0))
            # sleep(arduinoWait)  # Wait before sending next command
        except IncompleteRead:
            # Oh well, reconnect and keep trucking
            print("Incomplete Read")
            continue
            # Twitter API connection setup

    ########## Section of code to search for user tweets
    p = api.request('statuses/filter', {'follow': UserToTrack})
    for item in p.get_iterator():
        try:
            if 'text' in item:
                print(item['user']['screen_name'] + ' tweeted: ' + item['text'])  # Print screen name and the tweet text
                        # if availableArduino:
                print("Arduino turning on the LED")
                data = "TweetObtained"  # Set data of packet to command
                client_socket.sendto(data.encode('utf-8'), address)  # send command to arduino
                    # ser.write(bytes(1))  # The command is a simple byte intepretation of the integer 1
                    # sleep(arduinoWait)  # Wait before sending next command
                    # ser.write(bytes(0))
                    # sleep(arduinoWait)  # Wait before sending next command
        except IncompleteRead:
            # Oh well, reconnect and keep trucking
            print("Incomplete Read")
            continue


            #except KeyboardInterrupt:
        # Or however you want to exit this loop
    #    api.disconnect()
     #   print("Disconnecting from Twitter")
    #    exit()