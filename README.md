# OpenAI Toolbox
A command line and gui application for interacting with the OpenAI API

## Features
- Bot Identities - use the built in bots or create your own with it's own personality
- Conversation History - main conversation is ongoing and stored in a txt file
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
- [ ] Expanded chat history. 
  - My idea for this is to store all conversations in a folder, append an index to conversation.py for each conversation, as well as adding an optional parameter to the ```have_conversation()``` function to indicate if you want to pick up from an old chat or not.
    - Example: ```have_conversation(have_conversation(conversation: str = "", bot_identity: dict = bots.AI, resume_convercation: bool = False):)``` 
    - Separate ```resume_conversation()``` function will be fired if ```True``` and it will ask you which conversation you want to pick up on
    - This will load the previous bot and conversation automatically as well as a "resume interaction" that happens before your first prompt
    - Example resume interaction: ```r"Human: Hello, I'm back. Did you miss me?\n{bot_id}: {resume_text}"```
    - Resume text will be added as a bot value during this implementation.
- [ ] User Identities
  - This may be a tricky one and could get scrapped, but I may implement the ability for the user to setup a custom Identity as well.
  - Example: User is a Troll who lives in a cave and has never seen the outside world. Limited comprehension. Sometimes speaks in grunts.
  - This might actually be dumb.
- [ ] Add more bots.
- [ ] Make a ```chat.py``` and ```open_ai_toolbox.py``` baby.
  - Basically make them work together.


