# Underwater-Rover Project
# Overview:
The Underwater Rover was my Capstone project for my Computer Engineering Technology Diploma. 

I designed the electronics and software for the rover, while students from the Innovative Manufacturing program at Sask Polytech created the chassis, suspension, and tracks.

This project includes a rover to explore underwater, a base station on land containing the Raspberry Pi, and tether cables to connect the rover to the base station.


# Operation:
The operator will begin by connecting their phone or tablet to the Raspberry Pi’s wireless network. An internet connection is not required. The operator will then open a web browser and access the web page. From the web page, the operator can view the webcam stream, move the rover, rotate the webcam, toggle the flashlight, take pictures, and shut down the Raspberry Pi.


# Hardware:
-Selected Raspberry Pi to run software and control the electronics  
-Selected CAT6 cables to connect electronics in rover to electronics in base station  
-Selected battery to power electronics in rover  
-Selected motors capable of driving the rover underwater, and drivers to control them  
-Selected camera to mount inside the rover  
-Selected lights for increased visibility underwater  
-Designed PCB to connect all electronics in KiCAD, produced by JLCPCB in China  
-Soldered all components to PCB  


# Software:
-Developed Python program  
&nbsp;&nbsp;&nbsp;&nbsp;-Flask framework  
&nbsp;&nbsp;&nbsp;&nbsp;-Stream camera to web page  
&nbsp;&nbsp;&nbsp;&nbsp;-Control hardware through GPIO  
-Designed basic web page to view camera and control the rover  
-Set up NGINX web server  
-Set up uWSGI application server  
-Set up HostAPD and DNSMasq to use Raspberry Pi as wireless access point  
