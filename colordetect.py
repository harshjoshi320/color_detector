# import sys
import cv2 as cv
import numpy as np
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
	camera = cv.VideoCapture(dev_index)

	# Captures image and returns a boolean and image
	retval, img = camera.read()

	if retval:
		print("[INFO] Image Captured")
		return img
	else:
		print("[WARN] Image Not Captured")
		return None

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
		return roi
	else:
		print("[WARN] No Image Found!")
		return None

def getAvgHSV(img):
	'''
	list getAvgHSV(numpy.ndarray):
	Returns average HSV values of the image as a dictionary
	{'h':<val>, 's':<val>, 'v':<val>}
	'''
	# Get image size as a list
	img_size = img.shape[:2]

	# Converting Colorspace from BGR to HSV
	# It is easier to operate in HSV colorspace 
	hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	hists = list()
	# HSV values range from [0,0,0] to [179,255,255] 
	hsv_lmts = {'h':180,'s':256,'v':256}

	for i, prop in enumerate(hsv_lmts):
		hists.append(cv.calcHist([hsv_img],[i],None,[hsv_lmts[prop]],[0,hsv_lmts[prop]]))

	# print("[INFO] Calculated Histrograms")
	
	avg_hsv = {'h':0, 's':0, 'v':0}

	for i, prop in enumerate(hsv_lmts):
		prop_sum = 0
		for j in range(0, hsv_lmts[prop]):
			prop_sum = prop_sum + (hists[i][j][0] * j)
		avg_hsv[prop] = round(prop_sum/(img_size[0]*img_size[1]))

	
	# print(
	# 	f"Average HSV Values\n" 
	# 	f"+-------------------\n"
	# 	f"| {'Hue':<11}: {avg_hsv['h']:>5}\n"
	# 	f"| {'Saturation':<11}: {avg_hsv['s']:>5}\n"
	# 	f"| {'Value':<11}: {avg_hsv['v']:>5}\n"
	# 	)

	return avg_hsv

def getColor(hsv):
	'''
	int getColor(list[3]):
	Takes hsv values as a dictionary and returns an integer
	corresponding to the color.
	red: 0
	yellow: 1
	green: 2
	blue: 3
	other: -1
	'''
	if (hsv['s'] >= 200) and (hsv['v'] >= 200):
		if hsv['h'] in range(0, 7) or hsv in range(170, 180):
			return 0
		elif hsv['h'] in range(25, 34):
			return 1
		elif hsv['h'] in range(40, 71):
			return 2
		elif hsv['h'] in range(85, 134):
			return 3
		else:
			return -1
	else:
		return -1

# class ArmDummy():
# 	def initialize(self):
# 		print(f"[INFO] Initializing...")
# 		sleep(2)
# 		print(f"	...All servos in initial positions.")
	
# 	def pick(self, pos=0):
# 		print(f"[INFO] Start Routine: Pick At Pos-{pos}...", end='')
# 		sleep(4)
# 		print(" Picked")

# 	def drop(self):
# 		print(f"[INFO] Start Routine: Drop... ", end='')
# 		sleep(4)
# 		print(" Dropped")


if __name__=='__main__':
	
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
		f"\n	1: Yellow"
		f"\n	2: Green"
		f"\n	3: Blue"
		f"\nOnly three of these colors are available to pick from [ 0  2  3 ]\n"
		f"\nThree Regions Of Interest or ROIs are extracted from the captured image."
		f"\nThese ROIs will be examined to find the object with the choosen color."
		f"\nOnce the position is determined the arm will signaled to extract the object."
		f"\n----[DESC]\n"
		)

	print(f"## Choose the color to be picked")


	try:
		choice = int(input("\nEnter the color index [default 0]: "))

		if choice not in [ 0, 1, 2, 3]:
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

	image = captureImage(1)
	# image = cv.imread("../sample.png")
	
	rois = list()

	for i,(y,x) in enumerate(positions):
		rois.append(extractROI(y, x, image))
		print(f"[INFO] Extracted ROI at position:{i}")

	found = False
	for i,region in enumerate(rois):
		color = getColor(getAvgHSV(region))
		if color == choice:
			found = True
			print(f"[INFO] Found color [{choice}] at position [{i}]")
			arm.pick(i)
			sleep(1)
			arm.drop()
			break

	if not found:
		print(f"[WARN] Color with index [{choice}] not found")
