#!/bin/bash -e


pipx install poetry
pipx ensurepath
git clone https://github.com/Sailowtech/Sailowtech-CTD.git /home/ctd/Sailowtech-CTD
cd /home/ctd/Sailowtech-CTD
/root/.local/bin/poetry install || true