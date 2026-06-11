import socket
import time
import network
import _thread
from time import sleep
from artnetSettings import ArtnetSettings
import struct

class ArtnetListener:
    def __init__(self):
        #Start Timers
        self.system_start = time.ticks_ms()
        
        self.wlan = None
        
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
                time.sleep(1)

        
        print("WiFi connected:", wlan.ifconfig())
        return wlan
 
    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", 6454))
        sock.settimeout(8)  # short timeout = responsive loop
        
        return sock

    def send_keepalive(self,sock, target_ip):
        try:
            sock.sendto(b'\x00', (target_ip, 6454))
        except:
            pass
 
    def fixed_str(self,s, length):
            b = s.encode("ascii")
            return b[:length] + b"\x00" * (length - len(b))
     
     
    def ip_to_bytes(self,ip_str):
        return bytes(int(x) & 0xFF for x in ip_str.split("."))

     
    def build_artnet_poll_reply(self):
    
        packet = bytearray()

        # --- Header ---
        packet += b"Art-Net\x00"

        # OpCode (PollReply = 0x2100, little endian)
        packet += struct.pack("<H", 0x2100)

        # --- Core fields ---
        ip = self.wlan.ifconfig()[0]
        packet += self.ip_to_bytes(ip)      # Node IP (4 bytes)
        packet += struct.pack("<H", 0x1936)     # Port (6454)

        packet += struct.pack(">H", 1)          # Firmware version (big endian here)
        packet += bytes([0x00])                 # Net switch
        packet += bytes([0x00])                 # Sub switch

        packet += struct.pack(">H", 0xFFFF)     # OEM
        packet += bytes([0x00])                 # UBEA version
        packet += bytes([0x00])                 # Status1

        packet += struct.pack(">H", 0x7FFF)     # ESTA manufacturer code

        # --- Names ---
        packet += self.fixed_str(self.settings.artnetshort, 18)     # Short name
        packet += self.fixed_str(self.settings.artnetlong, 64)      # Long name

        # Node report (64 bytes)
        packet += self.fixed_str("#0001 [0000] OK", 64)

        # --- Ports ---
        packet += struct.pack(">H", 1)          # Num ports

        packet += bytes([0x80, 00, 0, 0])        # Port types
        packet += bytes([0, 0, 0, 0])           # Good input
        packet += bytes([0, 0, 0, 0])           # Good output
        packet += bytes([0, 0, 0, 0])           # SwIn
        packet += bytes([0, 0, 0, 0])           # SwOut set the first one to the universe you need , 0 based [[2,0,0,0]] is uni 3

        # --- Misc ---
        packet += bytes([0x00])                 # SwVideo
        packet += bytes([0x00])                 # SwMacro
        packet += bytes([0x00])                 # SwRemote
        packet += bytes([0x00, 0x00, 0x00])     # Spare
        packet += bytes([0x00])                 # Style

        # --- MAC & binding ---
        packet += bytes(self.wlan.config('mac'))     # MAC (6 bytes)
        packet += bytes(self.ip_to_bytes(ip))      # Bind IP
        packet += bytes([0x01])                 # Bind index
        packet += bytes([0x00])                 # Status2

        # Filler (26 bytes)
        packet += bytes([0x00] * 26)

        return bytes(packet)

 
    def listen(self):
        
        self.wlan = self.connect_wifi()
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
                packet,addr = sock.recvfrom(1024)
                src_ip = addr[0]
                # got data → reset watchdog
                last_packet_time = time.ticks_ms()
        
                #skip non artnet packets
                if not(packet.startswith(b'Art-Net\x00')):
                    continue
                
                #compare op-code
                #dmxOpCode = int.from_bytes(b'\x00\x50')
                opcode = int.from_bytes(packet[8:10], 'little')
                
                
                print("ArtNet from", src_ip, "opcode", hex(opcode), "len", len(packet))

                
                if opcode == 0x5000:
                    #get the universe
                    universe = int.from_bytes(packet[14:16], 'little')
                
                    #print("Artnet Packet Here")
                    self._raise_packet_event(
                        {
                            "universe":universe,
                            "channels":packet[18:529]
                        })
                    
                if opcode == 0x2000:
                    reply = self.build_artnet_poll_reply()
                    sock.sendto(reply, (src_ip,6454))
                    print("polled")
            
                
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
                self.wlan = self.connect_wifi()
                sock = self.create_socket()

                last_packet_time = time.ticks_ms()
    
    