#!/bin/bash -e

pipx install poetry
sudo pipx ensurepath --global
git clone https://github.com/Sailowtech/Sailowtech-CTD.git ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
cd ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
poetry install
