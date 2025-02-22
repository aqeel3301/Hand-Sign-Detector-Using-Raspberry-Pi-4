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

Open up a terminal and run the below code :

    sudo apt-get update && sudo apt-get upgrade

After this, now expand the swap file from 100 to 2048 by running this command:

    sudo nano /etc/dphys-swapfile

Then press Ctrl + X, Ctrl + Y, and then Enter key to save the changes

Then run these commands line by line and press Y for everything and proceed with the installation. 

    sudo apt-get install build-essential cmake pkg-config

    sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

    sudo apt-get install libxvidcore-dev libx264-dev

    sudo apt-get install libgtk2.0-dev libgtk-3-dev

    sudo apt-get install libatlas-base-dev gfortran

    sudo pip3 install numpy

    wget -O opencv.zip https://github.com/opencv/opencv/archive/4.4.0.zip

    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.4.0.zip

    unzip opencv.zip

    unzip opencv_contrib.zip

    cd ~/opencv-4.4.0/

    mkdir build

    cd build

    cmake -D CMAKE_BUILD_TYPE=RELEASE \

                                 -D CMAKE_INSTALL_PREFIX=/usr/local \
    
                                -D INSTALL_PYTHON_EXAMPLES=ON \

                                -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.4.0/modules \

                                -D BUILD_EXAMPLES=ON ..

    make -j $(nproc)


Now this make Command will take over an hour to complete. Be patient and let it run. 

Then run the below command again on the terminal and exit.

    sudo make install && sudo ldconfig

    sudo reboot

reboot will automatically reboot your raspberry pi and make it ready to execute and output the code.


Now i would like the personnaly thank this site to help me in running and executing the code for hand sign recognition. Without this, i wouldnt have been able to execute my code. 

The link to the website :

https://core-electronics.com.au/guides/hand-identification-raspberry-pi/


4) Now try to run the Simple-Hand-Tracker.py. If it runs without any issue, Congratulations!!. 

5) Now we will try to run the other codes.