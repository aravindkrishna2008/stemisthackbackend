import requests

url = "http://localhost:8000/leaderboard/get"

try:
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Request was successful!")
        print("Response content:")
        print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.RequestException as e:
    print(f"An error occurred: {e}")
