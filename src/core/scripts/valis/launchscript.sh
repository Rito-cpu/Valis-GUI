#!/usr/bin/env bash

# this is the command run in the terminal to launch the docker container, the $ values represent the variables passed
# from on_register_press.py

docker run --rm --memory=20g -v ~:/root cdgatenbee/valis-wsi python3 $1 -path $2 -il $3 -hdir $4