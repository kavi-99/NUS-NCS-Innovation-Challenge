# NUS-NCS-Innovation-Challenge

Brief description of the project, its purpose, main features, and what problems it aims to solve.

Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
What things you need to install the software and how to install them, for example:

Python 3.8 or higher
pip (Python Package Installer)
Installation
A step-by-step series of examples that tell you how to get a development environment running:

Clone the Repository

bash
Copy code
git clone https://github.com/kavi-99/NUS-NCS-Innovation-Challenge.git
cd NUS-NCS-Innovation-Challenge
Set up a Virtual Environment

For Windows:

bash
Copy code
python -m venv venv
.\venv\Scripts\activate
For macOS/Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install Required Packages

bash
Copy code
pip install -r requirements.txt
Create a .env File

Create a .env file in the root directory of the project, and populate it with the necessary API keys as follows:

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

Pinecone API Key
Hugging Face API Key
Google API Key
Start the Application

Run the Streamlit application:

bash
Copy code
streamlit run streamlit_app.py
