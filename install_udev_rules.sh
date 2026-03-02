#!/bin/bash

# Define udev rules for Movidius NCS1/NCS2
UDEV_RULES='SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666", GROUP="plugdev", TAG+="uaccess"'

# Create the rules file
echo "Creating udev rules for Movidius..."
echo "$UDEV_RULES" | sudo tee /etc/udev/rules.d/97-myriad-usbboot.rules > /dev/null

# Reload udev rules
echo "Reloading udev rules..."
sudo udevadm control --reload-rules
sudo udevadm trigger

# Ensure current user is in plugdev group
if ! groups $USER | grep -q "\bplugdev\b"; then
    echo "Adding user $USER to plugdev group..."
    sudo usermod -aG plugdev $USER
    echo "Note: You may need to logout and log back in for group changes to take effect."
fi

echo "Udev rules installed successfully."
