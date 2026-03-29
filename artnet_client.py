import socket

class ArtnetClient:
 
    def udp_listen(ip,motorController,settings):
        self.settings = settings
        sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #UDP
        server_addressUDP = (ip, 6454)  
        sockUDP.bind(server_addressUDP)
        
        while(True):
            #C1_RED.duty_u16(64 *256)
            packet = sockUDP.recv(1024)
            
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
            subuni = packet[14]
            net = packet[15]
            universe = (net << 8) | subun
            
            #ignore if not our universe
            if (not universe == self.settings.universe)
                continue
            
            #if this is our universe packet, then read the motor values
            m1cmd = packet[18] #0 -> 255
            m2cmd = packet[19] #0 -> 255
            
            if (m1cmd == 0):
                motorController.stop_motor1
                continue
                
            if (m2cmd == 0):
                motorController.stop_motor2
                continue
            
            if (m1cmd < 128)
                motorController.set_motor1speed(m1cmd)
                motorController.fwd_motor1()
                
            if (m2cmd < 128)
                motorController.set_motor2speed(m2cmd)
                motorController.fwd_motor1()
                
            if (m1cmd > 128)
                motorController.set_motor1speed(m1cmd - 128)
                motorController.rev_motor1()
                
            if (m2cmd > 128)
                motorController.set_motor2speed(m2cmd - 128)
                motorController.rev_motor2()
  
        
    
