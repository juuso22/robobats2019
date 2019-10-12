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

# Using MoveSteering motor (there are others)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
# Params: Andle (-100 to 100), speed (percent, 0 to 100), seconds it drives.
#steering_drive.on_for_seconds(0, SpeedPercent(-100), 2)
#steering_drive.on_for_seconds(-100, SpeedPercent(-15), 2)
#steering_drive.on_for_seconds(50, SpeedPercent(-50), 2)

# Init color sensor, connected to input 1
color_sensor = ColorSensor(address=INPUT_1)


while True:
    
    break
