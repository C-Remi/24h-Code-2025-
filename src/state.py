
import struct
import time
import asyncio

import websockets.legacy.client as websockets
from websockets.exceptions import ConnectionClosedError


ENDPOINT ="ws://haumbot-c5cfb8.local/infos.ws"

INFOS_POSITION = b"\x01"
INFOS_LED = b"\x02"
INFOS_MOTORS = b"\x04"
INFOS_WHEELS = b"\x08"
INFOS_SPEED = b"\x10"
INFOS_RANGEFINDER = b"\x20"

class StateManager:

    """
    Access self.records for a dict of all records, grouped by category.
    """

    def __init__(self):
        self.records = dict()
        self.tasks = list()

        self.tasks.append(
            asyncio.create_task(
                self._subscribe("position", INFOS_POSITION, ">xfff")
            )
        )
        self.tasks.append(
            asyncio.create_task(
                self._subscribe("led", INFOS_LED, ">xBBB")
            )
        )
        self.tasks.append(
            asyncio.create_task(
                self._subscribe("motors", INFOS_MOTORS, ">xff")
            )
        )
        self.tasks.append(
            asyncio.create_task(
                self._subscribe("wheels", INFOS_WHEELS, ">xHHHH")
            )
        )
        self.tasks.append(
            asyncio.create_task(
                self._subscribe("speed", INFOS_SPEED, ">xff")
            )
        )
        self.tasks.append(
            asyncio.create_task(
                self._subscribe("rangefinder", INFOS_RANGEFINDER, ">xH")
            )
        )

    def push_data(self, key, value):
        if key not in self.records:
            self.records[key] = list()

        self.records[key].append((time.time(), value))
        print(f"{key}: {value}")

    async def _subscribe(self, name, flag, format):
        async for ws in websockets.connect(ENDPOINT):
            print(name, flag, format, "start")
            try:
                await ws.send(b'2'+flag)
                print(name, flag, format, "flag sent")
                while True:
                    data = await ws.recv()
                    print(name, flag, format, "message:", data)
                    if isinstance(data, str):
                        data = data.encode()

                    if flag == data[:1]:
                        self.push_data(name, struct.unpack(format, data))

            except ConnectionClosedError:
                continue

    async def join(self):
        for task in self.tasks:
            await task

if __name__ == "__main__":
    async def main():
        s = StateManager()
        await s.join()

    asyncio.run(main())
