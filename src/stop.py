import struct
from wsclient import WebSocketClient

ENDPOINT = "ws://192.168.84.6/motors.ws"

async def stop():
    ws = WebSocketClient(ENDPOINT)
    await ws.connect()
    await ws.send_message(struct.pack('ff', 0.0, 0.0))
    await ws.close()
