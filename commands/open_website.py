import webbrowser
import json
import tts_module

with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)

def command(url):
    name = command_list['open_website'][url][1]
    webbrowser.open(url)
