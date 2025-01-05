#!/bin/bash -e

sudo systemctl disable wpa_supplicant
sudo systemctl enable NetworkManager.service
sudo cat /etc/network/interfaces || true
nmcli device wifi connect CTD password CTDCTDCTD || true
sudo ls /etc/NetworkManager/system-connections/ || true