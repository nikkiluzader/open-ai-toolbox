"""
This is the vanilla, open ended AI bot 
The original example code is provided by OpenAI at https://beta.openai.com/examples/default-chat
I have excluded a few config parameters that I prefer to change globally in the main .py file
Those parameters are: model, max_tokens, stop
You may change any of the constants to your liking.
"""


IDENTITY = "AI"
PERSONALITY = "is helpful, creative, clever, and very friendly."
START_PROMPT = f"The following is a conversation with an AI assistant.\nThe assistant is: {PERSONALITY}\n\n"
INTERACTION_1 = f"Human: Hello, who are you?\n{IDENTITY}: I am an AI created by OpenAI. How can I help you today?\n\n"
INTERACTION_2 = f"Human: What is 2 + 2?\n{IDENTITY}: I am an AI created by OpenAI. How can I help you today?\n\n"
STARTER_PACK = f"{START_PROMPT}{INTERACTION_1}{INTERACTION_2}"
EXIT_TEXT = "Goodbye my friend!\n\n"
RESUME_INTERACTION = f"Human: Just kidding, I'm back.\n{IDENTITY}: Hello there, how can I assist you?\n\n"
TEMPERATURE = 0.9
TOP_P = 1
FREQUENCY_PENALTY = 0.0
PRESENCE_PENALTY = 0.6


AI = {
    "identity": IDENTITY,
    "starter_pack": STARTER_PACK,
    "exit_text": EXIT_TEXT,
    "resume_interaction": RESUME_INTERACTION,
    "config": {
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "frequency_penalty": FREQUENCY_PENALTY,
        "presence_penalty": PRESENCE_PENALTY
    }
}