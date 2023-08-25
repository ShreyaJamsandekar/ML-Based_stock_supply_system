import cv2
import os
import time
from product import *


def get_frame1():
	camera_port=1
	camera=cv2.VideoCapture(camera_port) #this makes a web cam object
	time.sleep(2)

	while True:
		ret, img = camera.read()
		cv2.imwrite(os.path.join("static/images/","test_image.jpg"),img)
		result = predict(img)

		cv2.putText(img, result, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))

		imgencode=cv2.imencode('.jpg',img)[1]
		stringData=imgencode.tostring()
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

	del(camera)


def get_frame2():
	camera_port=1
	camera = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW)

	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # set new dimensionns to cam object (not cap)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	time.sleep(2)

	while True:
		ret, img = camera.read()
		cv2.imwrite(os.path.join("static/images/","ref1.jpg"),img)
		imgencode=cv2.imencode('.jpg',img)[1]
		stringData=imgencode.tostring()
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

	del(camera)

def get_frame3():
	camera_port=1
	camera = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW)

	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # set new dimensionns to cam object (not cap)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	time.sleep(2)

	while True:
		ret, img = camera.read()
		cv2.imwrite(os.path.join("static/images/","ref2.jpg"),img)
		imgencode=cv2.imencode('.jpg',img)[1]
		stringData=imgencode.tostring()
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

	del(camera)


def get_frame4():
	camera_port=1
	camera = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW)

	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # set new dimensionns to cam object (not cap)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	time.sleep(2)

	while True:
		ret, img = camera.read()
		cv2.imwrite(os.path.join("static/images/","test_image1.jpg"),img)
		imgencode=cv2.imencode('.jpg',img)[1]
		stringData=imgencode.tostring()
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

	del(camera)
	



