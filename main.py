from screenMotor import Screen
from time import sleep
from motorController import MotorController
from motorWebServer import MotorWebServer
from artnet_client import ArtnetClient
import _thread
from settings import Settings

import network
import ujson


settings = Settings()

if not settings.load():
    print("No settings file, using defaults")
    settings.save()


#Wifi

sleep(1) #1 second sleep for usb to respond
print('Connecting to network...')
print(settings.ssid)
print(settings.password)






#Configure the screen service
Screen = Screen()


#Configure the wifi
#we have to do this to clear the settings out of the wifi chip
wlan = network.WLAN(network.WLAN.IF_STA)
wlan.active(True)
wlan.disconnect()

sleep(0.1)

wlan.ifconfig(('192.168.68.55','255.255.255.0','192.168.68.1','192.168.68.1'))
#wlan.ifconfig(('192.168.137.2','255.255.255.0','192.168.137.1','192.168.137.1'))
wlan.connect(settings.ssid, settings.password)

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

myMotorController = MotorController(Screen,settings.freq)

t1 = _thread.start_new_thread(ArtnetClient.udp_listen, ("192.168.68.55",myMotorController))

myMotorWebServer = MotorWebServer(wlan, myMotorController,settings)
myMotorWebServer.webServerTask()
