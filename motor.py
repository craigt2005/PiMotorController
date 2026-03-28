from machine import Pin, PWM
import utime

class Motor:
    def __init__(self, ena, in1, in2, freq):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.speed_pin = PWM(Pin(ena))
        self.speed_pin.freq(freq) # Set PWM frequency to 1kHz

    def setFreq(self, freq):
        self.stop()
        self.speed_pin.freq(freq)

    def drive(self, speed):
        # Speed should be between -65535 and 65535
        if speed > 0:
            self.in1.value(1)
            self.in2.value(0)
            self.speed_pin.duty_u16(speed)
        elif speed < 0:
            self.in1.value(0)
            self.in2.value(1)
            self.speed_pin.duty_u16(abs(speed))
        else:
            self.stop()

    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.speed_pin.duty_u16(0)