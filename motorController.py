class MotorController:
    
    mode = "Basic"
    m1v = 0
    m2v = 0
        
    def __init__(self, Screen):
        self.screen = Screen
        pass

    def set_mode(self, mode):
        self.mode = mode
        self.screen.setMode(mode)
        print("Tape mode set to:", mode)
        # Set the LED tape to the specified mode
        pass

    def set_motor1speed(self, color):
        # Set the first color for the LED tape
        self.screen.setColor1(color)
        pass

    def set_motor2speed(self, color):
        # Set the second color for the LED tape
        self.screen.setColor2(color)
        pass