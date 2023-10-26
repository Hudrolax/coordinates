#!/bin/sh

# set -e

rm -f /tmp/.X0-lock
rm -rf /app/tmp

# Run Xvfb on dispaly 0.
Xvfb :0 -screen 0 1920x1080x16 &

# Run fluxbox windows manager on display 0.
fluxbox -display :0 &

# Run x11vnc on display 0
x11vnc -display :0 -forever -usepw &

# Add delay
sleep 5

exec python main.py
