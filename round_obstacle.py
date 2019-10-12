#!/usr/bin/env python3
from ev3dev2.motor import MoveJoystick, MoveDifferential, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from ev3dev2.wheel import EV3Tire
import time
import code

steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
# Params: Andle (-100 to 100), speed (percent, 0 to 100), seconds it drives.

LEFT = -1
RIGHT = 1

color_sensor = ColorSensor(address=INPUT_1)
infrared_sensor = InfraredSensor(INPUT_2)

def drive_until_proximity(proximity, direction):
    steering_drive.on(direction, SpeedPercent(-100))
    while (infrared_sensor.proximity > proximity):
        time.sleep(0.2)
        print('Infrared sensor is ' + str(infrared_sensor.proximity))
    steering_drive.off()



#steering_drive.on_for_seconds(0, SpeedPercent(-100), 2)
def wait_and_drive(direction, proximity, maxholes = 0, sleep_time = 0.3): 
    last_proximity = 0
    i = 0
    while True:
        curr_prox = infrared_sensor.proximity
        if (curr_prox < proximity):
            last_proximity = curr_prox
            time.sleep(0.2)
            print('Infrared sensor is ' + str(curr_prox))
            continue
        elif(last_proximity >= proximity):
            last_proximity = curr_prox
            time.sleep(0.1)
            print('Infrared sensor is ' + str(curr_prox))
            continue
        elif(i < maxholes):
            last_proximity = curr_prox
            i += 1
            print('Found first aukko')
            continue
        else:
            break

    time.sleep(sleep_time)
    print('CHARGE')
    drive_until_proximity(40, 15 * RIGHT)
# code.interact(local = locals())

drive_until_proximity(40, 0)
wait_and_drive(15 * RIGHT, 75, maxholes = 1, sleep_time = 0.5)
drive_until_proximity(40, 0)
wait_and_drive(15 * RIGHT, 75, maxholes = 2, )




# go straight

# turn left

# go straight

# turn right

# Move to conter

# Face to the right direction


