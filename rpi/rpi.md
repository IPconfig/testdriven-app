# Installation on a Raspberry Pi
There are a few steps to take to put these microservices on a raspberry pi.
## Prepare the SD card
1. [download](https://downloads.raspberrypi.org/raspbian_lite_latest) latest Raspbian Lite image
2. Burn the image on a SD card with [Etcher.io](https://etcher.io)
3. Enable SSH
    - Navigate to the boot volume: `$ cd /Volumes/boot`
    - Create an empty file named ssh: `$ touch ssh`
4. Configure Wi-Fi
    - Create a config file in the boot partition: `$ nano wpa_supplicant.conf`
    - Configure template with your settings
    -  ```
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        country=«your_ISO-3166-1_two-letter_country_code»
        
        network={
            ssid="«your_SSID»"
            psk="«your_PSK»"
            key_mgmt=WPA-PSK
        }
        ```
5. Put the SD card into the Raspberry Pi and SSH into it (default user is **pi** with password **raspberry**)
```
$ ssh pi@<<ipadress>>
```
6. Upgrade the default packages: `apt-get update && apt-get upgrade -y`

## Install Docker
Install Docker

```
$ curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
```
Install Docker-compose with pip
2. `pip3 install docker-compose`
1. `sudo apt-get install libssl-dev libffi-dev python3-pip -y`

### Run Docker without using sudo all the time
1. Add a docker group: `$ sudo groupadd docker`
2. Add the connected user to the docker group `$ sudo gpasswd -a $USER docker`
3. apply changes`$ sudo newgrp docker`


## Install the app
The following steps will setup the Raspberry Pi to start the app on startup. For my goals we need to connect to devices in the 192.168.0.X range.
1. Set eth0 to 192.168.0.10 (static). Don't configure the Router and DNS servers so these still work with DHCP and thus via wlan0
```
echo '# Static IP' >> /etc/dhcpcd.conf
echo 'static ip_address=192.168.0.10' >> /etc/dhcpcd.conf
```
2. Download the app
```
$ wget https://github.com/IPconfig/testdriven-app/archive/master.zip && \
unzip -o master && \
mv ~/testdriven-app-master ~/app --no-target-directory && \
rm master.zip
```
3. Set SECRET_KEY variable (See README.MD). The REACT_APP_SERVICE_URLS can be blank on the Raspberry Pi
4. Build the app manually for the first time to the environment variables get set.
   - Navigate to the app directory: `$ cd ~/app`
   - Build the app: `docker-compose -f docker-compose-prod.yml up -d --build`
   - Create (and seed) the databases: 
        ```
        $ docker-compose -f docker-compose-prod.yml run users python manage.py recreate-db && \
        docker-compose -f docker-compose-prod.yml run plc python manage.py recreate-db && \
        docker-compose -f docker-compose-prod.yml run users python manage.py seed-db && \
        docker-compose -f docker-compose-prod.yml run plc python manage.py seed-db
        ```
   - Verify that everything is okay and shutdown: `docker-compose -f docker-compose-prod.yml down`

### Start the docker-compose-prod.yml on boot
1. Make the service file executable: `$ chmod +x ~/app/rpi/service`
2. Move the boot service file to the appropriate directory: `$ sudo mv ~/app/rpi/docker-compose-app.service /etc/systemd/system/`
3. Enable the service: `$ sudo systemctl enable docker-compose-app`
4. Reload the service daemon: `$ sudo systemctl daemon-reload`
5. Start the service: `$ sudo systemctl start docker-compose-app`
6. Check the service: `$ sudo systemctl status docker-compose-app`
7. Make sure the app is working. You're done!


### Upgrade app
1. SSH into the rpi and stop the docker containers: 
   - Open terminal and SSH: `$ ssh pi@raspberrypi.local`
   - Stop the services: `$ docker-compose -f ~/app/docker-compose-prod.yml down`
2. Remove the app directory: `$ rm ~/app -r`
3. Download new version of the services: `wget https://github.com/IPconfig/testdriven-app/archive/master.zip &&
unzip -o master &&
mv ~/testdriven-app-master ~/app --no-target-directory &&
rm master.zip`
4. Build the services: `$ docker-compose -f ~/app/docker-compose-prod.yml up -d --build`
5. Verifiy if services run after a `$ sudo reboot`