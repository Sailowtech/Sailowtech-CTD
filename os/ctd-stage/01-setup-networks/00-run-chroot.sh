#!/bin/bash -e

sudo wpa_passphrase "CTD" "CTDCTDCTD" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
