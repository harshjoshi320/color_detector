Color Picker/Sorter Using OPi PC, MeArm v1 and USB Webcam.

Modules - 

orangepwm.py - This modules provides pwm functionality for OrangePi.
		Source: https://github.com/evergreen-it-dev/orangepwm

orangeservo.py - Defines 'Servo' object.

arm_control.py - Defines 'Arm', which creates Servo object for each servo in MeArm.
		Provides several methods for easy arm control.

color_detect.py - Main module that defines functions required for image capture, ROI extraction,
		histogram calculation and many more.
