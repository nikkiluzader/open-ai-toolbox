# OpenAI Toolbox
A command line and gui application for interacting with the OpenAI API

## Updates
- 2023-01-22 
  - You can now pass a simple config into the ```have_conversation()``` function.
  - Added expanded chat history. Start a new conversation or load a previous one (just set ```resume_saved_conversation``` to ```True```)
  - Added resume interactions to all bots (you dont see these printed, but it helps with continuity in the conversations)

## Features
- Bot Identities - use the built in bots or create your own with it's own personality
- Conversation History - Conversations are ongoing. You can load previous conversations or start a new one.
- Easy setup - nothing too fancy (yet)

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
- [x] Expanded chat history. 
- [ ] User Identities
  - This may be a tricky one and could get scrapped, but I may implement the ability for the user to setup a custom Identity as well.
  - Example: User is a Troll who lives in a cave and has never seen the outside world. Limited comprehension. Sometimes speaks in grunts.
  - This might actually be dumb.
- [ ] Add more bots.
- [ ] Make a ```chat.py``` and ```open_ai_toolbox.py``` baby.
  - Basically make them work together.


