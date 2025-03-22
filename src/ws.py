import time
import struct
import asyncio
import websockets
import math
from dataview import DataView

HOST = "haumbot-c5cfb8.local"
INFO_POSITION = 0x01
INFO_LED = 0x02

def readData(data):
    view = DataView(data)
    pos = 0

    mask = view.get_uint_8(pos)
    pos += 1

    if (mask & INFO_POSITION):
        position_x = view.get_float_32(pos + 0)
        
        position_y = view.get_float_32(pos + 4)
        position_a = view.get_float_32(pos + 8)
        pos += 3*4

        print(f"posX: {round(position_x * 1000)} mm, posY: {round(position_y * 1000)} mm , posA: {round(position_a * 180 / math.pi) } deg")

    if (mask & INFO_LED):
        led_r = view.get_uint_8(pos + 0)
        led_g = view.get_uint_8(pos + 1)
        led_b = view.get_uint_8(pos + 2)
        pos += 3

        print(f"ledR: {led_r}, ledG: {led_g}, ledB: {led_b}")
    


async def listen():
    uri = f"ws://{HOST}/infos.ws"  # Replace with your WebSocket server URL
    print(uri)
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}")
        try:
            while True:
                await websocket.send(b"\x03")
                message = await websocket.recv()

                print(f"Received: {message}")
                readData(message)

        except websockets.ConnectionClosed:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(listen())
    