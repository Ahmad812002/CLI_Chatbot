import openai
import json
from config.client import initialize_client
from config.prompts import cover_letter_prompt_format

client = initialize_client()

messages_arr = []

def generate_cover_letter(profile_chunks, job_description, job_scorer_result):
    from models.job_scorer_bot import job_scorer_mode

    global messages_arr
    
    # while(True):
    print("Generating cover letter...\n\n")
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
    print(format_cover_letter_json(response.choices[0].message.content))
    messages_arr.append({"role": "user", "content": profile_chunks + job_description})


    job_scorer_mode()

        

# Fromating ai json response to be more readable 
def format_cover_letter_json(ai_reply):
    try:
        result = json.loads(ai_reply)
        print(f"\nCover Letter: \n\n{result['opening']}")
        print(f"\n{result['middle']}\n")
        print(f"{result['gap']}\n")
        print(f"{result['closing']}\n")
    except json.JSONDecodeError:
        print(ai_reply) # fallback if LLM doesn't return valid Json