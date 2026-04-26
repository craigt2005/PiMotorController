from screenMotor import Screen
from time import sleep
from motorController import MotorController
from motorWebServer import MotorWebServer
from artnet_client import ArtnetClient
import _thread
from settings import Settings
import socket
import time

import network
import ujson



def connect_wifi(settings):
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    wlan.disconnect()
    sleep(0.1)
    
    if not wlan.isconnected():
        print("Connecting WiFi...")
        wlan.ifconfig(('2.0.0.10','255.0.0.0','2.0.0.1','2.0.0.1'))

        wlan.connect(settings.ssid, settings.password)



        start = time.ticks_ms()
        while not wlan.isconnected():
            statusText = status_meanings.get(wlan.status(), "UNKNOWN")
            print(statusText)
            if time.ticks_diff(time.ticks_ms(),start ) > 60000:
                print("WiFi connect timeout")
                return None
            time.sleep(0.5)

    elapsed_ms = time.ticks_diff(time.ticks_ms(), system_start)
    print("WiFi connected:", wlan.ifconfig(), "@", elapsed_ms)
    return wlan

def create_socket(settings):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((settings.ip, 6454))
    sock.settimeout(2)  # short timeout = responsive loop
    return sock

def send_keepalive(sock, target_ip):
    try:
        sock.sendto(b'\x00', (target_ip, 6454))
    except:
        pass

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

system_start = time.ticks_ms()

#Load Settings File
settings = Settings()
if not settings.load():
    print("No settings file, using defaults")
    settings.save()

#Configure the screen service
Screen = Screen()

motorController = MotorController(Screen,settings.freq)

print(settings.ip) 
wlan = connect_wifi(settings)
sock = create_socket(settings)

last_packet_time = time.ticks_ms()
last_keepalive = time.ticks_ms()


SIGNAL_TIMEOUT = 10000   # 10s no Art-Net = reconnect
KEEPALIVE_INTERVAL = 3000  # send every 3s

#Configure the wifi
#we have to do this to clear the settings out of the wifi chip
print("Listening for Art-Net...")

while True:
    try:
        packet = sock.recv(1024)
                
        # got data → reset watchdog
        last_packet_time = time.ticks_ms()

        #if len(packet) < 20:
        #   continue

        if not packet.startswith(b'Art-Net\x00'):
            continue

        opcode = int.from_bytes(packet[8:10], 'little')
        if opcode != 0x5000:
            continue

        #motorController.screen.ArtNetPacketReceived()

        universe = int.from_bytes(packet[14:16], 'little')
        #print(universe)
        if universe + 1 != settings.universe:
            continue

        m1cmd = packet[18]
        m2cmd = packet[19]

        motorController.screen.ArtNetPacketReceived()
        motorController.screen.DMXChannels(m1cmd, m2cmd)

        # --- motor logic (unchanged) ---
        if m1cmd in (0, 127):
            motorController.stop_motor1()
        elif m1cmd < 127:
            motorController.set_motor1speed(127 - m1cmd)
            motorController.fwd_motor1()
        else:
            motorController.set_motor1speed(m1cmd - 127)
            motorController.rev_motor1()

        if m2cmd in (0, 127):
            motorController.stop_motor2()
        elif m2cmd < 127:
            motorController.set_motor2speed(127 - m2cmd)
            motorController.fwd_motor2()   # fixed bug
        else:
            motorController.set_motor2speed(m2cmd - 127)
            motorController.rev_motor2()

    except OSError as e:
        # timeout = normal, ignore
        if e.args[0] != 110:
            print("Socket error:", e)

    # --- KEEPALIVE ---
    if time.ticks_diff(time.ticks_ms(), last_keepalive) > KEEPALIVE_INTERVAL:
        send_keepalive(sock, settings.controllerip)
        last_keepalive = time.ticks_ms()

    # --- WATCHDOG (THIS FIXES YOUR ISSUE) ---
    if time.ticks_diff(time.ticks_ms(), last_packet_time) > SIGNAL_TIMEOUT:
        print("Signal lost → reconnecting WiFi")

        try:
            sock.close()
        except:
            pass

        wlan = connect_wifi(settings)
        sock = create_socket(settings)

        last_packet_time = time.ticks_ms()



#status_meanings = {
#    -3: "FAIL",
#    -2: "NO AP FOUND",
#    -1: "CONNECT FAIL",
#     0: "IDLE",
#     1: "CONNECTING",
#     2: "HANDSHAKE",
#     3: "CONNECTED (NO IP YET)",
#     4: "GOT IP"
#    }

#while True:
#    statusText = status_meanings.get(wlan.status(), "UNKNOWN")
#    Screen.setConnectionStatus(statusText)
#    Screen.setIpAddress(wlan.ifconfig()[0])
#    if(wlan.isconnected()):
#        break

#myMotorController = MotorController(Screen,settings.freq)

#t1 = _thread.start_new_thread(ArtnetClient.udp_listen, ("2.0.0.10",myMotorController,settings,wlan))

#myMotorWebServer = MotorWebServer(wlan, myMotorController,settings)
#myMotorWebServer.webServerTask()
