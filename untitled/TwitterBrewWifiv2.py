'''
Created on Oct 23, 2016

@author: Rob Vrecic
'''
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
consumer_key = "2Rh95pJy8VNOPS6azkZ463lrz"
consumer_secret = "pploiYfMFHyb7yvZ7FvgjfKdNqfVw2lCd64UijTOfvFj7kR5MU"
access_token = "780057267592921088-JAfo28nhnNuqyEOklZbOtqKaTPXNWaq"
access_secret = "KzI80D02GPdni7iuTbQ94QEkimOmZYOTQQwOFaB1FCiwH"

#additional variables
TweetHashtoTrack = "motor123456" #place hashtag to track inside quotes
UserToTrack = "780057267592921088" #@cheavzy twitter ID
HandleToTrack = "charitytap123" #Follow a twitter handle
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