#!/bin/bash -e

sudo pipx install poetry --global || true
sudo pipx ensurepath
git clone https://github.com/Sailowtech/Sailowtech-CTD.git ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
cd ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
poetry install || true
