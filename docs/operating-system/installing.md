# Installation and Setup

It is assumed that a working CTD with a **Raspberry Pi Zero 2 W** is used for this setup.

## Download Image
The OS-images are automatically built for each release. Download the image (the file starting with *image*) of the latest release on the [Release Page](https://github.com/Sailowtech/Sailowtech-CTD/releases/).

Then, unpack the zip-file that was downloaded.

## Flash the image
The image needs to be flashed onto the SD-Card of the Raspberry Pi.
You can use one of those tools, for example:

- RPI-Imager: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)
- Balena Etcher: [https://etcher.balena.io/](https://etcher.balena.io/)
- DD: [https://wiki.archlinux.org/title/Dd](https://wiki.archlinux.org/title/Dd)

Flash the downloaded *.img* file to the SD-Card by following the instructions of the tool you chose.

## Prepare Hotspot
Prepare a Hotspot (WiFi-Network) with SSID `CTD` and password `CTDCTDCTD`. The CTD will automatically connect to it.

## Start the CTD and log in
 Plug in the SD-Card into the Raspberry Pi and start it. It will boot automatically and connect to the `CTD`-Hotspot.
 A IP address should be assigned (DHCP). Find the IP (for example over hotspot settings or `netdiscover`).
 Note that you can also try to use the hostname `sailowtech-ctd.local` instead of the IP-address

Then, connect over SSH with user `ctd` and password `ctd`:

`ssh ctd@sailowtech-ctd.local`

## Change passwords

Ideally, you should change the credentials of the `ctd`-user and also use another password for the hotspot.

The hotspot-password used in the connection attempt can be changed in `/var/lib/iwd/CTD.psk`
