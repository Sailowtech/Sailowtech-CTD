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

## Start the CTD, connect to the access point and log in
Plug in the SD-Card into the Raspberry Pi and start it. It will boot automatically and start an access point with the SSID `CTD`
Connect to this access point with password `CTDCTDCTD`. 

Then, connect over SSH with user `ctd` and password `ctd`:

`ssh ctd@192.168.42.1`

## Change passwords
Ideally, you should change the credentials of the `ctd`-user and also use another password for the access point.

The AP-password used can be changed in `/etc/hostapd/hostapd.conf`

## Setup internet access (if needed)
In case internet access is needed from the Raspberry Pi, you can set it up (with linux device as the other device, we'll call client).
1. Check which ip-address is assigned by the Raspberry Pi to the AP-client with `ifconfig` (for example: 192.168.42.4)
2. Enable IPv4-forwarding on client: `echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward`
3. Set up iptables, replace `eth0` with name of interface with internet access and `wlan0` with name of interface connected to the Raspberry Pi
   1. `sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`
   2. `sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT`
4. Then, on the Raspberry Pi, add the route: `sudo ip route add default via 192.168.42.4` (adapt IP-address if required)
5. Add nameserver: `echo "nameserver 9.9.9.9" | sudo tee /etc/resolv.conf`

## Running the software

1. Connect to the Raspberry Pi
2. Change to the correct directory: `cd Sailowtech-CTD`
3. Start the webserver: `poetry run web`

It will then be reachable over: http://192.168.42.1:8000

Start measurements over http://192.168.42.1:8000/run?measurements=100 where the last number is the amount of measurements

Then http://192.168.42.1:8000/csv to get all the data
