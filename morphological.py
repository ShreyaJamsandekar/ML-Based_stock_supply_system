import cv2
import imutils
import math

def euclidean_distance(point1 , point2):
	return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def initialCalibration():
	#get the images you want to compare.
	original = cv2.imread("static/images/ref1.jpg")
	new = cv2.imread("static/images/ref2.jpg")
	diff = cv2.absdiff(original, new)

	#converting the difference into grayscale images
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	#cv2.imshow('gray',gray)

	#increasing the size of differences after that we can capture them all
	for i in range(0, 3):
		dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)

	#cv2.imshow('dilated',dilated)


	(T, thresh) = cv2.threshold(dilated,100, 255, cv2.THRESH_BINARY)

	#cv2.imshow('thresh',thresh)

	#increasing the size of differences after that we can capture them all
	for i in range(0, 3):
		dilated = cv2.dilate(thresh.copy(), None, iterations= i+ 1)

	#cv2.imshow('dilate2',dilated)

	# now we have to find contours in the binarized image
	cnts = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	xc = []
	yc = []
	i = 0
	for c in cnts:
		# nicely fiting a bounding box to the contour
		(x, y, w, h) = cv2.boundingRect(c)
		area = w * h
		#print(area)
		if(area > 30000):
			xCenter = (x + (x+w)) / 2
			yCenter = (y+ (y+h)) / 2
			print(xCenter,yCenter)
			xc.append(xCenter)
			yc.append(yCenter)
			cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.putText(new, str(i), (round(xCenter),round(yCenter)), cv2.FONT_HERSHEY_COMPLEX, 5, (0,0,255))
			i = i + 1
	print(xc,yc)
	cv2.imshow('new',new)
	cv2.imwrite('static/images/final.jpg',new)

	return(xc,yc)

def stockCal(XC,YC):
	#get the images you want to compare.
	original = cv2.imread("static/images/ref1.jpg")
	new = cv2.imread("static/images/test_image1.jpg")
	diff = cv2.absdiff(original, new)

	#converting the difference into grayscale images
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	#cv2.imshow('gray',gray)

	#increasing the size of differences after that we can capture them all
	for i in range(0, 3):
		dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)

	#cv2.imshow('dilated',dilated)


	(T, thresh) = cv2.threshold(dilated,100, 255, cv2.THRESH_BINARY)

	#cv2.imshow('thresh',thresh)

	#increasing the size of differences after that we can capture them all
	for i in range(0, 3):
		dilated = cv2.dilate(thresh.copy(), None, iterations= i+ 1)

	#cv2.imshow('dilate2',dilated)

	# now we have to find contours in the binarized image
	cnts = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	i = 0
	products = {'Product':['Product1','Product2','Product3','Product4'],
	'Availibility':['Not Available','Not Available','Not Available','Not Available']}
	for c in cnts:
		# nicely fiting a bounding box to the contour
		(x, y, w, h) = cv2.boundingRect(c)
		area = w * h
		#print(area)
		if(area > 30000):
			xCenter = (x + (x+w)) / 2
			yCenter = (y+ (y+h)) / 2
			print(xCenter,yCenter)
			if(xCenter<620 and yCenter>378):
				products['Availibility'][0] = 'Available'

			if(xCenter>620 and yCenter>378):
				products['Availibility'][1] = 'Available'

			if(xCenter<620 and yCenter<378):
				products['Availibility'][2] = 'Available'

			if(xCenter>620 and yCenter<378):
				products['Availibility'][3] = 'Available'


	return products
