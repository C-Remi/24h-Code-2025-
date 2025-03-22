import asyncio
import websockets

class WebSocketClient:
    def __init__(self, uri):
        """Initialize the WebSocket client with a server URI."""
        self.uri = uri
        self.websocket = None
        self.closed = True

    async def connect(self):
        """Establish a connection to the WebSocket server."""
        try:
            print(self.uri)
            self.websocket = await websockets.connect(self.uri)
            self.closed = False
            print(f"Connected to WebSocket server at {self.uri}")
        except Exception as e:
            print(f"Connection failed: {e}")

    async def send_message(self, message):
        """Send a message to the WebSocket server."""
        if self.websocket:
            await self.websocket.send(message)
            print(f"Sent: {message}")

    async def receive_message(self):
        """Receive a message from the WebSocket server."""
        if self.websocket:
            try:
                message = await self.websocket.recv()
                # DEBUG
                #print(f"Received: {message}")
                return message
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed by server.")
                self.closed = True

    async def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            print("WebSocket connection closed.")

    async def run(self):
        """Run the WebSocket client (send & receive messages)."""
        await self.connect()
        while True:
            message = await self.receive_message()
            if message is None:
                break  # Exit loop if connection is closed
    def is_closed(self):
        """Check if the WebSocket connection is closed."""        
        return self.websocket is None or self.closed

    