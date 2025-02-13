#!/bin/bash -e

curl -fsSL https://pyenv.run | sudo -u ctd bash
sudo -u ctd /home/ctd/.pyenv/bin/pyenv install 3.12.8 # required python version for PonyORM to work
pipx install poetry
git clone https://github.com/Sailowtech/Sailowtech-CTD.git /home/ctd/Sailowtech-CTD
sudo chown -R ctd:ctd /home/ctd/Sailowtech-CTD
cd /home/ctd/Sailowtech-CTD
printf "# Sailowtech-CTD: install folder for poetry\nexport PATH=\"$PATH:/opt/pipx_bin\"" | sudo tee -a /home/ctd/.bashrc
sudo -u ctd /opt/pipx_bin/poetry env use /home/ctd/.pyenv/versions/3.12.8/bin/python3
sudo -u ctd /opt/pipx_bin/poetry install

(printf "[Unit]\nDescription=Sailowtech-CTD Web Service\n\n[Service]\nAmbientCapabilities=CAP_NET_BIND_SERVICE\nUser=ctd\nGroup=ctd\nExecStart=" && poetry env list --full-path | grep -Po ".* " | sed 's/.$//' | sed 's/$/\/bin\/web/' && printf "\n[Install]\nWantedBy=multi-user.target\n") | sudo tee /etc/systemd/system/sailowtech-ctd-web.service
sudo systemctl enable sailowtech-ctd-web

cd /home/ctd/Sailowtech-CTD/software/sailowtech-ctd-frontend/
sudo -u ctd npm install
sudo -u ctd npm run build