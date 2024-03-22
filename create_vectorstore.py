import pandas as pd
from dotenv import load_dotenv
import numpy as np
import time
import os
import requests

from langchain_community.embeddings import HuggingFaceHubEmbeddings
from pinecone import Pinecone, PodSpec
from langchain_pinecone import Pinecone as PC
from langchain_pinecone import PineconeVectorStore

def setup_vectorstore():
    # Load environment variables from .env file
    load_dotenv()

    posts_df = pd.read_json("data/reddit_data.json")
    content_df = posts_df[posts_df['content'].notna() & (posts_df['content'] != "")]
    text = content_df['content'].to_list()

    model_id = "sentence-transformers/all-MiniLM-L6-v2"
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    embeddings = HuggingFaceHubEmbeddings(repo_id="sentence-transformers/all-MiniLM-L6-v2", huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

    def get_embeddings(texts):
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()

    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )

    index_name = "reddit-transport"
    # Deleting index 

    print(pc.list_indexes(), len(pc.list_indexes().indexes))

    if len(pc.list_indexes().indexes) > 0:
        pc.delete_index(index_name)
        print("Done deleting..", pc.list_indexes())

    existing_indexes = [index_info.name for index_info in pc.list_indexes().indexes]
    index_name = "reddit-transport"

    if len(pc.list_indexes().indexes) > 0 and index_name in existing_indexes:
        # Index exists
        print("Index already exists!")
        index = pc.Index(index_name)
        # Fetch index information
        index_info = index.describe_index_stats()
        print(f"Index info: {index_info}")

        # Check the number of vectors in the index
        num_vectors = index_info['total_vector_count']
        print(f"Number of vectors in the index: {num_vectors}")
        
    else:

        # Index does not exist
        # Create the index and use it
        print(index_name)
        pc.create_index(index_name, dimension=384, metric="dotproduct",
                    spec=PodSpec(
                        environment="gcp-starter"
                    ))
        index = pc.Index(index_name)

        # Add the embeddings to the Index and get the vectorstore
        texts = content_df['content'].tolist()
        emb = get_embeddings(texts)
        print("Converted text to vector embeddings.")

        ids = [f'{i}' for i in range(len(texts))]
        metadata = [{'text': text} for text in texts]
        vector_pairs = list(zip(ids, emb, metadata))

        index.upsert(vectors=vector_pairs)
        print(f"Upserted vectors into index {index_name}.")

        vectorstore = PineconeVectorStore(index, embeddings)
        print("Created vectorstore.")        


    return vectorstore, index

if __name__ == "__main__":
    vectorstore, index = setup_vectorstore()
    while not index.describe_index_stats()['total_vector_count'] > 0:
        time.sleep(1)

    # Fetch index information
    index_info = index.describe_index_stats()
    print(f"Index info: {index_info}")

    # Check the number of vectors in the index
    num_vectors = index_info['total_vector_count']
    print(f"Number of vectors in the index: {num_vectors}")

    query = "the bus credit system with simplygo compared to ezlink is so sad"
    print(query)
    response = vectorstore.similarity_search(
        query,  # our search query
        k=3  # return 3 most relevant docs
    )
    print(response)