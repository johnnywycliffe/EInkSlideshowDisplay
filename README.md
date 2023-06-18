# E-Ink Slideshow Display

The E-Ink Slideshow Display (EISD) is a small, low power display that displays a series of images in sequence.

This project was designed to display some images in a well lit location isolated from an electrical socket. The hardware can be adapted based on need.

Photos can be uploaded or deleted via AP, which can be turned off to save power.

Two sets of instructions are provided, one with details and one if you just need all the steps in order.

## Sections

1. [TODOs](#todos-)
2. [How to use](#how-to-use)
3. [Hardware](#hardware)
4. [Installation](#installation)
5. [Installation explanation](#installation-verbose)
6. [Making images](#making-images)
7. [Known Issues](#known-issues)

## TODOs:

- main.py assumes AP is off, doesn't check
- Make it so AP mode isn't on at boot
- Better image file handling
- Add "AP in use" image to let user know it's active

## How to Use

Images go into ~/display-pi/images. By default, images are displayed in alphabetical order.

Once the script is running, the four buttons on the side of the display (A, B, C, D) can be used to control the display.

- A: Clears the display
- B: Advances to the next image
- C: Toggles Auto mode (Defaults to on)
- D: Turn on/off the AP

## Hardware

- Raspberry Pi 0W
- [Inky Impressions 4" 7-colour display](https://shop.pimoroni.com/products/inky-impression-4)
- SD Card, 8 GB 
- USB Micro cable, 90 degrees [Example](https://www.amazon.com/dp/B0045JHJDS?ref=ppx_yo2ov_dt_b_product_details&th=1)
- [USB power bank](https://www.amazon.com/Anker-PowerCore-Technology-High-Capacity-Compatible/dp/B07S829LBX/ref=sr_1_3?crid=3VLH6HB1MXUXX&keywords=anker+20000&qid=1677981712&sprefix=anker+20000%2Caps%2C80&sr=8-3) (Optional)
- Mouse/Keyboard/Screen for using Raspberry Pi OS with desktop (Optional)
- 3D printer (for case)

Additionally:
- A host device (laptop, android phone) capable of Wi-Fi and SSH.
- A standard Wi-Fi network (No captured portals, etc.)

### Additional options/Substitutions

- Instead of the 4" display, an [Inky Impressions 5.7" 7-colour display](https://shop.pimoroni.com/products/inky-impression-5-7) may be used instead. Presumably, the 7" display could also be used, but has not been tested.
- Instead of a Pi 0W, a 3B+ may be used. Pi 4 has not been tested.
- Instead of SSHing into the pi, a mouse, keyboard, and monitor can be used for the setup

### Hardware install

***WARNING!*** Inky screens are glass. Be careful when pressing anything into the screen, setting it down on a surface, etc. Do not remove the screen protector until final installation.

1. Solder headers onto the Pi. Ensure that the headers are straight. Don't be me.
2. If you want more room between your Pi and the screen, install standoffs:
   - Thread the standoffs into the back of the display in the four spots. Break the Kaptan tape with the thread of the standoff, the point of a knife, or just scrape it off.
   - Put the header extender on the Pi.
3. Flip over and press Pi onto the back of the screen gently.
4. If using standoffs, screw down the Pi securely.

Move on to [Installation](#installation) or [Installation w/ explanation](#installation --verbose) to program the SD card.

## Installation

1. Use Raspberry Pi imager and install the latest Raspberry Pi OS
   - Set Hostname
   - Configure WiFi
   - Configure SSH
2. Install SD card into Pi
3. SSH into Pi
4. Run apt update/upgrade + install the following:
   - `curl https://get.pimoroni.com/inky | bash`
   - `clone https://github.com/johnnywycliffe/EInkSlideshowDisplay.git` and move slideshow-display folder to ~/ 
5. Setup scripts to run at boot
   - `chmod +x main.py`
   - Add `@reboot python3 slideshow-display/main.py -r` to `crontab -e`
6. Run AP installer
7. Load images by connecting to AP

## Installation verbose

### Step 1: Setup Raspberry Pi OS

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
  - SSID: Your Wi-Fi name
  - Password: your Wi-Fi password

### Step 2: Install SD card to Pi and initial boot

Once the SD card is flashed, insert it into the Raspberry Pi and plug the Pi in via USB to your computer or power supply.

The Pi will take ~60 seconds to boot up.

### Step 3: SSH

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

### Step 4: Download software

For now, the pi is connected to the internet. Run the following commands:

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

To install the slideshow and support script:

```
mkdir temp
cd temp
git init
git clone https://github.com/johnnywycliffe/EInkSlideshowDisplay.git
mv slideshow-display/ ~/
cd ..
rm -r temp
```

For testing (linux):
- Pick 2-3 images that are distinct
- Load into a folder named "images"
- `scp -r images/ pi@display-pi.local:~/display-pi/images`

You will have to type in the password.

Once the command completes, SSH into the Pi once more.

### Step 5: Set up script and to run at boot

Now that the files are loaded onto the Pi, they need to be initialized.

```
chmod +x slideshow-display/main.py
```

To run the script, type `./slideshow-display/main.py`

There are some arguments that can be invoked:

| Arg          | Description                                                                 | Default     |
|--------------|-----------------------------------------------------------------------------|-------------|
| -h, --help   | Displays help message                                                       | N/A         |
| -d, --delay  | Adjusts the number of seconds between image changes. Minimum is 15 seconds. | 300 seconds |
| -p, --path   | Changes the path to load the images from.                                   | images/     |
| -s, --sat    | Changes the saturation of the images. Between 0-1.0                         | 0.5         |
| -r, --random | Loads pictures in a random order                                            | False       |

Once you are satisfied with the functionality of the script, set it to automatically load.

```
crontab -e
```

Choose the editor of your choice, assuming nano (1).

In the crontab file add `@reboot python3 slideshow-display/main.py` then press "ctrl+x" to close nano, then "y" to save the changes, then enter to save the cron file.

Arguments can be added after the line as normal, I.E. `@reboot python3 slideshow-display/main.py -d 30 -s 0.7`

Reboot Pi at least once to ensure crontab is properly set up before moving on.

### Step 6: Set up AP

Since this installation guide is assuming a headless install, the only way to control it is via SSH. Changing the wlan configuration will break the SSH connection, so this step is irreversible.

Make sure to edit config-files/ap_setup.conf before running the script and changing the SSID, passphrase, and static IPs if desired. These can be changed, but only if recalled and the `ap_update.sh` script is run.

```
nano ~slideshow-display/config-files/ap_setup.conf
```

Once configured, run the following:

```
chmod +x ~/slideshow-display/ap_setup.sh
chmod +x ~/slideshow-display/ap_update.sh
chmod +x ~/slideshow-display/ap_off.sh
sudo .~/slideshow-display/ap_setup.sh
```

The SSH will hang and disconnect. There are a few libraries it is installing,

#### Using Pi in GUI mode

If using the Pi with the desktop GUI, loss of the SSH can be worked around. The ap_setup.sh script doesn't need to be run, and below are the instructions to be run in order to ensure the device loads up correctly:

1. `sudo apt install dnsmasq hostapd`
2. `sudo systemctl stop dnsmasq`
3. `sudo systemctl stop hostapd`
4. `sudo nano /etc/dhcpcd.conf`
   ```
    interface wlan0
        static ip_address=192.168.4.1/24
        nohook wpa_supplicant
    ```
5. `sudo service dhcpcd restart`
6. `sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig`
7. `sudo nano /etc/dnsmasq.conf`
   ```
   interface=wlan0
   dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
   ```
8. `sudo systemctl start dnsmasq`
9. `sudo nano /etc/hostapd/hostapd.conf`
   ```
   country_code=US
   interface=wlan0
   ssid=YOURSSID
   channel=9
   auth_algs=1
   wpa=2
   wpa_passphrase=YOURPWD
   wpa_key_mgmt=WPA-PSK
   wpa_pairwise=TKIP CCMP
   rsn_pairwise=CCMP
   ```
10. `sudo nano /etc/default/hostapd`
11. Find `#DAEMON_CONF` and replace with `DAEMON_CONF="/etc/hostapd/hostapd.conf"`
12. `sudo systemctl unmask hostapd`
13. `sudo systemctl enable hostapd`
14. `sudo systemctl start hostapd`

For a breakdown of what this all means, visit [This Link](https://raspberrypi-guide.github.io/networking/create-wireless-access-point)

### Step 7: Load images/edit program

These instructions are how to connect to the display from this point forward, now that all the code is running.

To add images once the AP has been initialized:

1. Press the "D" button on the side of the device to start AP mode
   - **CAVEAT!** THe very first time the AP script is run, the AP will already be initialized. Skip step 1. 
2. Once the AP can be found, connect a computer, phone, or other device to it.
3. On the connecting device (*NOT* the Pi):
   1. Create a folder named "images" somewhere easy to find 
   2. Copy any images to be displayed into "images"
   3. `scp -r images/ pi@192.168.4.1:~/display-pi/images`
   4. Type in Pi's password
4. Press "D" button again to deactivate AP mode

To change the settings, delete pictures, or run other programs:

1. Press the "D" button on the side fo the device to start AP mode
2. Once the AP can be found, connect a computer, phone, or other device to it.
3. SSH into the Pi. `ssh pi@192.168.4.1`
4. Type in Pi's password
5. Navigate to the relevant folders as above
   1. `cd ~/slideshow-diplay/images` for images
   2. `cd ~/slideshow-diplay/config-files` to reconfigure AP
   3. `cd ~/slideshow-display/` for main script

#### Making images

The Pimoroni Impressions 4" 7-Colour E-Ink display has a resolution of 640 x 400 pixels. The code as written will squash any image in acceptable format down to fit this resolution, resulting in stretched images if source image not in the correct aspect ratio. The 5.7" screen is the same aside from the fact it has a resolution of 600 X 440.

Multicolor E-ink displays can only display one color per pixel out of the seven colors, so test the images before using the display.

It is good practice to check each image before it is slid into a full rotation to ensure it displays nicely.

## Known issues

- There is no file verification for files inside the 'images' folder.
- Auto mode doesn't clear between all images
- AP mode doesn't ever deactivate

