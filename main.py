#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


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
# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       codespace                                                    #
# 	Created:      3/20/2025, 9:02:32 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
controller = Controller()

brain.screen.print("Hello V5")


exponent = 1.25

# Claw machine motion variables
x_speed = 0
y_speed = 0

# Either -1 or 1; defines which direction the claw is moving
x_dir = 1
y_dir = 1

# These will stop the motors if the torque exceeds 50%
x_limit = False
y_limit = False

# Define motors
x_motor_1 = Motor(Ports.PORT2)
x_motor_2 = Motor(Ports.PORT13)

y_motor = Motor(Ports.PORT12)

claw_rotation_motor = Motor(Ports.PORT11)
claw_depression_motor = Motor(Ports.PORT3)

def set_claw_depression():
    if controller.buttonR1.pressing():
        claw_depression_motor.spin(REVERSE, 50)
    elif controller.buttonR2.pressing():
        claw_depression_motor.spin(FORWARD, 50)
    else:
        claw_depression_motor.stop()

def set_claw_rotation():
    if controller.axis1.position() > 10:
        claw_rotation_motor.spin(FORWARD, 50)
    elif controller.axis1.position() < -10:
        claw_rotation_motor.spin(REVERSE, 50)
    else:
        claw_rotation_motor.stop()
# Sets the direction of motion
def set_claw_dir():
    global x_dir, y_dir
    if(abs(controller.axis4.position()) > 5):
        y_dir = controller.axis4.position()/abs(controller.axis4.position())
    if(abs(controller.axis3.position()) > 5):
        x_dir = -controller.axis3.position()/abs(controller.axis3.position())

# Sets the speed of the claw motors
def set_claw_speed():
    global x_speed, y_speed, exponent

    # Speed should be raised to some power for better control
    y_speed = abs(controller.axis4.position()**exponent)
    x_speed = abs(controller.axis3.position()**exponent)

    # Speed should not exceed 100
    if x_speed > 100:
        x_speed = 100

    if y_speed > 100:
        y_speed = 100

# Commands the motors
def move_motor():
    global x_speed, y_speed, x_dir, y_dir, x_limit, y_limit

    if x_speed > 5 and not x_limit:
        x_motor_1.spin(REVERSE, x_speed*x_dir)
        x_motor_2.spin(FORWARD, x_speed*x_dir)
    else:
        x_motor_1.stop()
        x_motor_2.stop()

    if y_speed > 5 and not y_limit:
        y_motor.spin(FORWARD, y_speed*y_dir)
    else:
        y_motor.stop()
    
# Limit torque
def limit():
    global x_limit, y_limit, x_speed, y_speed

    if x_motor_1.torque() > 0.5 or x_motor_2.torque() > 0.5:
        x_limit = True
    if y_motor.torque() > 0.5:
        y_limit = True
    
    # Set limits to false if conditions are met
    if x_limit and x_speed == 0:
        x_limit = False
    if y_limit and y_speed == 0:
        y_limit = False

def main():
    while True:
        set_claw_dir()
        set_claw_speed()
        move_motor()
        set_claw_depression()
        set_claw_rotation()
        # limit()
        wait(10, MSEC)

main()


        
