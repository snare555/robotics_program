from vex import *
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY) #test2 test

motor_1 = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)  #RIGHT DRIVE

motor_2 = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)  #LEFT DRIVE

motor_3 = Motor(Ports.PORT14, GearSetting.RATIO_18_1, False)  #INTAKE

motor_4 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)  #RIGHT PUNCHER

motor_5 = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)  #LEFT PUNCHER

motor_6 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)  #FLAPS

motor_7 = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)  #RIGHT extra drive

motor_8 = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)  #LEFT extra drive

vision_1__SIG_1 = Signature(1, -5269, -4855, -5062,-4995, -4473, -4734,8.8, 0)

vision = Vision(Ports.PORT15, 50, vision_1__SIG_1)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def intake(status = None):

    if controller_1.buttonL1.pressing() or status == "in":  #in
        motor_3.set_velocity(-100, PERCENT)
        motor_3.spin(FORWARD)
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(0,0)
        controller_1.screen.print("intaking")

    elif controller_1.buttonL2.pressing() or status == "out":  #out
        motor_3.set_velocity(100, PERCENT)
        motor_3.spin(FORWARD)

    else:
        motor_3.stop(HOLD)

def shooting(status = None):

    if controller_1.buttonR1.pressing() or status == "single": #Single shot
        motor_4.set_velocity(40, PERCENT)
        motor_5.set_velocity(40, PERCENT)

        motor_4.spin_for(FORWARD, 360, DEGREES, wait = False)
        motor_5.spin_for(REVERSE, 360, DEGREES)

def underpass(status = None):
    if controller_1.buttonDown.pressing():
        motor_4.set_velocity(60, PERCENT)
        motor_5.set_velocity(60, PERCENT)

        motor_4.spin_for(FORWARD, 90, DEGREES, wait = False)
        motor_5.spin_for(REVERSE, 90, DEGREES)

    if controller_1.buttonUp.pressing():
        motor_4.set_velocity(60, PERCENT)
        motor_5.set_velocity(60, PERCENT)

        motor_4.spin_for(FORWARD, -90, DEGREES, wait = False)
        motor_5.spin_for(REVERSE, -90, DEGREES)

def flaps(status = None):

    if controller_1.buttonRight.pressing() or status == "fout":
        motor_6.set_velocity(100, PERCENT)
        motor_6.spin_to_position(-200, DEGREES)
    
    elif controller_1.buttonLeft.pressing() or status == "fin":
        motor_6.set_velocity(100, PERCENT)
        motor_6.spin_to_position(0, DEGREES)

class Drive():

    def __init__(self):

        self.speeds = []

        self.input = {
            "axis_1":[0, 0],
            "axis_2":[0, 0],
            "axis_3":[0, 0],
            "axis_4":[0, 0],
        }

        self.triball_location = (0, 0)
        self.triball_size = (0, 0)
        self.axis = [0, 0, 0, 0]
        self.slow_mode = 0   # 0 = normal, 1 = slow mode

    def control_input(self, status):

        """
        A method which will store the controller axis positions in the 
        self.axis array
        """

        if status is None:  #Driver control

            self.axis[0] = controller_1.axis1.position()# Responsible for turning the robot left and right
            self.axis[1] = controller_1.axis2.position()
            self.axis[2] = controller_1.axis3.position()# Responsible for moving the robot forward and backward
            self.axis[3] = controller_1.axis4.position()

        elif status is not None:    #Auto control

            self.axis[0] = status[0]
            self.axis[2] = status[1]

        # Add magnitudes to the input dictionary
        direction = [0, 0, 0, 0]

        # Iterate through the axis list and check for axis that the user is currently 
        # pushing the joystick towards. Divide the absolute value of the axis value
        # by the axis value to preserve the sign of the magnitude, giving up the direction
        # the user is pointing the joystick in
        for i in range(4):
            if self.axis[i] != 0:
                direction[i] = abs(self.axis[i])/self.axis[i]

        if controller_1.buttonX.pressing():
            self.slow_mode = 1 - self.slow_mode
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

        self.input["axis_1"][0] = (self.input["axis_1"][0])**axis_1_cf
        self.input["axis_2"][0] = (self.input["axis_2"][0])**axis_2_cf
        self.input["axis_3"][0] = (self.input["axis_3"][0])**axis_3_cf
        self.input["axis_4"][0] = (self.input["axis_4"][0])**axis_4_cf


    def parallel_input_calculations(self):


        # Iterate through the motors in a slice of the speeds index

        # Set an initial velocity variable to the a vector representing the
        # moving joysticks state (axis 3)
        init_velocity = self.input["axis_3"][0] * self.input["axis_3"][1]

        if self.slow_mode:
            init_velocity /= 5

        self.speeds = [init_velocity for i in range(2)]

        # if we are moving the joystick forward or backward
        if self.input["axis_1"][0] != 0:

            # Set a rotation variable the velocity of the first axis
            rotation = self.input["axis_1"][0] * self.input["axis_1"][1] / 2

            if self.slow_mode:
                rotation /= 2

            # increment and decrement the speed array elements for the rear left and right motors to the 
            # velocity previously calculated rotation
            self.speeds[0] -= rotation
            self.speeds[1] += rotation

    def motor_speed(self):
        """
        Convert the speed previously calculated into motor velocities
        and spin the motors
        """
        motor_1.set_velocity(self.speeds[0], PERCENT)
        motor_2.set_velocity(self.speeds[1], PERCENT)
        motor_7.set_velocity(self.speeds[0], PERCENT)
        motor_8.set_velocity(self.speeds[1], PERCENT)

        motor_1.spin(REVERSE)
        motor_2.spin(FORWARD)
        motor_7.spin(REVERSE)
        motor_8.spin(FORWARD)
    
    def drive(self, status = None):
        drive_program.control_input(status)
        drive_program.control_input_modification()
        drive_program.parallel_input_calculations()
        drive_program.motor_speed()


