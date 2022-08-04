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