#!/bin/bash -e

pipx install poetry
git clone https://github.com/Sailowtech/Sailowtech-CTD.git ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
cd ${ROOTFS_DIR}/home/ctd/Sailowtech-CTD
poetry install
