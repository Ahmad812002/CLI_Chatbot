from config.client import initialize_client
import openai
from config.prompts import cover_letter_prompt_format



client = initialize_client()


def generate_cover_letter(profile_chunks, job_description, job_scorer_result):
    cover_letter_prompt_format(profile_chunks, job_description, job_scorer_result)
    try:

        response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages= [cover_letter_prompt_format(profile_chunks, job_description, job_scorer_result)],
                max_tokens=1024,
                temperature=1
            )
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

    print(response.choices[0].message.content)
