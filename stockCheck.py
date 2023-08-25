import cv2
import numpy as np
import imutils

products = {'Product':['Product1','Product2','Product3','Product4'],
'Availibility':['Not Available','Not Available','Not Available','Not Available']}

def nothing(x):
	pass

def get_frame5():
	global products
	camera_port=0
	camera=cv2.VideoCapture(camera_port) #this makes a web cam object
	cv2.namedWindow("Trackbars")

	cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
	cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
	cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
	cv2.createTrackbar("U - H", "Trackbars", 179, 255, nothing)
	cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
	cv2.createTrackbar("U - V", "Trackbars", 250, 255, nothing)

	while True:
		#scen = session.get('scen',None)
		#print(scen)
		ret, img = camera.read()
		img = cv2.flip(img,1)
		l_h = cv2.getTrackbarPos("L - H", "Trackbars")
		l_s = cv2.getTrackbarPos("L - S", "Trackbars")
		l_v = cv2.getTrackbarPos("L - V", "Trackbars")
		u_h = cv2.getTrackbarPos("U - H", "Trackbars")
		u_s = cv2.getTrackbarPos("U - S", "Trackbars")
		u_v = cv2.getTrackbarPos("U - V", "Trackbars")

		lower_blue = np.array([l_h, l_s, l_v])
		upper_blue = np.array([u_h, u_s, u_v])
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower_blue, upper_blue)

		#increasing the size of differences after that we can capture them all
		for i in range(0, 9):
			dilated = cv2.erode(mask.copy(), None, iterations= i+ 1)

		'''    
		#increasing the size of differences after that we can capture them all
		for i in range(0, 3):
			dilated = cv2.dilate(mask.copy(), None, iterations= i+ 1)
		'''
		dilated = ~dilated
		cv2.imshow("mask", dilated)
		# now we have to find contours in the binarized image
		cnts = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		xc=[]
		yc=[]
		products['Availibility'][0] = 'Not Available'
		products['Availibility'][1] = 'Not Available'
		products['Availibility'][2] = 'Not Available'
		products['Availibility'][3] = 'Not Available'
		for c in cnts:
			# nicely fiting a bounding box to the contour
			(x, y, w, h) = cv2.boundingRect(c)
			area = w * h
			#print(area)
			if(area > 10000):
				xCenter = (x + (x+w)) / 2
				yCenter = (y+ (y+h)) / 2
				xc.append(xCenter)
				yc.append(yCenter)
				cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
				if(xCenter>300 and yCenter>265):
					products['Availibility'][0] = 'Available'

				if(xCenter<300 and yCenter>265):
					products['Availibility'][1] = 'Available'

				if(xCenter>300 and yCenter<265):
					products['Availibility'][2] = 'Available'

				if(xCenter<300 and yCenter<265):
					products['Availibility'][3] = 'Available'

		print(xc,yc)
		imgencode=cv2.imencode('.jpg',img)[1]
		stringData=imgencode.tostring()
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

		if cv2.waitKey(1) == 27:
			break
