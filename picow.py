from machine import Pin, UART
import network
import machine
import time
from umqtt.simple import MQTTClient

#connect to wifi
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ssid = "TorqueHouse"
    password = "ProvideInternet"
    wlan.connect(ssid, password)

    print('Connecting to WiFi...')
    # Wait for connect or fail
    print(wlan.status())
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    # Handle connection error
    if wlan.status() != 3:
        print(wlan.status())
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        return wlan


wifi = wifi_connect()

#initalize mqtt
SERVER = "192.168.1.104"
CLIENT_ID = "pico1"
TOPIC_PUB = b"pico1"

def mqtt_connect():
    client = MQTTClient(CLIENT_ID, SERVER)
    client.connect()
    print("Connected to %s MQTT broker" % (SERVER))
    return client

def reconnect():    
    print("Failed to connect to MQTT broker. Reconnecting...")
    time.sleep(10)
    machine.reset()

try:
    client = mqtt_connect()

except OSError as e:
    print("Exception: ", e)
    reconnect()

# Initialize UART at 9600 baud rate
uart = UART(0, baudrate=115200)

# Configure onboard LED
led = Pin("LED", Pin.OUT)
led2 = Pin("GP4", Pin.OUT)

lastData = 'off'
while True:
    if uart.any():
        # Read data from UART
        data = uart.read().decode()
        if data == '1':
            led.value(1)  # Turn on LED if '1' received
            led2.value(1)
            if(data != lastData):
                client.publish(TOPIC_PUB, "LED ON at " + str(time.localtime()))

        else:
            led.value(0) 
            led2.value(0)
            if(data != lastData):
                client.publish(TOPIC_PUB, "LED OFF at " + str(time.localtime()))
             # Turn off LED otherwise
        lastData = data
    time.sleep(0.1)  # Small delay for stability