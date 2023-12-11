from machine import Pin, UART
from time import sleep
import machine

#initialze uart
uart = UART(0, baudrate=115200)



led = Pin("LED", Pin.OUT)
button = Pin("GP4", Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        led.on()
        uart.write("1")
    else:
        led.off()
        uart.write("0")
    sleep(0.1)