
from anthropic import BaseModel
from data_access.embeddings import get_embedding, search_embedding
from data_access.db import get_embeddings_collection, get_preferences_collection
from config.client import initialize_client
import openai
from config.prompts import job_scorer_prompt
from fastapi import APIRouter
from config.prompts import cover_letter_prompt_format



client = initialize_client()

messages_arr = []


# i need a collection for messages to be saved, maybe i need to separate each model messages.

def llm_scorer(prompt):
    try:
        response = client.chat.completions.create(
        model="gpt-oss-120b",
        messages= [prompt] + messages_arr[-10:] ,
        max_tokens=1024,
        temperature=0.0 # For a job fit scorer, reliable scoring, temperature (creativity) should be low
    )
    except openai.APIError as e:
        return{ "API Error: ": e }
    except openai.APITimeoutError as e:
        return { "Timeout Error: ": e }
    except openai.APIConnectionError as e:
        return { "API Connection Error: ": e }
    except openai.BadRequestError as e:
        return { "Invalid Request Error (Bad Request): ": e }
    except openai.InternalServerError as e:
        return { "Internal Server Error: ": e }
    except openai.RateLimitError as e:
        return{ "Rate Limit Error: ": e }
    except openai.AuthenticationError as e:
        return { "Authentication Error: ": e }

    return response.choices[0].message.content

def llm_cover_letter(profile_chunks, job_description, job_scorer_result):
    try:
    
            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages= [cover_letter_prompt_format(profile_chunks, job_description, job_scorer_result)] + messages_arr[-2:],
                max_tokens=1024,
                temperature=1
            )
            messages_arr.append({"role": "user", "content": cover_letter_prompt_format(profile_chunks, job_description, job_scorer_result)})
    except openai.APIError as e:
        print(f"API Error: {e}")
        return
    except openai.APITimeoutError as e:
        print(f"Timeout Error: {e}")
        return
    except openai.APIConnectionError as e:
        print(f"API Connection Error: {e}")
        return
    except openai.BadRequestError as e:
        print(f"Invalid Request Error (Bad Request): {e}")
        return
    except openai.InternalServerError as e:
        print(f"Internal Server Error: {e}")
        return
    except openai.RateLimitError as e:
        print(f"Rate Limit Error: {e}")
        return
    except openai.AuthenticationError as e:
        print(f"Authentication Error: {e}")
        return

    messages_arr.append({"role": "assistant", "content": response.choices[0].message.content})
    messages_arr.append({"role": "user", "content": profile_chunks + job_description})
    return response.choices[0].message.content