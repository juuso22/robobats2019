from threading import Thread
import asyncio
import websockets
import json
from asyncio import TimeoutError


class Remote(Thread):
    def __init__(self, movesteering, fork):
        Thread.__init__(self)
        self.movesteering = movesteering
        self.fork = fork

    def run(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(websockets.serve(self.on_connect, '0.0.0.0', 9000))
            print("Done")
            loop.run_forever()
        except KeyboardInterrupt:
            print("FAIL")

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        self.running = False
        Thread.join(self, timeout)

    async def on_connect(self, socket, path):
        while self.running:
            try:
                raw_cmd = await asyncio.wait_for(socket.recv(), timeout=500)
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
                        elif move == 't':
                            self.fork.on(-100)
                        elif move == 'g':
                            self.fork.on(100)
                        elif move == 'stop':
                            self.movesteering.off()
                            self.fork.off()
            except TimeoutError:
                pass
