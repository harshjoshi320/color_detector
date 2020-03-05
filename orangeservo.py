from orangepwm import * 
from pyA20.gpio import gpio
from pyA20.gpio import port

class Servo:
    def __init__(self, port, frequency=50):
        self.position = 0
        self.port = port
        self.frequency = frequency
        self.pwm = OrangePwm(self.frequency, self.port)
        self.pwm.start(self.position)

    def setAngle(self, angle):
        duty = (angle/180)*10 + 2.5
        self.pwm.changeDutyCycle(duty)
    
    def stop(self):
        self.pwm.changeDutyCycle(0)
