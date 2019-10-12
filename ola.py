#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from time import sleep

import atexit

class Panu:
    sound = Sound()

    color_sensor = ColorSensor(address=INPUT_1)
    drive = MoveTank(OUTPUT_A, OUTPUT_B)

    def goodbye():
        self.drive.stop()
        

    atexit.register(goodbye)

    last_backtrack_direction = "left"

    def good_color(self, rgb):
        return rgb[0] + rgb[1] + rgb[2] > 200

    def yellow_color(self, rgb):
        return rgb[2] < 50 and rgb[2] < rgb[0] / 1.5 and rgb[2] < rgb[1] / 1.5 and rgb[0] > 75

    def green_color(self, ):
        color = self.color_sensor.color
        return color == ColorSensor.COLOR_GREEN

    def backtrack(self, direction):

        turn_amount = 1

        last_backtrack_direction = direction

        if (direction == "left"):
            left_motor = SpeedPercent(30)
            right_motor = SpeedPercent(-30)
        elif (direction == "right"):
            left_motor = SpeedPercent(-30)
            right_motor = SpeedPercent(30)

        rgb = self.color_sensor.rgb
        while (not self.good_color(rgb) and not self.yellow_color(rgb)):

            self.drive.on_for_seconds(left_motor, right_motor, 0.1*turn_amount, block=False)
            
            timer_countdown = 0

            while ((not self.good_color(rgb) and not self.yellow_color(rgb)) and timer_countdown < 0.1*turn_amount):
                timer_countdown += 0.01
                sleep(0.01)
                rgb = self.color_sensor.rgb
                # do nothing
            self.drive.stop()

            if (self.good_color(rgb) or self.yellow_color(rgb)):
                #intended overshoot to get to the center of the tape
                #should be modified to rely on the intensity of light with a max value similar to the one in this if clause
                self.drive.on_for_seconds(left_motor, right_motor, 0.1)

            rgb = self.color_sensor.rgb

            right_motor, left_motor = left_motor, right_motor

            turn_amount *= 2

            # if (last_backtrack_direction == "left"):
            #     last_backtrack_direction = "right"
            # else:
            #     last_backtrack_direction = "left"


    def find_track(self):
        self.backtrack(self.last_backtrack_direction)

    def force_back_and_turn_left(self):
        self.drive.on_for_seconds(100,100,1.0)
        sleep(5.0)
        self.drive.on_for_seconds(-100, -100, 2.5)
        self.drive.on_for_seconds(100, 0, 1.5)
        self.drive.on_for_seconds(100, 100, 0.5)

    def find_line(self):
        rgb = self.color_sensor.rgb
        left_motor = SpeedPercent(50)
        right_motor = SpeedPercent(25)
        while (not self.good_color(rgb)):
            timer_countdown = 0

            self.drive.on_for_seconds(left_motor, right_motor, 1, block=False)
            while ((not self.good_color(rgb) and not self.yellow_color(rgb)) and timer_countdown < 0.1*turn_amount):
                timer_countdown += 0.01
                sleep(0.01)
                rgb = self.color_sensor.rgb
                # do nothing

            right_motor, left_motor = left_motor, right_motor
            rgb = self.color_sensor.rgb

        self.drive.stop(brake=True)


    def main(self):
        self.find_line()

        self.color_sensor.calibrate_white()
        
        while True:
            rgb = self.color_sensor.rgb
            while(self.good_color(rgb)):
                self.drive.on(SpeedPercent(80), SpeedPercent(80))
                rgb = self.color_sensor.rgb
                if (self.yellow_color(rgb)):
                    print(str(self.color_sensor.rgb))
                    self.drive.stop(brake=True)
                    self.force_back_and_turn_left()
            self.drive.stop(brake=True)
            if (self.green_color()):
                self.drive.stop(brake=True)
                self.sound.speak("Move aside, MEATBAGS!")
            self.find_track()

    if __name__ == "__main__":
        main()
