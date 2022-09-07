# Tapster Robot Demos and Sample Code
This is a folder of sample programs for both the Tapster T3 and Tapster T3+. It has a wide range of demonstrations of the robots' abilities, and code that can be directly ported to a new project or integrated into an existing one.

## Usage

### Setup
```
sudo apt update
sudo apt install python3
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Other Requirements
Some demos have special requirements (A Push Button Module, certain device configuration, etc) or were meant for a specific device. These requirements will be listed at the top of each demo file.

Some items, such as the specific phone or tablet that the code was written for, isn't a strict requirement and the code can be easily changed to work on anything, or may even work out of the box. However, robot modules and device configuration, such as unlocking the bootloader, are absolutely required for certain demos to function.

### Running Demos
`python3 [demoName].py [PORT] [args]`
Regardless of the demo, the serial port of the Tapster robot will *always* be the first command argument. Any other arguments will come after. You must specify the port to run the demo.

### Deactivate enviroment
`deactivate`

### Writing Your Own Code
The `robot.py` file and its included `Robot` class are the basis for all of the demos. Use the `Robot` methods to control the End Effector, a Push Button Module, or send raw commands to the firmware. The usage instructions for each method are in the `robot.py` file.