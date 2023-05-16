#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

controller_1 = Controller(PRIMARY)
motor_6 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)

motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

# wait for rotation sensor to fully initialize
wait(30, MSEC)
# Begin project code
import math



while True:
    motor_6.set_velocity(controller_1.axis2.position()*2)
    motor_6.spin(FORWARD)

    if motor_1.velocity(RPM) <= -135:
        motor_2.spin_for(REVERSE, 90, DEGREES)
        wait(1, SECONDS)
        motor_2.spin_for(REVERSE, 270, DEGREES)




    if controller_1.buttonA.pressing():
        motor_1.set_velocity(200)
        motor_1.spin(REVERSE)




    wait(1/60,SECONDS)