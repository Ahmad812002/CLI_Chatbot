from models.chat_bot import chat_bot_mode
from models.job_scorer_bot import job_scorer_mode


# Handleing bot type (job_seeker or chat_bot)
def bot_mode():
    print("Welcome to the AI Career Coach!")
    print("Please select a mode:")
    print("\n1. Assistant\n")
    print("2. Job Seeker")

    while True:
        mode = input("Enter the number of your choice (or type 'exit' to quit): ").strip().lower()
        if mode in ["1", "assistant"]:
            chat_bot_mode()
            break
        elif mode in ["2", "job seeker", "job_seeker"]:
            job_scorer_mode()
            break
        elif mode in ["exit", "quit"]:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    try:
        bot_mode()
    except KeyboardInterrupt:
        print("\nSession ended.")

if __name__ == "__main__":
    main()