#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
#
#   Project:      VEXcode Project
#   Author:       VEX
#   Created:
#   Description:  VEXcode V5 Python Project
#
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
import math

controller_1.screen.clear_screen()

controller_1.screen.print("SHOOT") 
controller_1.rumble(".-.-")

wait(5, SECONDS)
controller_1.screen.clear_screen()

motor_1.set_velocity(200)
motor_1.spin(REVERSE)

wait(10, SECONDS)
temp = motor_1.temperature(PERCENT)

    

print(temp)
controller_1.screen.print(temp) 

