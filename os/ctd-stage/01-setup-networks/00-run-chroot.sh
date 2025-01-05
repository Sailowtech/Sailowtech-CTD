#!/bin/bash -e

sudo wpa_passphrase "CTD" "CTDCTDCTD" || sudo tee /etc/wpa_supplicant/wpa_supplicant.conf
