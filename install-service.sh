#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Copying service file"
cp ./py-erfid.service /etc/systemd/system/py-erfid.service

echo "Reloading systemctl daemon"
systemctl daemon-reload

echo "Starting service"
systemctl enable py-erfid
systemctl start py-erfid

echo "Done!"
