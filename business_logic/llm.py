from config.client import initialize_client
import openai   
from config.prompts import chat_bot_prompt
from business_logic.chat_logic import get_embedding, get_embedding_result



client = initialize_client()

messages_arr = []

# LLM function to generate a job fit score based on the job description and user preferences
def llm_scorer(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages= [prompt] + messages_arr[-10:] ,
            max_tokens=1024,
            temperature=0.0 # For a job fit scorer, reliable scoring, temperature (creativity) should be low
        )
    except openai.APIError as e:
        return{ "API Error:": str(e) }
    except openai.APITimeoutError as e:
        return { "Timeout Error:": str(e) }
    except openai.APIConnectionError as e:
        return { "API Connection Error:": str(e) }
    except openai.BadRequestError as e:
        return { "Invalid Request Error (Bad Request):": str(e) }
    except openai.InternalServerError as e:
        return { "Internal Server Error:": str(e) }
    except openai.RateLimitError as e:
        return{ "Rate Limit Error:": str(e) }
    except openai.AuthenticationError as e:
        return { "Authentication Error:": str(e) }
    if(response is None):
        return { "error": "Sorry, I could not generate a response." }
    return response.choices[0].message.content

# LLM function to generate a cover letter based
def llm_cover_letter(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages= [prompt] + messages_arr[-2:],
            max_tokens=1024,
            temperature=1
        )
        messages_arr.append({"role": "user", "content": prompt})
    except openai.APIError as e:
            return{ "API Error:": str(e) }
    except openai.APITimeoutError as e:
        return { "Timeout Error:": str(e) }
    except openai.APIConnectionError as e:
        return { "API Connection Error:": str(e) }
    except openai.BadRequestError as e:
        return { "Invalid Request Error (Bad Request):": str(e) }
    except openai.InternalServerError as e:
        return { "Internal Server Error:": str(e) }
    except openai.RateLimitError as e:
        return{ "Rate Limit Error:": str(e) }
    except openai.AuthenticationError as e:
        return { "Authentication Error:": str(e) }
    
    messages_arr.append({"role": "assistant", "content": response.choices[0].message.content})
    if(response is None):
        return { "error": "Sorry, I could not generate a cover letter." }
    return response.choices[0].message.content

# i need a collection for messages to be saved, maybe i need to separate each model messages.
# LLM function to generate chat_bot
def llm_chat(message):
    chunks = ""
    try:
        messages_arr.append({"role": "user", "content": message})
        #Data preperation

        embedded_vector = get_embedding(message)
        vector_embedding_result = get_embedding_result(embedded_vector)

        if vector_embedding_result is not None:
            chunks = "\n".join([chunk['documents'] for chunk in vector_embedding_result])
    
        #LLM part
        response = client.chat.completions.create(
            model = "gpt-oss-120b",
            messages = [chat_bot_prompt(chunks)] + messages_arr[-10:],
            temperature=1.0, # This is to make the model's response more creative and less deterministic, it will also help the model to provide more diverse responses and avoid repeating the same response.
            reasoning_effort = "high", # This is to make the model put more effort into reasoning and providing a more accurate and relevant response, it will take more time to generate a response but it will be worth it.
            verbosity = "low", # This is to make the model's response more concise and to the point, it will not provide unnecessary details or explanations.
            web_search_options = { "enabled": True }, # This is to enable the model to use web search to find relevant information and provide more accurate and up-to-date responses, it will also help the model to provide more detailed explanations and examples.
            max_tokens=1024,
        )

    except openai.APIError as e:
        return{ "API Error:": str(e) }
    except openai.APITimeoutError as e:
        return { "Timeout Error:": str(e) }
    except openai.APIConnectionError as e:
        return { "API Connection Error:": str(e) }
    except openai.BadRequestError as e:
        return { "Invalid Request Error (Bad Request):": str(e) }
    except openai.InternalServerError as e:
        return { "Internal Server Error:": str(e) }
    except openai.RateLimitError as e:
        return{ "Rate Limit Error:": str(e) }
    except openai.AuthenticationError as e:
        return { "Authentication Error:": str(e) }
    
    messages_arr.append({"role": "assistant", "content": response.choices[0].message.content})

    if(response is None):
        return { "error": "Sorry, I could not generate a response." }
    return response.choices[0].message.content