import requests

url = "http://127.0.0.1:8000/predict"

# Replace with real feature names from your dataset
data = {
    "Destination_Port": 80,
    "Flow_Duration": 12345,
    "Total_Fwd_Packets": 10,
    "Total_Backward_Packets": 12,
    # add the rest of the 71 features...
}

response = requests.post(url, json=data)
print(response.json())
