"""
Model handler module for torch serve. Memory and chat
history are working. Commented out section is for debugging
before conversion into .mar file.

@author: Michael Ray
@version: April 12, 2024
"""

import os
import logging
import threading
import torch
from ts.torch_handler.base_handler import BaseHandler
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from database_helper import Connection


class HSUHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.qa = None
        self.memory = None
        self.index_path = None
        self.model_path = None
        self.embeddings = None
        self.llm = None
        self.index = None
        self.session_histories = {}
        self.lock = threading.Lock()

    def initialize(self, context):
        self.manifest = context.manifest
        properties = context.system_properties
        model_dir = properties.get("model_dir")

        self.device = "gpu" if torch.cuda.is_available() else "cpu"
        self.model_path = os.path.join(model_dir, self.manifest["model"]["serializedFile"])
        self.index_path = model_dir

        self.embeddings = LlamaCppEmbeddings(model_path=self.model_path)
        self.index = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        self.memory = ConversationBufferMemory(input_key="question")
        self.llm = GPT4All(model=self.model_path, device=self.device)

        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.index.as_retriever(),
            chain_type="stuff",
            verbose=True,
            max_tokens_limit=4096,
            memory=self.memory
        )

        logging.info(f"Model path: {self.model_path}")
        logging.info(f"Index path: {self.index_path}")
        logging.info(f"Device info: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

    def preprocess(self, data):
        input_data = data[0].get("data")
        if input_data is None:
            input_data = data[0].get("body")
        return input_data

    def inference(self, input_data):
        question = input_data["question"]
        user_id = input_data["user_id"]

        with self.lock:
            if user_id not in self.session_histories:
                self.session_histories[user_id] = []
            chat_history = self.session_histories[user_id]

        # Invoke the conversational model with the current question and stored chat history
        result = self.qa.invoke({"question": question, "chat_history": chat_history})
        chat_history.append((question, result['answer']))  # Update the memory with the latest interaction

        # Optionally update the chat history in a database or other storage for persistence
        db_connection = Connection()
        db_connection.connect("admin", "Stevencantremember", "admin")
        db_connection.update_chat_history(user_id, chat_history)
        db_connection.close()

        logging.info(f"Chat History Updated for User {user_id}: {chat_history}")

        output = {"answer": result['answer']}
        return [output]

    def postprocess(self, inference_output):
        return inference_output

#
# class SimulatedContext:
#     def __init__(self, model_dir, serialized_file):
#         self.system_properties = {'model_dir': model_dir}
#         self.manifest = {'model': {'serializedFile': serialized_file}}
#
#
# def simulate_interaction(handler, question, user_id):
#     # Simulate preprocessing input
#     data = [{"data": {"question": question, "user_id": user_id}}]
#     processed_data = handler.preprocess(data)
#
#     # Call the synchronous inference method directly
#     response = handler.inference(processed_data)
#
#     # Simulate postprocessing output
#     postprocessed_response = handler.postprocess(response)
#     return postprocessed_response
#
#
# def main():
#     context = SimulatedContext('.', 'wizardlm-13b-v1.2.Q4_0.gguf')
#     handler = HSUHandler()
#     handler.initialize(context)
#
#     # Define a user ID for session consistency
#     user_id = "user123"
#
#     # Define a list of questions to simulate a conversation
#     questions = [
#         "hello",
#         "What does HSU stand for?",
#         "What majors does HSU offer?",
#         "What can you tell me about HSU?"
#     ]
#
#     # Loop through each question, simulating an interaction
#     for question in questions:
#         response = simulate_interaction(handler, question, user_id)
#         print("Question:", question)
#         print("Response:", response)
#
#         # Check and display the updated chat history
#         if user_id in handler.session_histories:
#             print("Updated Chat History for {}: {}".format(user_id, handler.session_histories[user_id]))
#
#
# if __name__ == "__main__":
#     main()

