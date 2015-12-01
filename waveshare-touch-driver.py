#!/usr/bin/env python
import argparse
import uinput
import pyudev
import os
import sys
import string
import glob
import struct
import time

def grab_device(device_file, serial, packet_length=None):
    """
    Grab an active touchscreen
    """
    emulated_device = uinput.Device([
        uinput.BTN_TOUCH,
        uinput.ABS_X + (0, 4000, 0, 0),
        uinput.ABS_Y + (0, 4000, 0, 0),
        uinput.ABS_PRESSURE,
    ], 
    name="Waveshare Touchscreen (%s)" % serial,
    vendor=0x0eef,
    product=0x0005)
    
    print("Device file found! Reading...")
    
    try:
        with open(device_file, 'rb') as f:
            # We don't know the packet length yet
            if packet_length == None:
                packet_length = 0
                found_tag = False
                
                print("Packet length unknown for this device, keep poking the screen until I figure it out.")
                
                while True:
                    sample = f.read(1)
                    
                    # Each packet starts with the tag 'aa' in hex
                    # After we find the first tag, we start counting the number of bytes
                    # until the next tag arrives
                    if sample[0] == b'\xaa' and not found_tag:
                        found_tag = True
                        packet_length += len(sample)
                    elif sample[0] == b'\xaa':
                        break
                    else:
                        packet_length += len(sample)
                    
                
                # Packet length is now known, this blocking read is done
                # so that the following reads always start with the tag as they should
                f.read(packet_length-1)
                print("Packet length for this device is %d bytes." % packet_length)
            else:
                print("Using provided packet length: %d" % packet_length)
            
            # The last coordinates for the device when it was touched
            last_x = 0
            last_y = 0
            
            while True:
                try:
                    packet = f.read(packet_length)
                except OSError:
                    print("Read failed, device was probably disconnected")
                    exit()
                
                clicked = True if packet[1:2] == b'\x01' else False
                x_pos = packet[2:4]
                
                (tag, click, x, y) = struct.unpack_from('>c?HH', packet)
                
                if clicked:
                    last_x = x
                    last_y = y
                    
                    #print("%dx%d" % (x, y))
                    
                    emulated_device.emit(uinput.BTN_TOUCH, 1, False)
                    emulated_device.emit(uinput.ABS_X, x, False)
                    emulated_device.emit(uinput.ABS_Y, y, False)
                    
                    emulated_device.emit(uinput.ABS_PRESSURE, 255, True)
                else:
                    emulated_device.emit(uinput.BTN_TOUCH, 0, False)
                    emulated_device.emit(uinput.ABS_X, last_x, False)
                    emulated_device.emit(uinput.ABS_Y, last_y, False)
                    emulated_device.emit(uinput.ABS_PRESSURE, 0, True)
    except OSError:
        print("Device disconnected.")
        exit()
        
def get_serial(sys_name):
    """
    Get the serial number for a device based on its sys_name
    """
    devices = context.list_devices(sys_name=sys_name)
    
    for device in devices:
        try:
            serial = device.attributes["serial"]
            
            # Serial numbers appear to have non-printable characters inside them
            # Remove those characters here
            serial = "".join(filter(lambda x: x in string.printable, serial))
            return serial
        except:
            pass
        
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Userspace driver for Waveshare touchscreens.")
    parser.add_argument('--devpath', type=str, required=True,
                        help="Devpath of the USB device (eg. /devices/usb.1/12000000.dwc3/xhci-hcd.2.auto/usb3/3-1/3-1.1/3-1.1.1/3-1.1.1.4). In normal operation this is passed automatically by udev.")
    parser.add_argument("--packet_length", type=int, required=False,
                        help="Packet length for the device. The driver should be able to determine this automatically.")
    
    args = parser.parse_args()
    
    devpath = args.devpath
    
    if "packet_length" in args:
        packet_length = args.packet_length
    else:
        packet_length = None
    
    # Get the sys_name from the full devpath (eg. 3-1.1.1.4)
    sys_name = devpath[devpath.rfind("/")+1:]
    
    os.system("modprobe uinput")
    
    context = pyudev.Context()
    
    # Get the device loaded as /dev/hidraw*
    devices = context.list_devices().match(subsystem = "hidraw")
    
    for device in devices:
        if "0EEF:0005" in device.sys_path and "%s/" % sys_name in device.sys_path:
            # We found a matching device, let's try to grab it
            print("Device found!")
            
            # Get the serial number for this device, since it allows
            # us to give each device a deterministic name (eg. changing the USB slot it's plugged into
            # shouldn't affect the configuration)
            serial = get_serial(sys_name)
            
            if serial != None:
                print("Serial number for this device: %s" % serial)
            else:
                print("Couldn't find the serial number for this device!")
                serial = "UNKNOWN SN"
                
            device_file = "/dev/%s" % (device.sys_path[device.sys_path.rfind('/')+1:])
            
            grab_device(device_file, serial, packet_length)
    
    print("Device not found!")