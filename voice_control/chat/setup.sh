#!/bin/sh

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-venv portaudio19-dev flac

if [ ! -d "venv" ]; then
    python3 -m venv .venv --upgrade-deps
    source .venv/bin/activate
    pip install -r requirements.txt
fi
