from artnetListener import ArtnetListener
from machine import Pin
import time
import utime
from settings import Settings
from motorController import MotorController

def packet_handler(packet):
    led.value(1)     # Turn LED on
    #utime.sleep(0.1) # Wait half a second
        # Turn LED off
    
    
    if packet["universe"] == 0: # artnet universes are 0 based
               # --- motor logic (unchanged) ---
        m1cmd = packet["channels"][0]
        m2cmd = packet["channels"][1]     
             
        print(m1cmd,m2cmd) 
            
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
    led.value(0) 

def connection_state_changed_handler(state):
    print(f"New State: {state}")


#Load Motor Settings File
settings = Settings()
if not settings.load():
    print("No settings file, using defaults")
    settings.save()

#set up the led
led = Pin("LED", Pin.OUT)

motorController = MotorController(settings.freq)

offset = 4
artnet = ArtnetListener()
artnet.on_packet(packet_handler)
artnet.listen()









 
 
   
   



 

 
 



