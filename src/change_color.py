import requests

TARGET='http://haumbot-c5cfb8.local'

def set_led_color(color:str = "#000000"):
    requests.post(f"{TARGET}/led/set_color", data={
        "ledcolor": color
    })

if __name__ == "__main__":
    import random
    from time import sleep
    while True:
        r, g, b = random.randrange(256), random.randrange(256), random.randrange(256)
        color_format = f"#{r:02x}{g:02x}{b:02x}"
        set_led_color(color_format)
        sleep(0.5)
