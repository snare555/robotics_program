#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
# vex-vision-config:begin
vision_1__OBJECT_1 = Signature(1, 6355, 9133, 7744,-1, 693, 346,3.7, 0)
vision_1 = Vision(Ports.PORT6, 50, vision_1__OBJECT_1)
# vex-vision-config:end

motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor_3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
motor_4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)



# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Begin project code

# while True:
#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)

#     object = vision_1.take_snapshot(vision_1__OBJECT_1)
#     if object is not None:
#         brain.screen.print("Center X: ", vision_1.largest_object().centerX)
#         brain.screen.next_row()
#         brain.screen.print("Center Y: ", vision_1.largest_object().centerY)
#         brain.screen.next_row()
#         brain.screen.print("Width: ", vision_1.largest_object().width)
#         brain.screen.next_row()
#         brain.screen.print("Height: ", vision_1.largest_object().height)
#         brain.screen.next_row()


#     elif object is None:
#         brain.screen.print("None")
#         brain.screen.next_row()

#     wait(0.2,SECONDS)

while True:
    
    
    object = vision_1.take_snapshot(vision_1__OBJECT_1)

    if object is not None:
        if vision_1.largest_object().centerX > 160:
            speed = (vision_1.largest_object().centerX - 160) * 0.6
            motor_1.set_velocity(speed)
            motor_2.set_velocity(speed)
            motor_3.set_velocity(speed)
            motor_4.set_velocity(speed)
            brain.screen.print("right")

        elif vision_1.largest_object().centerX < 140:
            speed = (140 - vision_1.largest_object().centerX) * -0.6
            motor_1.set_velocity(speed)
            motor_2.set_velocity(speed)
            motor_3.set_velocity(speed)
            motor_4.set_velocity(speed)
            brain.screen.print("left")

        else:
            motor_1.set_velocity(0)
            motor_2.set_velocity(0)
            motor_4.set_velocity(0)
            motor_3.set_velocity(0)
            brain.screen.print("centered")
        brain.screen.next_row()
        brain.screen.print(vision_1.largest_object().width * vision_1.largest_object().height)

    else:
        brain.screen.print("No object")
        motor_1.set_velocity(0)
        motor_2.set_velocity(0)
        motor_4.set_velocity(0)
        motor_3.set_velocity(0)

    motor_1.spin(FORWARD)
    motor_2.spin(FORWARD)
    motor_3.spin(FORWARD)
    motor_4.spin(FORWARD)

    wait(0.2, SECONDS)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


