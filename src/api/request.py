import requests

HOST = "http://haumbot-c5cfb8.local"

def set_led_color(color:str = "#000000"):
    requests.post(f"{HOST}/led/set_color", json={
        "ledcolor": color
    }).raise_for_status()

def turtle_move_forward(distance_mm):
    requests.post(f"{HOST}/turtle/send", json={
        "dist": distance_mm, "type": "dist"
    }).raise_for_status()

def turtle_rotate(angle):
    requests.post(f"{HOST}/turtle/send", json={
        "angle": angle, "type": "angle"
    }).raise_for_status()

def reset_position():
    requests.get(f"{HOST}/position/reset").raise_for_status()
