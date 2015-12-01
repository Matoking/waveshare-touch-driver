#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root." 1>&2
	exit 1
fi

# Install required dependencies
apt-get install python python-pip libudev-dev batch
pip install python-uinput pyudev

# Copy the files into place
sudo cp waveshare-touch-driver.py /usr/bin/waveshare-touch-driver.py
sudo cp waveshare-touch-driver.sh /usr/bin/waveshare-touch-driver.sh
sudo cp 91-waveshare.rules /lib/udev/rules.d/91-waveshare.rules
sudo cp waveshare-touch-driver.service /lib/systemd/system/waveshare-touch-driver.service

chmod +x /usr/bin/waveshare-touch-driver.py
chmod +x /usr/bin/waveshare-touch-driver.sh

# Reload udev rules
udevadm control --reload-rules
udevadm trigger

# Reload systemctl units
systemctl --system daemon-reload

echo "Done! You can now plug in your touchscreen. Don't forget to calibrate it using calibrate.sh!"
