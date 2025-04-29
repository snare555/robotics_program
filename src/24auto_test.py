from vex import *
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)

motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)  #LEFT DRIVE

motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)  #RIGHT DRIVE

motor_3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)  #INTAKE

motor_4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)  #SHOOTER

motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)  

motor_6 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)  

motor_7 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)  

motor_8 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)  

vision_1__SIG_1 = Signature(1, -5269, -4855, -5062,-4995, -4473, -4734,8.8, 0)

vision = Vision(Ports.PORT10, 50, vision_1__SIG_1)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def intake(status = None):

    if controller_1.buttonR1.pressing() or status == "in":  #in
        motor_3.set_velocity(-200)
        motor_3.spin(FORWARD)

    elif controller_1.buttonR2.pressing() or status == "out":  #out
        motor_3.set_velocity(200)
        motor_3.spin(FORWARD)

    else:
        motor_3.stop(COAST)

def shooting(status = None):

    if controller_1.buttonA.pressing() or status == "single": #Single shot
        motor_4.set_velocity(200)
        motor_4.spin_for(FORWARD, 1800, DEGREES)

    elif controller_1.buttonB.pressing() or status == "auto":   #Automatic
        motor_4.set_velocity(200)
        motor_4.spin(FORWARD)

    elif controller_1.buttonY.pressing() or status == "reset":   #Return to cocked position
        motor_4.set_position(0)

    else:
        motor_3.stop(COAST)



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
            self.speeds[0] += rotation
            self.speeds[1] -= rotation

    def motor_speed(self):
        """
        Convert the speed previously calculated into motor velocities
        and spin the motors
        """
        motor_1.set_velocity(self.speeds[0]*2)
        motor_2.set_velocity(self.speeds[1]*2)

        motor_1.spin(FORWARD)
        motor_2.spin(REVERSE)
    
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
        self.loaded = True  #Status of triball in the shooter
        self.primed = True  #Status of the shooter position
        self.triball_location = (0, 0)
        self.triball_size = (0, 0)

    def sensor_inputs(self):
        """Take the information from each sensor and motor and organize them"""
        if motor_4.position == 0:   #add primed position calculation later         %%Not Done%%
            self.primed = True
        
        else:
            self.primed = False

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

        if not self.loaded:
            
            # If the recognized object is closer to the right side of the vision
            # sensors FOV then upload information to the input dictionary
            # to make the robot slowly rotate move to the right
            if (self.triball_location[0]) > 190:
                self.driving_status[0] = 50
                controller_1.screen.print("right ")

            # Repeat the same code from above but this time with the left side
            elif (self.triball_location[0]) < 110:
                self.driving_status[0] = -50
                controller_1.screen.print("left ")

            # If the object is in between these margins then do not rotate
            else:
                self.driving_status[0] = 0
                controller_1.screen.print("center ")

            # Head towards the triball
            if (self.triball_size[0] * self.triball_size[1]) < 2600 and (self.triball_size[0] * self.triball_size[1]) > 50:
                self.driving_status[1] = 50
                controller_1.screen.print("forward", self.triball_size)
            
            # If the size of the object is larger than 2600 then prime the intake in preperation for tribal contact
            if (self.triball_size[0] * self.triball_size[1]) > 2600:
                self.intake_status = "in"

            #Once the triball have been picked up, stop the intake and declare the robot loaded
            elif (self.triball_size[0] * self.triball_size[1]) > 3600:
               self.intake_status = ""
               self.loaded = True
            
            #if we cant detect the object, rotate and scan
            elif self.triball_size == (0,0):
                self.driving_status[0] = 100
            
        elif self.loaded:   #Aim and shoot

            #Aim the robot (I really don't fucking know how we can do this without an actual field)
            self.shooting_status = "single"

        # Once the robot have shot the triball, return to priming position
        if not self.primed:
            self.shooting_status = "reset"

    def decision_output(self):
        """Take the generated decisions and execute them"""
        self.drive(self.driving_status)
        intake(self.intake_status)
        shooting(self.shooting_status)

    def auto_main(self):
        
        self.sensor_inputs()
        self.general_objective()
        self.decision_output()

drive_program = Drive()
auto_drive = Auto()

def display():
    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(0,0)
    controller_1.screen.clear_screen()
    controller_1.screen.print("Battery capacity: ", brain.battery.capacity())
    controller_1.screen.new_line()

    if drive_program.slow_mode:
        controller_1.screen.print("Slow mode")
    elif not drive_program.slow_mode:
        controller_1.screen.print("Normal mode")

#Driver

while True:

    drive_program.drive()
    intake()
    shooting()
    display()
    wait(1/60, SECONDS)

#Automatic

# while True:
#     auto_drive.auto_main()
#     if controller_1.buttonX.pressing():
#         break

