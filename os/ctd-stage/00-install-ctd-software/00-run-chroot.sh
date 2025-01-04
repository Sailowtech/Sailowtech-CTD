#!/bin/bash -e

sudo pipx install poetry || true
sudo pipx ensurepath
pipx install poetry || true
pipx ensurepath || true
git clone https://github.com/Sailowtech/Sailowtech-CTD.git ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
cd ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
/root/.local/bin/poetry install || true
