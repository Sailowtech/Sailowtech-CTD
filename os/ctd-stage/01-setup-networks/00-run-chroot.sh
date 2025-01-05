#!/bin/bash -e

sudo systemctl disable wpa_supplicant
sudo systemctl enable iwd.service
printf "[Security]\nPassphrase=CTDCTDCTD\n\n[Settings]\nAutoConnect=true\n" | sudo tee /var/lib/iwd/CTD.psk