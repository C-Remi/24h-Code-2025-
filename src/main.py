import asyncio
from robot import Robot

#HOST = "192.168.84.6"
HOST="haumbot-c5cfb8.local"

async def main():
    robot = Robot(HOST)
    await robot.activate()

if __name__ == "__main__":
    asyncio.run(main())
