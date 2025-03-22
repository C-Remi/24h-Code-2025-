import requests

def set_led_color(host, color:str = "#000000"):
    response = requests.post(f"http://{host}/led/set_color", json={
        "ledcolor": color
    })
    
    if response.status_code == 200:
        print(f"Changed led to {color}")
        return True
    
    return False

def turtle_move_forward(host, distance_mm):
    response = requests.post(f"http://{host}/turtle/send", json={
        "dist": distance_mm, "type": "dist"
    })

    if response.status_code == 200:
        return True

    return False


def turtle_rotate(host, angle):
    response = requests.post(f"http://{host}/turtle/send", json={
        "angle": angle, "type": "angle"
    })

    if response.status_code == 200:
        return True

    return False

def reset_position(host):
    response = requests.get(f"http://{host}/position/reset")
    
    if response.status_code == 200:
        print('Reset successful')
        return True
    
    return False