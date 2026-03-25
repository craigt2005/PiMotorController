import socket

class ArtnetClient:
 
    def udp_listen(ip,motorController):
        
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
            
            
            
            #C1_RED.duty_u16(packet[18] * 256)
            #C1_GREEN.duty_u16(packet[19] * 256)
            #C1_BLUE.duty_u16(packet[20] * 256)
    
