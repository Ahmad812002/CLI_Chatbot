from pyexpat.errors import messages

from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
import nomic
from embeddings import chunk_text, get_embedding, read_document, search_embedding, store_embedding
from headroom import compress


# reads variables from a .env file and sets them in os.environ
load_dotenv()

# Initialize the OpenAI client with the API key and base URL for OpenRouter.
client = OpenAI(
    # This is the API key which is inside .env file.
    api_key=os.environ.get("ROUTE_API_KEY"),
    base_url = "https://openrouter.ai/api/v1"
)

# Initialize and log into the Nomic Atlas client using the API key.
nomic.login(token=os.environ.get("NOMIC_API_KEY"))

doc_id = 0
messages_arr = []

# This function is the main function of the chatbot, it will keep running until the user types "exit" or "quit".
# It will also handle the user's input and the model's response, and it will also handle any errors that may occur during the API call.
def chat_bot():
    user_input = ""
    chunks = ""
    global doc_id

    #user_input_for_role = input("Please enter your role (student, senior): ")
    while user_input.lower() not in ["exit", "quit"]:
        user_input = input("You: ")
        messages_arr.append({"role": "user", "content": user_input})
        try:
            # Case 1: If the user input is a file path, read the document and chunk it into smaller pieces, then store the embeddings of each chunk in the database.
            if user_input.endswith(('.pdf', '.txt', '.docx', '.md')) and os.path.exists(user_input):
                try:
                    document = read_document(user_input)
                    text_chunks = chunk_text(document)
                    doc_id = str(int(doc_id) + 1)
                    for chunk in text_chunks:
                        if(len(chunk.strip()) < 100):  # Skip chunks that are too short
                            continue
                        embedding = get_embedding(chunk)
                        store_embedding(doc_id, chunk, embedding, source=user_input)
                        doc_id = str(int(doc_id) + 1)
                    print("\nDocument ingested successfully. Ask me anything about it.")
                except Exception as e:
                    print(f"Error occurred while processing the document: {e}")
                    continue
                continue
            # Case 2: If the user input is not a file path, get the embedding of the user input and search for similar documents in the database, then join the similar documents with each other and attacht them to the LLM.
            else:
                #Data preperation
                embedded_vector = get_embedding(user_input)
                chunks = search_embedding(embedded_vector)
                try:
                    if chunks is not None:
                        chunks = "\n".join([chunk['documents'] for chunk in chunks])
                except Exception as e:
                    print(f"Error occurred while processing the chunks: {e}")
                    continue
            
            #LLM part
            print("messages: ", messages_arr)
            response = client.chat.completions.create(
                model = "gpt-oss-120b",
                messages = [format_prompt(chunks)] + messages_arr[-10:],
                temperature=1.0, # This is to make the model's response more creative and less deterministic, it will also help the model to provide more diverse responses and avoid repeating the same response.
                reasoning_effort = "high", # This is to make the model put more effort into reasoning and providing a more accurate and relevant response, it will take more time to generate a response but it will be worth it.
                verbosity = "low", # This is to make the model's response more concise and to the point, it will not provide unnecessary details or explanations.
                web_search_options = { "enabled": True }, # This is to enable the model to use web search to find relevant information and provide more accurate and up-to-date responses, it will also help the model to provide more detailed explanations and examples.
                max_tokens=1024,
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


        messages_arr.append({"role": "assistant", "content": reply})

        pass
# This function is to return the model's history, it will return all the messages that have been exchanged between the user and the model.
def model_history():
    return messages_arr
# This function is to format the prompt in a way that the model can understand it better.
def format_prompt(chunks):    
    # next update plan to use an API text detictor to detect the user's input.

    #if(mode.lower() == "student"):
        system_content = "You are an expert career coach, resume writer, and interview prep partner"
        if chunks: system_content += "Use the following context to answer:" + chunks
        else: system_content += "There is no context available, please answer based on your knowledge."
    #elif(mode.lower() == "senior"):
        #system_content = "You are a knowledgeable assistant. You will provide detailed explanations, advanced examples, and insights to help them deepen their understanding of programming concepts and solve complex problems. Be more strict."
        #if chunks: system_content += "Use the following context to answer:" + chunks
    # Here we are returning the system message which will be used as the first message in the conversation, it will set the tone and the context for the rest of the conversation, it will also help the model to understand the user's role and how to respond accordingly.
        return ({"role": "system", "content": system_content})
# This function to log the whole conversation into a text file.
def log_conversation():
    try:
        if len(messages_arr) == 0:
            print("No conversation to log.\n")
            return
        with open("conversation_log.txt", "a", encoding='utf-8', errors='ignore') as log_file:
            for message in messages_arr:
                log_file.write(f"{message['role']}: {message['content']}\n")
    except Exception as e:
        print(f"Error occurred while logging conversation: {e}")

chat_bot()

