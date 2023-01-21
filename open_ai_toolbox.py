import dearpygui.dearpygui as dpg
import chat, requests, shutil, re, pyperclip
from screeninfo import get_monitors


screen_w = get_monitors()[0].width
screen_h = get_monitors()[0].height
app_w = 800
app_h = 600

field_list = {}

dpg.create_context()

# with dpg.font_registry():
#     default_font = dpg.add_font("Roboto-Black.ttf", 20)
#     second_font = dpg.add_font("Roboto-Black.ttf", 10)

# dpg.bind_font(default_font)

def print_value(sender):
    print(dpg.get_value(sender))

def copy_to_clipboard(sender):
    val = dpg.get_value(field_list["response"])
    print("{}: {} \n\ncopied to clipboard!".format(type(val),val))
    pyperclip.copy(val)

def make_api_call(sender):
    dpg.show_item(field_list["lin"])

    chat.init_openai()
    
    
    if(dpg.get_value(field_list["mtype"]) == "GPT3 - Completion"):
        dpg.hide_item(field_list["copy"])
        res = chat.run_model({"mtype":"com", "engine": dpg.get_value(field_list["engine"]), "tokens": dpg.get_value(field_list["tokens"]), "temperature": dpg.get_value(field_list["temp"]), "prompt": dpg.get_value(field_list["prompt"])})
        #res = format_response(res)
        #dpg.set_value(field_list["prompt"], "")
        dpg.hide_item(field_list["lin"])
        dpg.hide_item(field_list["img"])
        dpg.show_item(field_list["response"])
        dpg.show_item(field_list["copy"])
        dpg.set_value(field_list["response"], res[2:])
        
    elif(dpg.get_value(field_list["mtype"]) == "Codex"):
        dpg.hide_item(field_list["copy"])
        res = chat.run_model({"mtype":"cod", "engine": dpg.get_value(field_list["engine"]), "tokens": dpg.get_value(field_list["tokens"]), "temperature": dpg.get_value(field_list["temp"]), "prompt": dpg.get_value(field_list["prompt"])})
        #dpg.set_value(field_list["prompt"], "")
        dpg.hide_item(field_list["lin"])
        dpg.hide_item(field_list["img"])
        dpg.show_item(field_list["response"])
        dpg.show_item(field_list["copy"])
        dpg.set_value(field_list["response"], res[2:])

    elif(dpg.get_value(field_list["mtype"]) == "DALLE - Image"):
        dpg.hide_item(field_list["copy"])
        res = chat.run_model({"mtype":"img", "temperature": dpg.get_value(field_list["temp"]), "prompt": dpg.get_value(field_list["prompt"])})
        dpg.hide_item(field_list["img"])
        imgdata = get_image(res, dpg.get_value(field_list["prompt"]))
        #dpg.set_value(field_list["prompt"], "")
        dpg.set_value("imgraw", imgdata)
        dpg.hide_item(field_list["lin"])
        dpg.hide_item(field_list["response"])
        dpg.show_item(field_list["img"])


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



width, height, channels, data = dpg.load_image("./images/11.png")

with dpg.texture_registry(show=False):
    dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag="imgraw")


with dpg.window(width=300, tag="Primary Window"):

    with dpg.group(horizontal=True):
        with dpg.group():

            combo_models = dpg.add_combo(
                tag="models",
                label="Choose Model",
                items=("GPT3 - Completion", "Codex", "DALLE - Image"),
                default_value="GPT3 - Completion",
                callback=print_value
            )
            field_list["mtype"] = combo_models

            combo_engines = dpg.add_combo(
                tag="engines",
                label="Choose Engine",
                items=("text-davinci-003", "text-davinci-002","text-davinci-001","text-curie-001","text-babbage-001", "text-ada-001", "code-davinci-002","code-cushman-001"),
                default_value="text-davinci-002",
                callback=print_value
            )
            field_list["engine"] = combo_engines

            slider_temperature = dpg.add_slider_float(
                tag="temp",
                label="Temperature",
                min_value=0.0,
                max_value=1.0,
                default_value=1.0,
                callback=print_value
            )
            field_list["temp"] = slider_temperature

            slider_tokens = dpg.add_slider_int(
                tag="tokens",
                label="Max Tokens",
                min_value=50,
                max_value=3950,
                default_value=1000
            )
            field_list["tokens"] = slider_tokens


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
            field_list["prompt"] = input_prompt
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
        field_list["response"] = text_response



        img_container = dpg.add_image("imgraw",
            tag="img",
            width=512,
            height=512,
            show=False
        )
        field_list["img"] = img_container

        button_copy = dpg.add_button(
            tag="copy",
            label="Copy to Clipboard",
            show=False,
            callback=copy_to_clipboard
        )
        field_list["copy"] = button_copy


    loading_indicator = dpg.add_loading_indicator(
        tag="lin",
        pos=[400,300],
        show=False
    )

    field_list["lin"] = loading_indicator


# dpg.show_debug()
# dpg.show_metrics()
dpg.create_viewport(title='openAI Toolbox', width=app_w, height=app_h, x_pos = int((screen_w - app_w) / 2), y_pos = int((screen_h - app_h) / 2))
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.show_font_manager()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()

