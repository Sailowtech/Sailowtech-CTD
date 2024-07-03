# Sailowtech CTD


## Use with Raspberry Pi Zero 2W

### OS Setup
Use Ubuntu Server 22.04, 64bit, for Ansible compatibility. Also possible to try with 24.04.
For the installation, use the Raspberry Pi Imager. Set username to `ctd` and set appropriate password. Activate SSH. Set connection to a WiFi with SSID and password. This can be a mobile hotspot so that you can connect on the way.

### Installation
We use Ansible to install everything. You must be connected to the same network and have ansible installed.
In case the upgrade procedure fails over Ansible, redo this over SSH directly with `sudo apt upgrade`
