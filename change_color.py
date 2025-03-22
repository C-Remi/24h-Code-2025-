import requests

TARGET='http://192.168.84.6'

# URL of the target (adjust the IP/hostname as needed)
url = f"{TARGET}/led/set_color"

# Data to send (mimics the <input name="ledcolor"> value)
payload = {
    "ledcolor": "#ffff00"  # Example: red color
}

# Send the POST request
response = requests.post(url, data=payload)

# Check the response
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")