from machine import Pin, PWM
from motor import Motor

class MotorController:
    
       
        
    def __init__(self, Screen):  
        
        self.freq=2000        
        self.motor1 = Motor(15,14,13,self.freq)
        self.motor2 = Motor(12,11,10,self.freq)
        self.motor1.stop()
        self.motor2.stop()
    
        self.screen = Screen
        pass




    def set_motor1speed(self, spd):
        # Set the speed of M1
        self.motor1.drive(spd)
        v1perc = spd / 65535
        self.screen.setMotor1Speed(str(v1perc))
        
        pass

    def set_motor2speed(self, spd):
        # Set the speed of M2
        self.motor2.drive(spd)
        v2perc = spd / 65535
        self.screen.setMotor2Speed(str(v2perc))
        pass