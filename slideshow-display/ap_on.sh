#!/usr/bin/env bash
if [ $EUID -ne 0 ]; then
    echo "Script must be run as root"
    exit
fi
tee /etc/dhcpcd.conf << END
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
END
service dhcpcd restart
systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd