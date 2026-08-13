from data_access.embeddings import get_embedding, search_embedding
from data_access.db import embeddings_collection, preferences_collection, get_prefrences_records
import json
from config.client import initialize_client
import openai
from config.prompts import format_job_scorer_prompt
from models import cover_letter_generator, chat_bot

ids = embeddings_collection.get()["ids"]

client = initialize_client()

messages_arr = []
last_reply = ""


# Handleing job seeker mode chunk it into smaller pieces, get the embedding of each chunk and search for similar documents in the database,.    
def job_scorer_mode():
    
    global messages_arr, last_reply
    if not messages_arr:
        job_preferences = update_or_add_preferences()
        print("Paste Job description to tell if it's match your career or not or ask me about your career fit score for a job description, or type 'exit' to quit:\n")
    else:
        job_preferences = get_prefrences_records()

    while True:
        
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            return
        if len(user_input.strip()) < 50:
            # print("Rendering to chat mode...")
            # chat_bot.chat_bot_mode(user_input)
            print("Please provide a valid job description")
            continue
        if not user_input:
            continue
            
        messages_arr.append({"role": "user", "content": user_input})
        # Case 3 : If the user input is a job description, get the embedding and search for similar documents then attacht them to the LLM.
        profile_chunks = process_job_description(user_input)
        job_scorer_formated_result = format_job_scorer_prompt(profile_chunks, job_preferences, user_input)
        try:
            response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages= [job_scorer_formated_result] + messages_arr[-10:],
            max_tokens=1024,
            temperature=0.0 # For a job fit scorer, reliable scoring, temperature (creativity) should be low
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
        last_reply = response.choices[0].message.content
        format_job_scorer_json(last_reply)

        messages_arr.append({"role": "assistant", "content": last_reply})
        if(last_reply in "Sorry! there is no job description please enter a valid one or i couldn't answer you."):
            continue

        print("\n\nWould you like to generate a cover letter for this job? (yes/no)\n")
        user_input = input("You: ").strip()
        if user_input.lower() == "yes":
            cover_letter_generator.generate_cover_letter(profile_chunks, user_input, last_reply)

def update_or_add_preferences():
    global ids

    doc_id = str(max(int(i) for i in ids) + 1)

    try:
        existing_preferences = get_prefrences_records()
        if existing_preferences is not None:
            print("Preferences already exist in the database, if you wanna update them now write 'update'.")
            update_choice = input("You: ").strip().lower()
            if update_choice == "update":
                print("Which preferences you are looking for in your next job? (e.g. remote, hybrid, full-time, part-time, contract, internship, location etc.)")
                preferences_input = input("You: ").strip()
                try:
                    preferences_collection.update(
                        ids=[str(int(doc_id))],
                        documents=[preferences_input],
                    )
                    return preferences_input
                except Exception as e:
                    print(f"Error occurred while updating preferences: {e}")
                    return None
            return existing_preferences

        print("Which preferences you are looking for in your next job? (e.g. remote, hybrid, full-time, part-time, contract, internship, location etc.)")
        preferences_input = input("You: ").strip()
        try:
            preferences_collection.add(
                ids=[str(int(doc_id))],
                documents=[preferences_input],
            )
            return preferences_input
        except Exception as e:
            print(f"Error occurred while adding preferences: {e}")
            return None
    except Exception as e:
        print(f"Error occurred while checking preferences: {e}")
        return None

# Fromating ai json response to be more readable 
def format_job_scorer_json(ai_reply):
    try:
        result = json.loads(ai_reply)
        print(f"\nScore Category: {result['fit_category']}")
        print(f"\nJob Fit Score: {result['fit_score']}/100")
        print(f"\nMatching Points:")
        for point in result['matching_points']:
            print(f"  • {point}")
        print(f"\nGaps:")
        for gap in result['gaps']:
            print(f"  • {gap}")
        print(f"\nReasoning: {result['reasoning']}\n\n")
    except json.JSONDecodeError:
        print(ai_reply) # fallback if LLM doesn't return valid Json

# It will get the embedding of the entire job description and search for similar documents in the database.
def process_job_description(job_description):
    try:
        job_embedding = get_embedding(job_description)
        profile_chunks = search_embedding(job_embedding)
        if profile_chunks:
            return "\n".join([chunk['documents'] for chunk in profile_chunks])
        return None
    except Exception as e:
        print(f"Error occurred while processing job description: {e}")
        return None

