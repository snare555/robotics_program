from vex import *
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)


motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)  #RIGHT DRIVE

motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)  #LEFT DRIVE

motor_3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)  #INTAKE

motor_4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)  #RIGHT PUNCHER

motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)  #LEFT PUNCHER

motor_6 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)  #FLAPS

motor_7 = Motor(Ports.PORT7, GearSetting.RATIO_36_1, False)  #RIGHT CLIMBING MOTOR

motor_8 = Motor(Ports.PORT8, GearSetting.RATIO_36_1, False)  #LEFT CLIMBING MOTOR

vision_1__SIG_1 = Signature(1, -5269, -4855, -5062,-4995, -4473, -4734,8.8, 0)

vision = Vision(Ports.PORT10, 50, vision_1__SIG_1)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def shooting():

    # If a the shooting motors velocity is under less than or equal to -175RPM
    if motor_5.velocity(RPM) <= -120:

        # Print that we are shooting
        controller_1.rumble("---")
        
    
    # If we press the right bumper, cause the feeding motor to spin
    # pulling the disk on the floor into the launcher
    elif controller_1.buttonR1.pressing():
        motor_6.spin_to_position(-45, DEGREES)
        controller_1.screen.clear_screen()
        wait(1, SECONDS)
        motor_6.spin_to_position(0, DEGREES)


    # If we press the A button, set the shooting motors to max velocity to launch the disk
    elif controller_1.buttonA.pressing():
        motor_5.set_velocity(200)
        motor_5.spin(REVERSE)
    
    # If we press the B button, stop the shooting motor
    elif controller_1.buttonB.pressing():
        motor_5.set_velocity(0)
        motor_5.spin(REVERSE)

    elif motor_5.velocity != 0:
        controller_1.screen.set_cursor(0,0)
        controller_1.screen.print(motor_5.velocity)
        wait(0.3, SECONDS)
        controller_1.screen.clear_screen()

    # NOTE: Motors 7 and 8 spin in opposite directions

    if controller_1.buttonUp.pressing():

        # If we press up, spin the motors in their respective forward directions
        motor_7.set_velocity(5)
        motor_7.spin(FORWARD)

        motor_8.set_velocity(5)
        motor_8.spin(REVERSE)
    
    elif controller_1.buttonDown.pressing():

        # If we press down, spin the motors in their respective reverse directions
        motor_7.set_velocity(5)
        motor_7.spin(REVERSE)

        motor_8.set_velocity(5)
        motor_8.spin(FORWARD)
    
    # This will run if we dont press any of the key buttons
    else:
        motor_7.stop()
        motor_8.stop()


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
        self.size = (0, 0)
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
        of the respective axis coefficient (axis_num_cf). This provides finer control at smaller axis 
        input values while maintaining the speed for larger values
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

        # if we are moving the joystick forward or backward
        if self.input["axis_1"][0] != 0:

            # Set a rotation variable the velocity of the first axis
            rotation = self.input["axis_1"][0] * self.input["axis_1"][1]

            # increment and decrement the speed array elements for the rear left and right motors to the 
            # velocity previously calculated rotation
            self.speeds[0] -= rotation
            self.speeds[1] -= rotation
            self.speeds[2] += rotation
            self.speeds[3] += rotation

    def motor_speed(self):
        """
        Convert the speed previously calculated into motor velocities
        and spin the motors
        """
        motor_1.set_velocity(-self.speeds[0], PERCENT)
        motor_2.set_velocity(-self.speeds[1], PERCENT)

        motor_1.spin(REVERSE)
        motor_2.spin(REVERSE)


    def vision_data_collect(self):
        """
        A function which will take in several pieces of information from
        its surroundings. This data inckudes the location and size of the object
        the robot is seeking
        """

        # Take the snapshot of the object
        object = vision.take_snapshot(vision_1__SIG_1)

        brain.screen.print("Taking picture")


        # If there is a valid object
        if object is not None:

            # Create 2 tuples with the center x and y values of the object as well as the size of the object 
            self.location = (vision.largest_object().centerX, vision.largest_object().centerY)

            self.size = (vision.largest_object().width, vision.largest_object().height)
        elif object is None:
            self.size = (0, 0)

    def autonomous_chase(self):
        """A function that takes in visual data and outputs motor data to chases an object"""
        
        self.vision_data_collect()
        brain.screen.set_cursor(2,2)
        brain.screen.print(self.location, self.size)


        # Joseph you can comment this yourself
        

        # If the recognized object is closer to the right side of the vision
        # sensors FOV then upload information to the input dictionary
        # to make the robot slowly rotate move to the left
        if (self.location[0]) > 190:
            self.input["axis_1"] = [10, 1]
            controller_1.screen.print("right ")

        # Repeat the same code from above but this time with the left side
        elif (self.location[0]) < 110:
            self.input["axis_1"] = [10, -1]
            controller_1.screen.print("left ")

        # If the object is in between these margins dont rotate the motor
        else:

            self.input["axis_1"] = [0, 1]
            controller_1.screen.print("center ")
        
        # If the size 
        if (self.size[0] * self.size[1]) == 0:
            self.input["axis_3"] = [0, 1]

        # If the size of the object spotted is smaller than 700
        # Head towards it
        if (self.size[0] * self.size[1]) < 700:
            self.input["axis_3"] = [30, 1]
            controller_1.screen.print("forward", self.size)
        
        # If the size of the object is larger than 1300 it is too close
        # and we therefore need to back up
        if (self.size[0] * self.size[1]) > 1300:
            self.input["axis_3"] = [30, -1]
            controller_1.screen.print("backward", self.size)
        
        # if we cant detect the object, dont move it
        elif self.size == (0,0):
            self.input["axis_3"] = [0, 1]
        
        # If the object is within a certain size boundary, dont move
        elif (self.size[0] * self.size[1]) < 1300 and (self.size[0] * self.size[1]) > 700:
            self.input["axis_3"] = [0, 1]



drive_program = Drive()

def manual_drive():
    """
    Call all the neccesary functions to drive the robot
    """
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
    drive_program.motor_speed()

# #Lock piviot motors
motor_7.set_stopping(HOLD)
motor_8.set_stopping(HOLD)

while True:



    # automatic_drive()
    manual_drive()
    shooting()
    wait(1/30, SECONDS)

    brain.screen.clear_screen()



    # Display the motor temp when we press x
    # if controller_1.buttonX.pressing():
    #     controller_1.screen.set_cursor(0,0)
    #     controller_1.screen.print(motor_5.temperature(PERCENT))
    #     wait(0.3, SECONDS)
    #     controller_1.screen.clear_screen()

