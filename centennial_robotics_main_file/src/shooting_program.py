#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)

motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

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

while True:

    if motor_1.velocity(RPM) <= -175:
        controller_1.screen.print("SHOOT")
        controller_1.rumble("---") 

    
    if controller_1.buttonR1.pressing():
        motor_2.spin_for(FORWARD, 360, DEGREES)
        controller_1.screen.clear_screen()


    if controller_1.buttonA.pressing():
        motor_1.set_velocity(200)
        motor_1.spin(REVERSE)
    
    if controller_1.buttonB.pressing():
        motor_1.set_velocity(0)
        motor_1.spin(REVERSE)

    if controller_1.buttonX.pressing():
        controller_1.screen.print(motor_1.temperature())
        wait(5, SECONDS)
        controller_1.screen.clear_screen()

    wait(1/60,SECONDS)