#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

controller_1 = Controller(PRIMARY)

motor_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

motor_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)
# Begin project code

controller_1.screen.clear_screen()
controller_1.screen.set_cursor(0, 0)


speed = 50
spin = False
while True:
    controller_1.screen.clear_line(3)
    controller_1.screen.print("Speed: ", speed)
    if controller_1.buttonA.pressing():
        spin = True
    elif controller_1.buttonX.pressing():
        spin = False

    while spin:
        motor_1.spin_for(FORWARD, 360, velocity = speed, units_v = PERCENT, wait=False)
        motor_2.spin_for(REVERSE, 360, velocity = speed, units_v = PERCENT)

    
    if controller_1.buttonB.pressing():
        motor_1.set_velocity(-speed, PERCENT)
        motor_1.spin(FORWARD)
        motor_2.set_velocity(-speed, PERCENT)
        motor_2.spin(REVERSE)
    else:
        motor_1.stop(COAST)
        motor_2.stop(COAST)

    if controller_1.buttonUp.pressing() and speed < 100:
        speed += 2
    elif controller_1.buttonDown.pressing() and speed > 0:
        speed -= 2
    wait(30, MSEC)



