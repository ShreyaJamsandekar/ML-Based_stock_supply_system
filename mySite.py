# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from supportFile import *
import os
import cv2
from timeSeries import *
import pandas as pd
from twilio.rest import Client
from stockCheck import *
#from morphological import initialCalibration,stockCal

account_sid = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

app = Flask(__name__)
#to delete chache memory
app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/home', methods=['GET', 'POST'])
def home():
	return redirect(url_for('input'))

@app.route('/', methods=['GET', 'POST'])
def input():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('video1'))

	return render_template('input.html', error=error)

@app.route('/video1', methods=['GET', 'POST'])
def video1():
	return render_template('video1.html')
'''
@app.route('/video2', methods=['GET', 'POST'])
def video2():
	if request.method == 'POST':
		return redirect(url_for('video3'))
	return render_template('video2.html')

@app.route('/video3', methods=['GET', 'POST'])
def video3():
	if request.method == 'POST':
		return redirect(url_for('video4'))
	return render_template('video3.html')
'''
@app.route('/video4', methods=['GET', 'POST'])
def video4():
	if request.method == 'POST':
		return redirect(url_for('stock'))
	return render_template('video4.html')

@app.route('/video_stream1')
def video_stream1():  
	return Response(get_frame1(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stream2')
def video_stream2():
	return Response(get_frame2(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stream3')
def video_stream3():
	return Response(get_frame3(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stream4')
def video_stream4():
	return Response(get_frame5(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stock',methods=['GET','POST'])
def stock():
	global products
	df = pd.DataFrame(products)
	return render_template('stock.html',tables=[df.to_html(classes='w3-table-all w3-hoverable w3-padding')], titles=df.columns.values)

@app.route('/bulk', methods=['GET', 'POST'])
def bulk():
	if request.method == 'POST':
		company = request.form["company"]
		mgs = request.form["mgs"]
		categeory = request.form["categeory"]
		#print(mgs)
		#print(categeory)
		df = pd.read_csv('mgs/'+categeory+'.csv')
		#print(df.to_string())

		nums = df.values.tolist()
		#print(nums)

		for num in nums:
			message = client.messages \
			.create(
					body=company+":\n"+mgs,
					from_='+15017122661',
					to='+91' + str(num[0])
				)
			#print(message.sid)
		

	return render_template('bulk.html')

@app.route('/demand',methods=['GET','POST'])
def demand():
	products = demandPrediction()
	df = pd.DataFrame(products)
	return render_template('demand.html',tables=[df.to_html(classes='w3-table-all w3-hoverable w3-padding')], titles=df.columns.values)

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)
