from orangepwm import *
from orangeservo import Servo
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep


class Arm():
    def __init__(self, ports=[ port.PA6, port.PA12, port.PA3, port.PA11]):
        gpio.init()
        self.claw = Servo(ports[0])
        self.wrist = Servo(ports[1])
        self.elbow = Servo(ports[2])
        self.shoulder = Servo(ports[3])

    def __del__(self):
        del self.claw
        del self.wrist
        del self.elbow
        del self.shoulder


    def initialize(self, verb=0):
        if verb != 0:
            print(f"[INFO] Initializing...")
        self.claw.setAngle(0); sleep(0.5)
        self.wrist.setAngle(0); sleep(0.5)
        self.elbow.setAngle(0); sleep(0.5)
        self.stopAll()
        if verb != 0:
            print(f"    ...servos in initial positions.")
        # self.shoulder.setAngle(25); sleep(1)


    def fullSweep(self):
        self.shoulder.setAngle(0);sleep(1)
        self.shoulder.setAngle(180);sleep(1)
        self.shoulder.setAngle(25);sleep(1)


    def stopAll(self):
        self.claw.stop()
        self.wrist.stop()
        self.elbow.stop()
        self.shoulder.stop()


    def test(self):
        print("[INFO] Testing Shoulder")
        print(f"[INFO] Shoulder At Port [{self.shoulder.port}]")
        self.shoulder.setAngle(0)
        print("Position: 0")
        sleep(1)
        self.shoulder.setAngle(180)
        print("Position: 180")
        sleep(1)
        self.shoulder.setAngle(25)
        print("Position: 25")
        sleep(1)
        self.shoulder.stop()

        print("[INFO] Testing Elbow")
        print(f"[INFO] Elbow At Port [{self.elbow.port}]")
        self.elbow.setAngle
        print("Position: 0")
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
        print("Position: 0")
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
        self.claw.setAngle(90)
        print("Position: 60")
        sleep(2)
        self.claw.setAngle(0)
        print("Position: 0")
        sleep(1)

        print("[INFO] Tests Finished")

    
    def pick(self, pos=0):
        print(f"[INFO] Start Routine: Pick At Pos-{pos}... ", end='')
        positions = [0, 29, 48]
        self.initialize(0)
        self.shoulder.setAngle(positions[pos]); sleep(1)
        self.shoulder.stop()
        self.claw.setAngle(0); sleep(1)
        self.wrist.setAngle(0); sleep(1)
        self.elbow.setAngle(70); sleep(1)
        self.claw.setAngle(90); sleep(1)
        self.wrist.stop()
        self.elbow.setAngle(0); sleep(1)
        self.elbow.stop()
        print("Picked")


    def drop(self, pos=2):
        positions = [75, 95, 120]
        print(f"[INFO] Start Routine: Drop... ", end='')
        self.wrist.setAngle(0); sleep(1)
        self.shoulder.setAngle(positions[pos]); sleep(1)
        self.shoulder.stop()
        self.elbow.setAngle(40); sleep(1)
        self.claw.setAngle(0); sleep(0.5)
        self.initialize(0)
        print("Dropped")



if __name__ == '__main__':


    gpio.init()
    arm = Arm([ port.PA6, port.PA12, port.PA3, port.PA11])
    arm.initialize()
    arm.fullSweep()
    # arm.pick(0)
    # arm.drop()
    # arm.stopAll()
    # sleep(2)
    # arm.pick(1)
    # arm.drop()
    # arm.stopAll()
    # sleep(2)
    # arm.pick(2)
    # arm.drop()
    # arm.stopAll()
    # sleep(2)
    arm.stopAll()
    del arm

