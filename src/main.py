import asyncio

from robot import Robot

HOST = "haumbot-c5cfb8.local"


async def main():
    robot = Robot(0,0,0, HOST, 10,360,100, 0.5)
    
    await robot.activate()
    
    
            
            

if __name__ == "__main__":
    asyncio.run(main())