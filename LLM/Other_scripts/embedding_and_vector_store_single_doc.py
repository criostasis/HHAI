"""
File to create the embedding and vector store index from a single document.

@author: Michael Ray
@version: February 5, 2024
"""

from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS


llama_path = '../Model/wizardlm-13b-v1.2.Q4_0.gguf'
loader = TextLoader('../Dataset/HSU_website_data.txt')
embeddings = LlamaCppEmbeddings(
    model_path=llama_path,
    n_gpu_layers=41,  # Comment this out if you cant use your GPU
    # n_threads=max(multiprocessing.cpu_count() - 1, 1),  # Comment this in if you cant use your GPU
    n_ctx=int(32768),  # Need to use the same context size as the model
    # n_ctx=int(os.environ['MODEL_CONTEXT_SIZE'])  # Need to use the same context size as the model

)


# Split text
def split_chunks(sources):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=32)
    for chunk in splitter.split_documents(sources):
        chunks.append(chunk)
    return chunks


# Indexing
def create_index(chunks):
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]
    search_index = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    return search_index


def main():
    # Create Index
    docs = loader.load()
    chunks = split_chunks(docs)
    index = create_index(chunks)

    # Save Index for later use
    index.save_local("../Model")


if __name__ == "__main__":
    main()
