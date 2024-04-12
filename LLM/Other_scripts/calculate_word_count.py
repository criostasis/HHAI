"""
File to average word count of the documents in the Dataset folder.
Used to help with chunk size and overlap when doing embeddings and
vector store index.

@author: Michael Ray
@version: February 12, 2024
"""

import os


# Function to calculate the average word count of all the documents in the Dataset folder
def calculate_average_word_count(folder_path):
    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    total_words = 0
    num_files = len(files)

    # Iterate through each file
    for file in files:
        file_path = os.path.join(folder_path, file)

        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            contents = f.read()

        # Count the words
        words = contents.split()
        word_count = len(words)
        total_words += word_count

    # Calculate the average word count
    if num_files > 0:
        average_word_count = total_words / num_files
        print(f"Average word count per document: {average_word_count}")
    else:
        print("No documents found.")


folder_path = '../Dataset'
calculate_average_word_count(folder_path)
