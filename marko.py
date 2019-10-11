#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import time

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

# Optional cool message
sound = Sound()
sound.speak('Marko')

# Using MoveSteering motor (there are others)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
# Params: Andle (-100 to 100), speed (percent, 0 to 100), seconds it drives.
#steering_drive.on_for_seconds(0, SpeedPercent(-100), 2)
#steering_drive.on_for_seconds(-100, SpeedPercent(-15), 2)
#steering_drive.on_for_seconds(50, SpeedPercent(-50), 2)

# Init color sensor, connected to input 1
color_sensor = ColorSensor(address=INPUT_1)

def on_track():
    global last_brightness
    red = color_sensor.red
    green = color_sensor.green
    blue = color_sensor.blue

    last_brightness = red + green + blue

    color = color_sensor.color
    return color == 4 or color == 6 or color == COLOR_BLUE or color == COLOR_RED

def move_while_on_track(direction, speed):
    global last_brightness
    global last_search_direction
    last_brightness = 1000
    brightness = last_brightness
    steering_drive.on_for_seconds(0, SpeedPercent(-speed), TIME_STEP * STEPS_PER_SECOND * 10, False, False)
    while on_track():
        print(last_brightness)
        effective_direction = direction
        if last_brightness < brightness - VEERING_THRESHOLD:
            effective_direction = last_search_direction * 10
            print('Veering ' + direction_name(last_search_direction))
        #steering_drive.on_for_seconds(effective_direction, SpeedPercent(-speed), TIME_STEP, False)
        brightness = last_brightness

    steering_drive.off(None, False)

def move_until_on_track(direction, speed, max_steps):
    i = 0
    steering_drive.on_for_seconds(direction, SpeedPercent(-speed), TIME_STEP * max_steps, False, False)
    while (steering_drive.is_running or steering_drive.is_ramping) and not on_track() and color_sensor.color != COLOR_RED and color_sensor.color != COLOR_BLUE:
        #steering_drive.on_for_seconds(direction, SpeedPercent(-speed), TIME_STEP, False)
        i = i + 1
        #if i >= max_steps:
        #    break

    steering_drive.off(None, False)
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
    steering_drive.on_for_seconds(100 * turn_direction * -1, SpeedPercent(-SEARCH_SPEED), TIME_STEP * result, False)
    return False

def find_line(max_turn_steps):
    global last_search_direction
    if turn_and_seek(max_turn_steps, last_search_direction):
        return True
    
    if turn_and_seek(max_turn_steps, -last_search_direction):
        last_search_direction = -last_search_direction
        return True

    return False

direction = 1
max_turn_steps = SEARCH_MAX_STEPS

while True:
    if direction == 1:
        print('Forward')
    else:
        print('Backward')

    move_while_on_track(0, FORWARD_SPEED * direction)

    # XXX Turn a bit left when seeing red (this is specific to the test track)
    if color_sensor.color == COLOR_RED:
        steering_drive.on_for_seconds(-90, SpeedPercent(-SEARCH_SPEED), TIME_STEP * 8, False)
    # XXX Turn a bit right when seeing blue (this is specific to the test track)
    if color_sensor.color == COLOR_BLUE:
        steering_drive.on_for_seconds(90, SpeedPercent(-SEARCH_SPEED), TIME_STEP * 8, False)

    if color_sensor.color == 3:
        sound.speak('Finish')
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
        continue

    print('Lost it')
    sound.speak('Lost it')
    break
