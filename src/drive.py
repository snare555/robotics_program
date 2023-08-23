#region VEXcode Generated Robot Configuration
from vex import *
import math

# Brain should be defined by default
brain=Brain()




# Robot configuration code
controller_1 = Controller(PRIMARY)
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor_3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
motor_4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)

vision_1__OBJECT_1 = Signature(1, 4889, 6779, 5834,-1, 659, 329,3, 0)
vision_1 = Vision(Ports.PORT6, 50, vision_1__OBJECT_1)


# wait for rotation sensor to fully initialize
wait(30, MSEC)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
#   Project:      VEXcode Project
#   Author:       VEX
#   Created:
#   Description:  VEXcode V5 Python Project
# ------------------------------------------

# Begin project code

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
        self.axis[0] = controller_1.axis1.position()
        self.axis[1] = controller_1.axis2.position()
        self.axis[2] = controller_1.axis3.position()
        self.axis[3] = controller_1.axis4.position()


        # Add magnitudes to the input dictionary
        direction = [0, 0, 0, 0]
        for i in range(4):
            if self.axis[i] != 0:
                direction[i] = abs(self.axis[i])/self.axis[i]
        self.input = {
            "axis_1":[abs(self.axis[0]), direction[0]],
            "axis_2":[abs(self.axis[1]), direction[1]],
            "axis_3":[abs(self.axis[2]), direction[2]],
            "axis_4":[abs(self.axis[3]), direction[3]],
        }

    def control_input_modification(self, axis_1_cf = 1, axis_2_cf = 1, axis_3_cf = 1, axis_4_cf = 1):

        self.input["axis_1"][0] = (self.input["axis_1"][0]/10)**axis_1_cf
        self.input["axis_2"][0] = (self.input["axis_2"][0]/10)**axis_2_cf
        self.input["axis_3"][0] = (self.input["axis_3"][0]/10)**axis_3_cf
        self.input["axis_4"][0] = (self.input["axis_4"][0]/10)**axis_4_cf

    def parallel_input_calculations(self):
        # Iterate through the motors in a slice of the speeds index

        init_speed = self.input["axis_3"][0] * self.input["axis_3"][1]
        self.speeds = [init_speed for i in range(4)]
        if self.input["axis_4"][0] != 0:
            rotation = self.input["axis_4"][0] * self.input["axis_4"][1]
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
    while True:
        drive_program.control_input()
        drive_program.control_input_modification(axis_3_cf = 2, axis_4_cf = 3)
        drive_program.parallel_input_calculations()
        brain.screen.print(drive_program.input)
        drive_program.motor_speed()
        wait(1/60,SECONDS)
        brain.screen.clear_screen()
        brain.screen.set_cursor(2,2)

def automatic_drive():
    while True:
        drive_program.autonomous_chase()
        drive_program.parallel_input_calculations()
        brain.screen.print(drive_program.input["axis_3"])
        brain.screen.print(drive_program.size)
        drive_program.motor_speed()
        wait(1/60,SECONDS)
        brain.screen.clear_screen()
        brain.screen.set_cursor(2,2)

manual_drive()
