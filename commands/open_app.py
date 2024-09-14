import subprocess
import json
import tts_module

with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)

def command(app):
    name = command_list['open_app'][app][1]
    process = subprocess.Popen(app)
    tts_module.speak(f'команда выполнена: {name}')