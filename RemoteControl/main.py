# main.py -- put your code here!
########################################################
#  Code developed by Henk Uyttenhove
#  Date: 10 nov 2021  (ES32 version)
#
#  Code is not limited to any license and is free to use
########################################################

import time               # convert time format
import usocket             # network stack
import _thread             #none blocking network serving
from machine import WDT   #Watchdog timer for automatic reset

# Thread for handling a client connection
def StartSocket(arg):
    c = 0
    while True:
        # Accept the connection of the clients
        (clientsocket, address) = serversocket.accept()
        # Start a new thread to handle the client
        _thread.start_new_thread(client_thread, (clientsocket, c))
        c = c+1

def client_thread(clientsocket,n):
    global ShotclockRemaing
    counter = 0
    Running = True

    while Running:
        counter =+ 1
        print("doorsturen", ShotclockRemaing)
        StringShotClockRemaining = str(ShotclockRemaing)
        if len(StringShotClockRemaining)<2:
            StringShotClockRemaining = "0"+StringShotClockRemaining

        print("doorsturen na aanpassing", StringShotClockRemaining)
        if not clientsocket.send(StringShotClockRemaining):
            Running = False

        time.sleep(0.3)

    clientsocket.close()
    # Close the socket and terminate the thread
    #clientsocket.close()

# set the inputs for 24/14/start-stop for the pins
p_24 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)   #24 seconds reset
p_14 = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)   #14 seconds reset
p_hold = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP) #hold clock
#All variables required for the clock
StartCounter = time.time()
Reset24 = 24
Reset14 = 14
# startcounter is reset to remaining time when clock is stopped
ShotClock = Reset24
ShotclockRemaing = Reset24

#wdt = WDT(timeout=10000)  #autoreboot after 10 seconds if no solution

# Set up server socket
serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
serversocket.bind(("192.168.4.1", 6543))
serversocket.listen(5) # Accept maximum of 5 connections at the same time

#Start a thread for the network stack
_thread.start_new_thread(StartSocket,("start",))

#Actual code for the clock
while True:
#    wdt.feed()
    if not p_24() and p_14():   #if 24sec reset is pushed
        ShotClock = Reset24
        StartCounter = time.time()

    if not p_14() and p_24():   #if 14 seconds is pushed
        ShotClock = Reset14
        StartCounter = time.time()

    if not p_14() and not p_24():   #if 1both 14 and 24 are pushed, send 99 for blank
        ShotClock = 99
        StartCounter = time.time()

    if not p_hold():    #if stop counter is active
        if not p_24() and p_14():
            ShotclockRemaing = Reset24
        if not p_14() and p_24():
            ShotclockRemaing = Reset14
        if not p_24() and not p_14():
            ShotclockRemaing = 99
        ShotClock = ShotclockRemaing
        StartCounter = time.time()
    else:
        ShotclockRemaing = ShotClock - round(time.time()-StartCounter)

    if ShotclockRemaing <= 0:
        ShotClock = 0
        StartCounter = time.time()
