from distutils.log import Log
import time
import requests
import serial
from datetime import datetime
from serial.tools import list_ports


def comPorts(portType):
    dictOfComPorts = {}
    # Key = COM3,COM6,etc.
    # Value = "Qualcomm HS-USB","Arduino Uno",etc.
    key = ''
    value = ''
    ports = list_ports.comports()
    for dvc, desc, hwid in sorted(ports):
        dictOfComPorts[dvc] = desc

    if dictOfComPorts != {}:
        for key in dictOfComPorts:
            if portType in dictOfComPorts[key]:
                value = dictOfComPorts[key]
                return dictOfComPorts, key, value
            else:
                key = ''
                value = ''
    return dictOfComPorts, key, value

def Power_on_off(arduino, x):
    print(x)
    arduino.write(x.encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def powerCycle():
    dict, key, value = comPorts("Arduino")
    arduinoPort = key
    baud = 9600
    print("Arduino UNO Port" + arduinoPort)
    arduino = serial.Serial(port=arduinoPort, baudrate=baud, timeout=.1)
    arduino.write("1".encode('utf-8'))  # Power OFF
    print("Power Cycle", "OFF")
    time.sleep(2)
    arduino.write("2".encode('utf-8'))  # Power ON
    print("Power Cycle", "ON")

def debugBreaker(state):
    #state can be "normal" or "debug"
    dict, key, value = comPorts("CH340")
    arduinoPort = key
    baud = 9600
    print("CH340 Port" + arduinoPort)
    arduino = serial.Serial(port=arduinoPort, baudrate=baud, timeout=.1)
    time.sleep(2)
    arduino.write(state.encode('utf-8'))
    time.sleep(2)
    log = arduino.readlines()
    print(log)
    
    
dict, key, value = comPorts("CH340")
print(dict, key, value)



