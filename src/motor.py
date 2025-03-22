
import struct

import websockets.legacy.client as websockets
from websockets.exceptions import ConnectionClosedError

ENDPOINT ="ws://haumbot-c5cfb8.local/motors.ws"

class Motors:

    def __init__(self):
        self.socket = websockets.connect(ENDPOINT)
        self.vl = 0.0
        self.vr = 0.0

    async def set_motor_speed(self, vl, vr):
        self.vl = max(-1, min(vl, 1))
        self.vr = max(-1, min(vr, 1))
        motor_buffer = struct.pack('>ff', self.vl, self.vr)

        async with self.socket:
            await self.socket.send(motor_buffer)

    async def set_speed_left(self, vl):
        await self.set_motor_speed(vl, self.vr)

    async def set_speed_right(self, vr):
        await self.set_motor_speed(self.vl, vr)

    async def stop(self):
        await self.set_motor_speed(0, 0)
