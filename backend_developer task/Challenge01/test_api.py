import requests
import json
import os

def test_post_request():
    url = "http://localhost:8000/process-survey"
    
    # Check if the test_data.json file exists
    if not os.path.exists('test_data.json'):
        print("Error: The file 'test_data.json' does not exist.")
        return
    
    # Load data from the JSON file
    with open('test_data.json', 'r') as file:
        data = json.load(file)
    
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers)
        print("POST Status Code:", response.status_code)
        print("POST Response Headers:", response.headers)
        print("POST Response Content:", response.text)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # If the request was successful, print the JSON response
        print("POST Response JSON:", response.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except FileNotFoundError:
        print("The test_data.json file was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def test_get_request():
    url = "http://localhost:8000/test"
    try:
        response = requests.get(url)
        print("GET Status Code:", response.status_code)
        print("GET Response Headers:", response.headers)
        print("GET Response Content:", response.text)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # If the request was successful, print the JSON response
        print("GET Response JSON:", response.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Testing POST request:")
    test_post_request()
    print("\nTesting GET request:")
    test_get_request()
