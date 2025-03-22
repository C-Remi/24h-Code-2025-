import struct
from wsclient import WebSocketClient

ENDPOINT = "ws://haumbot-c5cfb8.local/motors.ws"

async def stop():
    ws = WebSocketClient(ENDPOINT)
    await ws.connect()
    await ws.send_message(struct.pack('ff', 0.0, 0.0))
    await ws.close()
