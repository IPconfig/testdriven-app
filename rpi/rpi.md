### Install PiBakery v2 (beta)

### download latest rpi Jessie image from https://downloads.raspberrypi.org/raspbian_lite_latest


<!-- Installs Docker -->
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh

# Run Docker without using sudo all the time
<!-- Add a docker group -->
sudo groupadd docker

<!-- Add the connected user to the docker group -->
sudo gpasswd -a $USER docker

<!-- apply changes -->
newgrp docker

<!-- run docker-compose as a container -->
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:/rootfs/$PWD" \
    -w="/rootfs/$PWD" \
    docker/compose:1.13.0 up

<!-- Make an alias -->
echo alias docker-compose="'"'docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:/rootfs/$PWD" \
    -w="/rootfs/$PWD" \
    docker/compose:1.13.0'"'" >> ~/.bashrc

<!-- Reload bash -->
source ~/.bashrc