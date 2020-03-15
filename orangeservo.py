from orangepwm import * 
from pyA20.gpio import gpio
from pyA20.gpio import port

class Servo:
    def __init__(self, port, frequency=50):
        self.port = port
        self.frequency = frequency
        self.pwm = OrangePwm(self.frequency, self.port)
        self.pwm.start(0)

    def __del__(self):
        self.pwm.stop()
        del self.pwm

    def setAngle(self, angle):
        duty = round(((angle/18) + 2.5),1)
        self.pwm.changeDutyCycle(duty)
    
    def stop(self):
        self.pwm.changeDutyCycle(0)
