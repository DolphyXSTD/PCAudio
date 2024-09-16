import webbrowser
import json
import tts_module
from pathfinder import find_path
with open(find_path('command_list.json'), "r", encoding='utf-8') as file:
    command_list = json.load(file)

def command(url):
    name = command_list['open_website'][url][1]
    webbrowser.open(url)
