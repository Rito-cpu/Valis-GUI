#!/usr/bin/env bash

docker run --rm --memory=20g -v $HOME:/root cdgatenbee/valis-wsi python3 $1 -path $2