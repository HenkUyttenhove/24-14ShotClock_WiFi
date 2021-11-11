# boot.py -- run on boot-up
import os
import machine
import network

wlan = network.WLAN(network.AP_IF) # get current object, without changing the mode
wlan.active(True)
wlan.config(essid="ShotClockAP", password="Boutersem1", authmode=3)

print("WLAN details:",wlan.ifconfig())
