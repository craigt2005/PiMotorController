from machine import Pin, PWM
import utime

class Motor:
    def __init__(self, in1, in2, freq):
        self.in1 = PWM(Pin(in1))
        self.in2 = PWM(Pin(in2))
        
        self.in1.freq(freq) # Set PWM frequency to 1kHz
        self.in2.freq(freq) # Set PWM frequency to 1kHz

    def setFreq(self, freq):
        self.stop()
        self.in1.freq(freq)
        self.in2.freq(freq)

    def drive(self, speed):
        print(speed)
        # Speed should be between -65535 and 65535
        if speed > 0:
            self.in1.duty_u16(speed)
            self.in2.duty_u16(0)
        elif speed < 0:
            self.in1.duty_u16(0)
            self.in2.duty_u16(-speed)
        else:
            self.stop()

    def stop(self):
        self.in1.duty_u16(0)
        self.in2.duty_u16(0)
        