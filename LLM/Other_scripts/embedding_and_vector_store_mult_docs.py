"""
File to create the embedding and vector store index from multiple documents.

@author: Michael Ray
@version: February 5, 2024
"""

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
import time

llama_path = '../Model/wizardlm-13b-v1.2.Q4_0.gguf'
# llama_path = '../Model/mistral-7b-openorca.Q4_0.gguf'  # Use if your GPU has 8GB or less of memory
loader = DirectoryLoader('../Dataset', show_progress=True)

embeddings = LlamaCppEmbeddings(
    model_path=llama_path,
    n_gpu_layers=41,   # Set according to your GPU
    n_ctx=int(4096),  # Need to use the same context size as the model
    verbose=True,
)


# Function to split the text into chunks
def split_chunks(sources):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=256,
        chunk_overlap=26,
        separators=["\n\n", "\n", " ", ""]
    )
    for chunk in splitter.split_documents(sources):
        # print(chunk)
        chunks.append(chunk)
    return chunks


# Function to create the index using FAISS
def create_index(chunks):
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]
    search_index = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    return search_index


# Main function to run the program
def main():
    start_time = time.time()
    docs = loader.load()
    chunks = split_chunks(docs)
    index = create_index(chunks)
    index.save_local("../Model")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time taken to run embeddings and create vector store: {elapsed_time:.2f}")


if __name__ == "__main__":
    main()
