#!/bin/bash -e

curl -fsSL https://pyenv.run | sudo -u ctd bash
sudo -u ctd /home/ctd/.pyenv/bin/pyenv install 3.12.8 # required python version for PonyORM to work
pipx install poetry
git clone https://github.com/Sailowtech/Sailowtech-CTD.git /home/ctd/Sailowtech-CTD
sudo chown -R ctd:ctd /home/ctd/Sailowtech-CTD
cd /home/ctd/Sailowtech-CTD
printf "# Sailowtech-CTD: install folder for poetry\nexport PATH=\"$PATH:/opt/pipx_bin\"" | sudo tee -a /home/ctd/.bashrc
/opt/pipx_bin/poetry env use /home/ctd/.pyenv/versions/3.12.8/bin/python3
/opt/pipx_bin/poetry install || true