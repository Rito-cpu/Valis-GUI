#!/usr/bin/env bash

SCRIPT_PATH=$1
USER_SETTINGS=$2
SLIDE_SETTINGS=$3
HOME_DIR=$4

echo "Launching Python script with arguments:"
echo "Script Path: $SCRIPT_PATH"
echo "User Settings Path: $USER_SETTINGS"
echo "Slide Settings Path: $SLIDE_SETTINGS"
echo "Home Dir: $HOME_DIR"



docker run --rm \
    --name pyqt_valis_container \
    --memory=20g \
    -v "$HOME_DIR:/root" \
    cdgatenbee/valis-wsi python3 "$SCRIPT_PATH" -path "$USER_SETTINGS" -il "$SLIDE_SETTINGS" -hdir "$HOME_DIR"