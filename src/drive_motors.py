from wsclient import WebSocketClient
import asyncio
import struct

from read_pos import log_pos_data

ENDPOINT = "ws://haumbot-c5cfb8.local/motors.ws"
DATA_FORMAT = ">ff"

SPEED_INCREMENT = 0.005

async def send_motor_command():
    ws = WebSocketClient(ENDPOINT)
    while True:
        if ws.is_closed():
            await ws.connect()

        left, right = (yield)
        message = struct.pack(DATA_FORMAT, left, right)
        await ws.send_message(message)

async def run_straight():
    poslogger = log_pos_data()
    driver = send_motor_command()

    # initial speed
    leftspeed = 0.3
    rightspeed = 0.3

    await driver.asend(None)
    await driver.asend((leftspeed, rightspeed))

    async for x, y, angle in poslogger:
        if angle > 0.0:
            leftspeed += SPEED_INCREMENT
        if angle < 0.0:
            rightspeed += SPEED_INCREMENT

        print(f"{angle=} {leftspeed=} {rightspeed=}")
        await driver.asend((leftspeed, rightspeed))


if __name__ == "__main__":
    asyncio.run(run_straight())
