'''
Created on Nov 07, 2016

@author: Rob Vrecic
'''
#This script utilizes Geduldig's TwitterAPI. Complements to him for the API and all of its function.
import time
from time import sleep
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterConnectionError
from TwitterAPI import TwitterRequestError
from serial import Serial
import struct
import os
import http.client
from http.client import IncompleteRead
import requests
from socket import *

#Twitter credentials should be entered here
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

#additional variables
TweetHashtoTrack = "" #place hashtag to track inside quotes without '#'
UserToTrack = "" #@xxxxx twitter ID - The ID number can be found by converting a screenname
HandleToTrack = "" #Follow a twitter handle. Enter the username to follow here without '@'
availableArduino = False
TestSerial = False
arduinoPort = "COM5"
arduinoBaud = "9600"
arduinoWait = 3

#setup the client you wish to talk to here. IN this case, it is the Arduino Wifi Shield.
address = ("x.x.x.x", 2390) #Define who you are talking to (must match arduino IP and port). typically 192.168.0.x
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.settimeout(1) #only wait 1 second for a resonse

# Arduino Serial Port Comms Establishment
#if availableArduino:
#    ser = Serial(arduinoPort, arduinoBaud, timeout = 3)

#sleep (arduinoWait)

if TestSerial:
    print("Serial Testing is On")
    #ser.write(bytes(1))
    #sleep(arduinoWait)
    #print("Serial Testing is now Off")
    #ser.write(bytes(0))
    #sleep(arduinoWait)
else:
    print("Initialization of Twitter connection OK")
    print("Twitter Stream API Authorizing!")
    try:
        api = TwitterAPI(consumer_key, consumer_secret, access_token, access_secret)

    ######### Section of code to search for specific twitter hashtag
        r = api.request('statuses/filter', {'track': TweetHashtoTrack, 'track' : HandleToTrack, 'follow':UserToTrack})
        for item in r.get_iterator():
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
            elif 'disconnect' in item:
                event = item['disconnect']
                if event['code'] in [2,5,6,7]:
                    # something needs to be fixed before re-connecting
                    raise Exception(event['reason'])
                else:
                    # temporary interruption, re-try request
                    break
            elif 'ReadTimeout' or 'Timeout' in item:
                print("Read Timeout detected, attempting to continue...")
                continue
    except TwitterRequestError as e:
        if e.status_code < 400:
            # something needs to be fixed before re-connecting
            raise
        else:
            # temporary interruption, re-try request
            pass
    except TwitterConnectionError:
        # temporary interruption, re-try request
        pass
    except IncompleteRead:
        # Oh well, reconnect and keep trucking
        print("Incomplete Read")
        pass