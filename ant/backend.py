import asyncio
import websockets
import json
from asyncio import TimeoutError
from ev3dev2.motor import MoveJoystick, MoveDifferential, MoveSteering, MediumMotor, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from websockets.exceptions import ConnectionClosed
from remote_control import RemoteControl
from fixed_mode import FixedMode
from round_obstacle import RoundObstacle

async def on_connect(socket, path):

    try:
        movesteering = MoveSteering(OUTPUT_A, OUTPUT_B)
        fork = MediumMotor(OUTPUT_C)
        remote_control = RemoteControl(socket, movesteering, fork)
        fixed_mode = FixedMode(socket, movesteering)

        mode = remote_control
        #mode = fixed_mode
#        while True:
#            raw_cmd = ""

        while True:
            try:
                raw_cmd = await asyncio.wait_for(socket.recv(), timeout = 500)
                #await mode.run(raw_cmd)
                mode.run(raw_cmd)
            except TimeoutError:
                pass

            # if raw_cmd != "":
            #     await mode.run(raw_cmd)
            #else:
                # print("CHANGING MODE")
                # print(raw_cmd)
                #
                # command = json.loads(raw_cmd)
                # command_type = command['type']
                # if command_type == 'MODE':
                #     old_number = mode_number
                #     mode_number = command['mode']
                #
                #     print(mode_number)
                #     print(old_number)
                #
                #     if mode_number != old_number:
                #         mode.stop()
                #         if mode_number == 1:
                #             print("1")
                #         elif mode_number == 2:
                #             print("2")
                #         elif mode_number == 3:
                #             print("3")
                #         elif mode_number == 4:
                #             print("4")
                #         elif mode_number == 5:
                #             print("5")
                #         elif mode_number == 6:
                #             mode = remote_control
                                # start repl
                #             mode.start()
                
    except ConnectionClosed:
        pass

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(on_connect, '0.0.0.0', 9000))
    print("READY")
    loop.run_forever()
except KeyboardInterrupt:
    print("FAIL")
