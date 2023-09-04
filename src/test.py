#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

controller_1 = Controller(PRIMARY)

motor_1 = Motor(Ports.PORT19, GearSetting.RATIO_36_1, False)

motor_2 = Motor(Ports.PORT20, GearSetting.RATIO_36_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)
# Begin project code

controller_1.screen.clear_screen()

speed = 50
max_torque_1 = 0
max_torque_2 = 0

while True:
    controller_1.screen.clear_line(0)
    controller_1.screen.set_cursor(0, 0)
    controller_1.screen.print("Speed:", speed)
    controller_1.screen.clear_line(1)
    controller_1.screen.new_line()
    controller_1.screen.print("Positions:", motor_1.position(), motor_2.position())
    controller_1.screen.new_line()
    if motor_1.torque() > max_torque_1:
        max_torque_1 = motor_1.torque()
    if motor_2.torque() > max_torque_2:
        max_torque_2 = motor_2.torque()
    controller_1.screen.print("Max torque:", max_torque_1, ",", max_torque_2)
    if controller_1.buttonA.pressing():
        motor_1.set_velocity(speed, PERCENT)
        motor_1.spin(FORWARD)
        motor_2.set_velocity(speed, PERCENT)
        motor_2.spin(REVERSE)
    elif controller_1.buttonB.pressing():
        motor_1.set_velocity(-speed, PERCENT)
        motor_1.spin(FORWARD)
        motor_2.set_velocity(-speed, PERCENT)
        motor_2.spin(REVERSE)
    else:
        motor_1.stop(HOLD)
        motor_2.stop(HOLD)


    if controller_1.buttonUp.pressing() and speed < 100:
        speed += 2
    elif controller_1.buttonDown.pressing() and speed > 0:
        speed -= 2
    wait(30, MSEC)



