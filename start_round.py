#!/usr/bin/env python3
from round_obstacle import RoundObstacle
import code
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering
from ev3dev2.sensor import INPUT_1co
from ev3dev2.sensor.lego import ColorSensor

color_sensor = ColorSensor(address=INPUT_1)

ms = MoveSteering(OUTPUT_A, OUTPUT_B)

ru = RoundObstacle()
code.interact(local = locals())