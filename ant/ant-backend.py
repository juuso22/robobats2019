import asyncio
import websockets
from asyncio import TimeoutError
from ev3dev2.motor import MoveSteering, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from websockets.exceptions import ConnectionClosed

async def on_connect(socket, path):
    color_sensor = ColorSensor(INPUT_1)
    motor = MoveSteering(OUTPUT_A, OUTPUT_B)
    try:
        while True:
            try:
                cmd = await asyncio.wait_for(socket.recv(), timeout = 0.25)
                if cmd == 'go':
                    motor.on(0, SpeedPercent(-25))
                elif cmd == 'stay':
                    motor.off()
            except TimeoutError:
                pass
            await socket.send(str(color_sensor.color_name))
    except ConnectionClosed:
        pass

try:
    asyncio.get_event_loop().run_until_complete(websockets.serve(on_connect, '0.0.0.0', 9000))
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print()
