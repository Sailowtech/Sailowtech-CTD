#!/bin/bash -e

sudo systemctl disable wpa_supplicant
sudo systemctl enable iwd.service
sudo mkdir /var/lib/iwd
printf "EnableNetworkConfiguration=true\n" | sudo tee /etc/iwd/main.conf
printf "[device]\nwifi.backend=iwd\n" | sudo tee /etc/NetworkManager/conf.d/iwd.conf
sudo mkdir -p /var/lib/iwd/ap/
printf "[Security]\nPassphrase=CTDCTDCTD\n\n[IPv4]\nAddress=192.168.42.1\nGateway=192.168.42.1\nNetmask=255.255.255.0\nDNSList=9.9.9.9" | sudo tee /var/lib/iwd/ap/CTD.ap

sudo iw dev wlan0 interface add ap0 type __ap
sudo ip link set dev ap0 address b8:27:eb:00:00:00
sudo systemctl restart iwd
sudo iwctl device ap0 set-property Mode ap
sudo iwctl ap ap0 start-profile CTD

# printf "[Security]\nPassphrase=CTDCTDCTD\n\n[Settings]\nAutoConnect=true\n" | sudo tee /var/lib/iwd/CTD.psk
