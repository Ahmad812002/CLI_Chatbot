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
history =  []


messages = [{"role": "system", "content": user_for_role_input}]

while user_input.lower() not in ["exit", "quit"]:
    
    user_input = input("You: ")

    messages.append({"role": "user", "content": user_input})
    try:

        response = client.chat.completions.create(
            model = "gpt-oss-120b",
            messages = messages,
           reasoning_effort = "high",
           verbosity = "low",
           web_search_options = {"enabled": True},

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
    except openai.BadRequestError as e:
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
    
    reply = response.choices[0].message.content
    print(f"Ai: {reply}")

    messages.append({"role": "assistant", "content": reply})

    continue

print("history: ", history)


