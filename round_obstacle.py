#!/usr/bin/env python3
from ev3dev2.motor import MoveJoystick, MoveDifferential, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from ev3dev2.wheel import EV3Tire
import time
import code

class RoundObstacle(ms = MoveSteering(OUTPUT_A, OUTPUT_B), cs = ColorSensor(address=INPUT_1), isensor = InfraredSensor(INPUT_2)):

    steering_drive = ms
    color_sensor = cs
    infrared_sensor = isensor

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
        i = 0
        while True:
            curr_prox = self.infrared_sensor.proximity
            if (curr_prox < proximity):
                last_proximity = curr_prox
                time.sleep(0.2)
                print('Dist: ' + str(curr_prox))
                continue
            elif(last_proximity >= proximity):
                last_proximity = curr_prox
                time.sleep(0.1)
                print('Dist: ' + str(curr_prox))
                continue
            elif(i < maxholes):
                last_proximity = curr_prox
                i += 1
                print('Aukko number:' + str(i))
                continue
            else:
                break

        time.sleep(sleep_time)

    def first_kiekko(self):
        self.drive_until_proximity()
        self.wait_and_sleep(75, maxholes = 1, sleep_time = 0.5)
        self.drive_until_proximity(direction = 8 * self.RIGHT)

    def second_kiekko_left(self):
        self.drive_until_proximity()
        self.wait_and_sleep(75, maxholes = 1, sleep_time = 0.5)
        self.drive_until_proximity(direction = 8 * self.RIGHT)


    def third_kiekko(self):
        self.drive_until_proximity()
        self.wait_and_sleep(75, maxholes = 1, sleep_time = 1)
        self.drive_until_proximity()

    def start(self):
        self.first_kiekko()
        self.second_kiekko_left()
        self.third_kiekko()


def main():
    code.interact(local = locals())

if __name__ == "__main__":
    main()