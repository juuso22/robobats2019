import asyncio
import websockets
import json
from asyncio import TimeoutError
from websockets.exceptions import ConnectionClosed

class RemoteControl():

    def __init__(self, movesteering):
        self.movesteering = movesteering

    def start():
        print("remote control enabled")

    def run():
        raw_cmd = asyncio.wait_for(socket.recv(), timeout = 0.1)
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
