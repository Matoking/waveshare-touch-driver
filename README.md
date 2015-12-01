# Waveshare touchscreen userspace driver
waveshare-touch-driver is an userspace driver for Waveshare touchscreens written in Python using python-uinput.

# Compatibility
This driver is compatible and has been tested with the Waveshare 5" HDMI LCD Resistive Touch Screen. 

In addition, the driver should also be compatible with the 7" model, as the only difference between the touch controllers in these two models is the packet length (25 bytes instead of 22). The driver determines this packet length automatically.

# Installation
If you are running a Debian-based distribution, run the following commands to install the driver using the provided script.

```
chmod +x install.sh
sudo ./install.sh
```

If you are using a different distribution, the installation script should work aside from the dependencies, which you'll need to install using your distribution's package manager:
python, python-pip, pyudev, python-uinput

# Calibration
After the driver is in use, you can use the touchscreen after plugging it in. However, you should calibrate your touchscreen using the provided calibrate.sh script, which uses xinput_calibrator to perform the calibration.

```
chmod +x calibrate.sh
./calibrate.sh
```

The program will instruct you on how to make the calibration permanent after successful calibration.

# Donations
BTC: 13YppQBmB7ghsfuRHnrLhmPPj1BgbREA4B

# License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
