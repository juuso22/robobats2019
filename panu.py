#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from time import sleep

import atexit

sound = Sound()

color_sensor = ColorSensor(address=INPUT_1)
drive = MoveTank(OUTPUT_A, OUTPUT_B)

def goodbye():
    drive.stop()
    

atexit.register(goodbye)

last_backtrack_direction = "left"

def good_color():
    rgb = color_sensor.rgb
    return rgb[0] + rgb[1] + rgb[2] > 300

def yellow_color():
    rgb = color_sensor.rgb
    return rgb[2] < 50 and rgb[2] < rgb[0] / 2 and rgb[2] < rgb[1] / 2 and rgb[0] > 75

def green_color():
    color = color_sensor.color
    return color == ColorSensor.COLOR_GREEN

def backtrack(direction):

    turn_amount = 1

    last_backtrack_direction = direction

    if (direction == "left"):
        left_motor = SpeedPercent(100)
        right_motor = SpeedPercent(-70)
    elif (direction == "right"):
        left_motor = SpeedPercent(-70)
        right_motor = SpeedPercent(100)

    while (good_color() == False):

        drive.on_for_seconds(left_motor, right_motor, 0.1*turn_amount, block=False)
        
        timer_countdown = 0

        while (good_color() == False and timer_countdown < 0.1*turn_amount):
            timer_countdown += 0.01
            sleep(0.01)
            # do nothing
        drive.stop()

        if (good_color() == True):
            #intended overshoot to get to the center of the tape
            #should be modified to rely on the intensity of light with a max value similar to the one in this if clause
            drive.on_for_seconds(left_motor, right_motor, 0.1)

        right_motor, left_motor = left_motor, right_motor

        turn_amount *= 2

        if (last_backtrack_direction == "left"):
            last_backtrack_direction = "right"
        else:
            last_backtrack_direction = "left"


def find_track():
    backtrack(last_backtrack_direction)

def force_back_and_turn_left():
    drive.on_for_seconds(-100, -100, 1.5)
    drive.on_for_seconds(0, 100, 0.5)
    drive.on_for_seconds(100, 100, 0.5)

def main():
    color_sensor.calibrate_white()
    while True:
        while(good_color() == True):
            drive.on(SpeedPercent(100), SpeedPercent(100))
            if (yellow_color() == True):
                print(str(color_sensor.rgb))
                drive.stop(brake=True)
                force_back_and_turn_left()
        drive.stop(brake=True)
        if (green_color() == True):
            drive.stop(brake=True)
            sound.speak("Move aside, MEATBAGS!")
        find_track()

if __name__ == "__main__":
    main()
