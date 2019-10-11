import asyncio
import websockets
import json
from asyncio import TimeoutError
from ev3dev2.motor import MoveJoystick, MoveDifferential, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor
from websockets.exceptions import ConnectionClosed
from ev3dev2.wheel import EV3Tire


async def on_connect(socket, path):
    color_sensor = ColorSensor(INPUT_1)
    infrared_sensor = InfraredSensor(INPUT_2)
    touch_sensor = TouchSensor(INPUT_3)
    movetank = MoveTank(OUTPUT_A, OUTPUT_B)
    movesteering = MoveSteering(OUTPUT_A, OUTPUT_B)
    
    try:
        while True:
            try:
                raw_cmd = await asyncio.wait_for(socket.recv(), timeout = 0.25)
                command = json.loads(raw_cmd)
                command_type = command['type']
                if command_type == 'CALIBRATE':
                    print("Calibrating white..")
                    color_sensor.calibrate_white()
                elif command_type == 'MOVETANK':
                    motors = command['payload']
                    if (motors['throttle']):
                        movetank.on(motors['left'] * (-1), motors['right'] * (-1))
                    else:
                        movetank.off()
                elif command_type == 'MOVESTEERING':
                    motors = command['payload']
                    if (motors['throttle']):
                        steer = motors['steering']
                        speed = motors['speed'] * -1
                        movesteering.on(steer, speed)
                    else:
                        movesteering.off()
                elif command_type == 'MODE':
                    print("Setting the MOOD(e)")
                    color_sensor.mode = command['payload']

            except TimeoutError:
                pass

            color_value = "230, 230, 230"
            color_rgb = "230, 230, 230"

            if color_sensor.mode == 'COL-REFLECT':
                color_value = color_sensor.reflected_light_intensity
            elif color_sensor.mode == 'COL-AMBIENT':
                color_value = color_sensor.ambient_light_intensity
            elif color_sensor.mode == 'COL-COLOR':
                color_value = color_sensor.color_name
            elif color_sensor.mode == 'REF-RAW':
                color_value = color_sensor.raw
                color_rgb = color_value
            elif color_sensor.mode == 'RGB-RAW':
                color_value = color_sensor.rgb
                color_rgb = color_value

            await socket.send(json.dumps(
                { 
                    "colour_sensor": {
                        "value":  color_value,
                        "rgb": color_rgb,
                        "mode": color_sensor.mode
                    },
                    "touch_sensor": touch_sensor.is_pressed,
                    "infrared_sensor": infrared_sensor.proximity
                }
            ))
    except ConnectionClosed:
        pass

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(on_connect, '0.0.0.0', 9000))
    print("READY")
    loop.run_forever()
except KeyboardInterrupt:
    print()
