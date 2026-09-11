import json

from config.prompts import cover_letter_prompt
from .llm import llm_cover_letter

def run_cover_letter(profile_chunks, job_description, matching_points =[], gaps =[], reasoning = ""):
    try:

        formated_prompt = cover_letter_prompt(
            profile_chunks, 
            job_description,
            matching_points,
            gaps,
            reasoning
        )
        response = llm_cover_letter(formated_prompt)

        formated_response = format_cover_letter_json(response)
        if(formated_response['opening'] is not None):
            return {
                        "opening": formated_response['opening'],
                        "middle": formated_response['middle'],
                        "gap": formated_response['gap'],
                        "closing": formated_response['closing']
                    }
    except Exception as e:
        raise ValueError(f"Error occurred while generating cover letter: {str(e)}")

# Fromating ai json response to be more readable 
def format_cover_letter_json(ai_reply):
    try:
        result = json.loads(ai_reply)
        return {
            "opening": result['opening'],
            "middle": result['middle'],
            "gap": result['gap'],
            "closing": result['closing']
        }
    except json.JSONDecodeError:
            raise ValueError(f"LLM returned invalid JSON: {ai_reply[:10]}")