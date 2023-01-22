from constants_nikluz import OPENAI_ORG_KEY, OPENAI_API_KEY
from bot_identities import bots
from datetime import datetime
import openai
import json
import os


def init_openai():
    openai.organization = OPENAI_ORG_KEY
    openai.api_key = OPENAI_API_KEY


def have_conversation(config: dict = {}):
    """
    Begin or continue a conversation with the AI model

    If no bot is chosen, the default bot will be used, which is open ended.
    """
    if config:
        if not "on_resume" in config:
            # build additional keys for config
            config["conversation"] = ""
            config["on_resume"] = False
            config["on_resume_conversation_path"] = ""
    else:
        # build default config
        config["bot_identity"] = bots.AI
        config["resume_saved_conversation"] = False
        config["conversation"] = ""
        config["on_resume"] = False
        config["on_resume_conversation_path"] = ""



    # print(json.dumps(config, indent=2))
    # exit()

    if config["resume_saved_conversation"]:
        conversation_data = choose_saved_conversation()
        resume_saved_conversation(conversation_data , True)
    else:


        bot = config["bot_identity"]

        bot_id = bot["identity"]
        bot_config = bot["config"]
        exit_text = bot["exit_text"]


        conversation_path = ""
        if config["on_resume"]:
            conversation_path = config["on_resume_conversation_path"]
        else:
            conversation_path = f"./conversations/conversation_{get_new_conversation_number()}.txt"
            config["on_resume"] = True
            config["on_resume_conversation_path"] = conversation_path
        

        # get user prompt
        prompt = input("prompt: ")


        if config["conversation"] == "":
            # if conversation is empty, load up a starter pack based on the bot
            config["conversation"] = bot["starter_pack"] + f"\nHuman: {prompt}\n{bot_id}: "
            with open(conversation_path, "w") as conversation_file:
                conversation_file.write(config["conversation"])
        else:
            # else load the conversation from the text file and continue
            with open(conversation_path, "a") as conversation_file:
                conversation_file.write(f"\nHuman: {prompt}\n{bot_id}: ")
            with open(conversation_path, "r") as conversation_file:
                config["conversation"] = conversation_file.read()

        
        if prompt == "exit":
            # kill the bot 
            print(f"{bot_id}: {exit_text}")
            with open(conversation_path, "a") as conversation_file:
                conversation_file.write(f"{exit_text}\n")
            exit()
        else:
            # continue harassing the bot
            # make a call to the API and get bot response
            res = openai.Completion.create(
                model="text-davinci-003",
                prompt=config["conversation"],
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
            with open(conversation_path, "a") as conversation_file:
                conversation_file.write(f"{txt_response}\n")

            # force conversation to continue (yeah I know this is hacky right now)
            have_conversation(config)


def resume_saved_conversation(conversation_data: dict = {}, on_resume: bool = False):
    """
    Begin or continue a conversation with the AI model

    If no bot is chosen, the default bot will be used, which is open ended.
    """

    bot_identity = conversation_data["bot_identity"]


    bot_id = bot_identity["identity"]
    bot_config = bot_identity["config"]
    resume_interaction = bot_identity["resume_interaction"]
    exit_text = bot_identity["exit_text"]
    conversation_path = conversation_data["file_path"]

    # get user prompt
    prompt = input("prompt: ")

    if(on_resume):
        # print and append resume interaction to conversation file
        with open(conversation_path, "a") as conversation_file:
            conversation_file.write(resume_interaction)
    

    # else load the conversation from the text file and continue
    with open(conversation_path, "a") as conversation_file:
        conversation_file.write(f"\nHuman: {prompt}\n{bot_id}: ")
    with open(conversation_path, "r") as conversation_file:
        conversation = conversation_file.read()

    
    if prompt == "exit":
        # kill the bot 
        print(f"{bot_id}: {exit_text}")
        with open(conversation_path, "a") as conversation_file:
            conversation_file.write(f"{exit_text}\n")
        exit()
    else:
        # continue harassing the bot
        # make a call to the API and get bot response
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=conversation,
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
        with open(conversation_path, "a") as conversation_file:
            conversation_file.write(f"{txt_response}\n")

        # force conversation to continue (yeah I know this is hacky right now)
        resume_conversation(conversation_data, False)



def choose_saved_conversation():
    # Get the list of all files and directories
    path = "./conversations/"
    files = os.listdir(path)

    conversation_list = []
    # prints all files
    for file in files:
        print("========================================================================================================")
        file_data = {}
        file_path = f"{path}{file}"
        file_index = int(file.split("_")[1].split(".")[0])
        file_last_modified = datetime.fromtimestamp(os.stat(file_path).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        file_data["index"] = file_index
        file_data["last_modified"] = file_last_modified
        print(f"\\/\\/\\/\\/ INDEX: {file_index} - LAST MODIFIED: {file_last_modified} \\/\\/\\/\\/")
        with open(file_path, "r") as file:
            text = file.read()
            bot_name = extract_bot_name(text)
            bot_identity = getattr(bots, bot_name.upper())
            file_data["bot_identity"] = bot_identity
            print("\n")
            lines = file.readlines()
            last_8_lines = lines[-8:]
            for line in last_8_lines:
                print(line)
        file_data["file_path"] = file_path

        conversation_list.append(file_data)
        print(f"/\\/\\/\\/\\ INDEX: {file_index} - LAST MODIFIED: {file_last_modified} /\\/\\/\\/\\")
        print("========================================================================================================")
    choice = int(input("Enter the index of the conversation you want to retrieve: "))

    print("here are the consequences of your choice:\n\n" + str(json.dumps(conversation_list[choice],indent=2)))

    return conversation_list[choice]


def extract_bot_name(text):
    lines = text.split("\n")
    bot_name = ""
    human_line = False
    for line in lines:
        print(line)
        if human_line:
            bot_name = line.split(":")[0]
            break
        if "Human:" in line:
            human_line = True
    if(human_line):
        return bot_name
    else:
        print(f"bot not found... sorry.")
        exit()




def get_new_conversation_number():
    path = "./conversations/"
    files = os.listdir(path)
    if files:
        numbers = [int(filename.split("_")[1].split(".")[0]) for filename in files]
        latest_conversation_number = max(numbers)
        new_conversation_number = latest_conversation_number + 1
        return new_conversation_number
    else:
        return 0


        


def main():
    init_openai()

    config = {
        "bot_identity": bots.MARV, # can be changed to bots.AI, bots.SWEETIE, bots.MARV or bots.<YOUR_CUSTOM_BOT>
        "resume_saved_conversation": False,  # change to true if you want to continue a previously saved conversation
    }

    have_conversation(config) 
    # have_conversation()


if __name__ == "__main__":
  main()