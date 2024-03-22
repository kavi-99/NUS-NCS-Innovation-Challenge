# NUS-NCS-Innovation-Challenge

Brief description of the project, its purpose, main features, and what problems it aims to solve.

This repository contains the code and resources for the NUS-NCS Innovation Challenge. It features an application designed to leverage social media data for enhancing urban traffic management through real-time sentiment analysis.

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites

Before starting, ensure you have Python installed on your system. This project requires Python 3.8 or newer.

### Installation

1. **Clone the Repository**

   Start by cloning this repository to your local machine:

`git clone https://github.com/kavi-99/NUS-NCS-Innovation-Challenge.git`
`cd NUS-NCS-Innovation-Challenge`

2. **Set Up a Virtual Environment**
Create and activate a virtual environment in the project directory:

For Windows:
`python -m venv venv`
`.\venv\Scripts\activate`

For macOS/Linux:
`python3 -m venv venv`
`source venv/bin/activate`

3. **Install Required Packages**
`pip install -r requirements.txt`

4. **Environment Variables**

Create a `.env` file in the project root directory and populate it with the necessary API keys:

plaintext
Copy code
# Pinecone API Key
PINECONE_API_KEY = "<your_pinecone_api_key_here>"

# Hugging Face API Token
HUGGINGFACEHUB_API_TOKEN = "<your_huggingface_api_token_here>"

# Google API Key
GOOGLE_API_KEY = "<your_google_api_key_here>"

# Reddit Credentials for traffic_management.ipynb
CLIENT_ID = "<your_reddit_client_id_here>"
CLIENT_SECRET = "<your_reddit_client_secret_here>"

Replace <your_pinecone_api_key_here>, <your_huggingface_api_token_here>, <your_google_api_key_here>, <your_reddit_client_id_here>, and <your_reddit_client_secret_here> with your actual API keys and credentials. Instructions for obtaining these keys can be found at:
- Get your Pinecone API Key: [Pinecone Quickstart Guide](https://docs.pinecone.io/guides/getting-started/quickstart)
- Get your Hugging Face API Key: [Hugging Face API Quicktour](https://huggingface.co/docs/api-inference/en/quicktour)
- Get your Google API Key: [Google AI Setup Tutorial](https://ai.google.dev/tutorials/setup)

### Running the Application

With the environment set up and the `.env` file configured, you can start the application:
`streamlit run streamlit_app.py`

Navigate to the URL provided in the terminal to view the application.

## Features

- **Interactive Chatbot**: Engage with our LLM-powered chatbot to explore public sentiments on urban transport.
- **Traffic Analysis Report**: Access in-depth reports generated from social media data to understand traffic management insights.
