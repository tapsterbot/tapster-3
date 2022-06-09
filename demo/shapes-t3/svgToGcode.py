#SVG To Gcode

from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import sys

if len(sys.argv) < 2:
    print("Please specify a file to convert.")
    raise SystemExit
else:
    file = sys.argv[1]

# Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
# how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
gcode_compiler = Compiler(interfaces.Gcode, movement_speed=30000, cutting_speed=30000, pass_depth=0)

curves = parse_file(file) # Parse an svg file into geometric curves

gcode_compiler.append_curves(curves) 
gcode_compiler.compile_to_file(file[:3] + "gcode", passes=2)