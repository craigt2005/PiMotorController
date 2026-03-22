from screenMotor import Screen
from time import sleep
from motorController import MotorController
from motorWebServer import MotorWebServer

import network

#Wifi
ssid = 'No More Mr WiFi'
password = '6BorderWay'
sleep(1) #1 second sleep for usb to respond
print('Connecting to network...')
print(ssid)
print(password)


#Configure the screen service
Screen = Screen()
Screen.setMode("Test")

#Configure the wifi
#we have to do this to clear the settings out of the wifi chip
wlan = network.WLAN(network.WLAN.IF_STA)
wlan.active(True)
wlan.disconnect()

sleep(0.1)

wlan.ifconfig(('192.168.68.55','255.255.255.0','192.168.68.1','192.168.68.1'))
#wlan.ifconfig(('192.168.137.2','255.255.255.0','192.168.137.1','192.168.137.1'))
wlan.connect(ssid, password)

status_meanings = {
    -3: "FAIL",
    -2: "NO AP FOUND",
    -1: "CONNECT FAIL",
     0: "IDLE",
     1: "CONNECTING",
     2: "HANDSHAKE",
     3: "CONNECTED (NO IP YET)",
     4: "GOT IP"
    }

while True:
    statusText = status_meanings.get(wlan.status(), "UNKNOWN")
    Screen.setConnectionStatus(statusText)
    Screen.setIpAddress(wlan.ifconfig()[0])
    if(wlan.isconnected()):
        break

myMotorController = MotorController(Screen)

myMotorWebServer = MotorWebServer(wlan, myMotorController)
myMotorWebServer.webServerTask()
