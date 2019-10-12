import asyncio
import websockets
import json
from asyncio import TimeoutError
from ev3dev2.motor import MoveDifferential, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
#from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
#from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from websockets.exceptions import ConnectionClosed

class RemoteControl:

    def __init__(self, movesteering):
        self.movesteering = movesteering

    def start():
        print("remote control enabled")

    def run():
        try:
            raw_cmd = await asyncio.wait_for(socket.recv(), timeout = 0.1)
            command = json.loads(raw_cmd)
            command_type = command['type']
            if command_type == 'MOVE':
                move = command['move']

                if move == 'w':
                    self.movesteering.on(0, 100)
                elif move == 's':
                    self.movesteering.on(0, -100)
                elif move == 'a':
                    self.movesteering.on(100, -100)
                elif move == 'd':
                    self.movesteering.on(-100, -100)
                elif move == 'stop':
                    self.movesteering.off()
                

                    
    def stop(movesteering):
        self.movesteering.off()
