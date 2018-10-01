#!/bin/sh
# installer.sh will install the necessary packages to get the gifcam up and running with 
# basic functions

echo
echo "----------------"
echo "Update & Upgrade"
echo "----------------"
echo
PACKAGES="python3-dev"
apt-get update
apt-get upgrade -y
apt-get install $PACKAGES -y
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh

# Run Docker without using sudo all the time
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker

docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:/rootfs/$PWD" \
    -w="/rootfs/$PWD" \
    docker/compose:1.22.0 up

echo alias docker-compose="'"'docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:/rootfs/$PWD" \
    -w="/rootfs/$PWD" \
    docker/compose:1.22.0'"'" >> ~/.bashrc

echo
echo "-----------------------"
echo "Install master release"
echo "-----------------------"
echo
cd ~
wget -O reactor.zip https://github.com/IPconfig/testdriven-app/archive/master.zip
unzip -o reactor.zip

mv ~/testdriven-app-master ~/app --no-target-directory
cd ~/app

#reload bash
source ~/.bashrc




function generate_key {
python3 - <<END
import binascii
import os
print(binascii.hexlify(os.urandom(24)))
END
}
echo
echo "-----------------------"
echo "Set environment variables"
echo "-----------------------"
echo
# Call it and capture the output
export SECRET_KEY=$(generate_key)
export REACT_APP_USERS_SERVICE_URL=http://localhost
export REACT_APP_PLC_SERVICE_URL=http://localhost