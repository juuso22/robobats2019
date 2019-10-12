#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import time

class LineFollowerTest:
    TIME_STEP = 0.1
    SEARCH_MAX_STEPS = 8
    FORWARD_SPEED = 50
    SEARCH_SPEED = 25
    STEPS_PER_SECOND = 1 / TIME_STEP
    LEFT = -1
    RIGHT = 1
    VEERING_THRESHOLD = 10000  # Veering off

    def __init__(self, movesteering, colorsensor):
        self.steering_drive = movesteering
        self.color_sensor = colorsensor
        self.last_search_direction = 1
        self.last_brightness = 1000

    def on_track(self):
        self.last_brightness
        red = self.color_sensor.red
        green = self.color_sensor.green
        blue = self.color_sensor.blue

        self.last_brightness = red + green + blue

        color = self.color_sensor.color
        return color == 6

    def move_while_on_track(self, direction, speed):
        self.last_brightness = 1000
        brightness = self.last_brightness
        self.steering_drive.on_for_seconds(0, SpeedPercent(-speed), LineFollowerTest.TIME_STEP * LineFollowerTest.STEPS_PER_SECOND * 10, False, False)
        while self.on_track():
            print(self.last_brightness)
            effective_direction = direction
            if self.last_brightness < brightness - LineFollowerTest.VEERING_THRESHOLD:
                effective_direction = self.last_search_direction * 10
                print('Veering ' + direction_name(self.last_search_direction))
            #self.steering_drive.on_for_seconds(effective_direction, SpeedPercent(-speed), LineFollowerTest.TIME_STEP, False)
            brightness = self.last_brightness

        self.steering_drive.off(None, False)

    def move_until_on_track(self, direction, speed, max_steps):
        i = 0
        self.steering_drive.on_for_seconds(direction, SpeedPercent(-speed), LineFollowerTest.TIME_STEP * max_steps, False, False)
        while (self.steering_drive.is_running or self.steering_drive.is_ramping) and not self.on_track() and self.color_sensor.color != 6:
            #self.steering_drive.on_for_seconds(direction, SpeedPercent(-speed), LineFollowerTest.TIME_STEP, False)
            i = i + 1
            #if i >= max_steps:
            #    break

        self.steering_drive.off(None, False)
        #if i < max_steps:
        if self.on_track():
            return -1
        else:
            return i

    def direction_name(self, turn_direction):
        if turn_direction < 0:
            return 'LineFollowerTest.LEFT'
        else:
            return 'right'

    def turn_and_seek(self, max_turn_steps, turn_direction):
        name = self.direction_name(turn_direction)
        print('Turn ' + name)
        result = self.move_until_on_track(100 * turn_direction, LineFollowerTest.SEARCH_SPEED, max_turn_steps)
        if result == -1:
            return True
        print('Turn back')
        self.steering_drive.on_for_seconds(100 * turn_direction * -1, SpeedPercent(-LineFollowerTest.SEARCH_SPEED), LineFollowerTest.TIME_STEP * result, False)
        return False

    def find_line(self, max_turn_steps):
        self.last_search_direction
        if self.turn_and_seek(max_turn_steps, self.last_search_direction):
            return True

        if self.turn_and_seek(max_turn_steps, -self.last_search_direction):
            self.last_search_direction = -self.last_search_direction
            return True

        return False

    def run(self):
        print("Dummy run method. Did not have time to adapt to framework (yet).")

    def stop(self):
        self.steering_drive.off()
        self.color_sensor.off()

    def start(self):
        direction = 1
        max_turn_steps = LineFollowerTest.SEARCH_MAX_STEPS
        yellow_count = 0

        #We need to go forward first
        #self.steering_drive.on_for_seconds(0, SpeedPercent(-2 * LineFollowerTest.FORWARD_SPEED), LineFollowerTest.TIME_STEP * 8, False)

        while True:
            if direction == 1:
                print('Forward')
            else:
                print('Backward')

            self.move_while_on_track(0, LineFollowerTest.FORWARD_SPEED * direction)

            # Go back after seeing yellow (track-specific)
            print("Currently seeing: " + self.color_sensor.color_name)
            if yellow_count > 5:
                print("Too much yellow :( Maybe I got stuck. Will stop line following.")
                break
            if self.color_sensor.color == 4: #Yellow
                yellow_count = yellow_count + 1
                self.steering_drive.on_for_seconds(0, SpeedPercent(LineFollowerTest.FORWARD_SPEED * 2), LineFollowerTest.TIME_STEP * 12, False)
                self.steering_drive.on_for_degrees(25, -25, 90, False)

            if self.color_sensor.rgb()[0] < 160 and self.color_sensor.rgb()[1] < 160 and self.color_sensor.rgb()[2] > 240:
                print("Victory!")
                break

            found = False
            i = 0
            max_turn_steps = LineFollowerTest.SEARCH_MAX_STEPS
            while i < 5:
                if self.find_line(max_turn_steps):
                    found = True
                    break
                i = i + 1
                max_turn_steps = max_turn_steps * 2

            if found:
                continue

            print('Lost it')

def main():
    movesteering = MoveSteering(OUTPUT_A, OUTPUT_B)
    colorsensor = ColorSensor(address=INPUT_1)
    colorsensor.calibrate_white()
    follower = LineFollowerTest(movesteering, colorsensor)
    follower.start()

if __name__ == "__main__":
    main()
