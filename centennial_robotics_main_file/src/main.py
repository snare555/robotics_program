#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)


motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)  #FR

motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)  #RR

motor_3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)  #RL

motor_4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)  #FL

motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)  #Shooting motor

motor_6 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)  #Feeding motor

motor_7 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)  #Tilt motor R

motor_8 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)  #Tilt motor L


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


def shooting():

    # If a the shooting motors velocity is under less than or equal to -175RPM
    if motor_5.velocity(RPM) <= -175:

        # Print that we are shooting
        controller_1.screen.print("SHOOT")
        controller_1.rumble("---") 

    
    # If we press the right bumper, cause the feeding motor to spin
    # pulling the disk on the floor into the launcher
    if controller_1.buttonR1.pressing():
        motor_6.spin_to_position(-90, DEGREES)
        controller_1.screen.clear_screen()
        wait(1, SECONDS)
        motor_6.spin_to_position(0, DEGREES)


    # If we press the A button, set the shooting motors to max velocity to launch the disk
    if controller_1.buttonA.pressing():
        motor_5.set_velocity(200)
        motor_5.spin(REVERSE)
    
    # If we press the B button, stop the shooting motor
    if controller_1.buttonB.pressing():
        motor_5.set_velocity(0)
        motor_5.spin(REVERSE)


    # NOTE: Motors 7 and 8 spin in opposite directions

    if controller_1.buttonUp.pressing():

        # If we press up, spin the motors in their respective forward directions
        motor_7.set_velocity(50)
        motor_7.spin(FORWARD)

        motor_8.set_velocity(50)
        motor_8.spin(REVERSE)
    
    elif controller_1.buttonDown.pressing():

        # If we press down, spin the motors in their respective reverse directions
        motor_7.set_velocity(50)
        motor_7.spin(REVERSE)

        motor_8.set_velocity(50)
        motor_8.spin(FORWARD)
    
    # This will run if we dont press any of the key buttons
    else:
        motor_7.stop()
        motor_8.stop()

    

        
    # if controller_1.buttonUp.pressing():
    #     motor_7.spin_for
    #     motor_8.


    wait(1/60,SECONDS)
    

