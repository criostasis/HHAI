"""
Program that tests the database connection and chat
history functionality.

@author: Ahmer Gondal
@version:
"""

from database_helper import Connection


def test_chat_history():
    # Create a database connection
    db_connection = Connection()
    db_connection.connect("admin", "Stevencantremember", "admin")

    # Test user ID
    user_id = "test_user_123"

    # Sample chat history
    chat_history = [
        ("User: Hello!", "Assistant: Hi there! How can I assist you today?"),
        ("User: Can you help me with a question?", "Assistant: Absolutely! What's your question?"),
        ("User: How do I create a Python function?",
         "Assistant: To create a Python function, you use the 'def' keyword followed by the function name and "
         "parentheses. Here's an example:\n\ndef my_function():\n    # Function body\n    print(\"Hello from the "
         "function!\")\n\nYou can define parameters inside the parentheses if needed, and the function body is "
         "indented below the function definition. Finally, you can call the function using its name followed by "
         "parentheses, like this: my_function()."),
    ]

    # Save chat history to the database
    db_connection.update_chat_history(user_id, chat_history)

    # Retrieve chat history from the database
    retrieved_chat_history = db_connection.get_chat_history(user_id)

    # Verify the retrieved chat history matches the original chat history
    assert retrieved_chat_history == chat_history, "Retrieved chat history does not match the original chat history"

    print("Chat history test passed successfully!")

    # Close the database connection
    db_connection.close()


# Run the test
test_chat_history()
