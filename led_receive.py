import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Constants
BROKER = 'iot.cs.calvin.edu'
USERNAME = "cs300" # Put broker username here
PASSWORD = "safeIoT" # Put broker password here
TOPIC = 'chrisNate/admit'
CERTS = '/etc/ssl/certs/ca-certificates.crt'
PORT = 8883
QOS = 0
unlockedLED = 16
lockedLED = 20
DELAY = 4.0 # how long the lock stays unlocked
BLINKS = 6

# Initialize GPIO input and output
GPIO.setmode(GPIO.BCM)
GPIO.setup(unlockedLED, GPIO.OUT)
GPIO.setup(lockedLED, GPIO.OUT)
GPIO.output(unlockedLED, False)
GPIO.output(lockedLED, True)


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
        os._exit(1)

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == "chrisNate/admit":
        print("Received message: LED = ", int(msg.payload))

    if(msg.topic == TOPIC):
        if int(msg.payload) == 1:
            print("admitted")
            GPIO.output(unlockedLED, True)
            GPIO.output(lockedLED, False)

            #lock after timer has expired
            time.sleep(DELAY)
            GPIO.output(unlockedLED, False)
            GPIO.output(lockedLED, True)   
        elif int(msg.payload) == 0:
            print("not admitted")
            blink(lockedLED) 
            GPIO.output(lockedLED, True) # ensure lock is still locked




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
    GPIO.output(unlockedLED, False)
    GPIO.output(lockedLED, False)
    print("Done")
    GPIO.cleanup()
    client.disconnect()