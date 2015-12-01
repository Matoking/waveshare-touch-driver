#!/bin/bash
if hash xinput_calibrator 2>/dev/null; then
	xinput_calibrator --geometry 800x480
else
	sudo apt-get install xinput-calibrator
fi
