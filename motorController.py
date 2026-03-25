class MotorController:
    
    mode = "Basic"
    m1v = 0
    m2v = 0
        
    def __init__(self, Screen):
        self.screen = Screen
        pass

    def set_motor1speed(self, spd):
        # Set the speed of M1
        self.screen.setMotor1Speed(str(spd))
        pass

    def set_motor2speed(self, spd):
        # Set the speed of M2
        self.screen.setMotor2Speed(str(spd))
        pass