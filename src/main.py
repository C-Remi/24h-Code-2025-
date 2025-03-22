import asyncio
from wsclient import WebSocketClient
from infos import readInfos

HOST = "haumbot-c5cfb8.local"

uri_ws_info = f"ws://{HOST}/infos.ws"  
uri_ws_motors = f"ws://{HOST}/motors.ws"  

async def main():
    ws_client_info = WebSocketClient(uri_ws_info)
    ws_client_motors = WebSocketClient(uri_ws_motors)
    
    
    while True:
        # Connect to information WS    
        if ws_client_motors.is_closed():
            await ws_client_motors.connect()
        
        if ws_client_info.is_closed():
            await ws_client_info.connect()
            await ws_client_info.send_message(b'\x03')
        

        # Read INFO WS
        readInfos(await ws_client_info.receive_message())
            
            

if __name__ == "__main__":
    asyncio.run(main())