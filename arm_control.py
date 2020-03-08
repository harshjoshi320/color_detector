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
		print("[INFO] Testing Shoulder")
		print(f"[INFO] Shoulder At Port [{self.shoulder.port}]")
		self.shoulder.setAngle(0)
		print("Position: 0")
		sleep(1)
		self.shoulder.setAngle(180)
		print("Position: 180")
		sleep(3)
		self.shoulder.setAngle(25)
		print("Position: 25")
		sleep(1)
		self.shoulder.stop()
		
		print("[INFO] Testing Elbow")
		print(f"[INFO] Elbow At Port [{self.elbow.port}]")
		self.elbow.setAngle
		print("Position: 0")(0)
		sleep(1)
		self.elbow.setAngle(45)
		print("Position: 45")
		sleep(1)
		self.elbow.setAngle(0)
		print("Position: 0")
		sleep(1)
		self.elbow.stop()

		print("[INFO] Testing Wrist")
		print(f"[INFO] Wrist At Port [{self.wrist.port}]")
		self.wrist.setAngle
		print("Position: 0")(0)
		sleep(1)
		self.wrist.setAngle(20)
		print("Position: 20")
		sleep(1)
		self.wrist.setAngle(0)
		print("Position: 0")
		sleep(1)
		self.wrist.stop()

		print("[INFO] Testing Claw")
		print(f"[INFO] Claw At Port [{self.claw.port}]")
		self.claw.setAngle(0)
		print("Position: 0")
		sleep(1)
		self.claw.setAngle(60)
		print("Position: 60")
		sleep(2)
		self.claw.setAngle(0)
		print("Position: 0")
		sleep(1)
		
		print("[INFO] Tests Finished")


if __name__ == '__main__':
	gpio.init()
	arm = Arm([ port.PA6, port.PA12, port.PA3, port.PA11])
	arm.test()
