import struct
import websockets
import time
import math
import asyncio

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
    print(motor_buffer)

    if ws and not ws.closed:
        try:
            await ws.send(motor_buffer)
        except Exception as e:
            print(f"Error sending data: {e}")
    else:
        # Open a new connection if no existing one
        try:
            ws = await websockets.connect(f'ws://{TARGET}/motors.ws')
            await ws.send(motor_buffer)
        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(send_motors(10, 10))
