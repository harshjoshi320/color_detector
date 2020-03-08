from orangepwm import *
from orangeservo import Servo
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep

class Arm():
	def __init__(self, ports):
		self.claw = Servo(ports[0]) 
		self.wrist = Servo(ports[1])
		self.elbow = Servo(ports[2])
		self.shoulder = Servo(ports[3])

	def test(self):
		print("[INFO] Test Shoulder")
		self.shoulder.setAngle(0)
		sleep(1)
		self.shoulder.setAngle(30)
		sleep(1)
		self.shoulder.setAngle(60)
		sleep(1)
		self.shoulder.setAngle(90)
		sleep(1)
		self.shoulder.setAngle(45)
		sleep(1)
		self.shoulder.stop()
		
		print("[INFO] Test Elbow")
		self.elbow.setAngle(0)
		sleep(1)
		self.elbow.setAngle(25)
		sleep(1)
		self.elbow.setAngle(45)
		sleep(1)
		self.elbow.setAngle(0)
		sleep(1)
		self.elbow.stop()

		print("[INFO] Test Wrist")
		self.wrist.setAngle(0)
		sleep(1)
		self.wrist.setAngle(20)
		sleep(1)
		self.wrist.setAngle(0)
		sleep(1)
		self.wrist.stop()

		print("[INFO] Test Claw")
		self.clawOpen()
		sleep(1)
		self.clawClose()

	def clawOpen(self):
		self.claw.setAngle(0)
		self.claw.stop()

	def clawClose(self):
		self.claw.setAngle(55)
		self.claw.stop()