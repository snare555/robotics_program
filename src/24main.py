#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

# hello
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
# 	Project:
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

motor_2 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)  #LEFT DRIVE 

motor_3 = Motor(Ports.PORT14, GearSetting.RATIO_18_1, False)  #INTAKE 

motor_4 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)  #RIGHT PUNCHER 

motor_5 = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)  #LEFT PUNCHER 

motor_6 = Motor(Ports.PORT12, GearSetting.RATIO_36_1, False)  #FLAPS 

motor_7 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)  #RIGHT extra drive 

motor_8 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)  #LEFT extra drive 


def pre_autonomous():
    # actions to do when the program starts
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(1, SECONDS)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("right side / match load autonomous code")
    # place automonous code here

    motor_1.set_velocity(30, PERCENT) 
    motor_2.set_velocity(15, PERCENT) 
    motor_7.set_velocity(30, PERCENT) 
    motor_8.set_velocity(15, PERCENT)
    motor_3.set_velocity(60, PERCENT)

    motor_2.spin_for(FORWARD, 1.25, TURNS, wait = False)
    motor_8.spin_for(FORWARD, 1.25, TURNS)

    motor_1.set_velocity(30, PERCENT) 
    motor_7.set_velocity(30, PERCENT) 
    motor_1.spin_for(REVERSE, 1.5, TURNS, wait = False) 
    motor_2.spin_for(FORWARD, 1.5, TURNS, wait = False) 
    motor_7.spin_for(REVERSE, 1.5, TURNS, wait = False) 
    motor_8.spin_for(FORWARD, 1.5, TURNS) 
 
    motor_2.set_velocity(15, PERCENT)  
    motor_8.set_velocity(15, PERCENT)
    motor_1.set_velocity(15, PERCENT)  
    motor_7.set_velocity(15, PERCENT)
    
    motor_1.spin_for(REVERSE, 1, TURNS, wait = False)
    motor_7.spin_for(REVERSE, 1, TURNS, wait = False)
    motor_2.spin_for(REVERSE, 0.8, TURNS)
    motor_8.spin_for(REVERSE, 0.8, TURNS)

    motor_2.set_velocity(30, PERCENT)  
    motor_8.set_velocity(30, PERCENT)
    motor_1.set_velocity(30, PERCENT)  
    motor_7.set_velocity(30, PERCENT)
    motor_3.spin_for(REVERSE, 10, TURNS, wait = False)    
    motor_1.spin_for(REVERSE, .8, TURNS, wait = False) 
    motor_2.spin_for(FORWARD, .8, TURNS, wait = False) 
    motor_7.spin_for(REVERSE, .8, TURNS, wait = False) 
    motor_8.spin_for(FORWARD, .8, TURNS)
# anything jgjgj
    wait(2, SECONDS)
    
    motor_1.spin_for(FORWARD, .75, TURNS, wait = False)
    motor_7.spin_for(FORWARD, .75, TURNS)
   

    motor_2.spin_for(REVERSE, 1.2, TURNS, wait = False)
    motor_8.spin_for(REVERSE, 1.2, TURNS, wait = False)
    motor_1.spin_for(FORWARD, 1.2, TURNS, wait = False)
    motor_7.spin_for(FORWARD, 1.2, TURNS)

  



def user_control():
    brain.screen.clear_screen()

    speed = 50 
    # place driver control in this while loop
    def intake(): 

        if controller_1.buttonL1.pressing():  #in 
            motor_3.set_velocity(-100, PERCENT) 
            motor_3.spin(FORWARD) 
            controller_1.screen.clear_screen() 
            controller_1.screen.set_cursor(0,0) 
            controller_1.screen.print("intaking")  

        elif controller_1.buttonL2.pressing():  #out 
            motor_3.set_velocity(100, PERCENT) 
            motor_3.spin(FORWARD) 
 
        else: 
            motor_3.stop(HOLD) 

    def shooting(): 

        if controller_1.buttonX.pressing(): #Single shot 
            motor_4.set_velocity(50, PERCENT) 
            motor_5.set_velocity(50, PERCENT)  

            motor_4.spin_for(FORWARD, 600, DEGREES, wait = False) 
            motor_5.spin_for(REVERSE, 600, DEGREES) 

    def underpass(): 
        if controller_1.buttonDown.pressing(): 
            motor_4.set_velocity(60, PERCENT) 
            motor_5.set_velocity(60, PERCENT) 

            motor_4.spin_for(FORWARD, 150, DEGREES, wait = False) # need to double check numbers
            motor_5.spin_for(REVERSE, 150, DEGREES) 

 

        if controller_1.buttonUp.pressing(): 
            motor_4.set_velocity(60, PERCENT) 
            motor_5.set_velocity(60, PERCENT) 

 
            motor_4.spin_for(FORWARD, -150, DEGREES, wait = False) # need to double check numbers
            motor_5.spin_for(REVERSE, -150, DEGREES) 

 

    def flaps():  

        if controller_1.buttonR1.pressing(): 
            motor_6.set_velocity(60, PERCENT) 
            motor_6.spin_to_position(150, DEGREES) 
            brain.screen.print(motor_6.position(DEGREES))

        if controller_1.buttonR2.pressing(): 
            motor_6.set_velocity(60, PERCENT) 
            motor_6.spin_to_position(0, DEGREES)
            brain.screen.print(motor_6.position(DEGREES))


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


    while True:
        drive_program.drive() 
        intake() 
        shooting() 
        flaps() #WORKS 
        underpass()  
        wait(1/60, SECONDS) 

 

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()
