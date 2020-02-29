import sys
import cv2 as cv
import numpy as np
# from matplotlib import pyplot as plt

def captureImage():
	# Initialize camera as videocapture object
	camera = cv.VideoCapture(-1)

	# Captures image and returns a boolean and image
	retval, img = camera.read()

	if retval:
		print("[INFO] Image Captured")
		return img
	else:
		print("[WARN] Image Not Captured")
		return None

def getColor():
	# orig_img = cv.imread(sys.argv[1])
	orig_img = captureImage()
	cv.imshow("Captured Image",orig_img)
	cv.waitKey(0)
	cv.destroyAllWindows()

	# Runs only if the image is valid
	if isinstance(orig_img, np.ndarray):
		
		# Extracts the Region of Interest
		img = orig_img[180:480, 80:560]
		print("[INFO] Extracted ROI")

		cv.imshow("ROI",img)
		cv.waitKey(0)
		cv.destroyAllWindows()

		# Converting Colorspace from BGR to HSV
		# It is easier to operate in HSV colorspace 
		hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
		hists = list()

		# HSV values range from [0,0,0] to [179,255,255] 
		hsv_lmts = {'h':180,'s':256,'v':256}

		for i, prop in enumerate(hsv_lmts):
			hists.append(cv.calcHist([hsv_img],[i],None,[hsv_lmts[prop]],[0,hsv_lmts[prop]]))

		print("[INFO] Calculated Histrograms")
		# print(hists[0],  len(hists[0]))
		# for i in range(1,4):
		# 	plt.subplot((310+i)), plt.plot(hists[i-1])

		# plt.xlim([0,256])

		# plt.show()

		avg_hsv = {'h':0, 's':0, 'v':0}

		for i, prop in enumerate(hsv_lmts):
			prop_sum = 0
			for j in range(0, hsv_lmts[prop]):
				prop_sum = prop_sum + (hists[i][j][0] * j)
			avg_hsv[prop] = round(prop_sum/144000)

		
		print(
			f"Average HSV Values" 
			f"+-------------------"
			f"| {"Hue":<11}: {avg_hsv['h']:>5}"
			f"| {"Saturation":<11}: {avg_hsv['s']:>5}"
			f"| {"Value":<11}: {avg_hsv['v']:>5}"
			)
			
	else:
		print("[WARN] No Image Found!")

if __name__=='__main__':
	getColor()