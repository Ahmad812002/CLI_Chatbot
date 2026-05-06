from openai import OpenAI
import openai
import os
from dotenv import load_dotenv


# reads variables from a .env file and sets them in os.environ
load_dotenv()


client = OpenAI(
    # This is the API key which is inside .env file.
    api_key=os.environ.get("ROUTE_API_KEY"),
    base_url = "https://openrouter.ai/api/v1"
)


user_input = ""
user_for_role_input = input("Welcome to the CLI Chatbot! in which role do you need me to assist you ?\n")
history = []

# sys.agrv is a list of command-line arguments passed to the script. sys.argv[0] is the script name, and sys.argv[1] is the first argument. 
# In this case, it is expected to be the path to a text file
while user_input.lower() not in ["exit", "quit"]:
    
    user_input = input("You: ")

    try:

        response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=[
                { "role": "system", "content": user_for_role_input },
                { "role": "user", "content": user_input },
            ],
        )
    except openai.APIError as e:
        print(f"API Error: {e}")
        continue
    except openai.APITimeoutError as e:
        print(f"Timeout Error: {e}")
        continue
    except openai.APIConnectionError as e:
        print(f"API Connection Error: {e}")
        continue
    except openai.InvalidRequestError as e:
        print(f"Invalid Request Error (Bad Request): {e}")
        continue
    except openai.InternalServerError as e:
        print(f"Internal Server Error: {e}")
        continue
    except openai.RateLimitError as e:
        print(f"Rate Limit Error: {e}")
        continue
    except openai.AuthenticationError as e:
        print(f"Authentication Error: {e}")
        continue
    
    message = response.choices[0].message.content
    print(f"Assistant: {message}")

    history.append(response.choices[0].message)
    continue

print("history: ", history)


