#! /usr/bin/python 
import RPi.GPIO as GPIO
import time 
import datetime
import sys
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from paho.mqtt import client as mqtt_client

# MQTT Broker
broker = '192.168.10.14'
port = 8883
topic = "entryscreen/status"
client_id = f'pi-python-mqtt-{random.randint(0, 1000)}'
username = "mqtt"
password = "odin0428" 
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

# Configuring logger
load_dotenv()
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'screen.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)
app_log = logging.getLogger('root')
app_log .setLevel(logging.DEBUG)
app_log .addHandler(my_handler)
app_log .info("***************Starting***************")

#GPIO
SCREEN = 21
GPIO.setmode(GPIO.BCM)# number scheme
GPIO.setwarnings(False)
GPIO.setup(SCREEN, GPIO.OUT, initial=GPIO.LOW)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def function_will_exit():
    sys.exit('some error log')

def togglescreen():
    GPIO.output(SCREEN,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(SCREEN,GPIO.LOW)
    writestatus()
    

def screenstatus():
    f = open("screen.txt","r")
    status = f.read()
    f.close
    app_log .info("current status: %s", status)
    if (status == "0"):
        app_log.info("on state")
        togglescreen()  
    elif (status == "1"):
        togglescreen()
        app_log.info("off state")
    else:
        app_log.info("correct state")

def writestatus():
    f = open("screen.txt","r")
    status = f.read()
    f.close()
    f = open("screen.txt","w")
    app_log.info("toggling screen")
    if (status == "0"):
        f.write("1")
        f.close()
    elif (status == "1"):
        f.write("0")
        f.close()
    else:
        app_log.info("resetting status")
        f.write("0")
        f.close()
try:
    while True:
        global now
        now = datetime.datetime.now()
        screenstatus()
        time.sleep(60)

except Exception as err:
    app_log.info("***************Exiting***************")
    app_log.error("Function exited with %s", err)
    sys.exit(err)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()