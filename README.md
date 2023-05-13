# E-Ink Slideshow Display

The E-Ink Slideshow Display (EISD) is a small, low power display that displays a series of images in sequence.

This project was designed to display some images in a well lit location isolated from an electrical socket. The hardware can be adapted based on need.

## Hardware

Necessary:
- Raspberry Pi 3B+ (Pi 0 will also work, not tested with Pi 4)
- [Inky Impressions 5.7" 7-colour display](https://shop.pimoroni.com/products/inky-impression-5-7)
- SD Card, 8 GB 
- ***OR***
- [Inky Impressions 4" 7-colour display](https://shop.pimoroni.com/products/inky-impression-4)
- [20 x 2 header extender](https://core-electronics.com.au/2x20-socket-riser-header-for-raspberry-pi-hats-and-bonnets.html) (Should be included)
- USB Micro cable, 90 degrees [Example](https://www.amazon.com/dp/B0045JHJDS?ref=ppx_yo2ov_dt_b_product_details&th=1)
- 3D printer (for case)
- [USB power bank](https://www.amazon.com/Anker-PowerCore-Technology-High-Capacity-Compatible/dp/B07S829LBX/ref=sr_1_3?crid=3VLH6HB1MXUXX&keywords=anker+20000&qid=1677981712&sprefix=anker+20000%2Caps%2C80&sr=8-3)
- Mouse/Keyboard/Screen for using Raspberry Pi OS with desktop

### Hardware install

***WARNING!*** Inky screens are glass. Be careful when pressing anything into the screen, setting it down on a surface, etc. Do not remove the screen protector until final install.

Thread the standoffs into the back of the display in the four spots. Break the Kaptan tape with the thread of the standoff, the point of a knife, or just scrape it off.

Put the header extender on the Pi, then flip over and press onto the back of the screen gently. The standoffs should line up with the holes in the Pi. Screw the Pi down to secure it.

Once the SD Card is programmed, insert it into the SD Card slot, and then power the Pi up by plugging in the power cable.

See the Case folder for how to assemble the case.

## Making images

The Pimoroni Impressions 5.7" 7-Colour E-Ink display has a resolution of 600 x 448 pixels. The code as written will squash any image down to fit this resolution, resulting in stretched looking images if that are not in the correct aspect ratio. The 4" screen is the same aside from the fact it has a resolution of 640 X 400.

Multi-color E-ink displays can only display one color per pixel out of the seven colors, so test the images before using the display.

## Installation

### Pi setup

This tutorial assumes a headless Raspberry Pi plugged into a linux computer with SSH installed. On windows, PuTTY can be used.

Install Raspberry Pi OS Lite by following the instructions [Here](https://www.raspberrypi.com/software/).

Recommended Options:
- Operating System: Raspberry Pi OS Lite
- Set Hostname: "display-pi" or to taste (Tutorial assumes 'display-pi')
- Enable SSH
- Set username and password
  - Username: "pi" or to taste (Tutorial assumes 'pi')
  - Password: An easy to remember password
- Configure wireless LAN
  - SSID: Your wifi name
  - Password: your wifi password

Once the SD card is flashed, insert it into the Raspberry Pi and plug the Pi in via USB to your computer.

The Pi will take ~15 seconds to boot up.

Open a terminal window and type the following:

```
ssh pi@display-pi.local
```

If the output looks like this:

```
ssh: Could not resolve hostname display-pi.local: Name or service not known
```

Wait a few more seconds and try again, the pi may still be booting. If it still doesn't work after a few more seconds, you will hav to diagnose the connection issue.

You may have to approve a certificate. Type "yes" to save the certificate to your system.

If you are greeted with a prompt like this:

```console
pi@display-pi:~$
```

You have successfully logged into the Pi.

### Install

If you haven't logged into the Pi, log in. Ensure the Pi is connected to the internet. Call the following commands to install the modules for the 7 color E-ink display.

```
sudo apt-get update
sudo apt-get upgrade
curl https://get.pimoroni.com/inky | bash
```

To verify install, run:

```
cd /home/pi/Pimoroni/inky/examples/7color
ls
```

and check that the folder has a few example python scripts. Run `python3 stripes.py --type 7colour` to verify the screen works as intended. Once completed, run `python3 clear.py --type 7colour` to clear the screen back to blank. 

The screen may have ghosting. Run the clear command a few more times if you like to reduce this.

Once installed, type `exit`to return to the default terminal. Run the following commands:

```
mkdir slideshow-display
cd slideshow-display
git init
git clone https://github.com/johnnywycliffe/EInkSlideshowDisplay.git
```

Look into the "slideshow-display" directory. Load any images you have prepared into the "images" directory, and then run the following command:

```
scp -r slideshow-display/ pi@display-pi.local:~/
```

You will have to type in the password.

Once the command reports success: 

```
ssh pi@display-pi.local
cd slideshow-display/
chmod +x main.py
```

The script is now installed. See the sections below to see how to use the script and how to have the script run on boot.

## How to use

To run the script, type `./slideshow-display/main.py`

By default, images are displayed in alphabetical order.

There are some arguments that can be invoked:

| Arg | Description | Default |
| --- | ----------- | ------- |
| -h, --help | Displays help message | N/A |
| -d, --delay | Adjusts the number of seconds between image changes. Minimum is 15 seconds. | 300 seconds |
| -p, --path | Changes the path to load the images from. | images/ |
| -s, --sat | Changes the saturation of the images. Between 0-1.0 | 0.5 |
| -r, --random | Loads pictures in a random order | False |

Once the script is running, the four buttons on the side of the display (A, B, C, D) can be used to control the display.

- A: Clears the display
- B: Advances to the next image
- C: Toggles Auto mode (Defaults to on)
- D: Shutdown device

Please give the Pi two minutes to power down before unplugging it.

## Run automatically at boot

Once you are satisfied with the functionality of the script, set it to automatically load.

Once SSH'd into the Pi:

```
crontab -e
```

Choose the editor of your choice, assuming nano (1).

In the crontab file add `@reboot python3 slideshow-display/main.py` then press "ctrl+x" to close nano, then "y" to save the changes, then enter to save the cron file.

Arguments can be added after the line as normal, I.E. `@reboot python3 slideshow-display/main.py -d 30 -s 0.7`

## Known issues

- There is no file verification for files inside of the images folder.