class Drive():

    def __init__(self):

        self.speeds = []

        self.input = {
            "axis_1":[0, 0],
            "axis_2":[0, 0],
            "axis_3":[0, 0],
            "axis_4":[0, 0],
        }

        self.location = (0, 0)
        self.size = ()
        self.axis = [0, 0, 0, 0]

    def control_input(self):
        """
        A method which will store the controller axis positions in the 
        self.axis array
        """


        self.axis[0] = controller_1.axis1.position()# Responsible for turning the robot left & right
        self.axis[1] = controller_1.axis2.position()# currently unused
        self.axis[2] = controller_1.axis3.position()# Responsible for moving the robot forward and backward
        self.axis[3] = controller_1.axis4.position()# currently unused


        # Add magnitudes to the input dictionary
        direction = [0, 0, 0, 0]

        # Iterate through the axis list and check for axis that the user is currently 
        # pushing the joystick towards. Divide the absolute value of the axis value
        # by the axis value to preserve the sign of the magnitude, giving up the direction
        # the user is pointing the joystick in
        for i in range(4):
            if self.axis[i] != 0:
                direction[i] = abs(self.axis[i])/self.axis[i]

        
        # A dictionary which holds vectors that contain the magnitude and direction
        # For each joystick axis
        self.input = {
            "axis_1":[abs(self.axis[0]), direction[0]],
            "axis_2":[abs(self.axis[1]), direction[1]],
            "axis_3":[abs(self.axis[2]), direction[2]],
            "axis_4":[abs(self.axis[3]), direction[3]],
        }


    def control_input_modification(self, axis_1_cf = 1, axis_2_cf = 1, axis_3_cf = 1, axis_4_cf = 1):
        """
        Curve the magnitude of each controller axis by dividing by 10 and putting it to the power
        of the respective axis coefficient (axis_num_cf)
        """

        self.input["axis_1"][0] = (self.input["axis_1"][0]/10)**axis_1_cf
        self.input["axis_2"][0] = (self.input["axis_2"][0]/10)**axis_2_cf
        self.input["axis_3"][0] = (self.input["axis_3"][0]/10)**axis_3_cf
        self.input["axis_4"][0] = (self.input["axis_4"][0]/10)**axis_4_cf

    def parallel_input_calculations(self):


        # Iterate through the motors in a slice of the speeds index

        # Set an initial velocity variable to the a vector representing the
        # moving joysticks state (axis 3)
        init_velocity = self.input["axis_3"][0] * self.input["axis_3"][1]

        self.speeds = [init_velocity for i in range(4)]

        if self.input["axis_1"][0] != 0:

            rotation = self.input["axis_1"][0] * self.input["axis_1"][1]
            self.speeds[1] -= rotation
            self.speeds[2] += rotation

    def motor_speed(self):

        motor_1.set_velocity(-self.speeds[0]*2)
        motor_2.set_velocity(-self.speeds[1]*2)
        motor_3.set_velocity(self.speeds[2]*2)
        motor_4.set_velocity(self.speeds[3]*2)

        motor_1.spin(FORWARD)
        motor_2.spin(FORWARD)
        motor_3.spin(FORWARD)
        motor_4.spin(FORWARD)

    def kill(self):
        motor_1.set_velocity(0)
        motor_2.set_velocity(0)
        motor_3.set_velocity(0)
        motor_4.set_velocity(0)

        motor_1.spin(FORWARD)
        motor_2.spin(FORWARD)
        motor_3.spin(FORWARD)
        motor_4.spin(FORWARD)


    def vision_data_collect(self):
        """
        A function which will take in several pieces of information from
        its surroundings. This data inckudes the location and size of the object
        the robot is seeking
        """
        object = vision_1.take_snapshot(vision_1__OBJECT_1)
        brain.screen.print("Taking picture")

        if object is not None:
            self.location = (vision_1.largest_object().centerX, vision_1.largest_object().centerY)

            self.size = (vision_1.largest_object().width, vision_1.largest_object().height)

    def autonomous_chase(self):
        """A function that takes in visual data and outputs motor data to chases an object"""
        
        self.vision_data_collect()

        if (self.location[0] * self.location[1]) > 495:
            self.input["axis_3"] = [75, -1]
        elif (self.location[0] * self.location[1]) < 473:
            self.input["axis_3"] = [75, 1]
        else:
            self.input["axis_3"] = [0, 1]



drive_program = Drive()
def manual_drive():
    drive_program.control_input()
    drive_program.control_input_modification(axis_1_cf = 2, axis_3_cf = 2)
    drive_program.parallel_input_calculations()
    drive_program.motor_speed()
    wait(1/60,SECONDS)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2,2)

def automatic_drive():
    drive_program.autonomous_chase()
    drive_program.parallel_input_calculations()
    brain.screen.print(drive_program.input["axis_3"])
    brain.screen.print(drive_program.size)
    drive_program.motor_speed()
    wait(1/60,SECONDS)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2,2)

while True:
    manual_drive()
    shooting()

    controller_1.screen.print(motor_5.velocity(RPM))
    if controller_1.buttonX.pressing():
        controller_1.screen.print(motor_5.temperature(PERCENT))
        wait(5, SECONDS)
        controller_1.screen.clear_screen()
    if controller_1.buttonY.pressing():
        motor_1.stop(mode="Break")
        motor_2.stop(mode="Break")
        motor_3.stop(mode="Break")
        motor_4.stop(mode="Break")
        motor_5.stop(mode="Break")
        motor_6.stop(mode="Break")
        motor_7.stop(mode="Break")
        motor_8.stop(mode="Break")
        wait(50, SECONDS)


    wait(1/60, SECONDS)