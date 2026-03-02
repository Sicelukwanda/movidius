#!/bin/bash
# Intel Movidius NCS udev rules
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666", GROUP="plugdev", TAG+="uaccess"' | sudo tee /etc/udev/rules.d/97-myriad-usbboot.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
echo "Udev rules updated. Please unplug and replug the NCS stick."
