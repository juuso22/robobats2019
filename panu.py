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

def good_luminance():
    return color_sensor.reflected_light_intensity > 50

def good_color(rgb):
    return rgb[0] + rgb[1] + rgb[2] > 200

def yellow_color(rgb):
    return rgb[2] < 50 and rgb[2] < rgb[0] / 2 and rgb[2] < rgb[1] / 2 and rgb[0] > 75

def green_color():
    color = color_sensor.color
    return color == ColorSensor.COLOR_GREEN

def backtrack(direction):

    turn_amount = 1

    last_backtrack_direction = direction

    if (direction == "left"):
        left_motor = SpeedPercent(30)
        right_motor = SpeedPercent(-30)
    elif (direction == "right"):
        left_motor = SpeedPercent(-30)
        right_motor = SpeedPercent(30)

    while (not good_luminance()):

        drive.on_for_seconds(left_motor, right_motor, 0.1*turn_amount, block=False)
        
        timer_countdown = 0

        while (not good_luminance() and timer_countdown < 0.1*turn_amount):
            timer_countdown += 0.01
            sleep(0.01)
            # do nothing
        drive.stop()

        if (not good_luminance()):
            #intended overshoot to get to the center of the tape
            #should be modified to rely on the intensity of light with a max value similar to the one in this if clause
            drive.on_for_seconds(left_motor, right_motor, 0.1)

        right_motor, left_motor = left_motor, right_motor

        turn_amount *= 2

      #  if (right_motor > left_motor):
      #      last_backtrack_direction = "right"
      #  else:
      #      last_backtrack_direction = "left"


def find_track():
    backtrack(last_backtrack_direction)

def force_back_and_turn_left():
    drive.on_for_seconds(100,100,0.5)
    sleep(5.0)
    drive.on_for_seconds(-100, -100, 1)
    drive.on_for_seconds(100, -100, 1.0)
    while (not good_luminance()):
        drive.on(80, 80)
    drive.stop(brake=True)
    last_backtrack_direction = 'left'

def find_line():
    drive.on_for_seconds(100,100,2)
    left_motor = SpeedPercent(50)
    right_motor = SpeedPercent(25)
    turn_amount = 10
    while(good_luminance() == False):
        timer_countdown = 0

        drive.on_for_seconds(left_motor, right_motor, 1, block=False)
        while(good_luminance() == False and timer_countdown < 0.1*turn_amount):
            timer_countdown += 0.01
            sleep(0.01)
            # do nothing
        drive.stop()

        right_motor, left_motor = left_motor, right_motor

    drive.stop(brake=True)


def main():
    find_line()

    #color_sensor.calibrate_white()
    
    while True:
        while(good_luminance() == True):
            drive.on(SpeedPercent(50), SpeedPercent(50))
            rgb = color_sensor.rgb
            if (yellow_color(rgb) == True):
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
