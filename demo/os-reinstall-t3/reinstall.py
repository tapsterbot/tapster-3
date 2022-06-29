#Arguments:
# folderPath : All dependencies and the os are already downloaded and installed from a previous reflash, just flash the device with the os at folderPath
# -F : First time setup, install ALL dependencies along with downloading the OS
# -f : First time setup WITH THIS OS (all other dependencies are already installed) -- just downlaod OS

# Precondition: This script is run inside the folder to be used as the download/install directory (i.e. ~/android-reflash/)

import sys
sys.path.append("..")

#import robot
import time
import os

if len(sys.argv) > 2: #take in the serial port name from the args
    PORT = sys.argv[1]
    if sys.argv[2] == '-F':
        firstTime = True
        downloadOS = True
        directoryName = sys.argv[3][sys.argv[3].rfind("/") + 1:]
    elif sys.argv[2] == '-f':
        firstTime = False
        downloadOS = True
        directoryName = sys.argv[3][sys.argv[3].rfind("/") + 1:]
    else:
        #if the second arg is not a flag (-f or -F), it's a path. if it doesn't exist, exit. if it does continue.
        if not os.path.isdir(sys.argv[2]):
            print("Argument not recognized. Please try again.")
            raise SystemExit
        firstTime = False
        downloadOS = False
        directoryName = sys.argv[2]
else:
    print("Please specify a port.")
    raise SystemExit

if firstTime:
    print("""
    Preconfigure your device.
     - Boot into the stock OS.
     - Enable developer mode.
     - Enable OEM bootloader unlocking.
    
    Press enter when done.""")
    while input() != "": pass
    
    os.system("""
sudo apt install curl
sudo apt install libarchive-tools
curl -O https://dl.google.com/android/repository/platform-tools_r33.0.1-linux.zip
echo 'a339548918c3ab31c4d88416c21cee753bd942040540216c06e640f4b6db3ae2  platform-tools_r33.0.1-linux.zip' | sha256sum -c
bsdtar xvf platform-tools_r33.0.1-linux.zip
echo export PATH=\\\"$PWD/platform-tools:$PATH\\\" >> ~/.bashrc
source ~/.bashrc
sudo apt install android-sdk-platform-tools-common
""")

print("""
\nReboot your device into the bootloader menu by rebooting while holding the volume down button.
Plug the device into the computer.

Press enter when done.""")
while input() != "": pass

os.system("fastboot flashing unlock")
while input("\nConfirm the bootloader unlock on your device. Press enter when done.") != "": pass

if downloadOS:
    os.system("""
curl -O """ + sys.argv[3] + """
bsdtar xvf """ + directoryName)

os.system("""
cd """ + directoryName[:-4] + """
chmod +x flash-all.sh 
./flash-all.sh
cd ..
fastboot flashing lock""")

while input("Confirm the bootloader relock on your device. Press enter when done.") != "": pass