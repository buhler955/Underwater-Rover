# Underwater-Rover Project
# Overview:
The Underwater Rover was my Capstone project for my Computer Engineering Technology Diploma. 

I designed the electronics and software for the rover, while students from the Innovative Manufacturing program at Sask Polytech created the chassis, suspension, and tracks.

This project includes a rover to explore underwater, a base station on land containing the Raspberry Pi, and tether cables to connect the rover to the base station.

This picture shows the base station and chassis provided. Tracks were unable to be manufactured due to COVID-19 restrictions.
<img src="https://github.com/buhler955/Underwater-Rover/blob/main/Pictures/overview.jpg" width="100%" height="auto">

Here is a screenshot of the CAD file for the tracks and suspension.
<img src="https://github.com/buhler955/Underwater-Rover/blob/main/Pictures/tracks_cad.jpg" width="100%" height="auto">

# Operation:
The operator will begin by flipping the killswitch on for the battery in the rover and turning on the battery bank for the Raspberry Pi. All of the required software runs at boot on the Raspberry Pi. Then the operator connects their phone or tablet to the Raspberry Pi’s wireless network. An internet connection is not required. The operator will then open a web browser and access the web page. From the web page, the operator can view the webcam stream, move the rover, rotate the webcam, toggle the flashlight, take pictures, and shut down the Raspberry Pi. Pictures are saved to a USB drive.


# Hardware:
-Selected Raspberry Pi to run software and control the electronics  
-Selected CAT6 cables to connect electronics in rover to electronics in base station  
-Selected battery to power electronics in rover  
-Selected motors capable of driving the rover underwater, and drivers to control them  
-Selected camera to mount inside the rover  
-Selected lights for increased visibility underwater  
-Designed PCB to connect all electronics in KiCAD, produced by JLCPCB in China  
-Soldered all components to PCB  

Here is a close-up picture of the PCB.
<img src="https://github.com/buhler955/Underwater-Rover/blob/main/Pictures/pcb.jpg" width="100%" height="auto">

Here is a close-up picture of the base station.
<img src="https://github.com/buhler955/Underwater-Rover/blob/main/Pictures/base_station.jpg" width="100%" height="auto">

Here is a picture of the electronics connected inside the chassis.
<img src="https://github.com/buhler955/Underwater-Rover/blob/main/Pictures/inside.jpg" width="100%" height="auto">

# Software:
-Developed Python program  
&nbsp;&nbsp;&nbsp;&nbsp;-Flask framework  
&nbsp;&nbsp;&nbsp;&nbsp;-Stream camera to web page  
&nbsp;&nbsp;&nbsp;&nbsp;-Control hardware through GPIO  
-Designed basic web page to view camera and control the rover  
-Set up NGINX web server  
-Set up uWSGI application server  
-Set up HostAPD and DNSMasq to use Raspberry Pi as wireless access point  

This is a screenshot of the web page on a Samsung Galaxy S20. The camera stream is shown in the center of the page.
<img src="https://github.com/buhler955/Underwater-Rover/blob/main/Pictures/webpage.jpg" width="100%" height="auto">
