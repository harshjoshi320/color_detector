import sys
import cv2 as cv
import numpy as np
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
		print("[INFO] Extracted ROI")

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

	print("[INFO] Calculated Histrograms")
	
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

if __name__=='__main__':
	image = captureImage(-1)
	# image = cv.imread("../sample.png")
	
	pos0 = extractROI([117,184], [91,160], image)
	pos1 = extractROI([117,184], [235,305], image)
	pos2 = extractROI([117,184], [380,454], image)

	print('pos0: ',getColor(getAvgHSV(pos0)))
	print('pos1: ',getColor(getAvgHSV(pos1)))
	print('pos2: ',getColor(getAvgHSV(pos2)))