#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project: Right Starting
#	Author:
#	Created:
#	Configuration:
# 
# ------------------------------------------

# Library imports
from vex import *
import math

# Begin project code

# Robot configuration code 

controller_1 = Controller(PRIMARY) #test  

motor_1 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)  #RIGHT DRIVE 

motor_2 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)  #LEFT DRIVE 

motor_7 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)  #RIGHT extra drive 

motor_8 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)  #LEFT extra drive 

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
 
    def control_input(self, status = None): 
 
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
 
        if controller_1.buttonB.pressing(): 
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
         
    def drive(self): 
        drive_program.control_input() 
        drive_program.control_input_modification() 
        drive_program.parallel_input_calculations() 
        drive_program.motor_speed() 
 
drive_program = Drive() 


while True:
    drive_program.drive() 
