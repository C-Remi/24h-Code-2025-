import requests

def set_led_color(host, color:str = "#000000"):
    response = requests.post(f"http://{host}/led/set_color", data={
        "ledcolor": color
    })
    
    if response.status_code == 200:
        print(f"Changed led to {color}")
        return True
    
    return False
    
def reset_position(host):
    response = requests.get(f"http://{host}/position/reset")
    
    if response.status_code == 200:
        print('Reset successful')
        return True
    
    return False