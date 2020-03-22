# Auto Backlight

AutoBacklight is a Python script for automatic adjustment of the LCD screen backlight intensity of a laptop, 
using the webcam as a light level sensor. 
The aim of the program is to keep the backlight as low as possible while maintaining user comfort.
Since what is considered comfortable to use is user dependant, there will be a method to adjust the response
curve of the script, right now it's linear (y=ax+b) where y is backlight level x is camera light level, a is 1/2.5 and b can be adjusted by editing the script.

# DISCLAIMER

The project is still in it's very early stages, this is literally the first working version.
There is no automated installation, it's untested on Windows and works on Linux but only on 
distributions that have the GNOME desktop enviroment, since it relies on gnome DBus calls 
to change brightness.

Currently it is envisioned to work only on laptops with LCD panels since those have a backlight 
and keeping it as low as possible will increase battery life. 
Support for OLED panels might be something that will be considered in the future, although since
they don't have a backlight, no power will be saved by keeping it low.


# Installation

The script uses OpenCV to capture images from the webcam and Numpy to process the data, so you need to have them installed 

Run the following commands in Terminal/Command Line

```bash
pip install python-opencv
pip install numpy
```

## Linux

Clone the repository on your system 

```bash
git clone https://github.com/stefanpejcinoski/automaticBacklight
```
Add a cron job to run the script every 2 minutes (you can play around with the time interval if you wish)

open your cron file for editing (i prefer nano as an editor, but you can use vim if you want)

```bash
export VISUAL=nano
crontab -e
```

Add this line to the end of your cron file, replace path-to-script with the path to the autoBacklight script
 
 ```
* */2 * * * * /usr/bin/python /path-to-script/autoBacklight.py
```
## Windows

Use the Windows task scheduler to create an automated task every 1/2/3...whatever minutes to run the python interpreter with this script as an argument. I currently do not have a machine with Windows to install and test the script on to, but you can find instructions on how to use the task scheduler online.

# Usage

There is no user intervention needed for this script, it runs in the backround with the interval
that you set in the cron file or task scheduler

# Contributing
Feel free to modify and improve on the code as much as you wish.
