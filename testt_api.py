import requests
import json

url = "https://defsec-ai-api-1.onrender.com/predict"

# Since payload.json is in the same folder as the script, just use the file name
payload_path = "payload.json"

with open(payload_path) as f:
    payload = json.load(f)

response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
