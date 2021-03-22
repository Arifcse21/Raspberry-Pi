from flask import Flask, render_template, request, redirect, url_for, make_response, Response
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import motors
import socket
from camera_pi import Camera

motors.stop()

# Get server ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()

app = Flask(__name__) 

@app.route('/')
def index():

	return render_template('index.html')
############
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

############

@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):

	changePin = int(changepin) 

	if changePin == 1:
		motors.turnLeft()
	elif changePin == 2:
		motors.forward()
	elif changePin == 3:
		motors.turnRight()
	elif changePin == 4:
		motors.backward()
	elif changePin == 5:
		motors.stop()
	else:
		print("Wrong command")

	response = make_response(redirect(url_for('index')))
	return(response)

app.run(debug=True, host='192.168.0.5', port=2743) 