class Auto(Drive):
    
    def __init__(self):
        self.driving_status = [0, 0]  #Decision output for driving, represented in [rotation, speed]
        self.intake_status = ""    #Decision output for the intake
        self.shooting_status = ""   #Decision output for the shooter
        self.loaded = False  #Status of triball in the shooter
        self.triball_location = (0, 0)
        self.triball_size = (0, 0)

    def sensor_inputs(self):
        """Take the information from each sensor and motor and organize them"""
        ##VISION## 

        # Take the snapshot
        object = vision.take_snapshot(vision_1__SIG_1)

        # If there is a valid object
        if object is not None:

            # Create 2 tuples with the center x and y values of the closest triball as the object as well as the size of the object 
            self.triball_location = (vision.largest_object().centerX, vision.largest_object().centerY)

            self.triball_size = (vision.largest_object().width, vision.largest_object().height)
        
        # If there is no valid object
        elif object is None:
            self.triball_size = (0, 0)


    def general_objective(self):
        """Take the sensor input and decide what appropriate action should be taken"""

            #Once the triball have been picked up, stop the intake and declare the robot loaded
        if (self.triball_location[1]) > 195:
            self.intake_status = "in"
            self.loaded = True
        else:
            self.loaded = False

        if not self.loaded:


            self.intake_status = "in"
            
            # If the recognized object is closer to the right side of the vision
            # sensors FOV then upload information to the input dictionary
            # to make the robot slowly rotate move to the right
            if (self.triball_location[0]) > 160:
                self.driving_status[0] = 25
                controller_1.screen.print("right ")

            # Repeat the same code from above but this time with the left side
            elif (self.triball_location[0]) < 140:
                self.driving_status[0] = -25
                controller_1.screen.print("left ")

            # If the object is in between these margins then do not rotate
            else:
                self.driving_status[0] = 0
                controller_1.screen.print("center ")

            # Head towards the triball
            if self.triball_size != (0,0):
                self.driving_status[1] = 50
                controller_1.screen.print("forward", self.triball_size)                

            
            #if we cant detect any object, rotate and scan
            elif self.triball_size == (0,0):
                self.driving_status[1] = 0
                self.driving_status[0] = 100
            

    def decision_output(self):
        """Take the generated decisions and execute them"""
        self.drive(self.driving_status)
        intake(status = self.intake_status)

    def auto_main(self):
        
        self.sensor_inputs()
        self.general_objective()
        self.decision_output()


class Recovery():
    
    def __init__(self):
        pass
    def shooter(self):
        if controller_1.buttonR1.pressing():
            motor_4.set_velocity(10, PERCENT)
            motor_4.spin(FORWARD)
        elif controller_1.buttonR2.pressing():
            motor_4.set_velocity(10, PERCENT)
            motor_4.spin(REVERSE)
        
        else:
            motor_4.stop(HOLD)
        
        if controller_1.buttonL1.pressing():
            motor_5.set_velocity(10, PERCENT)
            motor_5.spin(FORWARD)
        elif controller_1.buttonL2.pressing():
            motor_5.set_velocity(10, PERCENT)
            motor_5.spin(REVERSE)

        else:
            motor_5.stop(HOLD)


    def flaps(self):
        if controller_1.buttonLeft.pressing():
            motor_6.set_velocity(10, PERCENT)
            motor_6.spin(FORWARD)
        elif controller_1.buttonRight.pressing():
            motor_6.set_velocity(10, PERCENT)
            motor_6.spin(REVERSE)
        else:
            motor_6.stop(HOLD)
    def execute(self):
        self.flaps()
        self.shooter()

drive_program = Drive()
auto_drive = Auto()
recovery = Recovery()

def display(recovery_status):
    if recovery_status:
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(0,0)
        controller_1.screen.print("RECOVERY MODE")
        controller_1.screen.new_line()

    elif not recovery_status:
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(0,0)

        if drive_program.slow_mode:
            controller_1.screen.print("SLOW MODE")
        elif not drive_program.slow_mode:
            controller_1.screen.print("NORMAL MODE")
        controller_1.screen.new_line()

    controller_1.screen.print("Battery:", brain.battery.capacity(), "%")


#Driver

speed = 50
recovery_mode = False
controlled = False
# print("STARTING")
while controlled == False:
    motor_3.spin_for(REVERSE, 1, SECONDS)
    controlled = True
while controlled == True:
    while recovery_mode:
        recovery.execute()
        if controller_1.buttonB.pressing():
            recovery_mode = False
        display(recovery_mode)
        wait(1/60, SECONDS)

    while not recovery_mode:
        drive_program.drive()
        intake()
        shooting()
        flaps() #WORKS
        underpass()
        if controller_1.buttonB.pressing(): #WORKS
            recovery_mode = True
        display(recovery_mode)
        wait(1/60, SECONDS)

#Automatic
# motor_3.set_velocity(-100, PERCENT)
# motor_3.spin(FORWARD)

# while True:
#     auto_drive.auto_main()
#     wait(1/60, SECONDS)

#     if controller_1.buttonX.pressing():
#         break