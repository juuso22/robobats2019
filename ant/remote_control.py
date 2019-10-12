import asyncio
import websockets
import json
from asyncio import TimeoutError
from websockets.exceptions import ConnectionClosed

class RemoteControl():

    def __init__(self, socket, movesteering):
        self.socket = socket
        self.movesteering = movesteering

    def start(self):
        print("remote control enabled")

    async def run(self):
        raw_cmd = ""
        try:
            raw_cmd = await asyncio.wait_for(self.socket.recv(), timeout = 0.1)
        except TimeoutError:
            pass

        if raw_cmd != "":
            command = json.loads(raw_cmd)
            command_type = command['type']

            print("MOVE COMMAND")
            print(command)
            if command_type == 'MOVE':
                move = command['move']

                if move == 'w':
                    self.movesteering.on(0, 100)
                elif move == 's':
                    self.movesteering.on(0, -100)
                elif move == 'a':
                    self.movesteering.on(100, 100)
                elif move == 'd':
                    self.movesteering.on(-100, 100)
                elif move == 'stop':
                    self.movesteering.off()

                    
    def stop(self, movesteering):
        self.movesteering.off()
