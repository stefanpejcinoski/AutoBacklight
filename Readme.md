# Auto Backlight

AutoBacklight is a Python script for automatic adjustment of the LCD screen backlight intensity of a laptop, 
using the webcam as a light level sensor. 
The aim of the program is to keep the backlight as low as possible while maintaining user comfort.
Since what is considered comfortable to use is user dependant, there will be a method to adjust the response
curve of the script, right now it's linear (y=ax+b) where y is backlight level x is camera light level, a is 1/2.5 and b can be adjusted by editing the script.
The script will automatically detect if an external monitor is connected or if the screen is off after a long time being idle and it will not run. This feature is available only on the Linux version as of now.

# DISCLAIMER

The project is still in it's very early stages,
there is no automated installation, no user configurable parameters and no GUI. It's untested on Windows and works on Linux but only on 
distributions that have the GNOME desktop enviroment, since it relies on GNOME DBus calls 
to read and set the backlight level. 

This version of the script can work both with LCD and OLED diplay laptops, although only LCDs will see any sort of difference in power consumption, since they have an actual backlight.

# Installation

The script was made on a system running Python 3.7, if you don't have it already I recommend that you install Python 3.7 or above.

The script uses OpenCV to capture images from the webcam and Numpy to process the data, so you need to have them installed. 

Run the following commands in Terminal/Command Line after you've installed Python:

```bash
pip install opencv-python
pip install numpy
pip install schedule
```
Note that in order for these to work you need to have Python added to your path, most installation guides have this covered already.

## Linux

Clone the repository on your system: 

```bash
git clone https://github.com/stefanpejcinoski/AutoBacklight
```

Make an install directory to keep the script and stop and config (in the future) files:

```bash
mkdir ~/.AutoBacklight
```
Note that the directory you choose is completely up to you, there is no need to put it in the home folder specifically or even to place it in a subdirectory, wherever you want is fine.

You can choose to not use a hidden directory (don't place the '.' in front of the folder name), but that way it's easier to accidentally delete or modify something and break the install.

The Linux script is located in the "background-script-linux" directory. 
Move the script to the new install directory: 

```bash
cp autoBacklight.py ~/.AutoBacklight/autoBacklight.py
```
Run the script like this 
```bash
python /path-to-script/script.py & disown
```
disown will detach the process from the terminal window and you can safely close the window,
for persistance on boot the script can be added to cron on reboot using 
`@reboot  /usr/bin/python /path-to-script/script.py`
## Windows

I do not recommend installing the Windows script since it's untested and might not even work.
If you want to test it, it's better to just run it manually from the command line:

```
python \path-to-script\autoBacklight.py
```

Note that in order for these to work you need to have Python installed and added to your path, there are a plenty of guides on how to do this.

If you still wish to install, do as follows:

Make an installation directory (anywhere is fine) and copy the script located in "background-script-windows-untested" to it.

Use the Windows task scheduler to create an automated task with a frequency that you choose (I recommend 2 minutes),  to run the python interpreter with this script as an argument. I currently do not have a machine with Windows to install and test the script on to, but you can find instructions on how to use the task scheduler online.

The script is untested on Windows, it may run fine or it may not run at all. For now it lacks external monitor and sleep detection.

# Uninstallation
## Linux

Remove the cron job you created:

```bash
export VISUAL=nano
crontab -e
```

Find and remove the line you added during installation and save the file with Ctrl+O, and exit with Ctrl+X (if you chose to use nano).

Delete the install directory that you created:

```bash
rm -r ~/.AutoBacklight
```
replace "~/.AutoBacklight" with your install path, if you chose differently. 

## Windows

Remove the task you added to the Task Scheduler and 
delete the install directory that you created.

# Usage

There is no user intervention needed for this script, it runs in the backround with the interval
that you set in the cron file or task scheduler
If you wish to stop the script from running temporarily, create a file called stop (no extension) in the same directory as the script. To continue the script just delete this file.

# Contributing

Pull requests are welcome.
Feel free to modify and improve on the code as much as you wish.
