#!/usr/bin/env bash

# Install packages
apt-get update
apt-get install -y python3 
apt-get install -y python3-venv 
apt-get install -y python3-pip
apt-get install -y git

# Upgrade pip
pip3 install --upgrade pip

# Set up SSH and Github access
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# Set up directory & flask
if [ ! -d "youtube-party" ]
then
    echo "Creating dir youtube-party..."
    mkdir youtube-party
fi

cd youtube-party
python3 -m venv venv
. venv/bin/activate
pip install Flask
