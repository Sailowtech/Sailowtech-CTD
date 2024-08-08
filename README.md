# Sailowtech CTD
Welcome on the repository of the Sailowtech CTD Project, an affordable and open-source CTD probe tailored for scientific expeditions.
## Why this project exist ?
After all, Open source CTD probes already exists ? Indeed, there are some great projects like [Open CTD](https://github.com/OceanographyforEveryone/OpenCTD "Open CTD Project") or [CTDizzle](https://github.com/IanTBlack/CTDizzle/tree/main "CTDIzzle Project") but we wanted something more tailored for mid to long term expeditions while allowing a modularity in the embedded sensors. Therefore we aim to developp a project around a main electronic core and auxiliary cards that can be swapped depending on the research interest. For the moment, we propose a core based on a Rasperry pi Zero W and an auxilliary cards for 2 Atlas Scientific Sensors (Conductivity, Temperature, Dissolved Oxygen, pH...).

## Sailowtech

## Features 

# TODO cleanup this

Install poetry : https://python-poetry.org/docs/#installing-with-the-official-installer
In home :
curl -sSL https://install.python-poetry.org | python3 -
Add `export PATH="/home/ctd/.local/bin:$PATH"` to your shell configuration file. (in ~/.bashrc, add to last line)
Check install : poetry --version

git clone https://github.com/Sailowtech/Sailowtech-CTD

poetry install

poetry run python software/sailowtech_ctd/__main__.py

## Use with Raspberry Pi Zero 2W

### Poetry for package dependencies

To add a package, open a terminal and type
`poetry add <package>`

To build the requirement file, open a terminal and type
`poetry export --without-hashes --format=requirements.txt > ./software/ctd-collector/requirements.txt`

### OS Setup

Use the newest Raspian. For the installation, use the Raspberry Pi Imager. Set username to `ctd` and set appropriate
password. Activate SSH. Set connection to a WiFi with SSID and password. This can be a mobile hotspot so that you can
connect on the way.

### Installation

To install, you can pull the repository on the Raspberry or push it over with SCP.

On the Raspberry Pi, also install Litecli if you want to view the SQLite-File directly: `sudo apt install litecli`

### Get the ms5837.py file

Copy the file `ms5837.py` from Bluerobotics and place it in the main directory of the tool, that is `ctd-collector/`
You can get it from https://raw.githubusercontent.com/bluerobotics/ms5837-python/master/ms5837/ms5837.py
