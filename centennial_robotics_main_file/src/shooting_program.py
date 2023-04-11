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

    if motor_1.velocity(RPM) <= -135:
        motor_2.spin_for(REVERSE, 90, DEGREES)
        wait(1, SECONDS)
        motor_2.spin_for(REVERSE, 270, DEGREES)




    if controller_1.buttonA.pressing():
        motor_1.set_velocity(200)
        motor_1.spin(REVERSE)

    
    

    wait(1/60,SECONDS)
    

