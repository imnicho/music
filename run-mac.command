#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ ! -d venv ]; then
    echo "Creating virtualenv..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --quiet --upgrade pip
pip uninstall -y hid >/dev/null 2>&1 || true
pip install --quiet mido==1.3.2 python-rtmidi==1.5.8 hidapi==0.15.0

echo "Starting OctaveLights. Ctrl+C to stop."
echo "Log: ~/OctaveLights/octavelights.log"
echo
exec python octavelights.py
