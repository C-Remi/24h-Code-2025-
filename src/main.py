import asyncio
from wsclient import WebSocketClient
from infos import readInfos
from motors import motor_setpoint
import time

t0, t1 = 0, 0

HOST = "192.168.84.6"
K = 0.1

uri_ws_info = f"ws://{HOST}/infos.ws"
uri_ws_motors = f"ws://{HOST}/motors.ws"

previous_angle = None
compensation_factor = None
delta_angle = 0

async def main():
    ws_client_info = WebSocketClient(uri_ws_info)
    ws_client_motors = WebSocketClient(uri_ws_motors)

    global previous_angle
    global compensation_factor
    global t0
    global t1


    while True:
        # Connect websocket is not already connected
        if ws_client_motors.is_closed():
            await ws_client_motors.connect()

        # Connect websocket is not already connected
        if ws_client_info.is_closed():
            await ws_client_info.connect()
            await ws_client_info.send_message(b'\x03')


        # Read INFO WS
        infos = readInfos(await ws_client_info.receive_message())
        print(infos)

        if previous_angle == None:
            compensation_factor = 0
        else:
            compensation_factor = (infos['a'] - previous_angle) * K
        print(compensation_factor)
        previous_angle = infos['a']

        if not ws_client_motors.is_closed():
            await ws_client_motors.send_message(motor_setpoint(compensation_factor))

        t1 = time.time()

        #print(f"freq = {1/(t1-t0)}Hz")

        t0 = t1

if __name__ == "__main__":
    asyncio.run(main())