import requests

HOST = "http://haumbot-c5cfb8.local"

def set_led_color(red, green, blue):
    color = f"#{red:02x}{green:02x}{blue:02x}"
    requests.post(f"{HOST}/led/set_color", data={
        "ledcolor": color
    }).raise_for_status()

def turtle_move_forward(distance_mm):
    requests.post(f"{HOST}/turtle/send", data={
        "dist": distance_mm, "type": "dist"
    }).raise_for_status()

def turtle_rotate(angle):
    requests.post(f"{HOST}/turtle/send", data={
        "angle": angle, "type": "angle"
    }).raise_for_status()

def reset_position():
    requests.get(f"{HOST}/position/reset").raise_for_status()


if __name__ == "__main__":
    reset_position()
    set_led_color(0, 0, 255)
