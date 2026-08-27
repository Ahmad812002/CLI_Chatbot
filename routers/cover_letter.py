from anthropic import BaseModel
from business_logic.cover_letter_logic import format_cover_letter_json, run_cover_letter 
from config.client import initialize_client
from config.prompts import cover_letter_prompt_format
from fastapi import APIRouter

client = initialize_client()

router = APIRouter()

messages_arr = []

class CoverLetterRequest(BaseModel):
    job_description: str
    job_scorer_result: str

router.post("/cover_letter")
def generate_cover_letter(profile_chunks, request: CoverLetterRequest):


    return run_cover_letter(profile_chunks, request.job_description, request.job_scorer_result)

    # from routers.scorer import job_scorer_mode

    # global messages_arr

    # run_cover_letter(profile_chunks, request.job_description, request.job_scorer_result)
    # while(True):
    print("Generating cover letter...\n\n")
    # try:

    #     response = client.chat.completions.create(
    #         model="gpt-oss-120b",
    #         messages= [cover_letter_prompt_format(profile_chunks, request.job_description, request.job_scorer_result)] + messages_arr[-2:],
    #         max_tokens=1024,
    #         temperature=1
    #     )
    #     messages_arr.append({"role": "user", "content": cover_letter_prompt_format(profile_chunks, request.job_description, request.job_scorer_result)})
    # except openai.APIError as e:
    #     print(f"API Error: {e}")
    #     return
    # except openai.APITimeoutError as e:
    #     print(f"Timeout Error: {e}")
    #     return
    # except openai.APIConnectionError as e:
    #     print(f"API Connection Error: {e}")
    #     return
    # except openai.BadRequestError as e:
    #     print(f"Invalid Request Error (Bad Request): {e}")
    #     return
    # except openai.InternalServerError as e:
    #     print(f"Internal Server Error: {e}")
    #     return
    # except openai.RateLimitError as e:
    #     print(f"Rate Limit Error: {e}")
    #     return
    # except openai.AuthenticationError as e:
    #     print(f"Authentication Error: {e}")
    #     return

    # messages_arr.append({"role": "assistant", "content": response.choices[0].message.content})
    # print(format_cover_letter_json(response.choices[0].message.content))
    # messages_arr.append({"role": "user", "content": profile_chunks + request.job_description})


    # job_scorer_mode()

        

# Fromating ai json response to be more readable 
# def format_cover_letter_json(ai_reply):
#     try:
#         result = json.loads(ai_reply)
#         print(f"\nCover Letter: \n\n{result['opening']}")
#         print(f"\n{result['middle']}\n")
#         print(f"{result['gap']}\n")
#         print(f"{result['closing']}\n")
#     except json.JSONDecodeError:
#         print(ai_reply) # fallback if LLM doesn't return valid Json