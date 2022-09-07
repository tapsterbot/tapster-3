# Installation Instructions:

How to install dependencies and prepare for using computer vision on the Tapster 3. These instructions are for Ubuntu and its derivatives.

## Before Doing Anything....
Enable Python environment: 
```source env/bin/activate```<br>
Update packages: 
```sudo apt update```

## Install OpenCV, Verify Installation
Use OpenCV 4.x -- `pip install opencv-python`<br>
Verify your installation:
```
python3
>>> import cv2
```
If the installation worked, the REPL should output nothing.

### Numpy fix for Raspberry Pi
There are dependencies for Numpy that are not satisfied on Raspberry Pi with a standard install. If you get an ImportError exception, run the following command:
```
sudo apt install libatlas-base-dev
```

## Install pytesseract
```
sudo apt install libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
pip install pytesseract
```

## Install imgutils
```
pip install imgutils
```

# Usage

Start by calibrating your robot, then feel free to use the main `controller.py` script as you wish and explore all of the different configurations!

## Calibrating Your Robot
- Using the checkerboard pattern included with your robot, take a series of pictures with the built-in camera with the checkerboard in full view and at different angles. Use a program such as Ubuntu's Cheese, or the Camera app in Windows. You should end up with ~25 images.
- Put these images in `controller/calib-images/`
- Find the calibration stick that came with your robot.
- Position the calibration stick on top of the standard phone mount so the back of the stick lines up with the back of the mount and the sides line up with the sides.
- Run `calibrate.py` to get your calibration data. This will dump the data to `coordinateCalib.json` and `distortionCalib.json` by default.

## Using Controller
Run with `python3 controller.py [PORT] [CAMPORT]`. From there, you can click anywhere in the Camera window to make the robot tap at that location! Run `python3 controller.py --help` for help with additional arguments/options.

# Troubleshooting

## calibration.py - Calibration failed
This occurs when the algorithm to find the dots on the calibration stick cannot pick all 3 of them out. This is usually due to bad lighting. Try a different lighting situation, and remove any direct, bright light sources.

## calibration.py - Camera not initialized correctly
This means your index for the camera is incorrect. It should be a single integer. Keep trying, starting from 0 and going up until it runs successfully.

## controller.py - Serial port not available
This happens either when the robot is not connected to the computer (i.e. it's not plugged in/powered) or when another program is using that particular serial port. Try closing any other programs that may be communicating with the robot, and check your connections.

## controller.py - Calibration was not run correctly
This is rare, but usually happens when the `coordinateCalib.json` file was copied from somewhere as opposed to being created with `calibrate.py`, and certain coordinates are blank. Rerun `calibrate.py`.

## controller.py - Camera not initialized correctly
See the `calibration.py` solution.