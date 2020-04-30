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

# MQTT Constants
try:
    PASSWORD = os.getenv('CALVIN_MQTT_PASSWORD')
except:
    print('No environment varialble set for CALVIN_MQTT_PASSWORD')
    exit(1)
BROKER = 'iot.cs.calvin.edu'
USERNAME = "cs300" # Put broker username here
TOPIC = 'chrisNate/lock'
CERTS = '/etc/ssl/certs/ca-certificates.crt'
PORT = 8883
QOS = 0

# other constants
UNLOCKED_LED = 16
LOCKED_LED = 20
UNLOCKED_DELAY = 4.0 # how long the lock stays unlocked
BLINKS = 6
BLINK_DELAY = .2
MAIN_THREAD_DELAY = 10

#state variables
LOCKED = 0
UNLOCKED = 1
state = LOCKED

# Initialize GPIO input and output for LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setup(UNLOCKED_LED, GPIO.OUT)
GPIO.setup(LOCKED_LED, GPIO.OUT)


#blinks the red led to notify that authorization failed and system is locked
def blink(led):
    for count in range(BLINKS):
        GPIO.output(led, True)
        time.sleep(BLINK_DELAY)
        GPIO.output(led, False)
        time.sleep(BLINK_DELAY)

# function that handles locking the lock (LEDs representing a lock)
def lock():
    global state
    global LOCKED
    GPIO.output(UNLOCKED_LED, False)
    GPIO.output(LOCKED_LED, True)
    state = LOCKED

# function that handles unlocking the lock (LEDs representing a lock)
def unlock():
    global state
    global UNLOCKED
    GPIO.output(UNLOCKED_LED, True)
    GPIO.output(LOCKED_LED, False)
    state = UNLOCKED

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('Connected to',BROKER)
    else:
        print('Connection to',BROKER,'failed. Return code=',rc)
        exit(1)

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == TOPIC:
        print("Received message: LED = ", int(msg.payload))

    if(msg.topic == TOPIC):
        if int(msg.payload) == UNLOCKED:
            print("admitted")
            unlock()

            #lock after timer has expired
            time.sleep(UNLOCKED_DELAY)
            lock()

        elif int(msg.payload) == LOCKED:
            print("not admitted")
            blink(LOCKED_LED) 
            lock()


lock() #ensure device is locked on startup

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
        time.sleep(MAIN_THREAD_DELAY)
except KeyboardInterrupt:
    GPIO.output(UNLOCKED_LED, False)
    GPIO.output(LOCKED_LED, False)
    print("Done")
    GPIO.cleanup()
    client.disconnect()