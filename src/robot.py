
from utils.wsclient import WebSocketClient
from api.infos import readInfos
from api.request import reset_position, set_led_color

class Robot:
    def __init__(self, x=0, y=0, radial=0, host="haumbot-c5cfb8.local"):
        """Initialize Robot with x, y coordinates and radial angle."""
        self._x = x
        self._y = y
        self._radial = radial  # Angle in degrees
        self._host = host
        self._uri_ws_info = f"ws://{self._host}/infos.ws"  
        self._uri_ws_motors = f"ws://{self._host}/motors.ws"  
        self._ws_client_info = WebSocketClient(self._uri_ws_info)
        self._ws_client_motors = WebSocketClient(self._uri_ws_motors)
        
        reset_position(self._host)
        set_led_color(self._host, "#ffffff")


    @property
    def x(self):
        """Get the x-coordinate."""
        return self._x

    @x.setter
    def x(self, value):
        """Set the x-coordinate."""
        if isinstance(value, (int, float)):
            self._x = value
        else:
            raise ValueError("X must be a number.")

    @property
    def y(self):
        """Get the y-coordinate."""
        return self._y

    @y.setter
    def y(self, value):
        """Set the y-coordinate."""
        if isinstance(value, (int, float)):
            self._y = value
        else:
            raise ValueError("Y must be a number.")

    @property
    def radial(self):
        """Get the radial angle (0 to 360 degrees)."""
        return self._radial

    @radial.setter
    def radial(self, value):
        """Set the radial angle and keep it within 0-360 degrees."""
        if isinstance(value, (int, float)):
            self._radial = value % 360  # Ensure it's always within 0-360
        else:
            raise ValueError("Radial must be a number.")

    async def activate(self):
        while True:
            # Connect to information WS    
            if self._ws_client_motors.is_closed():
                await self._ws_client_motors.connect()
            
            if self._ws_client_info.is_closed():
                await self._ws_client_info.connect()
                await self._ws_client_info.send_message(b'\x03')
            

            # Read INFO WS
            readInfos(await self._ws_client_info.receive_message())
            

    def __repr__(self):
        return f"Robot(x={self._x}, y={self._y}, radial={self._radial}°)"