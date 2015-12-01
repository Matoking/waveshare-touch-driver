#!/bin/bash
echo "DEVPATH=\"$DEVPATH\"" > /etc/waveshare-touch-env
systemctl start waveshare-touch-driver.service
exit 0;
