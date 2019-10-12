#!/usr/bin/env python3
import keyboard
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering

def change_mode():
    keyboard.add_hotkey("1", lambda: keyboard.write('Hmm'))
    keyboard.add_hotkey("r", lambda: remote_mode())


def remote_mode():

    steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)

    while true:
        while keyboard.is_pressed('a'):
                #Turn left
        while keyboard.is_pressed('d'):
                #Turn right
        while keyboard.is_pressed('w'):
                #Go forward
        while keyboard.is_pressed('s'):
                #Go backwards


def main():
    remote_mode()
