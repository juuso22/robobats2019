#!/usr/bin/env python3
from ev3dev2.motor import MoveJoystick, MoveDifferential, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from ev3dev2.wheel import EV3Tire
import time
import code

class RoundObstacle:

    def __init__(self, ms = MoveSteering(OUTPUT_A, OUTPUT_B), cs = ColorSensor(address=INPUT_1), isensor = InfraredSensor(INPUT_2)):
        self.steering_drive = ms
        self.color_sensor = cs
        self.infrared_sensor = isensor

    LEFT = 1
    RIGHT = -1


    def drive_until_proximity(self, proximity_goal = 40, direction = 0):
        if (self.infrared_sensor.proximity > proximity_goal):
            self.steering_drive.on(direction, SpeedPercent(-100))
        while (self.infrared_sensor.proximity > proximity_goal):
            time.sleep(0.2)
            print('Dist: ' + str(self.infrared_sensor.proximity))
        self.steering_drive.off()

    def wait_and_sleep(self, proximity = 70, maxholes = 0, sleep_time = 0.3): 
        last_proximity = 0
        second_last_prox = 0
        i = 0
        while True:
            curr_prox = self.infrared_sensor.proximity
            if (curr_prox < proximity):
                second_last_prox = last_proximity
                last_proximity = curr_prox
                time.sleep(0.2)
                print('Dist: ' + str(curr_prox))
                continue
            elif(last_proximity >= proximity or second_last_prox >= proximity): # Allow seeing less than prox for the next 2 ticks
                second_last_prox = last_proximity
                last_proximity = curr_prox
                time.sleep(0.2)
                print('Dist: ' + str(curr_prox))
                continue
            elif(i < maxholes):
                second_last_prox = last_proximity
                last_proximity = curr_prox
                i += 1
                print('Aukko number:' + str(i))
                continue
            else:
                break

        time.sleep(sleep_time)

    def first_kiekko(self):
        self.drive_until_proximity()
        self.wait_and_sleep(75, maxholes = 1, sleep_time = 0.4)
        self.drive_until_proximity(direction = 8 * self.RIGHT)

    def second_kiekko_left(self, maxholes = 1):
        self.drive_until_proximity()
        self.wait_and_sleep(70, maxholes, sleep_time = 0.5)
        self.drive_until_proximity(direction = 8 * self.RIGHT)


    def third_kiekko(self, prox = 75):
        self.drive_until_proximity()
        self.wait_and_sleep(prox, maxholes = 1, sleep_time = 0.4)
        self.drive_until_proximity(60)

    def start(self):
        self.steering_drive.on_for_seconds(-40, -100, 2)
        self.first_kiekko()
        self.second_kiekko(maxholes = 1)
        self.third_kiekko()
        self.steering_drive.on_for_rotations(100,100,0.8)
        self.steering_drive.on_for_seconds(0, 100, 4)

    def start_2(self):
        self.steering_drive.on_for_seconds(-40, -100, 2)
        self.first_kiekko()
        self.second_kiekko(maxholes = 0)
        self.third_kiekko()
        self.steering_drive.on_for_rotations(100,100,0.8)
        self.steering_drive.on_for_seconds(0, 100, 4)

def main():
    code.interact(local = locals())

if __name__ == "__main__":
    main()