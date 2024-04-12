"""
Simple test for Torch Serve API endpoint functionality.

@author: Michael Ray
@version: April 10, 2024
"""

import requests
import json


def test_endpoint(question, user_id):
    url = "http://localhost:8080/predictions/wizardlmtest"
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({
        "question": question,
        "user_id": user_id
    })

    response = requests.post(url, headers=headers, data=payload)

    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response Body: {response.json()}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.")
        print(f"Raw Response: {response.text}")


if __name__ == "__main__":
    test_question = "What is the meaning of life?"
    test_user_id = "test_user_123"
    test_endpoint(test_question, test_user_id)
