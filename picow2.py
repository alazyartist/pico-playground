import network
from machine import Pin, UART
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
CLIENT_ID = "pico2"
TOPIC_SUB = b"pico1"
led = Pin("LED", Pin.OUT)

def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if "ON" in msg:
        led.on()
    if "OFF" in msg:
        led.off()
    print(msg)

def mqtt_connect():
    client = MQTTClient(CLIENT_ID, SERVER, keepalive=600)
    client.set_callback(sub_cb)
    client.connect()
    print("Connected to %s MQTT broker" % (SERVER))
    return client

def reconnect():
    print("Failed to connect to MQTT broker. Reconnecting...")
    time.sleep(10)
    machine.reset()





try:
    client = mqtt_connect()
    client.subscribe(TOPIC_SUB)
except OSError as e:
    reconnect()

while True:
    if(client):
        print("checking for messages",time.localtime())
        client.check_msg()
    
    time.sleep(1)