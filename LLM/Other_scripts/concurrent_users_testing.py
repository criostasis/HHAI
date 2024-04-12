"""
File for testing multiple concurrent simulated users asking multiple questions.
Used to test memory, chat history and if LLM can maintain contextual awareness.

@author: Michael Ray
@version: April 10, 2024
"""

import concurrent.futures
import requests
import uuid
import time

CHATBOT_ENDPOINT = 'http://localhost:5000/chat'
QUESTION_SETS = [
    [
        "Hello, how are you?",
        "What is the weather today?",
        "Tell me a joke."
    ],
    [
        "What's the latest news?",
        "Can you give me a movie recommendation?",
        "What day is it today?"
    ],
]
NUM_SIMULATED_USERS = 5  # Adjust this number based on your testing needs


# Function to simulate a user session by sending a series of messages
def simulate_user_session(session_id, messages):
    start_time = time.time()  # Record the start time
    responses = []

    for message in messages:
        payload = {
            'user_input': message,
            'session_id': session_id  # Use the same session_id for all messages in the session
        }
        try:
            response = requests.post(CHATBOT_ENDPOINT, json=payload)
            responses.append(response.json())
        except Exception as e:
            responses.append({'error': str(e)})

    end_time = time.time()
    duration = end_time - start_time
    return responses, duration


user_sessions = [(str(uuid.uuid4()), QUESTION_SETS[i % len(QUESTION_SETS)]) for i in range(NUM_SIMULATED_USERS)]

# Using ThreadPoolExecutor to simulate multiple users simultaneously
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_SIMULATED_USERS) as executor:
    future_to_session = {executor.submit(simulate_user_session, session_id, messages): session_id for
                         session_id, messages in user_sessions}

    for future in concurrent.futures.as_completed(future_to_session):
        session_id = future_to_session[future]
        try:
            session_results, duration = future.result()  # Unpack the results and duration
            print(f"Results for Session {session_id} (Completed in {duration:.2f} seconds):")
            for result in session_results:
                print(result)
        except Exception as e:
            print(f"Session {session_id} generated an exception: {e}")
