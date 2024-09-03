# Sailowtech Open-CTD - Low-Tech CTD Probe

Welcome on the repository of the Sailowtech CTD Project, an affordable and open-source CTD probe tailored for scientific expeditions.
## Why this project exist ?
After all, Open source CTD probes already exists ? Indeed, there are some great projects like [Open CTD](https://github.com/OceanographyforEveryone/OpenCTD "Open CTD Project") or [CTDizzle](https://github.com/IanTBlack/CTDizzle/tree/main "CTDIzzle Project") but we wanted something more tailored for mid to long term expeditions while allowing a modularity in the embedded sensors. Therefore we aim to developp a project around a main electronic core and auxiliary cards that can be swapped depending on the research interest. For the moment, we propose a core based on a Rasperry pi Zero W and an auxilliary cards for 2 Atlas Scientific Sensors (Conductivity, Temperature, Dissolved Oxygen, pH...).

## Features 


## Hardware

The files for the hardware are located in the subdirectory called `hardware`. It mainly contains the PCB files for the different shields.

### Shields
The following shields exist:
- CTD Base
- CTD Double Isolator

### Battery
A well functioning battery is crucial to ensure that the probe is working stable.




## Software setup - with Raspberry Pi Zero 2W

### Poetry for package dependencies

Okay this is awesome, trust me.  
Yes, it's a bit like firing a bazooka to kill mosquitoes (© Alexandre pour l'expression), but it's worth it.

Quick recap: Poetry is a **packaging** and **dependency** management tool. It uses/creates **virtualenvs** to manage
said
packages.

#### Poetry installation

- Follow this: https://python-poetry.org/docs/#installing-with-the-official-installer
- Add `export PATH="/home/ctd/.local/bin:$PATH"` to your shell configuration file. (in `~/.bashrc`, add to last line)
- Check installation: `poetry --version` (you may need to reboot for this to work)

#### Poetry use

Poetry works this way (simplified, see [this](https://python-poetry.org/docs/basic-usage/)):

- Create a project: `poetry new <project_name>` (or `poetry init` if directory is already created)
- A `pyproject.toml` file will be created. It contains all the dependencies needed for the project.
- To add a dependency: `poetry add <package>`
- To install all dependencies: `poetry install`. This will create a `poetry.lock` file (if non-existent), locking all
  the libs and their versions. This file **should be added to git**!

In our case, you should:

- `git clone https://github.com/Sailowtech/Sailowtech-CTD` (or git pull)
- `poetry install`

Finally, to run the project in our environment:

- `poetry run python software/sailowtech_ctd/__main__.py`

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
