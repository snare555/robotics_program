#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
# vex-vision-config:begin
vision_1__OBJECT_1 = Signature(1, 5435, 7537, 6486,-807, -141, -474,2.4, 0)
vision_1 = Vision(Ports.PORT1, 50, vision_1__OBJECT_1)
# vex-vision-config:end


# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

while True:
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

    object = vision_1.take_snapshot(vision_1__OBJECT_1)
    if object is not None:
        brain.screen.print("Center X: ", vision_1.largest_object().centerX)
        brain.screen.next_row()
        brain.screen.print("Center Y: ", vision_1.largest_object().centerY)
        brain.screen.next_row()
        brain.screen.print("Width: ", vision_1.largest_object().width)
        brain.screen.next_row()
        brain.screen.print("Height: ", vision_1.largest_object().height)
        brain.screen.next_row()


    elif object is None:
        brain.screen.print("None")
        brain.screen.next_row()

    wait(0.2,SECONDS)

