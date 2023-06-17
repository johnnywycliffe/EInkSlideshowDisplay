#!/usr/bin/env bash
if [ $EUID -ne 0 ]; then
    echo "Script must be run as root"
    exit
fi
systemctl stop hostap
tee /etc/dhcpcd.conf << END
END
reboot