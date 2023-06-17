#!/usr/bin/env bash
source config-files/ap_setup.conf # Load config file

# From https://stackoverflow.com/questions/50413579/bash-convert-netmask-in-cidr-notation
netmask_to_CIDR () {
   bits=0
   x=0$( printf '%o' ${1//./ } )
   while [ $x -gt 0 ];
   do
      let bits+=$((x%2)) 'x>>=1'
   done
   echo "$bits";
}
netmask_to_CIDR "$NETMASK"
CIDR=$bits

sudo apt install dnsmasq hostapd  # Install required programs
sudo systemctl stop dnsmasq       # Stop both new systems
sudo systemctl stop hostapd

# Set up static IP
tee -a /etc/dhcpcd.conf << END
interface wlan0
    static ip_address=$STATIC_IP/$CIDR
    nohook wpa_supplicant
END
sudo service dhcpcd restart

# Configure DHCP server
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
tee -a /etc/dnsmasq.conf << END
interface=wlan0
dhcp-range=$IP_RANGE_LOW,$IP_RANGE_HIGH,$NETMASK,24h
END
sudo systemctl start dnsmasq

# Configure AP Host
tee -a /etc/hostapd/hostapd.conf << END
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
tee -a /etc/default/hostapd << END
DAEMON_CONF="/etc/hostapd/hostapd.conf"
END

# Start AP
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd