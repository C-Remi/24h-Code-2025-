from utils.wsclient import WebSocketClient
import asyncio
import struct

ENDPOINT = "ws://192.168.84.6/infos.ws"
DATA_FORMAT = ">xfff"

async def log_pos_data():
    ws = WebSocketClient(ENDPOINT)
    while True:
        if ws.is_closed():
            await ws.connect()
            await ws.send_message(b"\x01")

        msg = await ws.receive_message()
        print(msg)
        if msg:
            yield struct.unpack(DATA_FORMAT, msg)

async def main():
    async for x, y, angle in log_pos_data():
        print(f"{x=} {y=} {angle=}")

if __name__ == "__main__":
    asyncio.run(main())
