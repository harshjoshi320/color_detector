from orangepwm import *
from orangeservo import Servo
from pyA20.gpio import gpio
from pyA20.gpio import port

class Arm():
	def __init__(self, claw, wrist, elbow, shoulder):
		self.claw = claw 
		self.wrist = wrist
		self.elbow = elbow
		self.shoulder = shoulder

	def clawOpen(self):
		self.claw.setAngle(0)
		self.claw.stop()

	def clawClose(self):
		self.claw.setAngle(55)
		self.claw.stop()