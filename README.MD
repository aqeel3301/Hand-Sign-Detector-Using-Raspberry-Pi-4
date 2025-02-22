Hand Sign Detector using Raspberry Pi 4.

This readme will tell you all about the things you have to do inorder to make this thing work in a raspberry pi 4.

Requirements: 
Raspberry Pi 4,
USB webcam,
Micro SD,
Sd card reader,
Laptop,
Ethernet Cable,
USB A to USB C cable,

Softwares used:
Putty,
Real VNC Viewer,
Raspberry Pi OS flasher


First of all, this code is trivial and very basic, and uses libraries like open cv, mediapipe. 

Secondly, this code was tested in the older OS, Raspberry Pi Buster OS. I dont know why, but the refrence page we used used the buster os instead of the new bullseye/ bookworm version. It has to do with OPEN-CV not working properly with the newer OS of raspberry pi. 

Also this wasnt tested on the newer raspberry pi 5. We dont know if it works or not, as we only had the pi 4. If you have the pi 5, you can clone it and test it.

Download link for the buster os version :
https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/

Steps to make this work:
1) Make sure you flash the correct Buster OS in the raspberry pi.
2) After flashing it, open up a terminal and copy these code one by one and press Y in each iteration. 

sudo pip3 install mediapipe-rpi3

sudo pip3 install mediapipe-rpi4

sudo pip3 install gtts

sudo apt install mpg321

(If any error pops up, try 
sudo pip install numpy --upgrade --ignore-installed
sudo pip3 install numpy --upgrade --ignore-installed)


3) Setting Up Open-CV on Raspberry Pi 'Buster' OS


4) Now try to run the Simple-Hand-Tracker.py. If it runs without any issue, Congratulations!!. 
