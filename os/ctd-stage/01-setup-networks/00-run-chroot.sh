#!/bin/bash -e

printf "interface wlan0\n\t\tstatic ip_address=192.168.42.1/24\n\t\tnohook wpa_supplicant\n" | sudo tee /etc/dhcpcd.conf
printf "interface=wlan0\ndhcp-range=192.168.42.2,192.168.42.20,255.255.255.0,24h\n" | sudo tee /etc/dnsmasq.conf

sudo mkdir -p /etc/hostapd/

printf "country_code=CH\ninterface=wlan0\nssid=CTD\nchannel=9\nauth_algs=1\nwpa=2\nwpa_passphrase=CTDCTDCTD\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP CCMP\nrsn_pairwise=CCMP\n" | sudo tee /etc/hostapd/hostapd.conf
printf "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"" | sudo tee -a /etc/default/hostapd

sudo systemctl enable dhcpcd
sudo systemctl enable dnsmasq
sudo systemctl enable hostapd