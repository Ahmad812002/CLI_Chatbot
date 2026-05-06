This is a project called CLI_chatbot. I build it for learning reason.
it's a Command Line Interface bot uses openai model API which is gpt-oss-120b.

i tried to add reading files feature but the models doesn't allow it, so i decieded to keep it as a chat only.

here is the code for reading a file 
try:
    if(user_input.__contains__('.txt') or user_input.__contains__('.pdf') or user_input.__contains__('.docx')):
    with open(user_input, 'rb') as file:
        file_text = file.read()
except IOError:
    print(f"Error: Could not read file {user_input}. Please check the path and try again.")
    continue


# To run it you need to install python and an venv 
