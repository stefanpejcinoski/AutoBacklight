import cv2
import os
import time
import numpy as np

# Constant used to calibrate the brightness calculation,
# reduce if brightness is too low or increase if too high
brightness_calibration_constant: float = -2.5

# Value by which the brightness is being incremented during multiple iterations, to avoid a
# sudden bright flash of the screen or a sudden darkening, raise if transition from dark to bright
# or bright to dark is too slow or lower if it is too fast
brightness_increment: int = 1

# Constant used in the calculation of the brightness, testing showed this should not be modified
brightness_multiplier: float = 1 / 2.5

# Constant used to define the camera location to the script
webcam_location_constant: int = 0

# Constant defining the amount of time in seconds the loop will pause between two consecutive changes in brightness
# decrease to speed up the transition or increase to slow it down
loop_sleep_constant: float = 0.025


def change_brightness(value):
    current_brightness_value_returned = os.popen(
        'gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power '
        '--method org.freedesktop.DBus.Properties.Get org.gnome.SettingsDaemon.Power.Screen Brightness').read()
    current_brightness_value = int(''.join(filter(str.isdigit, current_brightness_value_returned)))
    if current_brightness_value < value:
        brightness_increment_multiplier = 1
    elif current_brightness_value > value:
        brightness_increment_multiplier = -1
    else:
        return
    while True:
        current_brightness_value = current_brightness_value + (brightness_increment_multiplier * brightness_increment)
        os.system(
            'gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power '
            '--method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 '
            + str(
                current_brightness_value) + '>"')
        time.sleep(loop_sleep_constant)
        if current_brightness_value == value:
            break


def check_prerequisites():
    if os.path.isfile(os.path.join(os.getcwd(), "stop")):
        return False
    if "On" not in os.popen("cat /sys/class/drm/card0/*eDP*/dpms").read():
        return False
    if "disconnected" not in os.popen("cat /sys/class/drm/card0/*HDMI*/status").read():
        return False
    return True


def main():
    if not check_prerequisites():
        raise Exception("Prerequisites check failed")

    camera = cv2.VideoCapture(webcam_location_constant)

    if not camera.open(0):
        raise Exception("Can't open camera")

    ret, frame = camera.read()
    camera.release()
    avg = np.average(frame)
    value = np.uint32(np.round(avg * brightness_multiplier - brightness_calibration_constant))
    change_brightness(value)


if __name__ == '__main__':
    main()
