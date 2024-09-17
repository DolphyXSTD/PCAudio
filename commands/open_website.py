import webbrowser
import json
import tts_module
from start_config import command_list_dir

with open(command_list_dir, "r", encoding='utf-8') as file:
    command_list = json.load(file)

def command(url):
    name = command_list['open_website'][url][1]
    webbrowser.open(url)
    tts_module.speak(f'команда выполнена: {name}')
