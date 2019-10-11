import asyncio
import websockets
import json
from asyncio import TimeoutError
#from ev3dev2.motor import MoveJoystick, MoveDifferential, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
#from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
#from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from websockets.exceptions import ConnectionClosed
import remote_control


async def on_connect(socket, path):


    try:
        mode_number = "6"
        movesteering = MoveSteering(OUTPUT_A, OUTPUT_B)

        while True:
            try:
                raw_cmd = await asyncio.wait_for(socket.recv(), timeout = 0.25)
                command = json.loads(raw_cmd)
                command_type = command['type']
                if command_type == 'MODE':
                    old_number = mode_number
                    mode_number = command['mode']

                    if mode_number == 1:
                        print("1")
                    elif mode_number == 2:
                        print("2")
                    elif mode_number == 3:
                        print("3")
                    elif mode_number == 4:
                        print("4")
                    elif mode_number == 5:
                        print("5")
                    elif mode_number == 6:
                        remote_control.stop(movesteering)

                    if mode_number == 1:
                        print("1")
                    elif mode_number == 2:
                        print("2")
                    elif mode_number == 3:
                        print("3")
                    elif mode_number == 4:
                        print("4")
                    elif mode_number == 5:
                        print("5")
                    elif mode_number == 6:
                        remote_control.start(movesteering)
                
            except TimeoutError:
                pass
    except ConnectionClosed:
        pass

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(on_connect, '0.0.0.0', 9000))
    print("READY")
    loop.run_forever()
except KeyboardInterrupt:
    print()
