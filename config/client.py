
from dotenv import load_dotenv
from openai import OpenAI
import os
import nomic

load_dotenv()

def initialize_client():
    client = OpenAI(
    # This is the API key which is inside .env file.
    api_key=os.environ.get("ROUTE_API_KEY"),
    base_url = "https://openrouter.ai/api/v1"
    )

    # Initialize and log into the Nomic Atlas client using the API key.
    nomic.login(token=os.environ.get("NOMIC_API_KEY"))

    return client

