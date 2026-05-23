import socket
import time
import network
import _thread
from time import sleep
from artnetSettings import ArtnetSettings

class ArtnetListener:
    def __init__(self):
        #Start Timers
        self.system_start = time.ticks_ms()
        
        #Define the meanings
        self.status_meanings = {
            -3: "FAIL",
            -2: "NO AP FOUND",
            -1: "CONNECT FAIL",
             0: "IDLE",
             1: "CONNECTING",
             2: "HANDSHAKE",
             3: "CONNECTED (NO IP YET)",
             4: "GOT IP"
        }
        
        #Packet Handlers
        self._on_packet_callbacks = []
        self._on_connection_state_changed_callbacks = []
        
        #Load the settings file
        self.settings = ArtnetSettings()
        if not self.settings.load():
            print("No settings file artnetSettings.json, using defaults")
            self.settings.save()
        
        
    def on_connection_state_changed(self, callback):
        self._on_connection_state_changed_callbacks.append(callback)
        
    def _raise_connection_state_changed_event(self, state):
        for cb in self._on_connection_state_changed_callbacks:
            cb(state)
        
        
        
    def on_packet(self, callback):
        """Register a callback: callback(packet)"""
        self._on_packet_callbacks.append(callback)
        
    def _raise_packet_event(self, packet):
        for cb in self._on_packet_callbacks:
            cb(packet)
        
    def receive_packet(self, raw_data):
        packet = raw_data
        self._raise_packet_event(packet)
 
    def connect_wifi(self):
        wlan = network.WLAN(network.WLAN.IF_STA)
        wlan.active(True)
        wlan.disconnect()
        sleep(0.1)
    
        if not wlan.isconnected():
            print("Connecting WiFi...")
            print("ssid:",self.settings.ssid)
            wlan.ifconfig((self.settings.ip,self.settings.subnet,self.settings.gateway,self.settings.dns))
            wlan.connect(self.settings.ssid, self.settings.password)



            start = time.ticks_ms()
            while not wlan.isconnected():
                statusText = self.status_meanings.get(wlan.status(), "UNKNOWN")
                self._raise_connection_state_changed_event(statusText)
                print(statusText)
                if time.ticks_diff(time.ticks_ms(),start ) > 60000:
                    print("WiFi connect timeout")
                    return None
                time.sleep(0.5)

        
        print("WiFi connected:", wlan.ifconfig())
        return wlan
 
    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.settings.ip, 6454))
        sock.settimeout(2)  # short timeout = responsive loop
        return sock

    def send_keepalive(self,sock, target_ip):
        try:
            sock.sendto(b'\x00', (target_ip, 6454))
        except:
            pass
 
    def listen(self):
        
        wlan = self.connect_wifi()
        sock = self.create_socket()
        
        last_packet_time = time.ticks_ms()
        last_keepalive = time.ticks_ms()
        
        SIGNAL_TIMEOUT = 10000   # 10s no Art-Net = reconnect
        KEEPALIVE_INTERVAL = 3000  # send every 3s
        
        print("Listening for Art-Net...")

        
        

        while(True):
            #print("packet")
            #C1_RED.duty_u16(64 *256)
            try:
                packet = sock.recv(1024)
            
                # got data → reset watchdog
                last_packet_time = time.ticks_ms()
        
                #skip non artnet packets
                if not(packet.startswith(b'Art-Net\x00')):
                    continue
                
                #compare op-code
                #dmxOpCode = int.from_bytes(b'\x00\x50')
                opcode = int.from_bytes(packet[8:10], 'little')
                if opcode != 0x5000:
                    continue
                
                #get the universe
                universe = int.from_bytes(packet[14:15], 'little') +1
                
                #print("Artnet Packet Here")
                self._raise_packet_event(
                    {
                        "universe":universe,
                        "channels":packet[18:529]
                    })               
            
                
            except OSError as e:
                # timeout = normal, ignore
                #if e.args[0] != 110:
                print("Socket error:", e)
                    
            # --- KEEPALIVE ---
            if time.ticks_diff(time.ticks_ms(), last_keepalive) > KEEPALIVE_INTERVAL:
                self.send_keepalive(sock,self.settings.ip)
                last_keepalive = time.ticks_ms()

            # --- WATCHDOG (THIS FIXES YOUR ISSUE) ---
            if time.ticks_diff(time.ticks_ms(), last_packet_time) > SIGNAL_TIMEOUT:
                print("Signal lost → reconnecting WiFi")

                try:
                    sock.close()
                except:
                    pass

                print("reconnecting")
                wlan = self.connect_wifi()
                sock = self.create_socket()

                last_packet_time = time.ticks_ms()
    
    