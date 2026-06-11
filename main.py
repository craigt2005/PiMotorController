from artnetListener import ArtnetListener
from machine import Pin
import time
import utime
from settings import Settings
from motor import Motor

def packet_handler(packet):
    led.value(1)     # Turn LED on
    #utime.sleep(0.1) # Wait half a second
        # Turn LED off
    
    
    if packet["universe"] == universe: # artnet universes are 0 based
               # --- motor logic (unchanged) ---
        m1cmd = packet["channels"][offset]
           
             
        #print(m1cmd) 
            
        if m1cmd in (0, 127): #stop if its 0 or 127
            motor.stop()
            spd = 0
        
        else:
            #take the number and subtract 127 so we get a neg fwd, or pos bac
            spd = (m1cmd - 127) *512
            motor.drive(spd)

            
                
        print(spd)
       
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

#motorController = MotorController(settings.freq)
motor = Motor(12,13,settings.freq)
motor.stop()

artnet = ArtnetListener()
offset = artnet.getAddress()-1
universe = artnet.getUniverse() -1
artnet.on_packet(packet_handler) 
artnet.listen()









 
 
   
   



 

 
 



