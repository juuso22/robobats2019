#!/usr/bin/env python3
from ev3dev2.motor import MoveJoystick, MoveDifferential, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from ev3dev2.wheel import EV3Tire
import time
import code

class Forest:
    def woop(self):
        steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
        steering_drive.on_for_seconds(-30, -100, 3)
        steering_drive.on_for_seconds(35, -100, 4.1)
        steering_drive.on_for_seconds(0, -100, 1.8)
        steering_drive.on_for_seconds(-40, -100, 1.3)
        steering_drive.on_for_seconds(0, -100, 0.8)
        steering_drive.on_for_seconds(40, -100, 1)