from machine import Pin, PWM
from motor import Motor

class MotorController:
    
       
        
    def __init__(self, Screen, PwmFreq):  
        
        self.freq=PwmFreq        
        self.motor1 = Motor(15,14,13,self.freq)
        self.motor2 = Motor(12,11,10,self.freq)
        self.motor1.stop()
        self.motor2.stop()
    
        self.m1rpm = 0
        self.m2rpm = 0
    
        self.m1run = True
        self.m2run = True
        
        self.m1fwd = True
        self.m2fwd = True
        
        self.screen = Screen
        pass


    def set_motorPWM(self, freq):
        self.motor1.setFreq(freq)
        self.motor2.setFreq(freq)

    def set_motor1speed(self, spd):
        # Set the speed of M1
        p1 = (spd / 128)
        #print(p1)
        if (not self.m1fwd):
            p1 = p1 *-1
        
        self.m1rpm = int(p1 * 65535)
        
        
        
        self.screen.setMotor1Speed(str(p1))
        if (self.m1run):
            self.motor1.drive(self.m1rpm)
        pass
    
    def set_motor2speed(self, spd):
        # Set the speed of M2 128 = max
        p2 = (spd / 128)
        
        if (not self.m2fwd):
            p2 = p2 *-1
        
        self.m2rpm = int(p2 * 65535)
        
        
        
        
        self.screen.setMotor2Speed(str(p2))
        if (self.m2run):
            self.motor2.drive(self.m1rpm)
        pass
    
    
         
    def start_motor1(self):
        self.m1run = True
        self.motor1.drive(self.m1rpm)
    
    def start_motor2(self):
        self.m2run = True
        self.motor2.drive(self.m2rpm)
        
    def rev_motor1(self):
        self.m1fwd = False
        self.start_motor1()
        
    def fwd_motor1(self):
        self.m1fwd = True
        self.start_motor1()
        
    def fwd_motor2(self):
        self.m2fwd = True
        self.start_motor2()
        
    def rev_motor2(self):
        self.m2fwd = False
        self.start_motor2()
    
    def stop_motor1(self):
        self.m1run = False
        self.motor1.stop()
        
    def stop_motor2(self):
        self.m2run = False
        self.motor2.stop()

   