import asyncio
import websockets
import json
from asyncio import TimeoutError
from websockets.exceptions import ConnectionClosed

async def wait(period):
    try:
        await asyncio.wait_for(self.socket.recv(), timeout = period)
        raise InterruptedError
    except TimeoutError:
        pass

class FixedMode():
    def __init__(self, socket, movesteering):
        self.socket = socket
        self.movesteering = movesteering

    async def run(self):
        try:
            self.movesteering.on(0, 100) # go forward
            await wait(2)

            self.movesteering.on(100, 100) # turn left
            await wait(0.5)

            self.movesteering.on(0, 100) # go forward
            await wait(3)
        except InterruptedError:
            pass
