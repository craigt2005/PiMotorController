from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

class Screen:

    i2c=I2C(0,sda=Pin(4), scl=Pin(5), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)

    status = ""
    mode = ""
    ip = ""
    color1 = (0, 0, 0)
    color2 = (0, 0, 0)
    artnet = "Idle"

#some bollocks 2
    def __init__(self):       
        self.oled.fill(0)
        self.oled.show()

    def setMode(self, mode):
        self.mode = mode
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

    def render(self):
        self.oled.fill(0)
        #self.oled.text("WiFi Status:",0,0)
        self.oled.text(self.status,0,0)

        #self.oled.text("Ip",0,20)
        self.oled.text(self.ip,0,8)

        self.oled.line(0, 18, 128, 18,1)
        self.oled.line(64, 18, 64, 64,1)

        self.oled.text('Motor 1',3,19)
        self.oled.text('Motor 2',67,19)

        self.oled.show()
