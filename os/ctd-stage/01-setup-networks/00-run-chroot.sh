#!/bin/bash -e

sudo systemctl disable wpa_supplicant
sudo systemctl enable iwd.service
printf "[Security]\nPassphrase=CTDCTDCTD\n\n[Settings]\nAutoConnect=true\n" | sudo tee /var/lib/iwd/CTD.psk
printf "[device]\nwifi.backend=iwd\n" | sudo tee /etc/NetworkManager/conf.d/iwd.conf || true
ls /etc/NetworkManager/conf.d/ || true