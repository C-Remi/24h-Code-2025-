import asyncio
import tkinter as tk
from tkinter import Canvas
import struct
import websockets
import time
import math

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

    async with websockets.connect(f'ws://{TARGET}/motors.ws') as ws:
        await ws.send(motor_buffer)

# Update motors when sliders move
async def update_motors():
    vl = motor_ml.get() / 100
    vr = motor_mr.get() / 100
    await send_motors(vl, vr)

# Stop button callback
async def stop_motors():
    motor_ml.set(0)
    motor_mr.set(0)
    await update_motors()

# Joystick drawing
def draw_joystick():
    joystick.delete("all")
    w = joystick.winfo_width()
    h = joystick.winfo_height()

    joystick.create_oval(btn_size, btn_size, w - btn_size, h - btn_size, fill="#aaff40", outline="")
    joystick.create_oval(w/2 + pos_x - btn_size, h/2 + pos_y - btn_size,
                         w/2 + pos_x + btn_size, h/2 + pos_y + btn_size,
                         fill="#00aaff", outline="#0099ee", width=2)

# Joystick logic
async def update_position(event):
    global pos_x, pos_y, last_send
    w = joystick.winfo_width()
    h = joystick.winfo_height()
    kw = w / 2 - btn_size
    vx = max(-1, min((event.x - w / 2) / kw, 1))
    vy = max(-1, min((event.y - h / 2) / kw, 1))
    if vx * vx + vy * vy > 1:
        angle = math.atan2(vy, vx)
        vx = math.cos(angle)
        vy = math.sin(angle)
    pos_x = vx * kw
    pos_y = vy * kw
    vy *= -1

    if time.time() * 1000 - last_send > 250:
        await send_motors(vy + vx, vy - vx)
        last_send = time.time() * 1000

    draw_joystick()

def on_down(event):
    global clicked
    clicked = True
    asyncio.create_task(update_position(event))

def on_move(event):
    if clicked:
        asyncio.create_task(update_position(event))

async def on_up(event=None):
    global clicked, pos_x, pos_y
    if clicked:
        await send_motors(0, 0)
        clicked = False
        pos_x = pos_y = 0
        draw_joystick()

# Async Tkinter loop
async def tk_loop():
    while True:
        root.update()
        await asyncio.sleep(0.01)

# Tkinter setup
root = tk.Tk()
root.title("Motor Control")

motor_ml = tk.Scale(root, from_=-100, to=100, orient='horizontal', label='Left Motor')
motor_mr = tk.Scale(root, from_=-100, to=100, orient='horizontal', label='Right Motor')
motor_ml.pack()
motor_mr.pack()

motor_ml.bind("<ButtonRelease-1>", lambda e: asyncio.create_task(update_motors()))
motor_mr.bind("<ButtonRelease-1>", lambda e: asyncio.create_task(update_motors()))

stop_btn = tk.Button(root, text="Stop", command=lambda: asyncio.create_task(stop_motors()))
stop_btn.pack()

joystick = Canvas(root, width=300, height=300, bg='white')
joystick.pack()

joystick.bind("<ButtonPress-1>", on_down)
joystick.bind("<B1-Motion>", on_move)
joystick.bind("<ButtonRelease-1>", lambda e: asyncio.create_task(on_up()))

draw_joystick()

# Start the asyncio event loop with Tkinter
asyncio.run(tk_loop())
