import dearpygui.dearpygui as dpg
import chat, requests, shutil, re, pyperclip
from screeninfo import get_monitors
import os


screen_w = get_monitors()[0].width
screen_h = get_monitors()[0].height
app_w = 800
app_h = 600

fields = {}
field_data = {}

conversation_data = []
conversation_list = []

dpg.create_context()

# with dpg.font_registry():
#     default_font = dpg.add_font("Roboto-Black.ttf", 20)
#     second_font = dpg.add_font("Roboto-Black.ttf", 10)

# dpg.bind_font(default_font)

def print_value(sender):
    print(dpg.get_value(sender))

def copy_to_clipboard(sender):
    val = dpg.get_value(fields["response"])
    print("{}: {} \n\ncopied to clipboard!".format(type(val),val))
    pyperclip.copy(val)

def make_api_call(sender):

    chat.init_openai()

    conversation = {}
    config = {}

    if dpg.get_value(fields["conversation_type"]) == "New Conversation":
        dpg.hide_item(fields["response"])
        dpg.hide_item(fields["copy"])
        dpg.hide_item(fields["conversation_list"])
        dpg.show_item(fields["loading_indicator"])

        config = {
            "in_gui": True,
            "bot_identity": getattr(chat.bots, dpg.get_value(fields["bots"]).upper()),
            "conversation": "",
            "model": dpg.get_value(fields["engine"]),
            "prompt": dpg.get_value(fields["prompt"]),
            "resume_saved_conversation": False,
            "on_resume": False,
            "on_resume_conversation_path": ""
        }
        response = chat.have_conversation(config)
        dpg.set_value(fields["response"], response)
        dpg.show_item(fields["response"])
        dpg.show_item(fields["copy"])
        dpg.set_value(fields["prompt"], "")
        dpg.hide_item(fields["loading_indicator"])
    elif dpg.get_value(fields["conversation_type"]) == "No Memory":
        dpg.hide_item(fields["response"])
        dpg.hide_item(fields["copy"])
        dpg.hide_item(fields["conversation_list"])
        dpg.show_item(fields["loading_indicator"])

        config = {
            "no_memory": True,
            "bot_identity": getattr(chat.bots, dpg.get_value(fields["bots"]).upper()),
            "conversation": "",
            "temperature": dpg.get_value(fields["temp"]),
            "tokens": dpg.get_value(fields["tokens"]),
            "model": dpg.get_value(fields["engine"]),
            "prompt": dpg.get_value(fields["prompt"])
        }
        response = chat.have_conversation(config)
        dpg.set_value(fields["response"], response)
        dpg.show_item(fields["response"])
        dpg.show_item(fields["copy"])
        dpg.set_value(fields["prompt"], "")
        dpg.hide_item(fields["loading_indicator"])
    elif dpg.get_value(fields["conversation_type"]) == "Load Conversation":
        dpg.hide_item(fields["response"])
        dpg.hide_item(fields["copy"])
        dpg.hide_item(fields["conversation_list"])
        dpg.show_item(fields["loading_indicator"])
        conversation_index = int(str(dpg.get_value(fields["conversation_list"])[0]))
        conversation = None
        for c in conversation_data:
            if c["index"] == conversation_index:
                conversation = c
        conversation["in_gui"] = True
        conversation["prompt"] = dpg.get_value(fields["prompt"])
        response = chat.resume_saved_conversation(conversation)
        dpg.set_value(fields["response"], response)
        dpg.show_item(fields["response"])
        dpg.show_item(fields["copy"])
        dpg.set_value(fields["prompt"], "")
        dpg.hide_item(fields["loading_indicator"])
    else:
        print("You must choose a conversation type.")
        exit()


def display_response(res):
    print(res)

def format_response(res):
    lines = []
    line = ''
    words = res.split()
    for word in words:
        if len(line) + len(word) <= 80:
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)
    return '\n'.join(lines)

def get_image(url, name):
    file_name = "{}.png".format(name)
    res = requests.get(url, stream = True)
    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)


        width, height, channels, data = dpg.load_image(file_name)
        img_tag = re.sub('[\W_]+','',name)

        shutil.move(file_name, "./images/{}".format(file_name))

        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=img_tag)

        return data

    else:
        print('Image Couldn\'t be retrieved')


