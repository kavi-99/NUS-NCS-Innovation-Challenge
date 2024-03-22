import os
import time
from dotenv import load_dotenv
import create_vectorstore
from langchain.prompts import (
 PromptTemplate,
 SystemMessagePromptTemplate,
 HumanMessagePromptTemplate,
 ChatPromptTemplate
  )
from langchain import HuggingFaceHub
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import RetrievalQA

from pinecone import Pinecone
from langchain_pinecone import Pinecone as PC
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


def create_chain():
    print("Creating the vectorscore..")
    # Load environment variables from .env file
    load_dotenv()
    # Retrieving the index and creating the vectorscore
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )
    index_name = 'reddit-transport'
    existing_indexes = [index_info.name for index_info in pc.list_indexes().indexes]
    # Check for index
    if index_name in existing_indexes:
        print("Retrieving index,", index_name)
        index = pc.Index(index_name)

        embeddings = HuggingFaceHubEmbeddings(repo_id="sentence-transformers/all-MiniLM-L6-v2", huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
        vectorstore = PineconeVectorStore(index, embeddings)
    else:
        print("Creating index and vector store...")
        vectorstore, index = create_vectorstore.setup_vectorstore()
        # wait for newly created index to be initialised
        while not index.describe_index_stats()['total_vector_count'] > 0:
            time.sleep(1)

        # Fetch index information
        index_info = index.describe_index_stats()
        print(f"Index info: {index_info}")

    print("created vectorstore, loading llm..")

    # llm = HuggingFaceHub(
    #         # repo_id='declare-lab/flan-alpaca-base', # Uncomment this line to use other models instead
    #         # repo_id='nlpcloud/instruct-gpt-j-fp16', # Uncomment this line to use other models instead
    #         repo_id="declare-lab/flan-alpaca-large",
    #         # repo_id = "mistralai/Mistral-7B-Instruct-v0.2",
    #     model_kwargs={'temperature':0.5,"max_length":256} # temperature parameter: The higher the value, the more random the output
    #                                                         # max_length parameter: The maximum length of the sequence to be generated
    # )
    # llm = HuggingFaceHub(
    #         repo_id= "mistralai/Mistral-7B-Instruct-v0.2",
    #         huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    #         model_kwargs={
    #             "temperature": 1e-10,
    #             # "top_p": top_p,
    #             # "do_sample": True,
    #             "max_new_tokens":1024,
    #             "max_length":256
    #         },
    #     )

    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", 
        google_api_key=gemini_api_key, convert_system_message_to_human=True,
    )

    # Instruction template for the chatbot

    # template_str = """Your job is to use the context you have to answer the following question to the best of your capabilities. The question below describes a task. 
    # Write a response that appropriately completes the task. Use the following context to answer questions about transport and traffic in Singapore. 
    # Aim for detail and clarity, but avoid introducing any facts not supported by the provided context. DO NOT REPEAT YOUR SENTENCES.

    # Question:
    # {question}

    # Context:
    # {context}
    # """

    template_str = """The question below describes a task. Write a response that appropriately completes the task.
        Use the following context to answer questions about transport and traffic. Be as detailed as possible, but don't make up any information. DO NOT REPEAT YOUR SENTENCES.

        {context}

        {question}
        """

    # template_str = """
    # Task: Provide a well-informed response based on the context given below. Your answer should address the specified question comprehensively, with a focus on transport and traffic within Singapore. Ensure your response is detailed and clear. Avoid assumptions or unsupported facts, and maintain sentence variety without repetition.

    # Question:
    # {question}

    # Context:
    # {context}
    # """

    # template_str = """Based on the provided context, your task is to answer the following question as thoroughly and accurately as 
    # possible. Ensure your response is directly related to transport and traffic, based on the context given. 
    # Aim for detail and clarity, but avoid introducing any facts not supported by the provided context. 
    # Also, ensure your response is concise and avoids repetition.

    # {question}
    # {context}
    # """

    template = ChatPromptTemplate.from_template(template_str)

    review_system_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["context"],
            template=template_str,
        )
    )

    review_human_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["question"],
            template="{question}",
        )
    )
    messages = [review_system_prompt, review_human_prompt]

    prompt_template = ChatPromptTemplate(
        input_variables=["context", "question"],
        messages=messages,
    )

    output_parser = StrOutputParser()

    posts_retriever  = vectorstore.as_retriever()

    review_chain = (
        {"context": posts_retriever, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    reviews_vector_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(k=12),
    )
    reviews_vector_chain.combine_documents_chain.llm_chain.prompt = prompt_template
    
    return reviews_vector_chain

if __name__ == "__main__" :
    chain = create_chain()
    # question = "What are the main issues people have with the MRT system?"
    question = "What do people think about the bus credit system with simplygo compared to ezlink?"
    print(question)
    result = chain.invoke(question)
    print(result)




