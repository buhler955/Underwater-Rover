#====================================================================================================================
# Program: Underwater Rover v2 Project
# Programmer: Austin Buhler
# Class: PROJ 222
# Date: April 13, 2021
#
#--------------------------------------------------------------------------------------------------------------------
# Sources
#--------------------------------------------------------------------------------------------------------------------
# Title: OpenCV – Stream video to web browser/HTML page
# Author: Adrian Rosebrock
# Date: Sept. 2, 2019
# Availablility: https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
# Usage: Used modified generate and video_stream functions
#--------------------------------------------------------------------------------------------------------------------
# Title: Video Streaming Web Server
# Author: Marcelo Rovai
# Date: Jun. 15, 2018
# Availablilty: https://medium.com/mjrobot-org/video-streaming-web-server-5315fd48899c
# Usage: Used for Flask setup. Also uses very similar video streaming setup to Rosebrock's article.
#--------------------------------------------------------------------------------------------------------------------
# Title: Flask app working really slow with opencv
# Author: Ahx
# Date: Sept. 11, 2020
# Availablilty: https://stackoverflow.com/questions/63703313/flask-app-working-really-slow-with-opencv
# Usage: Used for imutils WebcamVideoStream syntax, as OpenCV stream was too slow.
#--------------------------------------------------------------------------------------------------------------------
# Title: Flask - Calling python function on button OnClick event
# Author: Gihan Gamage
# Date: Mar. 17, 2018
# Availablilty: https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event
# Usage: Used background_process_test function for handling buttons without refreshing webpage. 
#        The JavaScript code was also used in home.html.
#--------------------------------------------------------------------------------------------------------------------
# Title: Using mousedown event on mobile without jQuery mobile?
# Author: Jasper
# Date: Jun 21, 2012
# Availablilty: https://stackoverflow.com/questions/11144370/using-mousedown-event-on-mobile-without-jquery-mobile
# Usage: Used JavaScript functions for touchstart and touchend in home.html. 
#        This allows the motors to move only when the button is being held.
#--------------------------------------------------------------------------------------------------------------------
#Web Page Pictures Used:
#https://www.pngjoy.com/freepng/arrow-clipart/2/
#https://www.stickpng.com/img/icons-logos-emojis/camera-icons/camera-icon-simple
#https://www.freeiconspng.com/thumbs/flashlight-icon/flashlight-icon-8.png
#https://www.google.com/imgres?imgurl=http://www.learnbydoing.org/wp-content/uploads/2014/11/cropped-mono-power-button-hi-270x270.png
#--------------------------------------------------------------------------------------------------------------------
# Libraries used: Flask, OpenCV, PiGPIO, OS, Imutils, Time, Subprocess, JQuery (In JavaScript/HTML Code)
#====================================================================================================================

from flask import Flask, render_template, Response, request
import cv2
import pigpio
import os
from imutils.video import WebcamVideoStream
from time import sleep
from subprocess import call

#====================================================================================================================
#Read local file to set session number - new pictures placed in new directory, so previous pictures are not overwritten due to naming conflicts
with open('/home/pi/underwater_rover/ses_count.txt', 'r') as read: #Open count file as read only
    session_num = read.readline() #Read numbers from file as strings
    PATH = '/home/pi/usb/Rover Session '+ session_num + ' Pictures' #Path to create pictures directory
    session_num = int(session_num) + 1 #Convert to integer

#Opened seperately so contents of file are replaced, not appended
with open('/home/pi/underwater_rover/ses_count.txt', 'w') as write: 
    write.write(str(session_num)) #Increment session count in file

#Attempt to create directory for pictures
try:
    os.mkdir(PATH)
except OSError:
    print ("Creation of the directory %s failed" % PATH)
    
has_drive = os.path.isdir(PATH) #Check if directory is present, if not, camera button will not appear on web page

#====================================================================================================================
#GPIO Config - Tether Pins (Pin 2 - 3.3V, Pin 8 - GND)
L_DIRECTION = 26    #Pin 6 - Green
M_STEP = 13         #Pin 1 - Orange/White
R_DIRECTION = 19    #Pin 5 - Blue/White
MOTOR_SW = 11       #Pin 4 - Blue, Motor relay/transistor
LIGHT_SW = 12       #Pin 3 - Green/White, Light relay/transistor
SERVO = 18          #Pin 7 - Brown/White, For camera angle

#Camera Pulsewidths
cam_dir = 1500 #Current direction of camera
CAM_CENTER = 1500 #Camera Center Pulsewidth 1500
CAM_MIN = 1000 #Camera Far Left Pulsewidth 1000
CAM_MAX = 2000 #Camera Far Right Pulsewidth 2000

pic_flag = False #Flag that is set true when photo button is pressed
pic_num = 0 #Used for picture name, will increment as pictures are saved

m_power = False #Boolean for toggling motor power relay
l_power = False #Boolean for toggling light power relay
SPEED = 2400 #Maximum motor speed of 2400 Hz (Half step)

