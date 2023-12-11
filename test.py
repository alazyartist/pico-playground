import network  
import urequests
import socket 

from machine import Pin
from time import sleep

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = "Pico_AP"
password = "password"
#create wifi networ in ap mode
def ap_mode(ssid,password):
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.config(essid=ssid, password=password)
    
    while wlan.active() == False:
        pass
    print('AP Mode Network Config:', wlan.ifconfig())
    print("Connect to :",wlan.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n'
        conn.send(response)
        conn.close()
        print('Connection closed')

ap_mode("Pico_AP","password")

# wlan.connect(ssid, password)

# print('Connecting to WiFi...')
# Wait for connect or fail
# print(wlan.status())
# max_wait = 10
# while max_wait > 0:
#     if wlan.status() < 0 or wlan.status() >= 3:
#         break
#     max_wait -= 1
#     print('waiting for connection...')
#     sleep(1)
# # Handle connection error
# if wlan.status() != 3:
#     print(wlan.status())
#     raise RuntimeError('network connection failed')
# else:
#     print('connected')
#     status = wlan.ifconfig()
#     print( 'ip = ' + status[0] )


# # print("\n\n2. Querying the current GMT+0 time using an API")
# # req2 = urequests.get("http://worldtimeapi.org/api/timezone/America/Denver")
# # print('Req: ', req2.json())
# html = """<!DOCTYPE html>
# <html>
#     <head> <title>Led Controller</title> </head>
#     <body> <h1>
#         %s 
#     </h1>
#     </body>
# </html>
# """
# addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
# s = socket.socket()
# s.bind(addr)
# s.listen(1)
# print('listening on', addr)
# led = Pin(0, Pin.OUT)
# board_led = Pin("LED", Pin.OUT)
# print('Setup New Project')

# while True:
#     try:
#         print("Waiting for client")
#         cl,addr = s.accept()
#         print('client connected from', addr)
#         incomingRequest = cl.recv(1024)
#         print('Request: ', incomingRequest)

#         request =str(incomingRequest)
#         led_on = request.find('/light/on')
#         led_off = request.find('/light/off')
#         stateis = "Unknown"
#         if led_on == 6:
#             print('LED ON')
#             led.value(1)
#             stateis = "LED is ON"

#         if led_off == 6:
#             print('LED OFF')
#             led.value(0)
#             stateis = "LED is OFF"

#         response = html % stateis
#         cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
#         cl.send(response)
#         cl.close()
#     except OSError as e:
#         cl.close()
#         print('Connection Failed')
#         print('Exception: ', e)
#         break




# # while True:
# #     led.value(not led.value())
# #     sleep(0.5)
# #     board_led.value(not board_led.value())
# #     sleep(0.5)