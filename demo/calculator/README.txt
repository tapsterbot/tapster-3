# Tapster 3 - Calculator App Demo
Demo code for the Tapster 3 robot

Video of demo: https://youtu.be/dlpzl9pZYQk

## Setup

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Source Modification

Modify calculator-demo.py with the correct serial port string.
```
PORT = "/dev/tty.usbserial-1420"
```

## Run Demo
1) Make sure the Tapster 3 robot is plugged in and connected to your computer.

2) Run demo:

```
python3 calculator-demo.py
```

## Deactivate enviroment

```
deactivate
```