# Auto Brightness

Auto Brightness is a Python script for automatic adjustment of the backlight intensity of a laptop, 
using the webcam as a light level sensor.

# DISCLAIMER

The project is still in it's very early stages, this is literally the first working version.
There is no automated installation, it only works on Linux and only on distributions that
have the GNOME desktop enviroment, since it relies on gnome DBus calls to change brightness


## Installation

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

Add this line to the end of your cron file, replace path-to-script with the path to the autoBacklight folder
 
 ```
* */2 * * * * /usr/bin/python /path-to-script/autoBacklight.py
```

## Usage

There is no user intervention needed for this script, it runs in the backround with the interval
that you set in the cron file

## Contributing
Feel free to modify and improve on the code as much as you wish.
