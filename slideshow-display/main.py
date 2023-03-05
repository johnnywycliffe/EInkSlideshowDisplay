#!/usr/bin/env python3

import os
import time
import argparse
import RPi.GPIO as GPIO
from subprocess import call
from PIL import Image
from inky import Inky7Colour
from inky.inky_uc8159 import CLEAN

# State variables
loop = [True, 0]  # Looping var, index
# Image list
image_list = []
# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--delay', type=int, help="Length of time between changing pictures in auto mode. "
                                                    "Default is 300 seconds. Min time is 15 seconds")
parser.add_argument('-p', '--path', type=str, help="Folder containing images to display. Default is "
                                                   "'slideshow-display/images'.")
parser.add_argument('-s', '-sat', type=float, help="How deep the saturation is set on the screen. Values "
                                                   "between 0 - 1.0, default is 0.5.")
# Display init
inky = Inky7Colour()
# A, B, C, D GPIO Pins
BUTTONS = [5, 6, 16, 24]
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def handle_button(pressed_pin: BUTTONS):
    """ Handles button inputs.

    :param pressed_pin: integer of pin of button pressed
    :return: None
    """
    if pressed_pin == 5:  # Clear Screen
        print("Clearing")
        clear()
        print("Cleared")
    elif pressed_pin == 6:  # Set display to run once, quickly
        print("Next image")
        show_image(image_list)
    elif pressed_pin == 16:  # Set display to constantly loop
        if loop[0]:
            print("Auto off")
        else:
            print("Auto on")
        loop[0] = not loop[0]
    elif pressed_pin == 24:  # Shutdown Pi
        print("Shutting down")
        call("sudo shutdown --poweroff", shell=True)
        quit()
    else:
        # Something went wrong
        print("ERROR: Bad pin number entered. Somehow.")


# init buttons
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)


def clamp(num: float, min_value: float, max_value: float):
    """Clamp a value to a range"""
    return max(min(num, max_value), min_value)


def clear():
    """Clears the screen to blank"""
    for _ in range(4):
        for y in range(inky.height - 1):
            for x in range(inky.width - 1):
                inky.set_pixel(x, y, CLEAN)
        inky.show()
        time.sleep(1.0)


def get_images(directory: str, images: list):
    """ Finds all images in the specified directory

    :param directory: Directory to examine
    :param images: List to add images to
    :return: Length of list of images
    """
    if not os.path.exists(directory):
        print("Path '{}' doesn't exist!".format(directory))
        quit()
    for filename in os.listdir(directory):
        if filename == "README.md":
            continue
        path = directory + "/" + filename
        if os.path.isfile(path):
            images.append(path)
    return len(images)


def show_image(directory: list, sat: float = 0.5):
    """ Displays the image to the display and increments index

    :param directory: Directory of part
    :param sat: Saturation value
    :return: None
    """
    image = Image.open(directory[loop[1]])
    resized_image = image.resize(inky.resolution)
    inky.set_image(resized_image, saturation=sat)
    inky.show()
    loop[1] += 1
    if loop[1] >= img_list_len:
        loop[1] = 0


if __name__ == '__main__':
    print("Starting Slideshow")
    args = parser.parse_args()
    print(args)
    if args.delay:
        image_delay = args.delay
        if image_delay < 15:
            image_delay = 15
        print("Image delay set to {}".format(image_delay))
    else:
        image_delay = 300
    if args.s:
        image_sat = clamp(args.s, 0.0, 1.0)
        print("Saturation set to {}".format(image_sat))
    else:
        image_sat = 0.5
    if args.path:
        image_path = args.path
        print("Image path set to {}".format(image_path))
    else:
        image_path = "slideshow-display/images"
    # Initialize
    img_list_len = get_images(image_path, image_list)
    start_time = time.time() - float(image_delay)
    print("Number of images: {}".format(img_list_len))
    if img_list_len == 0:
        print("No images to show!")
        quit()
    while True:
        if loop[0] and time.time() > (start_time + float(image_delay)):
            show_image(image_list)
            start_time = time.time()
        else:
            time.sleep(0.1)
