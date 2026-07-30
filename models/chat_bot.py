import openai
import os
from data_access.embeddings import get_embedding, search_embedding
from config.client import initialize_client
from config.prompts import format_prompt_chat_bot
from data_access.document_reader import process_document

# Initialize the OpenAI client with the API key and base URL for OpenRouter.
client = initialize_client()

doc_id = 0
user_input = ""
job_preferences = ""
profile_chunks = ""
messages_arr = []

# Handleing assistant mode.
def chat_bot_mode():
    chunks = ""
    global doc_id, user_input, messages_arr

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input:
            continue

        messages_arr.append({"role": "user", "content": user_input})
        try:
            # Case 1: If the user input is a file path, read the document and chunk it into smaller pieces, then store the embeddings of each chunk in the database.
            if user_input.endswith(('.pdf', '.txt', '.docx', '.md')) and os.path.exists(user_input):
                process_document(user_input, doc_id)
                continue
            # Case 2: If the user input is not a file path, get the embedding of the user input and search for similar documents in the database, then join the similar documents with each other and attacht them to the LLM.
            else:
                #Data preperation
                embedded_vector = get_embedding(user_input)
                vector_embedding_result = search_embedding(embedded_vector)
                
                if vector_embedding_result is not None:
                    chunks = "\n".join([chunk['documents'] for chunk in vector_embedding_result])

            #LLM part
            response = client.chat.completions.create(
                model = "gpt-oss-120b",
                messages = [format_prompt_chat_bot(chunks)] + messages_arr[-10:],
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
