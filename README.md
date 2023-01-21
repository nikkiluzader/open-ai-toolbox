# OpenAI Toolbox
A command line and gui application for interacting with the OpenAI API

## Notes
- Currently, you can only run ```chat.py``` (**after following the setup instructions**).
  - ```chat.py``` is the command-line tool that lets you hold a conversation.
- The other python file, ```open_api_toolbox.py``` is the GUI application that I plan on integrating with ```chat.py```.
  - It is not ready, play with it if you want.
- The conversation is handled with file storage in ```conversation.txt```.
  - By default, ```conversation.txt``` is updated after every prompt.
  - The conversation is stored even after exiting the command line.
  - If you start a new conversation, the old ```conversation.txt``` will be overwritten.
  - If you want to save a previous conversation before starting a new one, rename ```conversation.txt``` to something else.
    - If you rename it for safekeeping, a new ```conversation.txt``` file will be generated automatically when you start a new conversation.
- See roadmap for planned updates.

## Setup
1. Go to https://beta.openai.com/ and sign up.
2. Go to https://beta.openai.com/account/org-settings and get your Organization ID.
3. Go to https://beta.openai.com/account/api-keys and get your API key.
4. Put your keys in ```constants.py```.
5. Change the import statement in ```chat.py```. It should be ```from constants import OPENAI_ORG_KEY, OPENAI_API_KEY```
6. Run ```pip install -r requirements.txt```
7. Run ```python chat.py```


## Modifications
- To change the bot that is being used, open ```chat.py``` and change the bot identity in the main function call for ```have_conversation()```.
- You can create your own custom bot by making a copy of ```bot_template.py``` and updating it to your liking
  - To complete this step, must open ```bots.py``` and write a new import statement with your bot's name in order to access it as a bot identity.
    - The bot's name is the name of the dict


## Roadmap
- [x] Release a functional version.
- [x] Make a custom bot template.
- [ ] Add more bots.
- [ ] Make a ```chat.py``` and ```open_ai_toolbox.py``` baby.


