"""
File to test multiple concurrent simulated users asking a single question.

@author: Michael Ray
@version: April 10, 2024
"""

import concurrent.futures
import requests
import time
import random
import string
import statistics
from tqdm import tqdm

CHATBOT_ENDPOINT = 'http://localhost:5000/chat'
SAMPLE_QUESTION = "hello"
NUM_SIMULATED_USERS = 100


# Function to generate a random user_id for tracking
def generate_random_id(length=7):
    # Generate a random string of letters and digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# Function that simulates a user querying the chatbot
def simulate_user_request(user_id):
    start_time = time.time()  # Start timing

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'  # Explicitly stating that the client expects JSON
    }
    payload = {
        'question': SAMPLE_QUESTION,
        'user_id': user_id  # Unique user/session ID
    }
    response_data = {}
    try:
        response = requests.post(CHATBOT_ENDPOINT, headers=headers, json=payload)
        response_data = response.json()
    except Exception as e:
        response_data = {'error': str(e)}

    duration = time.time() - start_time  # Calculate the duration
    return user_id, response_data, duration  # Return the user_id, response data, and duration


# List of user_ids
user_ids = [generate_random_id() for _ in range(NUM_SIMULATED_USERS)]
# Set up the progress bar
progress_bar = tqdm(total=NUM_SIMULATED_USERS, desc="Processing user requests")
# List to store results in
results = []
# Thread Pool to keep track of users and the responses they get
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_SIMULATED_USERS) as executor:
    futures = [executor.submit(simulate_user_request, user_id) for user_id in user_ids]

    for future in concurrent.futures.as_completed(futures):
        user_id, response_data, duration = future.result()
        results.append((user_id, response_data, duration))
        progress_bar.update(1)
# Close the progress bar
progress_bar.close()
# Calculate results
durations = [result[2] for result in results]
average_duration = statistics.mean(durations)
median_duration = statistics.median(durations)
max_duration = max(durations)
min_duration = min(durations)
# Print the results
print(f"\nTotal processed requests: {len(results)}")
for user_id, response, duration in results:
    print(f"User {user_id} got response {response} in {duration:.2f} seconds")
print(f"Average response time: {average_duration:.2f} seconds")
print(f"Median response time: {median_duration:.2f} seconds")
print(f"Max response time: {max_duration:.2f} seconds")
print(f"Min response time: {min_duration:.2f} seconds")
