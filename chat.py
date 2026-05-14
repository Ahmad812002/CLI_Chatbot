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

messages_arr = []

# This function is the main function of the chatbot, it will keep running until the user types "exit" or "quit".
# It will also handle the user's input and the model's response, and it will also handle any errors that may occur during the API call.
def chat_bot():
    user_input = ""

    user_input_for_role = input("Please enter your role (student, senior): ")
    while user_input.lower() not in ["exit", "quit"]:
        
        user_input = input("You: ")

        messages_arr.append({"role": "user", "content": user_input})
        try:

            response = client.chat.completions.create(
                model = "gpt-oss-120b",
                messages = ([format_prompt(user_input_for_role)] + messages_arr),
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
        # Never forget to append the assistant's reply back into messages otherwise the model forgets what it just said on the next turn.
        reply = response.choices[0].message.content
        print(f"Ai: {reply}")

        messages_arr.append({"role": "system", "content": reply})

        pass
# This function is to return the model's history, it will return all the messages that have been exchanged between the user and the model.
def model_history():
    return messages_arr
# This function is to format the prompt in a way that the model can understand it better.
def format_prompt(mode):
    # next update plan to use an API text detictor to detect the user's input.

    if(mode.lower() == "student"):
        system = "You are a helpful assistant. You will provide clear and concise explanations, examples, and guidance to help them understand programming concepts and solve problems. Be patient."
    elif(mode.lower() == "senior"):
        system = "You are a knowledgeable assistant. You will provide detailed explanations, advanced examples, and insights to help them deepen their understanding of programming concepts and solve complex problems. Be more strict."

    return ({"role": "system", "content": system})
# This function to log the whole conversation into a text file.
def log_conversation():
    try:
        if(len(messages_arr) == 0):
                log_file.write("No conversation to log.\n")
                return
        with open("conversation_log.txt", "a", encoding='utf-8', errors='ignore') as log_file:
            for message in messages_arr:
                log_file.write(f"{message['role']}: {message['content']}\n")
    except Exception as e:
        print(f"Error occurred while logging conversation: {e}")

chat_bot()
log_conversation()






