#!/usr/bin/env bash

docker run --rm --memory=20g -v ~:/root cdgatenbee/valis-wsi python3 $1 -path $2 -il $3 -hdir $4