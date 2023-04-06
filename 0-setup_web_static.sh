#!/usr/bin/env bash
# Configure servers for the web static part of the project

sudo apt-get -y update
sudo apt-get -y install nginx

sudo ufw allow ""
