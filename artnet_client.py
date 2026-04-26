import socket

class ArtnetClient:
 
    
 
 
    def udp_listen(ip,motorController,settings,wlan):
        #self.settings = settings
        sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #UDP
        sockUDP.settimeout(5.0)
        server_addressUDP = (ip, 6454)  
        sockUDP.bind(server_addressUDP)
        print("waiting for Artnet Packets")
        
        last_packet_time = time.ticks_ms()
        last_keepalive = time.ticks_ms()
        
        try:
            while(True):
                #print("packet")
                #C1_RED.duty_u16(64 *256)
                try:
                    packet = sockUDP.recv(1024)
                
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
                    
                    motorController.screen.ArtNetPacketReceived()
                
                    #get the universe
                    universe = int.from_bytes(packet[14:15], 'little') +1
                    
                    #ignore if not our universe
                    if (not universe == settings.universe):
                        continue
            
                #except OSError as e:
                #   print("Socket state", wlan.isconnected())
                #    print("Socket error:", e)
                 #   continue
                
                  
                
                #net = packet[15]
                #universe = (net << 8) | subuni
                #print()
                
     
                    #if this is our universe packet, then read the motor values
                    m1cmd = int(packet[18]) #0 -> 255
                    m2cmd = int(packet[19]) #0 -> 255
                
                    motorController.screen.DMXChannels(m1cmd,m2cmd)
                
                    if (m1cmd == 0 or m1cmd == 127):
                        motorController.stop_motor1()
                        
                        
                    if (m2cmd == 0 or m2cmd == 127):
                        motorController.stop_motor2()
                        
                    
                    if (0<m1cmd < 127):
                        #print(m1cmd)
                        motorController.set_motor1speed(127-m1cmd)
                        motorController.fwd_motor1()
                        
                    if (0<m2cmd < 127):
                        motorController.set_motor2speed(127-m2cmd)
                        motorController.fwd_motor1()
                        
                    if (m1cmd > 127):
                        motorController.set_motor1speed(m1cmd - 127)
                        motorController.rev_motor1()
                        
                    if (m2cmd > 127):
                        motorController.set_motor2speed(m2cmd - 127)
                        motorController.rev_motor2()
              
        
                 except OSError as e:
                    # timeout = normal, ignore
                    if e.args[0] != 110:
                    print("Socket error:", e)
        
    