#Initialize GPIO values
pi = pigpio.pi()
pi.set_mode(MOTOR_SW, pigpio.OUTPUT)
pi.set_mode(LIGHT_SW, pigpio.OUTPUT)
pi.set_mode(L_DIRECTION, pigpio.OUTPUT)
pi.set_mode(M_STEP, pigpio.OUTPUT)
pi.set_mode(R_DIRECTION, pigpio.OUTPUT)
pi.write(MOTOR_SW, m_power) #Motor power relay starts OFF
pi.write(LIGHT_SW, l_power) #Light power relay starts OFF
pi.hardware_PWM(M_STEP, SPEED, 0) #Start with 0% duty cycle for motors - OFF
pi.set_servo_pulsewidth(SERVO, CAM_CENTER) #Set camera servo to center to begin

app = Flask(__name__) #Initialize Flask App

#Set up camera
cam = WebcamVideoStream(src=0).start()
sleep(2) #Give camera 2 seconds to start up

#====================================================================================================================
@app.route('/')
def home():
    return render_template('home.html', drive=has_drive) #has_drive determines if photo button is shown

#====================================================================================================================
#Functions for video stream on web page
def gen():
    global cam, pic_flag, pic_num
    while True:
        frame = cam.read() #Get frame from camera success,
        if pic_flag:
            pic_name = "Picture_" + str(pic_num) + ".jpg" #Create name for picture with current time
            cv2.imwrite(os.path.join(PATH, pic_name), frame) #Save picture in directory created earlier
            pic_flag = False #Reset flag to false
            pic_num += 1 #Increment pic_num
            print(pic_name + ' saved')
        ret, buffer = cv2.imencode('.jpg', frame) #Encode image as .jpg
        frame = buffer.tobytes() #Convert frame to byte array
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

#====================================================================================================================
#Set flag to save picture, routed to camera button on web page
@app.route('/save_picture')
def save_picture():
    global pic_flag
    pic_flag = True
    return "Nothing"

#====================================================================================================================
#Functions to control the relays, each corresponds to a button on the web page
@app.route('/toggle_power')
def toggle_power():
    global m_power
    m_power = not m_power #Toggle motor power
    pi.write(MOTOR_SW, m_power) #Change state of transistor/relay
    return "Nothing"

@app.route('/toggle_light')
def toggle_light():
    global l_power
    l_power = not l_power #Toggle Light
    pi.write(LIGHT_SW, l_power) #Change state of transistor/relay
    return "Nothing"
    
#====================================================================================================================
#Move function is used every time the signals to the motor drivers need to change, each corresponds to a button on the web page
def move(l_dir, r_dir, is_stop):
    if is_stop: 
        for i in reversed(range(6)):
            pi.hardware_PWM(M_STEP, SPEED + (i * 500), 250000)  #ramp down for smoother stop
            sleep(0.01)
        pi.hardware_PWM(M_STEP, 0, 0) #stop
    else:
        pi.hardware_PWM(M_STEP, 0, 0) #stop first
        pi.write(L_DIRECTION, l_dir) #write updated directions
        pi.write(R_DIRECTION, r_dir)
        if l_dir == r_dir: #If turning, move at 70% speed for increased torque
            for i in range(6):
                pi.hardware_PWM(M_STEP, int((SPEED * 0.7) + (i * 500)), 250000) #Ramp speed up
                sleep(0.01)
        else: #moving straight - full speed
            for i in range(6):
                pi.hardware_PWM(M_STEP, SPEED + (i * 500), 250000) #Ramp speed up
                sleep(0.01)

#====================================================================================================================
#Various movement functions, each corresponds to a button on the web page
@app.route('/stop')
def stop():
    move(0, 0, 1)
    return "Nothing"

@app.route('/move_forward')
def move_forward():
    move(0, 1, 0) #Both sides forward
    return "Nothing"

@app.route('/move_reverse')
def move_reverse():
    move(1, 0, 0) #Both sides reverse
    return "Nothing"

@app.route('/move_left')
def move_left():
    move(1, 1, 0) #Right side forward, left side reverse
    return "Nothing"

@app.route('/move_right')
def move_right():
    move(0, 0, 0) #Left side forward, right side reverse
    return "Nothing"

@app.route('/cam_left')
def cam_left():
    global cam_dir
    if cam_dir <= CAM_MAX - 50:
        cam_dir += 50 #Increase servo pulsewidth by 50us
        pi.set_servo_pulsewidth(SERVO, cam_dir)
    else:
        pi.set_servo_pulsewidth(SERVO, CAM_MAX)
    return "Nothing"

@app.route('/cam_right')
def cam_right():
    global cam_dir
    if cam_dir >= CAM_MIN + 50:
        cam_dir -= 50 #Decrease servo pulsewidth by 50us
        pi.set_servo_pulsewidth(SERVO, cam_dir)
    else:
        pi.set_servo_pulsewidth(SERVO, CAM_MIN)
    return "Nothing"
#====================================================================================================================

@app.route('/pi_power')
def pi_power():
    call("sudo poweroff", shell=True) #Used to safely shutdown the Raspberry Pi from the app. The pictures saved to the USB drive will go corrupt if power is unplugged
    return "Nothing"

#====================================================================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True) #Run Flask App
    
#====================================================================================================================