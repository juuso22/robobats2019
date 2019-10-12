#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import asyncio
import websockets
import time

class LineFollower:
    TIME_STEP = 0.1
    SEARCH_MAX_STEPS = 8
    FORWARD_SPEED = 50
    SEARCH_SPEED = 25
    STEPS_PER_SECOND = 1 / TIME_STEP
    COLOR_BLUE = 2
    COLOR_RED = 5
    LEFT = -1
    RIGHT = 1
    VEERING_THRESHOLD = 10000  # Veering off

    last_search_direction = 1
    last_brightness = 1000

    def __init__(self, movesteering, colorsensor):
        self.steering_drive = movesteering
        self.color_sensor = colorsensor

    def on_track():
        global last_brightness
        red = self.color_sensor.red
        green = self.color_sensor.green
        blue = self.color_sensor.blue

        last_brightness = red + green + blue

        color = self.color_sensor.color
        return color == 6

    def move_while_on_track(direction, speed):
        global last_brightness
        global last_search_direction
        last_brightness = 1000
        brightness = last_brightness
        self.steering_drive.on_for_seconds(0, SpeedPercent(speed), TIME_STEP * STEPS_PER_SECOND * 10, False, False)
        while on_track():
            print(last_brightness)
            effective_direction = direction
            if last_brightness < brightness - VEERING_THRESHOLD:
                effective_direction = last_search_direction * 10
                print('Veering ' + direction_name(last_search_direction))
            #self.steering_drive.on_for_seconds(effective_direction, SpeedPercent(-speed), TIME_STEP, False)
            brightness = last_brightness
            #TODO: Check if we got new instructions from websocket

        self.steering_drive.off(None, False)

    def move_until_on_track(direction, speed, max_steps):
        i = 0
        self.steering_drive.on_for_seconds(direction, SpeedPercent(-speed), TIME_STEP * max_steps, False, False)
        while (self.steering_drive.is_running or self.steering_drive.is_ramping) and not on_track() and self.color_sensor.color != 6:
            #self.steering_drive.on_for_seconds(direction, SpeedPercent(-speed), TIME_STEP, False)
            i = i + 1
            #if i >= max_steps:
            #    break
            #TODO: Check if we got new instructions from websocket

        self.steering_drive.off(None, False)
        #if i < max_steps:
        if on_track():
            return -1
        else:
            return i

    def direction_name(turn_direction):
        if turn_direction < 0:
            return 'left'
        else:
            return 'right'

    def turn_and_seek(max_turn_steps, turn_direction):
        name = direction_name(turn_direction)
        print('Turn ' + name)
        result = move_until_on_track(100 * turn_direction, SEARCH_SPEED, max_turn_steps)
        if result == -1:
            return True
        print('Turn back')
        self.steering_drive.on_for_seconds(100 * turn_direction * -1, SpeedPercent(-SEARCH_SPEED), TIME_STEP * result, False)
        return False

    def find_line(max_turn_steps):
        global last_search_direction
        if turn_and_seek(max_turn_steps, last_search_direction):
            return True

        if turn_and_seek(max_turn_steps, -last_search_direction):
            last_search_direction = -last_search_direction
            return True

        return False

    def start()
        print("Falling on line")

    def stop()
        self.steering_drive.off()
        self.color_sensor.off()

    def run():
        direction = 1
        max_turn_steps = SEARCH_MAX_STEPS

        while True:
            if direction == 1:
                print('Forward')
            else:
                print('Backward')

            move_while_on_track(0, FORWARD_SPEED * direction)

            # Go back after seeing yellow (track-specific)
            if self.color_sensor.color == COLOR_YELLOW:
                self.steering_drive.on_for_seconds(0, SpeedPercent(-FORWARD_SPEED), TIME_STEP * 8, False)
                self.steering_drive.on_for_degrees(-100, SpeedPercent(SEARCH_SPEED), 90, False)

            if self.color_sensor.color == 5:
                break

            found = False
            i = 0
            max_turn_steps = SEARCH_MAX_STEPS
            while i < 5:
                if find_line(max_turn_steps):
                    found = True
                    break
                i = i + 1
                max_turn_steps = max_turn_steps * 2

            if found:
                check_for_mode_change()
                continue

            print('Lost it')
            #TODO: Check if we got new instructions from websocket and wait if there isn't any
