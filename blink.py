from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
led2 = Pin("GP0", Pin.OUT)

while True:
    led.on()
    led2.on()
    sleep(0.25)
    led.off()
    led2.off()
    sleep(0.25)