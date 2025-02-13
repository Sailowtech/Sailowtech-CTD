# Quick guide


## Turn on the CTD
The CTD can be turned on by closing (turning clockwise) the on/off switch as marked in the image below.
![CTD](assets/ctd-top.jpg)


## Connect to the CTD
The CTD will start after turning on the power supply. Please note that this might take up to one minute.
A Wi-Fi network called `CTD` will then appear. Connect to it with the password `CTDCTDCTD`.

For further settings and system upgrades, it is possible to connect over SSH `ssh ctd@192.168.42.1` and password `ctd`.

## Start a recording
To start a CTD recording, use the web-interface, and open the URL: [http://192.168.42.1/run?measurements=100](http://192.168.42.1/run?measurements=100)

Change the number after `measurements=` to change the number of measurements that should be taken (a measurement is done every ~1.5 seconds)

### Approximate measurements per duration
- For < 1 minute of measurements: [http://192.168.42.1/run?measurements=30](http://192.168.42.1/run?measurements=30)
- For ~5 minutes of measurements: [http://192.168.42.1/run?measurements=150](http://192.168.42.1/run?measurements=150)
- For ~10 minutes of measurements: [http://192.168.42.1/run?measurements=300](http://192.168.42.1/run?measurements=300)

## Download data
To download the recorded data as a CSV-file, open the following URL: [http://192.168.42.1/csv](http://192.168.42.1/csv)