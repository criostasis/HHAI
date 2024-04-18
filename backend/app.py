"""
Backend that handles chat functionality using FastAPI

@author: Ahmer Gondal, Jaden Barnwell
@version: April 18, 2024
"""

import asyncio
import logging
import requests
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database_helper import Connection
from asyncio import Lock
from bson import json_util
import json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    user_id: str


class SaveChatRequest(BaseModel):
    user_id: str
    user_inputs: list
    bot_inputs: list


lock = Lock()


@app.get("/")
def index():
    return {"message": "API is running"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)},
    )


async def process_chat_request(question, user_id):
    try:
        input_data = {"question": question, "user_id": user_id}
        # Send a synchronous POST request to the model server
        response = requests.post("http://localhost:8080/predictions/wizardlmtest", json=input_data)

        if response.status_code == 200 and response.text:
            try:
                result = response.json()
                if 'answer' in result:
                    logging.info(f"Generated response: {result['answer']}")
                    return {"reply": result['answer']}
                else:
                    logging.error("Response JSON does not contain 'answer'.")
                    return {"error": "The model server did not return an expected answer."}
            except ValueError:  # Catching JSON decode error
                logging.error("Failed to decode JSON from response.")
                return {"error": "The model server response was not in expected JSON format."}
        else:
            logging.error(f"Model server request failed with status code: {response.status_code}")
            return {"error": f"Model server request failed with status code: {response.status_code}"}
    except requests.RequestException as e:
        logging.error(f"An error occurred during chat processing: {e}", exc_info=True)
        return {"error": "An error occurred during chat processing."}


@app.get("/status")
def status():
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest):
    question = request.question
    user_id = request.user_id

    if not question:
        logging.warning("User input is missing")
        raise HTTPException(
            status_code=400,
            detail="No question provided"
        )

    result = await process_chat_request(question, user_id)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to process chat"
        )


@app.post("/save_chat")
async def save_chat(request: SaveChatRequest):
    user_id = request.user_id
    user_inputs = request.user_inputs
    bot_inputs = request.bot_inputs

    if not user_inputs or not bot_inputs:
        return JSONResponse(content={"error": "Missing required parameters"}, status_code=400)

    async def save_chat_history(user_id, user_inputs, bot_inputs):
        try:
            db_connection = Connection()
            db_connection.connect("admin", "password", "admin")  # Placeholder password
            # Retrieve the existing chat history for the user from MongoDB
            chat_history = db_connection.get_chat_history(user_id)
            # Append the new user inputs and bot inputs to the chat history
            chat_history.extend(zip(user_inputs, bot_inputs))
            # Update the chat history in MongoDB
            db_connection.update_chat_history(user_id, chat_history)
            db_connection.close()
        except Exception as e:
            logging.error(f"An error occurred while saving chat history: {e}", exc_info=True)

    try:
        await asyncio.gather(save_chat_history(user_id, user_inputs, bot_inputs))
        return JSONResponse(content={"message": "Chat history updated successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

#will be used for admin page to see all the logs through our save chat
@app.route('/find_chat_logs', methods=['GET'])
def find_chatlog():
    with app.app_context():
        db_connection = Connection()
        db_connection.connect("admin", "Stevencantremember", "admin")
        users = db_connection.read("chatbot", "chat_logs")
        #returns list [] with results need to jsonify this
        #print(f'api end users: {users}')
        db_connection.close()
        
        if users:
            # below line fixes object_id so it can be processed
            users_json = json_util.dumps(users)
            #loads gets rid of \\ in front of every variable
            parsed_data = json.loads(users_json)
            return JSONResponse(parsed_data), 200
        return JSONResponse({'error': 'chatlog not found'}), 404


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, workers=4)

