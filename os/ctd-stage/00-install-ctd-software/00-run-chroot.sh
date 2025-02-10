#!/bin/bash -e

curl -fsSL https://pyenv.run | bash
/home/ctd/.pyenv/bin/pyenv install 3.12.8 # required python version for PonyORM to work
pipx install poetry
pipx ensurepath
git clone https://github.com/Sailowtech/Sailowtech-CTD.git /home/ctd/Sailowtech-CTD
sudo chown -R ctd:ctd /home/ctd/Sailowtech-CTD
cd /home/ctd/Sailowtech-CTD
printf "# Sailowtech-CTD: install folder for poetry\nexport PATH=\"$PATH:/opt/pipx_bin\"" | sudo tee -a /home/ctd/.bashrc
/opt/pipx_bin/poetry env use 3.12.8
/opt/pipx_bin/poetry install || true