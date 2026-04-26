from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

class Screen:

    i2c=I2C(1,sda=Pin(6), scl=Pin(7), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)

    status = ""
    mode = ""
    ip = ""
    M1 = "NA"
    M2 = "NA"
    c1 = 0
    c2 = 0

#some bollocks 2
    def __init__(self):       
        self.oled.fill(0)
        self.oled.show()

    def setMode(self, mode):
        self.mode = mode
        self.render()
        
    def setMotor1Speed(self,M1Spd):
        self.M1 = M1Spd
        self.render()

    def setMotor2Speed(self,M2Spd):
        self.M2 = M2Spd
        self.render()

    def setConnectionStatus(self, status):
        self.status = status
        self.render()
        
    def setIpAddress(self, ip):
        self.ip = ip
        self.render()

    def setArtnetStatus(self, artnetStatus):
        self.artnet = artnetStatus
        self.render()
        
    def ArtNetPacketReceived(self):
        
        #self.oled.fill_rect(0, 56, 8, 64, 1)
        self.oled.text('A',0,57,1)
        self.oled.show()
        self.oled.fill_rect(0, 56, 8, 64, 0)
        #self.oled.text('A',0,56,0)
        self.oled.show()
    
    def DMXChannels(self, c1, c2):
        self.c1 = c1
        self.c2 = c2
        self.render()

    def render(self):
        self.oled.fill(0)
        #self.oled.text("WiFi Status:",0,0)
        self.oled.text(self.status,0,0)

        #self.oled.text("Ip",0,20)
        self.oled.text(self.ip,0,8)

        #top horizontal line
        self.oled.line(0, 18, 128, 18,1)
        
        #vertical line
        self.oled.line(64, 18, 64, 55,1)

        #bottom horizontal line
        self.oled.line(0, 55, 128, 55,1)

        #artnet icon vertical line
        self.oled.line(10, 55, 10, 64,1)

        self.oled.text('Motor 1',3,19)
        self.oled.text('Motor 2',67,19)
        
        self.oled.text(self.M1,3,29)
        self.oled.text(self.M2,67,29)
        
        self.oled.text(str(self.c1),3,37)
        self.oled.text(str(self.c2),67,37)

        self.oled.show()
