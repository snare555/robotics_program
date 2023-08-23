#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

controller_1 = Controller(PRIMARY)

motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_36_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)
# Begin project code

controller_1.screen.clear_screen()
controller_1.screen.set_cursor(0, 0)
controller_1.screen.print("port 1 = green")
controller_1.screen.new_line()
controller_1.screen.print("port 2 = red")


while True:
    if controller_1.buttonA.pressing():
        motor_1.set_velocity(100, PERCENT)
        motor_1.spin(FORWARD)
        motor_2.set_velocity(100, PERCENT)
        motor_2.spin(FORWARD)
    elif controller_1.buttonB.pressing():
        motor_1.set_velocity(-100, PERCENT)
        motor_1.spin(FORWARD)
        motor_2.set_velocity(-100, PERCENT)
        motor_2.spin(FORWARD)
    else:
        motor_1.stop(COAST)
        motor_2.stop(COAST)#hello
