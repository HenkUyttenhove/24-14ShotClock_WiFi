from machine import SoftI2C
import time
import socket
import math

ChipAddress = 0x20

i2c = SoftI2C(scl=Pin(19), sda=Pin(18), freq=100000)

ReturnCode = i2c.scan()  #detect the chip
print("Detected chip :",ReturnCode)
code = [0,0]
byte_array = bytearray(code)
if i2c.writeto_mem(32, 0x00, byte_array):
    print("ports set to output")
i2c.writeto_mem(32, 0x01, byte_array)

list = [63,6,91,79,102,109,125,7,127,111]

#network settings
HOST = '192.168.4.1'
PORT = 6543
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
LastUpdate = 99

while True:
    print("Device detected", ReturnCode)
    print("Hexadecimaal :",hex(ReturnCode[0]))
    data = int(s.recv(2))
    print(data)
    HighNumber = math.floor(data/10)
    LowNumber  = int(data-HighNumber*10)
    
    print("High digit", HighNumber, " Low digit", LowNumber)
    code = [list[HighNumber],list[LowNumber]]
    byte_array = bytearray(code)
    i2c.writeto_mem(32, 0x14, byte_array)  #set ports A to out
    
    if not (LastUpdate == data) and data == 0:
        print("Buzzer")
        pinbuzzer.value(1)
        time.sleep(1)
    
    LastUpdate = data
    pinbuzzer.value(0)
    
    
    