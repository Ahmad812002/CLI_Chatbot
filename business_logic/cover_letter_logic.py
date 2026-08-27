import json
from llm import llm_cover_letter



def run_cover_letter(profile_chunks, job_description, job_scorer_result):
    response = llm_cover_letter(profile_chunks, job_description, job_scorer_result)

    formated_response = format_cover_letter_json(response)
    return {
        "Cover Letter: ": formated_response
    }

# Fromating ai json response to be more readable 
def format_cover_letter_json(ai_reply):
    try:
        result = json.loads(ai_reply)
        # print(f"\nCover Letter: \n\n{result['opening']}")
        # print(f"\n{result['middle']}\n")
        # print(f"{result['gap']}\n")
        # print(f"{result['closing']}\n")
        return {
            "opening": result['opening'],
            "middle": result['middle'],
            "gap": result['gap'],
            "closing": result['closing']
        }
    except json.JSONDecodeError:
        # print(ai_reply) # fallback if LLM doesn't return valid Json
        return {
            "error": "Invalid JSON response from LLM",
            "raw_response": ai_reply
        }