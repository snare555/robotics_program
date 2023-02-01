#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor_3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
motor_4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)


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

def input_calculation():

    # Get input signals from the controller and assign them to various variables
    yaw_control_factor = controller_1.axis1.position() / 2
    x_control_factor = controller_1.axis4.position() ** 3 / -100
    y_control_factor = controller_1.axis3.position() ** 3 / 100

    # The heading variable is the angle the robot travels at

    # If the left analog stick is moved right
    # and its either moved up or stays horizontal
    if x_control_factor > 0 and y_control_factor >= 0:

        #
        heading = math.atan(y_control_factor/x_control_factor)

    elif x_control_factor < 0 and y_control_factor >= 0:
        heading = math.pi - math.atan(-y_control_factor/x_control_factor)

    elif x_control_factor < 0 and y_control_factor < 0:
        heading = math.atan(y_control_factor/x_control_factor) + math.pi

    elif x_control_factor > 0 and y_control_factor < 0:
        heading = 2 * math.pi - math.atan(-y_control_factor/x_control_factor)

    elif x_control_factor == 0 and y_control_factor >= 0:
        heading = 0.5 * math.pi

    elif x_control_factor == 0 and y_control_factor < 0:
        heading = 1.5 * math.pi

    # Set a magnitude variable to whichever analog
    # input component is greater
    # (If we move the stick higher up than sideways) set the magnitude
    # to the vertical component
    if abs(y_control_factor) > abs(x_control_factor):
        magnitude = abs(y_control_factor)
    else:
        magnitude = abs(x_control_factor)
   
    x_drive_factor = math.cos(heading - math.pi / 4)
    y_drive_factor = math.sin(heading - math.pi / 4)

    if abs(x_drive_factor) > abs(y_drive_factor):
        diff = abs(y_drive_factor / x_drive_factor)
        x_drive_factor = magnitude * x_drive_factor
        y_drive_factor = magnitude * diff * y_drive_factor
   
    else:
        diff = abs(x_drive_factor / y_drive_factor)
        y_drive_factor = magnitude * y_drive_factor
        x_drive_factor = magnitude * diff * x_drive_factor

    motor_1_speed = y_drive_factor
    motor_3_speed = - y_drive_factor
    motor_2_speed = - x_drive_factor
    motor_4_speed = x_drive_factor

    motor_1_speed += yaw_control_factor
    if motor_1_speed >= 100:
        motor_1_speed = 100
    elif motor_1_speed <= -100:
        motor_1_speed = -100

    motor_2_speed += yaw_control_factor
    if motor_2_speed >= 100:
        motor_2_speed = 100
    elif motor_2_speed <= -100:
        motor_2_speed = -100

    motor_3_speed += yaw_control_factor
    if motor_3_speed >= 100:
        motor_3_speed = 100
    elif motor_3_speed <= -100:
        motor_3_speed = -100

    motor_4_speed += yaw_control_factor
    if motor_4_speed >= 100:
        motor_4_speed = 100
    elif motor_4_speed <= -100:
        motor_4_speed = -100



    return(motor_1_speed, motor_2_speed, motor_3_speed, motor_4_speed, magnitude, heading*180/math.pi, yaw_control_factor)

def motor_set():
    speeds = input_calculation()

   
    motor_1.set_velocity(speeds[0]*2)
    motor_2.set_velocity(speeds[1]*2)
    motor_3.set_velocity(speeds[2]*2)
    motor_4.set_velocity(speeds[3]*2)



while True:
    motor_set()
    brain.screen.print(input_calculation())
    wait(1/60,SECONDS)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2,2)

    motor_1.spin(FORWARD)
    motor_2.spin(FORWARD)
    motor_3.spin(FORWARD)
    motor_4.spin(FORWARD)