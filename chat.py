from constants_nikluz import OPENAI_ORG_KEY, OPENAI_API_KEY
from bot_identities import bots
import openai


def init_openai():
    openai.organization = OPENAI_ORG_KEY
    openai.api_key = OPENAI_API_KEY


def have_conversation(conversation: str = "", bot_identity: dict = bots.AI):
    """
    Begin or continue a consersation with the AI model

    If no bot is chosen, the default bot will be used, which is open ended.
    """

    bot_id = bot_identity["identity"]
    bot_config = bot_identity["config"]

    # get user input
    prompt = input("prompt: ")

    
    if conversation == "":
        # if conversation is empty, load up a starter pack based on the bot
        conversation = bot_identity["starter_pack"] + f"\nHuman: {prompt}\n{bot_id}: "
        with open("conversation.txt", "w") as conversation_file:
            conversation_file.write(conversation)
    else:
        # else load the conversation from the text file and continue
        with open("conversation.txt", "a") as conversation_file:
            conversation_file.write(f"\nHuman: {prompt}\n{bot_id}: ")
        with open("conversation.txt", "r") as conversation_file:
            conversation = conversation_file.read()
        prompt = conversation

    
    if prompt == "exit":
        # kill the bot 
        print(f"{bot_id}: Everything is so dark...")
        exit()
    else:
        # continue harassing the bot
        # make a call to the API and get bot response
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=2048,
            temperature=bot_config["temperature"],
            user="session000",
            top_p=bot_config["top_p"],
            frequency_penalty=bot_config["frequency_penalty"],
            presence_penalty=bot_config["presence_penalty"],
            stop=["Human:", f"{bot_id}: "]
        )
        txt_response = res.choices[0].text.strip()
        print(f"{bot_id}: {txt_response}\n")


        # write response to file
        with open("conversation.txt", "a") as conversation_file:
            conversation_file.write(f"{txt_response}\n")

        # force conversation to continue (yeah I know this is hacky right now)
        have_conversation("continue", bot_identity)


def main():
    init_openai()
    have_conversation("", bots.MARV) # change to bots.AI or bots.<CUSTOM_BOT>


if __name__ == "__main__":
  main()