def on_select_conversation_type(sender):
    if dpg.get_value(sender) == "Load Conversation":
        dpg.show_item(fields["conversation_list"])
        dpg.hide_item(fields["temp"])
        dpg.hide_item(fields["tokens"])
    elif dpg.get_value(sender) == "New Conversation":
        dpg.hide_item(fields["conversation_list"])
        dpg.hide_item(fields["temp"])
        dpg.hide_item(fields["tokens"])
    elif dpg.get_value(sender) == "No Memory":
        dpg.hide_item(fields["conversation_list"])
        dpg.show_item(fields["temp"])
        dpg.show_item(fields["tokens"])



width, height, channels, data = dpg.load_image("./images/temp.jpg")

with dpg.texture_registry(show=False):
    dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag="imgraw")


with dpg.window(width=300, tag="Primary Window"):

    with dpg.group(horizontal=True):
        with dpg.group():
            path = "./bot_identities/"
            bot_list = os.listdir(path)
            exclusion_list = ["__inity__.py","bot_template.py","bots.py", "__pycache__"]
            bots = [item[:-3].title() for item in bot_list if item not in exclusion_list]
            exclude = ""
            combo_bots = dpg.add_combo(
                tag="bots",
                label="Choose Bot",
                items=bots,
                default_value="Default",
                callback=print_value
            )
            fields["bots"] = combo_bots

            combo_engines = dpg.add_combo(
                tag="engines",
                label="Choose Engine",
                items=("text-davinci-003", "text-davinci-002","text-davinci-001","text-curie-001","text-babbage-001", "text-ada-001", "code-davinci-002","code-cushman-001"),
                default_value="text-davinci-002",
                callback=print_value
            )
            fields["engine"] = combo_engines


            conversation_type = dpg.add_radio_button(
                tag="conversation_type",
                label="Type of conversation",
                items=("New Conversation", "No Memory", "Load Conversation"),
                default_value="New Conversation",
                horizontal=True,
                callback=on_select_conversation_type
            )
            fields["conversation_type"] = conversation_type

            slider_temperature = dpg.add_slider_float(
                tag="temp",
                label="Temperature",
                min_value=0.0,
                max_value=1.0,
                default_value=1.0,
                show=False,
                callback=print_value
            )
            fields["temp"] = slider_temperature

            slider_tokens = dpg.add_slider_int(
                tag="tokens",
                label="Max Tokens",
                min_value=50,
                max_value=3950,
                default_value=1000,
                show=False,
                callback=print_value
            )
            fields["tokens"] = slider_tokens


            conversation_data = chat.choose_saved_conversation(in_gui=True)
            conversations = tuple(str(obj['index']) + "\n" + re.sub(r'(?:\n){2,}', '\n', obj['last_n_lines'].strip()) for obj in conversation_data)

            conversation_list = dpg.add_radio_button(
                tag="conversation_list",
                label="Conversation List",
                items=conversations,
                default_value=conversations[0],
                show=False,
            )
            fields["conversation_list"] = conversation_list
            fields["conversation_data"] = conversation_data
            field_data["conversation_list"] = conversations

    dpg.add_separator()
    dpg.add_separator()
    with dpg.group(horizontal=True):
        with dpg.group():

            input_prompt = dpg.add_input_text(
                tag="prompt",
                label="Prompt",
                height=100,
                multiline=True,
                callback=print_value
            )
            fields["prompt"] = input_prompt
    button_send = dpg.add_button(
        label="Send",
        width=520,
        height=50,
        callback=make_api_call
    )
        
    dpg.add_separator()
    dpg.add_separator()

    with dpg.group(horizontal=True):

        text_response = dpg.add_text(
            tag="response",
            label="Response",
            wrap=600,
            show=False
        )
        fields["response"] = text_response



        img_container = dpg.add_image("imgraw",
            tag="img",
            width=512,
            height=512,
            show=False
        )
        fields["img"] = img_container

        button_copy = dpg.add_button(
            tag="copy",
            label="Copy to Clipboard",
            show=False,
            callback=copy_to_clipboard
        )
        fields["copy"] = button_copy


    loading_indicator = dpg.add_loading_indicator(
        tag="loading_indicator",
        pos=[400,300],
        show=False,
    )

    fields["loading_indicator"] = loading_indicator


# dpg.show_debug()
# dpg.show_metrics()
dpg.create_viewport(title='openAI Toolbox', width=app_w, height=app_h, x_pos = int((screen_w - app_w) / 2), y_pos = int((screen_h - app_h) / 2))
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.show_font_manager()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()

