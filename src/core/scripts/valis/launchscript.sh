#!/usr/bin/env bash

# this is the command run in the terminal to launch the docker container, the $ values represent the variables passed
# from on_register_press.py

echo "Launching Python script with arguments:"
echo "Script Path: $1"
echo "User Settings Path: $2"
echo "Slide Settings Path: $3"
echo "Home Dir: $4"

docker run --rm --name pyqt_valis_container --memory=20g -v ~:/root cdgatenbee/valis-wsi python3 $1 -path $2 -il $3 -hdir $4