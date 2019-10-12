import asyncio
import websockets
import json
from asyncio import TimeoutError
from ev3dev2.motor import MoveSteering, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1


async def on_connect(socket, path):
    movesteering = MoveSteering(OUTPUT_A, OUTPUT_B)
    fork = MediumMotor(OUTPUT_C)
    color_sensor = ColorSensor(address=INPUT_1)

    while True:
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
                        movesteering.on(0, 100)
                    elif move == 's':
                        movesteering.on(0, -100)
                    elif move == 'a':
                        movesteering.on(100, 100)
                    elif move == 'd':
                        movesteering.on(-100, 100)
                    elif move == 't':
                        fork.on(-100)
                    elif move == 'g':
                        fork.on(100)
                    elif move == 'c':
                        print(color_sensor.color_name)
                    elif move == 'stop':
                        movesteering.off()
                        fork.off()
        except TimeoutError:
            pass


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(on_connect, '0.0.0.0', 9000))
    print("READY")
    loop.run_forever()
except KeyboardInterrupt:
    print("FAIL")
