#!/bin/bash

sudo apt install git
#git clone https://github.com/CS5331-Group-10/A3.git
sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip
sudo pip install requests
sudo apt install python-scrapy

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get install docker-ce

docker run -p 8050:8050 scrapinghub/splash

# echo "cs5331 Y Y Y Y Y" | ./setup.sh
