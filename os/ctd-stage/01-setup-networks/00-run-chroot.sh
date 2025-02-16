#!/bin/bash -e



printf "nmcli con delete CTD-AP\nnmcli con add type wifi ifname wlan0 mode ap con-name CTD-AP ssid CTD autoconnect true\nnmcli con modify CTD-AP 802-11-wireless.band bg\nnmcli con modify CTD-AP 802-11-wireless.channel 3\nnmcli con modify CTD-AP ipv4.method shared ipv4.address 192.168.42.1/24\nnmcli con modify CTD-AP ipv6.method disabled\nnmcli con modify CTD-AP wifi-sec.key-mgmt wpa-psk\nnmcli con modify CTD-AP wifi-sec.psk \"CTDCTDCTD\"\nnmcli con up CTD-AP\n" | sudo tee /opt/nmcli-ctd-ap.sh


echo "@reboot sh /opt/nmcli-ctd-ap.sh" | sudo tee /opt/cron
echo "@reboot timedatectl set-ntp false" | sudo tee -a /opt/cron
sudo crontab /opt/cron
sudo systemctl enable NetworkManager
sudo systemctl disable dhcpcd || true
sudo systemctl disable dnsmasq || true
sudo systemctl disable hostapd || true