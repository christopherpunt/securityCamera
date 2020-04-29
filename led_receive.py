'''
What: led_receive.py has mqtt callbacks that subscribe to a secure mqtt
        broker and waits for locked and unlocked state of the security
        camera. It represents the locked and unlocked state of the IoT
        lock by changing LEDs depending on state.
Who: Chris Punt and Nate Herder
When: 04/29/2020
Why: CS 300 Calvin University
'''

import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import os

# Constants
try:
    PASSWORD = os.getenv('CALVIN_MQTT_PASSWORD')
except:
    print('No environment varialble set for CALVIN_MQTT_PASSWORD')
    exit(1)
BROKER = 'iot.cs.calvin.edu'
USERNAME = "cs300" # Put broker username here
TOPIC = 'chrisNate/admit'
CERTS = '/etc/ssl/certs/ca-certificates.crt'
PORT = 8883
QOS = 0
UNLOCKED_LED = 16
LOCKED_LED = 20
DELAY = 4.0 # how long the lock stays unlocked
BLINKS = 6

# Initialize GPIO input and output
GPIO.setmode(GPIO.BCM)
GPIO.setup(UNLOCKED_LED, GPIO.OUT)
GPIO.setup(LOCKED_LED, GPIO.OUT)
GPIO.output(UNLOCKED_LED, False)
GPIO.output(LOCKED_LED, True)


#blinks the red led to notify that authorization failed and system is locked
def blink(led):
    for count in range(BLINKS):
        GPIO.output(led, True)
        time.sleep(0.2)
        GPIO.output(led, False)
        time.sleep(0.2)

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('Connected to',BROKER)
    else:
        print('Connection to',BROKER,'failed. Return code=',rc)
        exit(1)

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == "chrisNate/admit":
        print("Received message: LED = ", int(msg.payload))

    if(msg.topic == TOPIC):
        if int(msg.payload) == 1:
            print("admitted")
            GPIO.output(UNLOCKED_LED, True)
            GPIO.output(LOCKED_LED, False)

            #lock after timer has expired
            time.sleep(DELAY)
            GPIO.output(UNLOCKED_LED, False)
            GPIO.output(LOCKED_LED, True)   
        elif int(msg.payload) == 0:
            print("not admitted")
            blink(LOCKED_LED) 
            GPIO.output(LOCKED_LED, True) # ensure lock is still locked


# Setup MQTT client and callbacks
client = mqtt.Client()
client.username_pw_set(USERNAME, password=PASSWORD)
client.tls_set(CERTS)
client.on_connect = on_connect
client.on_message = on_message
# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC, qos=QOS)
client.loop_start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    GPIO.output(UNLOCKED_LED, False)
    GPIO.output(LOCKED_LED, False)
    print("Done")
    GPIO.cleanup()
    client.disconnect()