import struct
import websockets
import time
import math
import asyncio
import sys

# Global variables
ws = None
motor_buffer = bytearray(8)  # 2 float32
last_send = 0
clicked = False
pos_x = 0
pos_y = 0
btn_size = 40

TARGET = '192.168.84.6'

# WebSocket send function
async def send_motors(vl, vr):
    global ws, motor_buffer
    vl = max(-1, min(vl, 1))
    vr = max(-1, min(vr, 1))
    motor_buffer = struct.pack('ff', vl, vr)
    print(vl, vr)
    print(motor_buffer)

    # Print the byte length and the actual byte content
    print(f"Motor buffer length: {len(motor_buffer)} bytes")
    print(f"Motor buffer (hex): {motor_buffer.hex()}")

    try:
        while(1):
            ws = await websockets.connect(f'ws://{TARGET}/motors.ws')
            await ws.send(motor_buffer)
            print('loop')
            time.sleep(0.1)
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    asyncio.run(send_motors(0.33, 1))
