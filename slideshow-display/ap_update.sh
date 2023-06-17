#!/usr/bin/env bash
if [ $EUID -ne 0 ]; then
    echo "Script must be run as root"
    exit
fi
source /home/$SUDO_USER/slideshow-display/config-files/ap_setup.conf
if [ x"${SSID}" == "x" ]; then
    echo "SSID not set! Set in ap_setup.conf"
    exit
fi
if [ x"${PASS}" == "x" ]; then
    echo "PASS not set! Set in ap_setup.conf"
    exit
fi
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
tee /etc/dhcpcd.conf << END
interface wlan0
    static ip_address=$STATIC_IP/$CIDR
    nohook wpa_supplicant
END
sudo service dhcpcd restart
tee /etc/dnsmasq.conf << END
interface=wlan0
dhcp-range=$IP_RANGE_LOW,$IP_RANGE_HIGH,$NETMASK,24h
END
sudo systemctl start dnsmasq
tee /etc/hostapd/hostapd.conf << END
country_code=$COUNTRY
interface=wlan0
ssid=$SSID
channel=9
auth_algs=1
wpa=2
wpa_passphrase=$PASS
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
END
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd