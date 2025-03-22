import asyncio
from wsclient import WebSocketClient
from infos import readInfos

HOST = "haumbot-c5cfb8.local"

uri_ws_info = f"ws://{HOST}/infos.ws"  
uri_ws_motors = f"ws://{HOST}/motors.ws"  

async def main():
    ws_client_info = WebSocketClient(uri_ws_info)
    
    while True:    
        if not ws_client_info.is_closed():

            # Read INFO WS
            readInfos(await ws_client_info.receive_message())
            
        else:
            # Connect to information WS
            await ws_client_info.connect()
            await ws_client_info.send_message(b'\x03')
        

if __name__ == "__main__":
    asyncio.run(main())