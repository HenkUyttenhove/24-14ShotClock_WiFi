# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
import time
from machine import Pin

pinbuzzer = Pin(23, Pin.OUT)
pinbuzzer.value(0)

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    print(sta_if.scan())
    sta_if.connect("ShotClockAP", "Boutersem1")
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())
