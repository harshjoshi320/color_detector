# import sys
import cv2 as cv
import numpy as np
import pygame, pygame.camera
from time import sleep
from orangepwm import *
from orangeservo import Servo
from pyA20.gpio import gpio, port
from arm_control import Arm
# from matplotlib import pyplot as plt


def captureImage(dev_index):
	'''
	numpy.ndarray captureImage():
	Captures image and return an numpy.ndarray object
	'''
	# Initialize camera as videocapture object
	# camera = cv.VideoCapture(dev_index)

	# # Captures image and returns a boolean and image
	# retval, img = camera.read()

	# if retval:
	# 	print("[INFO] Image Captured")
	# 	return img
	# else:
	# 	print("[WARN] Image Not Captured")
	# 	return None
	
	camera = pygame.camera.Camera(f'/dev/video{dev_index}', (640, 480))
	camera.start()
	image = camera.get_image()
	pygame.image.save(image, "/tmp/captured_image.png")

def extractROI(rangey, rangex, image):
	'''
	numpy.ndarray extractROI(list, list, numpy.ndarray):
	Takes x and y ranges and returns the 'Region Of Interest'
	extracted from the image
	'''
	if isinstance(image, np.ndarray):
		# Extracts the Region of Interest
		roi = image[rangey[0]:rangey[1], rangex[0]:rangex[1]]
		# print("[INFO] Extracted ROI")

		# Display the extracted ROI
		cv.imshow("ROI",roi)
		cv.waitKey(0)
		cv.destroyAllWindows()
		# cv.imwrite(f"{str(rangex[0])}.png", roi)
		return roi
	else:
		print("[WARN] No Image Found!")
		return None

def getAvgBGR(img):
	'''
	list getAvgBGR(numpy.ndarray):
	Returns average BGR values of the image as a dictionary
	{'b':<val>, 'g':<val>, 'r':<val>}
	'''
	# Get image size as a list
	img_size = img.shape[:2]

	hists = list()

	for i in range(3):
		hists.append(cv.calcHist([img],[i],None,[256],[0,256]))

	# print("[INFO] Calculated Histrograms")
	
	avg_bgr = {'b':0, 'g':0, 'r':0}

	for i,prop in enumerate(avg_bgr):
		prop_sum = 0
		for j in range(0, 256):
			prop_sum = prop_sum + (hists[i][j][0] * j)
		avg_bgr[prop] = round(prop_sum/(img_size[0]*img_size[1]))

	print(
			f"Average BGR Values\n" 
			f"+-------------------\n"
			f"| {'B':<11}: {avg_bgr['b']:>5}\n"
			f"| {'G':<11}: {avg_bgr['g']:>5}\n"
			f"| {'R':<11}: {avg_bgr['r']:>5}\n"
			)

	print(avg_bgr)
	return avg_bgr


def getColor(bgr):
	'''
	int getColor(list[3]):
	Takes bgr values as a dictionary and returns an integer
	corresponding to the color.
	red: 0
	green: 1
	blue: 2
	other: -1
	'''
	if bgr['b']>bgr['g'] and bgr['b']>bgr['r']:
		return 2
	elif bgr['g']>bgr['b'] and bgr['g']>bgr['r']:
		return 1
	elif bgr['r']>bgr['b'] and bgr['r']>bgr['g']:
		return 0
	else:
		return -1


if __name__=='__main__':

	pygame.init()
	pygame.camera.init()

	
	# 
	# positions:
	# 
	# pos 0:	[y0, y1], [x0, x1]
	# pos 1:	[y0, y1], [x0, x1]
	# pos 2:	[y0, y1], [x0, x1]
	# 

	positions = (
		([384, 430], [61, 121]),
		([284, 333], [314, 365]),
		([104, 160], [470, 530])
		)

	arm = Arm([ port.PA6, port.PA12, port.PA3, port.PA11])

	arm.initialize()

	print(
		f"\n#### Starting the color sorter/picker program ####\n"
		f"\n[DESC]----\n"
		f"\nThis user will be asked to choose a color."
		f"\nThe colors are indexed as:"
		f"\n	0: Red"
		f"\n	1: Green"
		f"\n	2: Blue"
		f"\nThree Regions Of Interest or ROIs are extracted from the captured image."
		f"\nThese ROIs will be examined to find the object with the choosen color."
		f"\nOnce the position is determined the arm will signaled to extract the object."
		f"\n----[DESC]\n"
		)

	print(f"## Choose the color to be picked")


	try:
		choice = int(input("\nEnter the color index [default 0]: "))

		if choice not in [ 0, 1, 2]:
			print(
				f"[WARN] Invalid user input\n"
				f"[WARN] Using default color index [0]"
				)
			choice = 0
	except ValueError:
		print(
				f"[WARN] Invalid user input\n"
				f"[WARN] Using default color index [0]"
				)
		choice = 0

	captureImage(1)
	image = cv.imread("/tmp/captured_image.png")
	
	rois = list()

	for i,(y,x) in enumerate(positions):
		rois.append(extractROI(y, x, image))
		print(f"[INFO] Extracted ROI at position:{i}")

	found = False
	for i,region in enumerate(rois):
		color = getColor(getAvgBGR(region))
		if color == choice:
			found = True
			print(f"[INFO] Found color [{choice}] at position [{i}]")
			arm.pick(i)
			sleep(1)
			arm.drop()
			break

	if not found:
		print(f"[WARN] Color with index [{choice}] not found")
